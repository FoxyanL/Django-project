import requests
from xml.etree import ElementTree as ET
from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation
from django.core.management.base import BaseCommand
from main.models import Vacancy, CBank_rates
import time


class Command(BaseCommand):
    help = "Импортирует вакансии из базы данных и сохраняет курсы валют из ЦБР."

    def handle(self, *args, **kwargs):
        vacancies = Vacancy.objects.values('валюта')
        valutes = set(vacancy['валюта'] for vacancy in vacancies if vacancy['валюта'] and vacancy['валюта'] != "RUR")
        start_date = datetime(2005, 1, 1)
        end_date = datetime(2025, 1, 1)
        current_date = start_date
        
        while current_date <= end_date:
            formatted_date = current_date.strftime('%d/%m/%Y')

            try:
                url = f"https://www.cbr.ru/scripts/XML_daily.asp?date_req={formatted_date}"
                time.sleep(1)
                response = requests.get(url, timeout=10)
                response.raise_for_status()

                # Парсинг XML ответа
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
                                    CBank_rates.objects.create(
                                        currency=valute,
                                        rate=Decimal(rates),
                                        date=current_date,
                                    )
                                except Exception as e:
                                    # Логируем ошибку с полными данными строки
                                    self.stderr.write(self.style.ERROR(f"Ошибка при сохранении CBank_rates: {e}. Строка: {valute, rates, formatted_date}"))



            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Ошибка при получении курса валют: {e}"))
                continue  # Переходим к следующей дате
            current_date = current_date + timedelta(days=32)
            current_date = current_date.replace(day=1)

        self.stdout.write(self.style.SUCCESS('CBank_rates успешно импортированы!'))

