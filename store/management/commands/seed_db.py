import os
from pathlib import Path
from django.db import connection
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Populates dastabase with collections and products'

    def handle(self,*args,**options):
        print('populating the database')
        curr_dir = os.path.dirname(__file__)
        file_path = os.path.join(curr_dir,'seed.sql')

        sql = Path(file_path).read_text()

        with connection.cursor() as cursor:
            cursor.execute(sql)
