from django.db.models import Avg, Count
from main.models import Vacancy


def calculate_geography():
    # Фильтруем вакансии с некорректной зарплатой
    vacancies = Vacancy.objects.filter(
        максимальная_зарплата__lt=10_000_000
    )

    # 3. Уровень зарплат по городам
    salaries_by_city = (
        vacancies.filter(валюта="RUR")
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

    return {
        "salaries_by_city": salaries_by_city,
        "city_distribution": city_distribution,
    }
