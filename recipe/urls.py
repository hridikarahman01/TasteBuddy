from django.urls import path
from .views import *
from home.views import home

urlpatterns = [
    path('addrecipe/', add_recipe, name='add_recipe'),
    path('addimages/<int:recipe_id>/', add_images, name='add_images'),
    path('editrecipe/<int:recipe_id>/', edit_recipe, name='edit_recipe'),
    path('deleterecipe/<int:recipe_id>/', delete_recipe, name='delete_recipe'),
    path('viewrecipe/<int:recipe_id>/', view_recipe, name='view_recipe'),
    path('viewallrecipes/', view_all_recipes, name='view_all_recipes'),
    path('viewallrecipes/<str:username>/', view_user_recipes, name='view_user_recipes'),
    path('like/<int:recipe_id>/', like_recipe, name='like_recipe'),
    path('unlike/<int:recipe_id>/', unlike_recipe, name='unlike_recipe'),
    path('addreview/<int:recipe_id>/', add_review, name='add_review'),
    path('deletereview/<int:review_id>/', delete_review, name='delete_review'),
    path('', home, name='home')

]