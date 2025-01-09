from django.contrib import admin
from main.models import *

# Регистрация модели CBank_rates
@admin.register(CBank_rates)
class CBankAdmin(admin.ModelAdmin):
    list_display = ('currency', 'rate', 'date')

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

@admin.register(Python_avg_salary_by_year)
class Python_avg_salary_by_yearAdmin(admin.ModelAdmin):
    list_display = ('year', 'salary')

@admin.register(Python_vacancies_by_year)
class Python_vacancies_by_yearAdmin(admin.ModelAdmin):
    list_display = ('year', 'count')

@admin.register(Python_avg_salary_by_city)
class Python_avg_salary_by_cityAdmin(admin.ModelAdmin):
    list_display = ('city', 'salary')

@admin.register(Python_city_distribution)
class Python_city_distributionAdmin(admin.ModelAdmin):
    list_display = ('city', 'percentage')

@admin.register(Python_top_skills_by_year)
class Python_top_skills_by_yearAdmin(admin.ModelAdmin):
    list_display = ('year', 'skills', 'frequency')

