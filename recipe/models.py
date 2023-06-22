from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models import Count
from django.apps import apps


# Create your models here.

def upload_location_instructions(instance, filename):
    return "photos/recipe/instructions/%s/%s" %(instance.recipe_id, filename)


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Recipe_Step(models.Model):
    step = models.TextField()
    recipe_id = models.IntegerField()
    image = models.ImageField(upload_to=upload_location_instructions, blank=True)

    def __str__(self):
        return self.step




class Recipe(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField()
    time_required = models.CharField(max_length=100, blank=True)
    ingredients = models.TextField()
    instructions = models.ManyToManyField(Recipe_Step)
    photo = models.ImageField(upload_to='photos/recipe/thumbnails/' , blank=True, null=True)
    video = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(default=datetime.now)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    calories = models.IntegerField(blank=True, null=True)
    viewed_by = models.ManyToManyField(User, related_name='viewed_recipes', blank=True)

    def __str__(self):
        return self.title
    
    def total_likes(self):
        return self.likes.count()
    
    def is_liked(self, user):
        return self.likes.filter(id=user.id).exists()
    


def recommend_recipes(user):
    # Get the UserFavourites instance for this user
    UserFavourites = apps.get_model('user', 'UserFavourites')
    user_favourites = UserFavourites.objects.get(user=user)

    # Get recipes from the user's favorite categories
    favorite_categories = user_favourites.favorite_categories.all()
    category_recipes = Recipe.objects.filter(category__in=favorite_categories)

    # Get recipes liked or shared by users with similar interests
    similar_users_favourites = UserFavourites.objects.filter(favorite_categories__in=favorite_categories).exclude(user=user)
    similar_users = [favourites.user for favourites in similar_users_favourites]
    similar_users_recipes = Recipe.objects.filter(likes__in=similar_users)

    # Merge the two QuerySets
    recommended_recipes = category_recipes | similar_users_recipes

    # Order the recipes by the number of likes and shares
    recommended_recipes = recommended_recipes.annotate(num_likes=Count('likes')).order_by('-num_likes')

    return recommended_recipes


class Review(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.TextField()
    created_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.review