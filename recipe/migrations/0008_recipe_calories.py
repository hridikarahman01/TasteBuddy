# Generated by Django 4.0.2 on 2023-06-18 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0007_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='calories',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]