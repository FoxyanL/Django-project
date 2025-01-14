from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # Главная страница
    path('statistics/', views.statistics_page, name='statistics'),
    path('demand/', views.demand_page, name='demand'),
    path('geography/', views.geography_page, name='geography'),
    path('skills/', views.skills_page, name='skills'),
    path('latest_vacancies/', views.latest_vacancies, name='latest_vacancies'),
]