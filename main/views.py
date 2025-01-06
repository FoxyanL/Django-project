import matplotlib.pyplot as plt
from django.db.models import Avg, F, FloatField
from django.db.models.functions import ExtractYear
from io import BytesIO
from django.shortcuts import render
from django.http import HttpResponse
from main.statistics_page import calculate_statistics
from main.demand import calculate_demand
from main.geography import calculate_geography
from main.skills import calculate_skills
from main.models import Vacancy

# Create your views here.
def index(request):
    return render(request, 'main/index.html', {})

def statistics_page(request):
    stats = calculate_statistics()
    return render(request, 'main/statistics.html', stats)

def demand_page(request):
    stats = calculate_demand()
    return render(request, 'main/demand.html', {
        'vacancies_by_year': stats["vacancies_by_year"],
        'avg_salary_by_year': stats["avg_salary_by_year"],
    })

def geography_page(request):
    stats = calculate_geography()
    return render(request, 'main/geography.html', {
        'salaries_by_city': stats["salaries_by_city"],
        'city_distribution': stats["city_distribution"],
    }) 

def skills_page(request):
    stats = calculate_skills()
    return render(request, 'main/skills.html', {
        'top_skills_by_year': stats["top_skills_by_year"],
    })  

def generate_salary_chart(request):
    # Группировка данных по годам и расчет средней зарплаты
    salaries_data = (
        Vacancy.objects.annotate(year=ExtractYear('дата_публикации'))
        .filter(минимальная_зарплата__isnull=False, максимальная_зарплата__isnull=False)
        .values('year')  # Группировка по годам
        .annotate(
            average_salary=Avg(
                (F('минимальная_зарплата') + F('максимальная_зарплата')) / 2,
                output_field=FloatField()
            )
        )
        .order_by('year')
    )

    # Подготовка данных для графика
    years = [entry['year'] for entry in salaries_data]
    salaries = [entry['average_salary'] for entry in salaries_data]

    # Построение графика
    plt.figure(figsize=(10, 6))
    plt.plot(years, salaries, marker='o', label='Средняя зарплата')
    plt.title('Динамика уровня зарплат по годам')
    plt.xlabel('Годы')
    plt.ylabel('Средняя зарплата (в рублях)')
    plt.xticks(years)  # Отображаем только те годы, которые есть в данных
    plt.legend()

    # Генерация изображения
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    return HttpResponse(buffer, content_type='image/png')
