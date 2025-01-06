import requests
from xml.etree import ElementTree as ET
from main.models import CBank_rates

def get_exchange_rate(date, currency):
    """
    Получает курс валюты по отношению к рублю на указанную дату.
    date: Дата в формате 'DD/MM/YYYY'
    currency: Код валюты (например, USD, EUR)
    """

    year, month = date.year, date.month
    rate_record = CBank_rates.objects.filter(
        currency=currency,
        date__year=year,  # Условие для года
        date__month=month  # Условие для месяца
    ).first()
    if rate_record:
        rate = rate_record.rate
        return rate
    else:
        return None

