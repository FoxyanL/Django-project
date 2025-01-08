import pandas as pd
from decimal import Decimal, InvalidOperation
from django.db.models import Q
from main.models import *
from decimal import Decimal, InvalidOperation
from django.core.management.base import BaseCommand


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
        # Чтение файла с обработкой mixed types
        dtype_map = {
            "salary_from": "str",
            "salary_to": "str",
        }
        df = pd.read_csv(file_path, encoding='utf-8-sig', low_memory=False, dtype=dtype_map)

        # Предварительная обработка зарплат
        def process_salary(value):
            """Обрабатывает зарплатное значение, возвращает Decimal или None."""
            try:
                if value and float(value) < 1_000_000:  # Фильтр на корректные значения
                    return Decimal(str(value).replace(',', '.'))
            except (ValueError, InvalidOperation):
                return None
            return None

        df['salary_from'] = df['salary_from'].apply(process_salary)
        df['salary_to'] = df['salary_to'].apply(process_salary)

        # Удаляем строки с некорректными значениями
        df = df.dropna(subset=['name', 'published_at'])

        # Преобразуем даты публикации
        df['published_at'] = pd.to_datetime(df['published_at'], errors='coerce', utc=True)
        df = df.dropna(subset=['published_at'])

        # Вычисляем среднюю зарплату
        df['avg_salary'] = (df['salary_from'].fillna(0) + df['salary_to'].fillna(0)) / 2

        # Добавляем год публикации
        df['year'] = df['published_at'].dt.year

        # Получение курсов валют из базы данных
        def get_exchange_rate(currency, date):
            """Ищет курс валюты для конкретной даты в модели CBank_rates."""
            try:
                rate_obj = CBank_rates.objects.filter(
                    Q(currency=currency) & Q(date=date.date())
                ).first()
                return float(rate_obj.rate) if rate_obj and rate_obj.rate else None
            except Exception as e:
                print(f"Ошибка получения курса валют для {currency} на {date}: {e}")
                return None

        # Конвертация валют
        def convert_to_rub(row):
            """Конвертирует зарплату в рубли."""
            if row['avg_salary'] and row['salary_currency']:
                if row['salary_currency'] == 'RUR':
                    return float(row['avg_salary'])
                rate = get_exchange_rate(row['salary_currency'], row['published_at'])
                if rate:
                    return float(row['avg_salary']) * rate
            return None

        df['avg_salary_rub'] = df.apply(convert_to_rub, axis=1)

        # Анализ данных
        # 1. Средняя зарплата по годам
        avg_salary_by_year = (
            df.groupby('year')['avg_salary_rub']
            .mean()
            .dropna()
            .to_dict()
        )

        # 2. Количество вакансий по годам
        vacancies_by_year = (
            df.groupby('year').size()
            .to_dict()
        )

        # 3. Средняя зарплата по городам
        avg_salary_by_city = (
            df.groupby('area_name')['avg_salary_rub']
            .mean()
            .dropna()
            .sort_values(ascending=False)
            .to_dict()
        )

        # 4. Доля вакансий по городам
        total_vacancies = len(df)
        city_distribution = (
            df['area_name'].value_counts(normalize=True) * 100
        )
        # Фильтруем только те города, доля которых >= 1%
        city_distribution = city_distribution[city_distribution >= 1].to_dict()

        # 5. Топ-20 навыков по годам
        skills_by_year = {}
        for year, group in df.groupby('year'):
            # Проверяем, есть ли ненулевые key_skills в текущем году
            if group['key_skills'].dropna().empty:
                continue
            
            # Разделяем ключевые навыки, убираем пробелы и считаем частоту
            skills = (
                group['key_skills']
                .dropna()
                .str.split(r'[\n,]+')  # Разделяем по запятым или переносам строки
                .explode()
                .str.strip()
            )
            
            # Подсчет топ-20 навыков
            top_skills = skills.value_counts().head(20).to_dict()
            skills_by_year[year] = top_skills


        # Вывод статистики

        #НУЖНО СДЕЛАТЬ ЗАПОЛНЕНИЕ МОДЕЛЕЙ!!!!!!!

# Заполняем модель All_avg_salary_by_year
        for year, salary in avg_salary_by_year.items():
            try:
                All_avg_salary_by_year.objects.update_or_create(
                    year=year,
                    salary=Decimal(salary)  # Преобразуем среднюю зарплату в Decimal
                )
            except Exception as e:
                self.stderr.write(self.style.ERROR(f'Ошибка при импорте: {e}. Строка {year} {salary}'))
        
        for year, count in vacancies_by_year.items():
            try:
                All_vacancies_by_year.objects.update_or_create(
                    year=year,
                    count=Decimal(count)  # Преобразуем среднюю зарплату в Decimal
                )
            except Exception as e:
                self.stderr.write(self.style.ERROR(f'Ошибка при импорте: {e}. Строка {year} {count}'))
        
        for city, salary in avg_salary_by_city.items():
            try:
                All_avg_salary_by_city.objects.update_or_create(
                    city=city,
                    salary=Decimal(salary)  # Преобразуем среднюю зарплату в Decimal
                )
            except Exception as e:
                self.stderr.write(self.style.ERROR(f'Ошибка при импорте: {e}. Строка {city} {salary}'))

        for city, percentage in city_distribution.items():
            try:
                All_city_distribution.objects.update_or_create(
                    city=city,
                    percentage=Decimal(percentage)  # Преобразуем среднюю зарплату в Decimal
                )
            except Exception as e:
                self.stderr.write(self.style.ERROR(f'Ошибка при импорте: {e}. Строка {city} {percentage}'))

        # Заполняем модель All_top_skills_by_year
        for year, skills in skills_by_year.items():
            for skill, frequency in skills.items():
                try:
                    All_top_skills_by_year.objects.update_or_create(
                        year=year,
                        skills=skill,
                        frequency=frequency  # Частота использования навыка
                    )
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f'Ошибка при импорте: {e}. Год: {year}, Навык: {skill}, Частота: {frequency}')) 
