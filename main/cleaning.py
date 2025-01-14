import os
import glob

def clean_old_charts(directory, prefix):
    files = glob.glob(os.path.join(directory, f"{prefix}_*.png"))
    for file in files:
        try:
            os.remove(file)
            print(f"Удален старый файл: {file}")
        except Exception as e:
            print(f"Не удалось удалить файл {file}: {e}")