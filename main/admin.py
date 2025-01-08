from django.contrib import admin
from main.models import *

# Регистрация модели Vacancy
@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('название', 'минимальная_зарплата', 'максимальная_зарплата', 'валюта', 'город', 'дата_публикации', 'key_skills')

# Регистрация модели CBank_rates
@admin.register(CBank_rates)
class CBankAdmin(admin.ModelAdmin):
    list_display = ('currency', 'rate', 'date')

# Регистрация модели All_Vacancies
@admin.register(All_Vacancies)
class All_VacanciesAdmin(admin.ModelAdmin):
    list_display = ('название', 'минимальная_зарплата', 'максимальная_зарплата', 'валюта', 'город', 'дата_публикации', 'key_skills')

@admin.register(All_avg_salary_by_year)
class All_avg_salary_by_yearAdmin(admin.ModelAdmin):
    list_display = ('year', 'salary')

@admin.register(All_vacancies_by_year)
class All_vacancies_by_yearAdmin(admin.ModelAdmin):
    list_display = ('year', 'count')

@admin.register(All_avg_salary_by_city)
class All_avg_salary_by_cityAdmin(admin.ModelAdmin):
    list_display = ('city', 'salary')

@admin.register(All_city_distribution)
class All_city_distributionAdmin(admin.ModelAdmin):
    list_display = ('city', 'percentage')

@admin.register(All_top_skills_by_year)
class All_top_skills_by_yearAdmin(admin.ModelAdmin):
    list_display = ('year', 'skills', 'frequency')

