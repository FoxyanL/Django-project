from django.contrib import admin
from main.models import Vacancy
# Register your models here.
@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('название', 'минимальная_зарплата', 'максимальная_зарплата', 'валюта', 'город', 'дата_публикации', 'key_skills')