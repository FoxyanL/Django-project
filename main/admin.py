from django.contrib import admin
from main.models import Vacancy, CBank_rates

# Регистрация модели Vacancy
@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('название', 'минимальная_зарплата', 'максимальная_зарплата', 'валюта', 'город', 'дата_публикации', 'key_skills')

# Регистрация модели CBank_rates
@admin.register(CBank_rates)
class CBankAdmin(admin.ModelAdmin):
    list_display = ('currency', 'rate', 'date')
