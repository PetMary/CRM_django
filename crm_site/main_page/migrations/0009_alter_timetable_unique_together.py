# Generated by Django 4.2.1 on 2023-05-28 17:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0008_alter_timetable_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='timetable',
            unique_together={('id_employee', 'date')},
        ),
    ]
