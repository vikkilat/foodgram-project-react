import csv
import os

from django.conf import settings

from recipes.models import Ingredient

FILE_DIR = os.path.join(settings.BASE_DIR, 'data')


def import_csv():
    """Импорт данных из csv."""
    with open(
        os.path.join(FILE_DIR, 'ingredients.csv'), 'r', encoding='utf-8'
    ) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name, unit = row
            Ingredient.objects.get_or_create(
                name=name, unit=unit
            )
        print(f'Файл {csvfile.name} загружен.')
