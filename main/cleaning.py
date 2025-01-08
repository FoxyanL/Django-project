import os
import glob

# Функция для очистки старых графиков
def clean_old_charts(directory, prefix):
    # Поиск всех файлов с указанным префиксом в указанной директории
    files = glob.glob(os.path.join(directory, f"{prefix}_*.png"))
    for file in files:
        try:
            os.remove(file)
            print(f"Удален старый файл: {file}")
        except Exception as e:
            print(f"Не удалось удалить файл {file}: {e}")