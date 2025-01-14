from collections import defaultdict
from main.models import Python_top_skills_by_year


def calculate_skills():
    top_skills_by_year = defaultdict(dict)
    for record in Python_top_skills_by_year.objects.all():
        skills = record.skills.split(",") if record.skills else []
        for skill in skills:
            top_skills_by_year[record.year][skill.strip()] = record.frequency

    return {
        "top_skills_by_year": dict(top_skills_by_year),
    }
