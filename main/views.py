import matplotlib
matplotlib.use('Agg')
import os
from datetime import datetime
from django.conf import settings
import matplotlib.pyplot as plt
from django.shortcuts import render
from main.statistics_page import calculate_statistics
from main.demand import calculate_demand
from main.geography import calculate_geography
from main.skills import calculate_skills
from main.models import *
from matplotlib import pyplot as plt
from main.cleaning import clean_old_charts
from matplotlib.ticker import FuncFormatter

# Create your views here.
def index(request):
    return render(request, 'main/index.html', {})

def statistics_page(request):
    # Генерация основных графиков
    salary_chart = generate_salary_chart(request, All_avg_salary_by_year, 'All')
    vacancies_chart = generate_vacancies_chart(request, All_vacancies_by_year, 'All')
    salary_by_city_chart = generate_salary_by_city_chart(request, All_avg_salary_by_city, 'All')
    city_distribution_chart = generate_city_distribution_chart(request, All_city_distribution, 'All')

    # Создание словаря для хранения данных графиков
    stats = {
        'salary_chart': salary_chart,
        'vacancies_chart': vacancies_chart,
        'salary_by_city_chart': salary_by_city_chart,
        'city_distribution_chart': city_distribution_chart,
    }

    # Генерация графиков и данных для ТОП-20 навыков по годам
    top_skills = {}
    years = All_top_skills_by_year.objects.values_list('year', flat=True).distinct()
    clean_old_charts(os.path.join(settings.BASE_DIR, 'main', 'static', 'main', 'images'), "top_skills_chart")
    for year in years:
        # Получение данных о навыках за год
        skills_data = All_top_skills_by_year.objects.filter(year=year).order_by('-frequency')[:20]
        skills = {record.skills: record.frequency for record in skills_data}

        # Генерация графика для текущего года
        plt.figure(figsize=(12, 6))
        plt.barh(list(skills.keys())[::-1], list(skills.values())[::-1], color='skyblue')
        plt.title(f'ТОП-20 навыков за {year}', fontsize=14)
        plt.xlabel('Частота', fontsize=12)
        plt.ylabel('Навык', fontsize=12)
        plt.tight_layout()

        # Уникальное имя файла
        filename = f"top_skills_chart_{year}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        filepath = os.path.join(settings.BASE_DIR, 'main', 'static', 'main', 'images', filename)

        # Сохранение графика
        plt.savefig(filepath)
        plt.close()

        # Добавление данных в словарь
        top_skills[year] = {
            'skills': skills,
            'chart_path': f"main/images/{filename}",
        }

    # Объединение данных графиков навыков с остальной статистикой
    stats['top_skills'] = top_skills

    # Добавление дополнительных данных для таблиц
    stats.update(calculate_statistics())

    return render(request, 'main/statistics.html', stats)


def demand_page(request):
    salary_chart = generate_salary_chart(request, Python_avg_salary_by_year, 'Python')
    vacancies_chart = generate_vacancies_chart(request, Python_vacancies_by_year, 'Python')
    stats = calculate_demand()
    return render(request, 'main/demand.html', {
        'vacancies_by_year': stats["vacancies_by_year"],
        'avg_salary_by_year': stats["avg_salary_by_year"],
        'salary_chart': salary_chart,
        'vacancies_chart': vacancies_chart,
    })

def geography_page(request):
    stats = calculate_geography()
    salary_by_city_chart = generate_salary_by_city_chart(request, Python_avg_salary_by_city, 'Python')
    city_distribution_chart = generate_city_distribution_chart(request, Python_city_distribution, 'Python')
    return render(request, 'main/geography.html', {
        'avg_salary_by_city': stats["avg_salary_by_city"],
        'city_distribution': stats["city_distribution"],
        'salary_by_city_chart': salary_by_city_chart,
        'city_distribution_chart': city_distribution_chart,
    }) 

def skills_page(request):
    stats = calculate_skills()
        # Генерация графиков и данных для ТОП-20 навыков по годам
    top_skills = {}
    years = Python_top_skills_by_year.objects.values_list('year', flat=True).distinct()
    clean_old_charts(os.path.join(settings.BASE_DIR, 'main', 'static', 'main', 'images'), "Python_top_skills_chart")
    for year in years:
        # Получение данных о навыках за год
        skills_data = Python_top_skills_by_year.objects.filter(year=year).order_by('-frequency')[:20]
        skills = {record.skills: record.frequency for record in skills_data}

        # Генерация графика для текущего года
        plt.figure(figsize=(12, 6))
        plt.barh(list(skills.keys())[::-1], list(skills.values())[::-1], color='skyblue')
        plt.title(f'ТОП-20 навыков за {year}', fontsize=14)
        plt.xlabel('Частота', fontsize=12)
        plt.ylabel('Навык', fontsize=12)
        plt.tight_layout()

        # Уникальное имя файла
        filename = f"Python_top_skills_chart_{year}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        filepath = os.path.join(settings.BASE_DIR, 'main', 'static', 'main', 'images', filename)

        # Сохранение графика
        plt.savefig(filepath)
        plt.close()

        # Добавление данных в словарь
        top_skills[year] = {
            'skills': skills,
            'chart_path': f"main/images/{filename}",
        }

    # Объединение данных графиков навыков с остальной статистикой
    stats['top_skills'] = top_skills
    return render(request, 'main/skills.html', {
        'top_skills_by_year': stats["top_skills"],
    })  

def generate_salary_chart(request, model, type):
    clean_old_charts(os.path.join(settings.BASE_DIR, 'main', 'static', 'main', 'images'), f"{type}_salary_chart")
    # Подготовка данных для графика
    data = {
        record.year: float(record.salary)
        for record in model.objects.all().order_by('year')
    }

    years = list(data.keys())
    salaries = list(data.values())

    # Построение графика
    plt.figure(figsize=(10, 6))
    plt.plot(years, salaries, marker='o', label='Средняя зарплата', color='blue')
    plt.title('Динамика уровня зарплат по годам', fontsize=14)
    plt.xlabel('Годы', fontsize=12)
    plt.ylabel('Средняя зарплата (в рублях)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(years, rotation=45)  # Отображаем только те годы, которые есть в данных
    plt.tight_layout()
    plt.legend()

    # Генерация уникального имени файла
    filename = f"{type}_salary_chart_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    filepath = os.path.join(settings.BASE_DIR, 'main', 'static', 'main', 'images', filename)

    # Сохранение файла
    plt.savefig(filepath)
    plt.close()

    # Возвращаем путь к файлу для использования в шаблоне
    return filepath

def generate_vacancies_chart(request, model, type):
    clean_old_charts(os.path.join(settings.BASE_DIR, 'main', 'static', 'main', 'images'), f"{type}_vacancies_chart")
    # Подготовка данных
    data = {
        record.year: float(record.count)
        for record in model.objects.all().order_by('year')
    }

    years = list(data.keys())
    counts = list(data.values())

    # Построение графика
    plt.figure(figsize=(10, 6))
    plt.bar(years, counts, color='green', alpha=0.7, label='Количество вакансий')
    plt.title('Количество вакансий по годам', fontsize=14)
    plt.xlabel('Годы', fontsize=12)
    plt.ylabel('Количество вакансий', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(years, rotation=45)
    plt.tight_layout()
    plt.legend()

    # Генерация уникального имени файла
    filename = f"{type}_vacancies_chart_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    filepath = os.path.join(settings.BASE_DIR, 'main', 'static', 'main', 'images', filename)

    # Сохранение файла
    plt.savefig(filepath)
    plt.close()

    # Возвращаем путь к файлу для использования в шаблоне
    return filepath

def generate_salary_by_city_chart(request, model, type):
    clean_old_charts(os.path.join(settings.BASE_DIR, 'main', 'static', 'main', 'images'), f"{type}_salary_by_city_chart")
    # Подготовка данных
    data = {
        record.city: float(record.salary)
        for record in model.objects.all().order_by('-salary')[:10]  # Топ-10 городов
    }

    cities = list(data.keys())
    salaries = list(data.values())

    # Построение графика
    plt.figure(figsize=(12, 8))
    plt.barh(cities, salaries, color='purple', alpha=0.7)
    plt.title('Средняя зарплата по городам (Топ-10)', fontsize=14)
    plt.xlabel('Средняя зарплата (в рублях)', fontsize=12)
    plt.ylabel('Города', fontsize=12)
    plt.gca().invert_yaxis()  # Перевернуть города сверху вниз для читаемости
    # Настройка формата чисел на оси X
    formatter = FuncFormatter(lambda x, _: f'{int(x):,}'.replace(',', ' '))
    plt.gca().xaxis.set_major_formatter(formatter)
    plt.tight_layout()

    # Генерация уникального имени файла
    filename = f"{type}_salary_by_city_chart_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    filepath = os.path.join(settings.BASE_DIR, 'main', 'static', 'main', 'images', filename)

    # Сохранение файла
    plt.savefig(filepath)
    plt.close()

    # Возвращаем путь к файлу для использования в шаблоне
    return filepath

def generate_city_distribution_chart(request, model, type):
    clean_old_charts(os.path.join(settings.BASE_DIR, 'main', 'static', 'main', 'images'), f"{type}_city_distribution_chart")
    # Подготовка данных
    data = {
        record.city: float(record.percentage)
        for record in model.objects.all().order_by('-percentage')
    }

    cities = list(data.keys())[:10]  # Топ-10 городов
    percentages = list(data.values())[:10]

    # Построение графика
    plt.figure(figsize=(10, 6))
    plt.pie(
        percentages,
        labels=cities,
        autopct='%1.1f%%',
        startangle=140,
        colors=plt.cm.tab10.colors
    )
    plt.title('Распределение вакансий по городам (Топ-10)', fontsize=14)
    plt.tight_layout()

    # Генерация уникального имени файла
    filename = f"{type}_city_distribution_chart_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    filepath = os.path.join(settings.BASE_DIR, 'main', 'static', 'main', 'images', filename)

    # Сохранение файла
    plt.savefig(filepath)
    plt.close()

    # Возвращаем путь к файлу для использования в шаблоне
    return filepath



