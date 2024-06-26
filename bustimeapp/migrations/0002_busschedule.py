# Generated by Django 5.0.4 on 2024-06-15 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bustimeapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_dia', models.IntegerField()),
                ('cod_variante', models.IntegerField()),
                ('frecuencia', models.IntegerField()),
                ('cod_ubic_parada', models.IntegerField()),
                ('ordinal', models.IntegerField()),
                ('hora', models.IntegerField()),
                ('dia_anterior', models.CharField()),
            ],
        ),
    ]
