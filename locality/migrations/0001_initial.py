# Generated by Django 2.2.10 on 2020-09-09 16:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('locality_type', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Locality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('locality_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locality_type.LocalityType')),
            ],
            options={
                'db_table': 'locality',
            },
        ),
        migrations.CreateModel(
            name='SectorisationLocality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('locality_inf', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='id_locality_inf', to='locality.Locality')),
                ('locality_sup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='id_locality_sup', to='locality.Locality')),
            ],
            options={
                'db_table': 'sectorisation_locality',
            },
        ),
        migrations.CreateModel(
            name='Allocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('description', models.CharField(max_length=100, null=True)),
                ('locality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locality.Locality')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'allocation',
            },
        ),
    ]
