import pika
import json
from connect import connect_db
from models import Contact
from bson.objectid import ObjectId  # Для перетворення рядка назад в ObjectId

# Налаштування RabbitMQ
RABBITMQ_HOST = 'localhost'
RABBITMQ_QUEUE_NAME = 'email_queue'


def send_email_stub(contact_email: str, contact_fullname: str):
    """
    Функція-заглушка, що імітує надсилання email.
    """
    print(f"Імітація надсилання email до {contact_fullname} на {contact_email}...")
    # Тут могла б бути реальна логіка надсилання email
    # Наприклад, time.sleep(1) для імітації затримки
    print(f"Email до {contact_fullname} успішно 'надіслано'!")


def callback(ch, method, properties, body):
    """
    Функція зворотного виклику, що обробляє отримані повідомлення з черги.
    """
    contact_id_str = body.decode('utf-8')
    print(f" [x] Отримано ObjectID контакту: {contact_id_str}")

    try:
        # Знаходимо контакт у MongoDB за ObjectID
        contact = Contact.objects(id=ObjectId(contact_id_str)).first()

        if contact:
            if not contact.is_sent:
                send_email_stub(contact.email, contact.fullname)  # Імітуємо надсилання
                contact.is_sent = True  # Встановлюємо is_sent в True
                contact.save()  # Зберігаємо оновлений контакт у MongoDB
                print(f" [x] Оновлено статус контакту '{contact.fullname}' на 'надіслано'.")
            else:
                print(f" [x] Контакт '{contact.fullname}' вже має статус 'надіслано'. Пропускаємо.")
        else:
            print(f" [x] Контакт з ObjectID {contact_id_str} не знайдено в базі даних.")

    except Exception as e:
        print(f" [x] Помилка обробки повідомлення для ObjectID {contact_id_str}: {e}")

    # Підтверджуємо, що повідомлення оброблено, щоб воно було видалено з черги
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    connect_db()  # Підключаємося до MongoDB

    # Підключення до RabbitMQ
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        channel.queue_declare(queue=RABBITMQ_QUEUE_NAME)
        print(f"Очікування повідомлень на черзі '{RABBITMQ_QUEUE_NAME}'. Для виходу натисніть CTRL+C")
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Помилка підключення до RabbitMQ: {e}. Переконайтеся, що RabbitMQ запущено.")
        return

    # Встановлюємо споживача для черги
    channel.basic_consume(queue=RABBITMQ_QUEUE_NAME, on_message_callback=callback, auto_ack=False)

    try:
        channel.start_consuming()  # Запускаємо нескінченний цикл очікування повідомлень
    except KeyboardInterrupt:
        print("\nВихід з споживача.")
    except Exception as e:
        print(f"Виникла помилка під час споживання повідомлень: {e}")
    finally:
        if connection:
            connection.close()
        print("З'єднання з RabbitMQ закрито.")


if __name__ == "__main__":
    main()
