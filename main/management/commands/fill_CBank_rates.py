import requests
from xml.etree import ElementTree as ET
from datetime import datetime, timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand
import time
import pandas as pd
from main.models import CBank_rates


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
        dtype_map = {"salary_from": "str", "salary_to": "str", "salary_currency": "str"}
        df = pd.read_csv(file_path, encoding='utf-8-sig', dtype=dtype_map, low_memory=False)
        filtered_currencies = df['salary_currency'].dropna()
        valutes = filtered_currencies[filtered_currencies != 'RUR'].unique()
        start_date = datetime(2003, 1, 1)
        end_date = datetime(2025, 1, 1)
        current_date = start_date
        
        while current_date <= end_date:
            formatted_date = current_date.strftime('%d/%m/%Y')

            try:
                url = f"https://www.cbr.ru/scripts/XML_daily.asp?date_req={formatted_date}"
                time.sleep(3)
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                              
                tree = ET.fromstring(response.content)
                rates = None
                for valute in valutes:
                    for val in tree.findall("Valute"):
                        char_code = val.find("CharCode").text
                        if char_code == valute:
                            vunit_rate = val.find("VunitRate")
                            if vunit_rate is not None:
                                rates = float(vunit_rate.text.replace(",", "."))
                                try:
                                    CBank_rates.objects.update_or_create(
                                        currency=valute,
                                        rate=Decimal(rates),
                                        date=current_date,
                                    )
                                except Exception as e:
                                    self.stderr.write(self.style.ERROR(f"Ошибка при сохранении CBank_rates: {e}. Строка: {valute, rates, formatted_date}"))



            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Ошибка при получении курса валют: {e}"))
                continue
            current_date = current_date + timedelta(days=32)
            current_date = current_date.replace(day=1)

        self.stdout.write(self.style.SUCCESS('CBank_rates успешно импортированы!'))

