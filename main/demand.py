from main.models import Python_avg_salary_by_year, Python_vacancies_by_year



def calculate_demand():
    avg_salary_by_year = {
        record.year: float(record.salary)
        for record in Python_avg_salary_by_year.objects.all()
    }

    vacancies_by_year = {
        record.year: int(record.count)
        for record in Python_vacancies_by_year.objects.all()
    }


    return {
        "avg_salary_by_year": avg_salary_by_year,
        "vacancies_by_year": vacancies_by_year,
    }
