import requests
from xml.etree import ElementTree as ET

def get_exchange_rate(date: str, currency: str) -> float:
    """
    Получает курс валюты по отношению к рублю на указанную дату.
    date: Дата в формате 'DD/MM/YYYY'
    currency: Код валюты (например, USD, EUR)
    """
    if currency == "RUR":
        return 1.0  # Рубль не требует конвертации

    try:
        url = f"https://www.cbr.ru/scripts/XML_daily.asp?date_req={date}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Парсинг XML ответа
        tree = ET.fromstring(response.content)
        for valute in tree.findall("Valute"):
            char_code = valute.find("CharCode").text
            if char_code == currency:
                value = valute.find("Value").text
                return float(value.replace(",", "."))

        # Если указанная валюта не найдена
        raise ValueError(f"Курс для валюты '{currency}' не найден на дату {date}")

    except Exception as e:
        print(f"Ошибка при получении курса валют: {e}")
        return None
