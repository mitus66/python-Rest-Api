from django.db import models
from django.contrib.auth.models import User # Для зв'язку з користувачами

class Author(models.Model):
    fullname = models.CharField(max_length=100, unique=True)
    born_date = models.CharField(max_length=50)
    born_location = models.CharField(max_length=150)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fullname

class Quote(models.Model):
    tags = models.CharField(max_length=255) # Зберігаємо теги як рядок, розділений комою
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    quote = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'"{self.quote[:50]}..." - {self.author.fullname}'

    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',')]
