from django.core.management.base import BaseCommand
from main.models import Vacancy

class Command(BaseCommand):
    help = 'Удаляет все вакансии из базы данных'

    def handle(self, *args, **kwargs):
        count, _ = Vacancy.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Удалено {count} вакансий'))
