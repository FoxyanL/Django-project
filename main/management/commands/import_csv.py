import csv
from datetime import datetime
from decimal import Decimal, InvalidOperation
from django.core.management.base import BaseCommand
from main.models import Vacancy


class Command(BaseCommand):
    help = "Импортирует вакансии из CSV файла в базу данных."

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file',
            type=str,
            help='Путь к CSV файлу с вакансиями'
        )

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        try:
            with open(csv_file, newline='', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if not any(keyword in row['name'].lower() for keyword in ['python', 'питон', 'пайтон']):
                        continue
                    # Обработка минимальной зарплаты
                    минимальная_зарплата = None
                    if row['salary_from'] and int(float(row['salary_from'])) < 1000000:  # Проверка на пустое значение
                        try:
                            минимальная_зарплата = Decimal(row['salary_from'].replace(',', '.'))
                        except InvalidOperation:
                            self.stderr.write(self.style.ERROR(f"Некорректное значение в поле 'salary_from': {row['salary_from']}"))
                            минимальная_зарплата = None
                    
                    # Обработка максимальной зарплаты
                    максимальная_зарплата = None
                    if row['salary_to'] and int(float(row['salary_to'])) < 1000000:  # Проверка на пустое значение
                        try:
                            максимальная_зарплата = Decimal(row['salary_to'].replace(',', '.'))
                        except InvalidOperation:
                            self.stderr.write(self.style.ERROR(f"Некорректное значение в поле 'salary_to': {row['salary_to']}"))
                            максимальная_зарплата = None
                    
                    # Создание вакансии в базе данных
                    try:
                        Vacancy.objects.create(
                            название=row['name'],
                            минимальная_зарплата=минимальная_зарплата,
                            максимальная_зарплата=максимальная_зарплата,
                            валюта=row['salary_currency'],
                            город=row['area_name'],
                            дата_публикации=datetime.strptime(row['published_at'], '%Y-%m-%dT%H:%M:%S%z'),
                            key_skills=row['key_skills'],
                        )
                    except Exception as e:
                        # Логируем ошибку с полными данными строки
                        self.stderr.write(self.style.ERROR(f"Ошибка при сохранении вакансии: {e}. Строка: {row}"))

            self.stdout.write(self.style.SUCCESS('Вакансии успешно импортированы!'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Ошибка при импорте: {e}'))
