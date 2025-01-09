from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # Главная страница
    path('statistics/', views.statistics_page, name='statistics'),
    path('salary_chart/', views.generate_salary_chart, name='salary_chart'),
    path('vacancies_chart/', views.generate_vacancies_chart, name='vacancies_chart'),
    path('salary_by_city_chart/', views.generate_salary_by_city_chart, name='salary_by_city_chart'),
    path('city_distribution_chart/', views.generate_city_distribution_chart, name='city_distribution_chart'),
    path('demand/', views.demand_page, name='demand'),
    path('geography/', views.geography_page, name='geography'),
    path('skills/', views.skills_page, name='skills'), 
]