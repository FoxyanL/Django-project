from django.core.management.base import BaseCommand
from main.models import *

class Command(BaseCommand):
    help = 'Удаляет все вакансии из базы данных'

    def handle(self, *args, **kwargs):
        count, _ = All_avg_salary_by_city.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Удалено {count} вакансий'))
        count, _ = All_vacancies_by_year.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Удалено {count} вакансий'))
        count, _ = All_top_skills_by_year.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Удалено {count} вакансий'))
        count, _ = All_avg_salary_by_year.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Удалено {count} вакансий'))
        count, _ = All_city_distribution.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Удалено {count} вакансий'))
