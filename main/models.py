from django.db import models

# Create your models here.

class Vacancy(models.Model):
    название = models.CharField(max_length=255)
    минимальная_зарплата = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    максимальная_зарплата = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    валюта = models.CharField(max_length=10)
    город = models.CharField(max_length=100)
    дата_публикации = models.DateField()
    key_skills = models.TextField(null=True, blank=True)  # Список навыков через запятую

    def __str__(self):
        return self.название
