import pika
import json
from faker import Faker
from connect import connect_db
from models import Contact  # Імпортуємо нову модель Contact

# Налаштування RabbitMQ
RABBITMQ_HOST = 'localhost'
RABBITMQ_QUEUE_NAME = 'email_queue'


def main():
    connect_db()  # Підключаємося до MongoDB

    # Підключення до RabbitMQ
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        channel.queue_declare(queue=RABBITMQ_QUEUE_NAME)
        print(f"Підключено до RabbitMQ на {RABBITMQ_HOST}, черга '{RABBITMQ_QUEUE_NAME}' створена.")
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Помилка підключення до RabbitMQ: {e}. Переконайтеся, що RabbitMQ запущено.")
        return

    fake = Faker('uk_UA')
    num_contacts = 10  # Кількість фейкових контактів для генерації

    print(f"Генерація та збереження {num_contacts} фейкових контактів...")
    for _ in range(num_contacts):
        fullname = fake.name()
        email = fake.email()
        phone_number = fake.phone_number()
        address = fake.address()

        try:
            contact = Contact(
                fullname=fullname,
                email=email,
                phone_number=phone_number,
                address=address,
                is_sent=False  # За замовчуванням False
            )
            contact.save()  # Зберігаємо контакт у MongoDB

            contact_id = str(contact.id)  # Отримуємо ObjectID контакту

            # Публікуємо ObjectID контакту в чергу RabbitMQ
            channel.basic_publish(
                exchange='',
                routing_key=RABBITMQ_QUEUE_NAME,
                body=contact_id.encode('utf-8')  # Кодуємо ObjectID в байти
            )
            print(f"  Збережено контакт '{fullname}' ({contact_id}) та додано до черги.")
        except Exception as e:
            print(f"  Помилка при збереженні або публікації контакту '{fullname}': {e}")

    connection.close()
    print("\nГенерація контактів та публікація повідомлень завершено.")


if __name__ == "__main__":
    main()
