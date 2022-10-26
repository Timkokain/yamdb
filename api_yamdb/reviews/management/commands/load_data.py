import csv
import logging.config
from logging.handlers import RotatingFileHandler

from django.core.management.base import BaseCommand
from django.db import IntegrityError

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import CustomUser

logging.basicConfig(
    level=logging.INFO,
    filename='log.txt',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s',
    filemode='w',
)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler('log.txt', maxBytes=50000000, backupCount=5)
logger.addHandler(handler)
handler.setFormatter(formatter)


FILE_DICT = (
    {Category: 'static/data/category.csv'},
    {Genre: 'static/data/genre.csv'},
    {CustomUser: 'static/data/users.csv'},
    {Title: 'static/data/titles.csv'},
    {Review: 'static/data/review.csv'},
    {Comment: 'static/data/comments.csv'},
    {Genre: 'static/data/genre_title.csv'}
)

KEY_DICT = {
    'author': 'author_id',
    'category': 'category_id',
}


def validate(row):
    """Проверяем правильность названий полей в csv-файле"""
    for key, value in KEY_DICT.items():
        if key in row and row[key].isdigit():
            row[value] = row.pop(key)
    return row


class Command(BaseCommand):
    """Класс для чтения файла csv и записи данных в базу данных"""
    def handle(self, *args, **options):
        for i in range(len(FILE_DICT)):
            key, value = FILE_DICT[i].popitem()
            with open(value, encoding='utf-8', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        model_object = key(**row)
                        model_object.save()
                    except IntegrityError as error:
                        logger.error(f'Ошибка записи в базу данных: {error}')
                    except TypeError:
                        title = Title.objects.get(pk=row['title_id'])
                        genre = Genre.objects.get(pk=row['genre_id'])
                        title.genre.add(genre)
                        title.save()
                    except Exception:
                        validated_data = validate(row)
                        model_object = key(**validated_data)
                        model_object.save()
