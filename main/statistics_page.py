from collections import defaultdict
from django.db.models import Avg, Count
from main.models import Vacancy
from datetime import datetime
from main.utils import get_exchange_rate
from decimal import Decimal
from django.db.models.functions import ExtractYear


def calculate_statistics():
    # Фильтруем вакансии с некорректной зарплатой
    vacancies = Vacancy.objects.filter(
        максимальная_зарплата__lt=10_000_000
    )

    # 1. Динамика уровня зарплат по годам
    salary_dynamics = defaultdict(list)
    for vacancy in vacancies:
        avg_salary = (
            (vacancy.минимальная_зарплата or 0) +
            (vacancy.максимальная_зарплата or 0)
        ) / 2
        if vacancy.валюта != "RUB":
            date = vacancy.дата_публикации.strftime('%d/%m/%Y')
            rate = get_exchange_rate(date, vacancy.валюта)
            avg_salary *= Decimal(rate or 1)
        year = vacancy.дата_публикации.year
        salary_dynamics[year].append(avg_salary)

    avg_salary_by_year = {
        year: sum(salaries) / len(salaries) for year, salaries in salary_dynamics.items()
    }

    # 2. Динамика количества вакансий по годам
    vacancies_by_year = (
        Vacancy.objects.annotate(year=ExtractYear('дата_публикации'))
        .values('year')
        .annotate(count=Count('id'))
    )

    # 3. Уровень зарплат по городам
    salaries_by_city = (
        vacancies.filter(валюта="RUB")
        .values('город')
        .annotate(avg_salary=Avg('максимальная_зарплата'))
        .order_by('-avg_salary')
    )

    # 4. Доля вакансий по городам
    total_vacancies = vacancies.count()
    city_distribution = (
        vacancies.values('город')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    city_distribution = {
        entry['город']: entry['count'] / total_vacancies * 100 for entry in city_distribution
    }

    # 5. ТОП-20 навыков по годам
    skills_by_year = defaultdict(lambda: defaultdict(int))
    for vacancy in vacancies:
        if vacancy.key_skills:
            year = vacancy.дата_публикации.year
            for skill in vacancy.key_skills.split(','):
                skills_by_year[year][skill.strip()] += 1

    top_skills_by_year = {
        year: sorted(skills.items(), key=lambda x: x[1], reverse=True)[:20]
        for year, skills in skills_by_year.items()
    }

    return {
        "avg_salary_by_year": avg_salary_by_year,
        "vacancies_by_year": vacancies_by_year,
        "salaries_by_city": salaries_by_city,
        "city_distribution": city_distribution,
        "top_skills_by_year": top_skills_by_year,
    }
