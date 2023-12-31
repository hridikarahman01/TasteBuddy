# Generated by Django 4.0.2 on 2023-05-18 20:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recipe', '0006_recipe_viewed_by'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFavourites',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('favorite_categories', models.ManyToManyField(blank=True, related_name='liked_by_users', to='recipe.Category')),
            ],
        ),
    ]
