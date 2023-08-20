from .models import *

             #удаление всех миграций
# from django.db import connection
# with connection.cursor() as cursor:
#     cursor.execute("DELETE FROM 'django_migrations' WHERE 'app'='metal'")


START_DB=False
if START_DB:
        # удаление начальных данных
    Metal.objects.all().delete()
    Metal_2.objects.all().delete()
    Metal_info.objects.all().delete()
    Metal_class.objects.all().delete()
    from .csv_to_bd import zapis
    with open('metal\sourse\metal.csv') as f: zapis(f)

OBRABOTKA=False
if OBRABOTKA:
    pass