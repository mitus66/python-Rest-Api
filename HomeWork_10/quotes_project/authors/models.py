# authors/models.py
from django.db import models

# Модель авторів
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