import pandas as pd
from decimal import Decimal, InvalidOperation
from django.db.models import Q
from main.models import *
from django.core.management.base import BaseCommand
from datetime import datetime

class Command(BaseCommand):
    help = "Импортирует вакансии из CSV файла в базу данных."

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path',
            type=str,
            help='Путь к CSV файлу с вакансиями'
        )

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        # Заранее получаем курсы валют из базы данных
        self.exchange_rates = self.load_exchange_rates()

        # Функция для обработки зарплаты
        def process_salary(value, currency, year, month):
            if currency == 'RUR':
                try:
                    value = Decimal(str(value).replace(',', '.'))
                    return value if value < Decimal('10_000_000') else None
                except (InvalidOperation, ValueError):
                    return None
            if not value or not currency or not year or not month:
                return None
            try:
                value = Decimal(str(value).replace(',', '.'))
                if currency != 'RUR':
                    rate = self.exchange_rates.get((currency, month, year), None)
                    if rate:
                        value *= Decimal(rate)
                return value if value < Decimal('10_000_000') else None
            except (InvalidOperation, ValueError):
                return None

        # Читаем и обрабатываем файл порциями
        chunksize = 100_000
        dtype_map = {"salary_from": "str", "salary_to": "str", "salary_currency": "str"}
        all_data = []
        keywords = ('python', 'питон', 'пайтон')  # Список ключевых слов

        for chunk in pd.read_csv(file_path, chunksize=chunksize, encoding='utf-8-sig', low_memory=False, dtype=dtype_map):
            # Приводим названия вакансий в нижний регистр для проверки
            chunk['name'] = chunk['name'].str.lower()

            # Фильтруем вакансии, оставляя только те, которые содержат ключевые слова
            chunk = chunk[chunk['name'].str.contains('|'.join(keywords), na=False)]

            # Обработка зарплат
            chunk['published_at'] = pd.to_datetime(chunk['published_at'], errors='coerce', utc=True)
            chunk.dropna(subset=['published_at'], inplace=True)  # Удаляем строки с некорректными датами
            chunk['year'] = chunk['published_at'].dt.year  # Извлекаем год
            chunk['month'] = chunk['published_at'].dt.month  # Извлекаем месяц

            chunk['salary_from'] = chunk.apply(
                lambda row: process_salary(row['salary_from'], row['salary_currency'], row['year'], row['month']),
                axis=1
            )
            chunk['salary_to'] = chunk.apply(
                lambda row: process_salary(row['salary_to'], row['salary_currency'], row['year'], row['month']),
                axis=1
            )

            # Удаляем строки с некорректными данными
            chunk.dropna(subset=['name'], inplace=True)

            # Вычисляем среднюю зарплату
            chunk['avg_salary'] = (chunk['salary_from'].fillna(0) + chunk['salary_to'].fillna(0)) / 2

            # Если salary_from и salary_to уже в рублях, то:
            chunk['avg_salary_rub'] = chunk['avg_salary']

            all_data.append(chunk)
        df = pd.concat(all_data, ignore_index=True)
        # Анализ данных
        self.analyze_data(df)

    def load_exchange_rates(self):
        """Заранее загружаем все курсы валют из базы данных в словарь."""
        rates = {}
        for rate in CBank_rates.objects.all():
            rates[(rate.currency, rate.date.month, rate.date.year)] = Decimal(rate.rate)
        return rates

    def analyze_data(self, df):
        """Анализ и сохранение данных в базе."""
        # 1. Средняя зарплата по годам
        df['avg_salary_rub'] = df['avg_salary_rub'].astype(float)
        avg_salary_by_year = df.groupby('year')['avg_salary_rub'].mean().dropna().to_dict()

        # 2. Количество вакансий по годам
        vacancies_by_year = df.groupby('year').size().to_dict()

        # 3. Средняя зарплата по городам
        avg_salary_by_city = (
            df.groupby('area_name')['avg_salary_rub'].mean()
            .dropna().sort_values(ascending=False).to_dict()
        )

        # 4. Доля вакансий по городам
        total_vacancies = len(df)
        city_distribution = (
            df['area_name'].value_counts(normalize=True) * 100
        )
        city_distribution = city_distribution[city_distribution >= 1].to_dict()

        # 5. Топ-20 навыков по годам
        top_skills_by_year = self.get_top_skills_by_year(df)

        # Сохраняем результаты
        self.save_statistics(avg_salary_by_year, vacancies_by_year, avg_salary_by_city, city_distribution, top_skills_by_year)

    def get_top_skills_by_year(self, df):
        """Извлекает и подсчитывает топ-20 навыков по годам."""
        top_skills_by_year = {}
        for year, group in df.groupby('year'):
            if group['key_skills'].dropna().empty:
                continue
            skills = (
                group['key_skills']
                .dropna()
                .str.split(r'[\n,]+')  # Разделяем навыки по запятым и переносам строки
                .explode()
                .str.strip()
            )
            top_skills_by_year[year] = skills.value_counts().head(20).to_dict()
        return top_skills_by_year

    def save_statistics(self, avg_salary_by_year, vacancies_by_year, avg_salary_by_city, city_distribution, top_skills_by_year):
        """Сохраняем статистику в базе данных."""
        # Средняя зарплата по годам
        for year, salary in avg_salary_by_year.items():
            Python_avg_salary_by_year.objects.update_or_create(
                year=year,
                defaults={"salary": Decimal(salary)}
            )

        # Количество вакансий по годам
        for year, count in vacancies_by_year.items():
            Python_vacancies_by_year.objects.update_or_create(
                year=year,
                defaults={"count": count}
            )

        # Средняя зарплата по городам
        for city, salary in avg_salary_by_city.items():
            Python_avg_salary_by_city.objects.update_or_create(
                city=city,
                defaults={"salary": Decimal(salary)}
            )

        # Доля вакансий по городам
        for city, percentage in city_distribution.items():
            Python_city_distribution.objects.update_or_create(
                city=city,
                defaults={"percentage": Decimal(percentage)}
            )

        # Топ-20 навыков по годам
        for year, skills in top_skills_by_year.items():
            for skill, frequency in skills.items():
                Python_top_skills_by_year.objects.update_or_create(
                    year=year,
                    skills=skill,
                    defaults={"frequency": frequency}
                )
