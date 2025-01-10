from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Удаляет определённые таблицы из SQLite базы данных'

    def handle(self, *args, **kwargs):
        # Укажите список таблиц, которые нужно удалить
        tables_to_delete = ['All_vacancies', 'Vacancy']  # Замените на ваши имена таблиц

        with connection.cursor() as cursor:
            cursor.execute("PRAGMA foreign_keys=OFF;")  # Отключаем внешние ключи
            cursor.execute("BEGIN TRANSACTION;")

            for table in tables_to_delete:
                self.stdout.write(f'Удаляется таблица: {table}')
                cursor.execute(f"DROP TABLE IF EXISTS {table};")  # Удаляем таблицу

            cursor.execute("COMMIT;")  # Завершаем транзакцию

        self.stdout.write(self.style.SUCCESS('Указанные таблицы успешно удалены!'))
