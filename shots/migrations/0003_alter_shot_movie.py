# Generated by Django 3.2 on 2022-05-19 13:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
        ('shots', '0002_auto_20220519_2151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shot',
            name='movie',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='movies.movie'),
        ),
    ]
