from django.db import models
from django.apps import apps
from django.contrib.auth.models import User

class UserFavourites(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    favorite_categories = models.ManyToManyField('recipe.Category', related_name='liked_by_users', blank=True)

