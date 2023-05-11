import csv
import os

from django.db.utils import IntegrityError
from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient

FILE_DIR = os.path.join(settings.BASE_DIR, 'data')


class Command(BaseCommand):
    help = 'Загрузка из csv файла'

    def handle(self, *args, **kwargs):
        with open(
            os.path.join(FILE_DIR, 'ingredients.csv'), 'r', encoding='utf-8'
        ) as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                name, measurement_unit = row
                try:
                    Ingredient.objects.create(
                        name=name,
                        measurement_unit=measurement_unit
                    )
                except IntegrityError:
                    self.stdout.write(
                        f'Ингредиент {name} уже существует в базе данных'
                    )
        self.stdout.write(self.style.SUCCESS('Все ингридиенты загружены!'))
