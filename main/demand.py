from collections import defaultdict
from django.db.models import Avg, Count
from main.models import Vacancy
from datetime import datetime
from main.utils import get_exchange_rate
from decimal import Decimal
from django.db.models.functions import ExtractYear


def calculate_demand():
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
        if avg_salary == 0 or vacancy.валюта is None or not vacancy.валюта:
            continue
        if vacancy.валюта != "RUR":
            date = vacancy.дата_публикации
            rate = get_exchange_rate(date, vacancy.валюта)
            if rate:
                avg_salary *= Decimal(rate)
            else:
                continue
        year = date.year
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


    return {
        "avg_salary_by_year": avg_salary_by_year,
        "vacancies_by_year": vacancies_by_year,
    }
