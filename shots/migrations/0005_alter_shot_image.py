# Generated by Django 3.2 on 2022-05-19 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shots', '0004_alter_shot_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shot',
            name='image',
            field=models.ImageField(blank=True, default='media/default_image.jpg', upload_to=''),
        ),
    ]