from django.db.models import Avg, Count
from main.models import Python_avg_salary_by_city, Python_city_distribution


def calculate_geography():
        # Средняя зарплата по городам
    avg_salary_by_city = {
        record.city: float(record.salary)
        for record in Python_avg_salary_by_city.objects.all()
    }

    # Доля вакансий по городам
    city_distribution = {
        record.city: float(record.percentage)
        for record in Python_city_distribution.objects.all()
    }

    return {
        "avg_salary_by_city": avg_salary_by_city,
        "city_distribution": city_distribution,
    }
