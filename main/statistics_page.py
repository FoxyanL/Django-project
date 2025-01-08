from main.models import (
    All_avg_salary_by_year,
    All_vacancies_by_year,
    All_avg_salary_by_city,
    All_city_distribution,
    All_top_skills_by_year,
)
from collections import defaultdict

def calculate_statistics():
    # Средняя зарплата по годам
    avg_salary_by_year = {
        record.year: float(record.salary)
        for record in All_avg_salary_by_year.objects.all()
    }

    # Количество вакансий по годам
    vacancies_by_year = {
        record.year: int(record.count)
        for record in All_vacancies_by_year.objects.all()
    }

    # Средняя зарплата по городам
    avg_salary_by_city = {
        record.city: float(record.salary)
        for record in All_avg_salary_by_city.objects.all()
    }

    # Доля вакансий по городам
    city_distribution = {
        record.city: float(record.percentage)
        for record in All_city_distribution.objects.all()
    }

    # Топ навыков по годам
    top_skills_by_year = defaultdict(dict)
    for record in All_top_skills_by_year.objects.all():
        skills = record.skills.split(",") if record.skills else []  # Разделяем навыки через запятую
        for skill in skills:
            top_skills_by_year[record.year][skill.strip()] = record.frequency

    return {
        "avg_salary_by_year": avg_salary_by_year,
        "vacancies_by_year": vacancies_by_year,
        "avg_salary_by_city": avg_salary_by_city,
        "city_distribution": city_distribution,
        "top_skills_by_year": dict(top_skills_by_year),
    }
