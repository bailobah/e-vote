# Generated by Django 2.2.10 on 2020-08-24 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20200824_1703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='id',
            field=models.PositiveIntegerField(choices=[(2, 'VICE PRESIDENT'), (4, 'ADMIN SOUS PREFECTORAL'), (3, 'ADMIN PREFECTORAL'), (1, 'PRESIDENT')], primary_key=True, serialize=False),
        ),
    ]
