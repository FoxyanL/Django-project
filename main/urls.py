from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # Главная страница
    path('statistics/', views.statistics_page, name='statistics'),
    path('salary_chart/', views.generate_salary_chart, name='salary_chart'),
    path('vacancies/', views.vacancies_view, name='vacancies'), 
]