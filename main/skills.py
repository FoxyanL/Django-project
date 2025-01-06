from collections import defaultdict
from main.models import Vacancy


def calculate_skills():
    # Фильтруем вакансии с некорректной зарплатой
    vacancies = Vacancy.objects.filter(
        максимальная_зарплата__lt=10_000_000
    )

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
        "top_skills_by_year": top_skills_by_year,
    }
