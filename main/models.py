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

class CBank_rates(models.Model):
    currency = models.CharField(max_length=255)
    rate = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True)
    date = models.DateField()
    def __str__(self):
        return self.currency

class All_Vacancies(models.Model):
    название = models.CharField(max_length=255)
    минимальная_зарплата = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    максимальная_зарплата = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    валюта = models.CharField(max_length=10)
    город = models.CharField(max_length=100)
    дата_публикации = models.DateField()
    key_skills = models.TextField(null=True, blank=True)  # Список навыков через запятую

    def __str__(self):
        return self.название
    
# Модели статистики

class All_avg_salary_by_year(models.Model):
    year = models.IntegerField()
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return str(self.year)

class All_vacancies_by_year(models.Model):
    year = models.IntegerField()
    count = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return str(self.year)

class All_avg_salary_by_city(models.Model):
    city = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.city

class All_city_distribution(models.Model):
    city = models.CharField(max_length=100)
    percentage = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.city

class All_top_skills_by_year(models.Model):
    year = models.IntegerField()
    skills = models.TextField(null=True, blank=True)
    frequency = models.IntegerField()

    def __str__(self):
        return str(self.year)
