# Generated by Django 4.0.2 on 2022-02-26 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contatos', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='categoria',
            old_name='categoria',
            new_name='nome',
        ),
    ]
