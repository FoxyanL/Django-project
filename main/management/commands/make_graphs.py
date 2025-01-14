import matplotlib
matplotlib.use('Agg')
from main.models import *
from django.core.management.base import BaseCommand
from datetime import datetime
import os
from django.conf import settings
from main.models import *
from matplotlib import pyplot as plt
from main.cleaning import clean_old_charts
from matplotlib.ticker import FuncFormatter
import glob

class Command(BaseCommand):
    help = "Создает графики по статистике из БДшки"

    def clean_old_charts(self, directory, prefix):
        files = glob.glob(os.path.join(directory, f"{prefix}*.png"))
        for file in files:
            try:
                os.remove(file)
                self.stderr.write(self.style.SUCCESS(f"Удален файл: {file}"))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Ошибка {e}. Не удалось удалить файл: {file}"))
    
    def generate_salary_chart(self, model, type):
        clean_old_charts(os.path.join(settings.BASE_DIR, 'main', 'static', 'main', 'images'), f"{type}_salary_chart")
        data = {
            record.year: float(record.salary)
            for record in model.objects.all().order_by('year')
        }

        years = list(data.keys())
        salaries = list(data.values())

        plt.figure(figsize=(10, 6))
        plt.plot(years, salaries, marker='o', label='Средняя зарплата', color='blue')
        plt.title('Динамика уровня зарплат по годам', fontsize=14)
        plt.xlabel('Годы', fontsize=12)
        plt.ylabel('Средняя зарплата (в рублях)', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.xticks(years, rotation=45)
        plt.tight_layout()
        plt.legend()

        filename = f"{type}_salary_chart.png"
        filepath = os.path.join(settings.BASE_DIR, 'main', 'static', 'main', 'images', filename)

        plt.savefig(filepath)
        plt.close()
        
    def generate_vacancies_chart(self, model, type):
        clean_old_charts(os.path.join(settings.BASE_DIR, 'main', 'static', 'main', 'images'), f"{type}_vacancies_chart")
        data = {
            record.year: float(record.count)
            for record in model.objects.all().order_by('year')
        }

        years = list(data.keys())
        counts = list(data.values())

        plt.figure(figsize=(10, 6))
        plt.bar(years, counts, color='green', alpha=0.7, label='Количество вакансий')
        plt.title('Количество вакансий по годам', fontsize=14)
        plt.xlabel('Годы', fontsize=12)
        plt.ylabel('Количество вакансий', fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.xticks(years, rotation=45)
        plt.tight_layout()
        plt.legend()

        filename = f"{type}_vacancies_chart.png"
        filepath = os.path.join(settings.BASE_DIR, 'main', 'static', 'main', 'images', filename)

        plt.savefig(filepath)
        plt.close()

    def generate_salary_by_city_chart(self, model, type):
        clean_old_charts(os.path.join(settings.BASE_DIR, 'main', 'static', 'main', 'images'), f"{type}_salary_by_city_chart")
        data = {
            record.city: float(record.salary)
            for record in model.objects.all().order_by('-salary')[:10]
        }

        cities = list(data.keys())
        salaries = list(data.values())

        plt.figure(figsize=(12, 8))
        plt.barh(cities, salaries, color='purple', alpha=0.7)
        plt.title('Средняя зарплата по городам (Топ-10)', fontsize=14)
        plt.xlabel('Средняя зарплата (в рублях)', fontsize=12)
        plt.ylabel('Города', fontsize=12)
        plt.gca().invert_yaxis()  # Перевернуть города сверху вниз для читаемости
        formatter = FuncFormatter(lambda x, _: f'{int(x):,}'.replace(',', ' '))
        plt.gca().xaxis.set_major_formatter(formatter)
        plt.tight_layout()

        filename = f"{type}_salary_by_city_chart.png"
        filepath = os.path.join(settings.BASE_DIR, 'main', 'static', 'main', 'images', filename)

        plt.savefig(filepath)
        plt.close()

    def generate_city_distribution_chart(self, model, type):
        clean_old_charts(os.path.join(settings.BASE_DIR, 'main', 'static', 'main', 'images'), f"{type}_city_distribution_chart")
        data = {
            record.city: float(record.percentage)
            for record in model.objects.all().order_by('-percentage')
        }

        cities = list(data.keys())[:10]
        percentages = list(data.values())[:10]

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

        filename = f"{type}_city_distribution_chart.png"
        filepath = os.path.join(settings.BASE_DIR, 'main', 'static', 'main', 'images', filename)

        
        plt.savefig(filepath)
        plt.close()
    def generate_top_skills_chart(self, model, type):
        years = model.objects.values_list('year', flat=True).distinct()
        clean_old_charts(os.path.join(settings.BASE_DIR, 'main', 'static', 'main', 'images'), f"{type}_top_skills_chart")
        for year in years:
            skills_data = All_top_skills_by_year.objects.filter(year=year).order_by('-frequency')[:20]
            skills = {record.skills: record.frequency for record in skills_data}

            plt.figure(figsize=(12, 6))
            plt.barh(list(skills.keys())[::-1], list(skills.values())[::-1], color='skyblue')
            plt.title(f'ТОП-20 навыков за {year}', fontsize=14)
            plt.xlabel('Частота', fontsize=12)
            plt.ylabel('Навык', fontsize=12)
            plt.tight_layout()

            filename = f"{type}_top_skills_{year}_chart.png"
            filepath = os.path.join(settings.BASE_DIR, 'main', 'static', 'main', 'images', filename)

            plt.savefig(filepath)
            plt.close()

    def handle(self, *args, **kwargs):
        self.generate_salary_chart(All_avg_salary_by_year, 'all')
        self.generate_salary_chart(Python_avg_salary_by_year, 'python')

        self.generate_vacancies_chart(All_vacancies_by_year, 'all')
        self.generate_vacancies_chart(Python_vacancies_by_year, 'python')

        self.generate_salary_by_city_chart(All_avg_salary_by_city, 'all')
        self.generate_salary_by_city_chart(Python_avg_salary_by_city, 'python')

        self.generate_city_distribution_chart(All_city_distribution, 'all')
        self.generate_city_distribution_chart(Python_city_distribution, 'python')

        self.generate_top_skills_chart(All_top_skills_by_year, 'all')
        self.generate_top_skills_chart(Python_top_skills_by_year, 'python')



