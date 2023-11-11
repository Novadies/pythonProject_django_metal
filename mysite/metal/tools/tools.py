DieMigrationsDie = False
START_DB=False
DEATH=False

if DieMigrationsDie:
    from django.db import connection #удаление всех миграций
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM 'django_migrations' WHERE 'app'='metal'")

if START_DB:
        # удаление начальных данных
    if DEATH:
        from metal.models import *
        Metal.objects.all().delete()
        Metal_2.objects.all().delete()
        Metal_info.objects.all().delete()
        Metal_class.objects.all().delete()
        MetalSearch.objects.all().delete()

    from metal.tools.csv_to_bd import zapis
    with open('metal\sourse\metal.csv') as f: zapis(f)