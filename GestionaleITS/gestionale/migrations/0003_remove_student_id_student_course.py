# Generated by Django 4.2.16 on 2024-10-24 14:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestionale', '0002_supplier_is_deleted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='id_student_course',
        ),
    ]
