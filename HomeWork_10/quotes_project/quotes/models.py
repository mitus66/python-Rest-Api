from django.db import models

# Спочатку визначаємо клас Author, бо на нього посилається клас Quote
class Author(models.Model):
    """
    Модель для зберігання інформації про автора цитати.
    """
    fullname = models.CharField(max_length=255, unique=True, null=False)
    born_date = models.CharField(max_length=50, null=False)
    born_location = models.CharField(max_length=255, null=False)
    description = models.TextField(null=True)

    def __str__(self):
        return self.fullname

# Потім визначаємо клас Quote
class Quote(models.Model):
    """
    Модель для зберігання цитат.
    """
    text = models.TextField(null=False)
    tags = models.CharField(max_length=255)
    # Тепер клас Author вже існує і може бути використаний
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f'"{self.text[:50]}..." by {self.author.fullname}'
