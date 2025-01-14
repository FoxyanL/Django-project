from main.models import CBank_rates
from django.db.models import Q

def get_exchange_rate(currency, date):
    try:
        rate_obj = CBank_rates.objects.filter(
            Q(currency=currency) & Q(date=date.date())
        ).first()
        return float(rate_obj.rate) if rate_obj and rate_obj.rate else None
    except Exception as e:
        print(f"Ошибка получения курса валют для {currency} на {date}: {e}")
        return None

