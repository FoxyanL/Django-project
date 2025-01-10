from django.db import models

# Create your models here.

class CBank_rates(models.Model):
    currency = models.CharField(max_length=10)
    rate = models.DecimalField(max_digits=15, decimal_places=10, null=True, blank=True)
    date = models.DateField()


    
# Модели статистики

class All_avg_salary_by_year(models.Model):
    year = models.IntegerField()
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


class All_vacancies_by_year(models.Model):
    year = models.IntegerField()
    count = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


class All_avg_salary_by_city(models.Model):
    city = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


class All_city_distribution(models.Model):
    city = models.CharField(max_length=100)
    percentage = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)


class All_top_skills_by_year(models.Model):
    year = models.IntegerField()
    skills = models.TextField(null=True, blank=True)
    frequency = models.IntegerField()

class Python_avg_salary_by_year(models.Model):
    year = models.IntegerField()
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


class Python_vacancies_by_year(models.Model):
    year = models.IntegerField()
    count = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


class Python_avg_salary_by_city(models.Model):
    city = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


class Python_city_distribution(models.Model):
    city = models.CharField(max_length=100)
    percentage = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)


class Python_top_skills_by_year(models.Model):
    year = models.IntegerField()
    skills = models.TextField(null=True, blank=True)
    frequency = models.IntegerField()

