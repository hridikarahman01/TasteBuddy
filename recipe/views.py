from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from user.models import UserFavourites

# Create your views here.

def add_recipe(request):
    if request.method == 'POST':
        # Get the data submitted by the form
        title = request.POST['title']
        category_id = request.POST['category']
        description = request.POST['description']
        time_required = request.POST['time_required']
        calories = request.POST['calory_count']
        ingredients = request.POST['ingredients']
        photo = request.FILES.get('photo')
        video = request.POST['video']
        
        # Create a new recipe instance
        try:
            recipe = Recipe(title=title, author=request.user, description=description, time_required=time_required, ingredients=ingredients, photo=photo, video=video)
            recipe.category_id = category_id
            recipe.save()
        except Exception as e:
            return render(request, 'recipe/addrecipe.html', {'categories': Category.objects.all(), 'error': 'An error occurred while adding the recipe. Please try again.'})
        
        # Get the instructions submitted by the user and add them to the recipe instance
        for key in request.POST.keys():
            if key.startswith('instruction_'):
                step_text = request.POST[key]
                step = Recipe_Step(step=step_text, recipe_id=recipe.id)
                step.save()
                recipe.instructions.add(step)
        
        return redirect('view_recipe', recipe_id=recipe.id)
    else:
        return render(request, 'recipe/addrecipe.html', {'categories': Category.objects.all()})


def add_images(request, recipe_id):
    if request.method == 'POST':
        recipe = Recipe.objects.get(id=recipe_id)
        steps = recipe.instructions.all()
        for step in steps:
            image = request.FILES.get(str(step.id))
            step.image = image
            step.save()
        return redirect('view_recipe', recipe_id=recipe_id)
    else:
        return render(request, 'recipe/addimages.html', {'steps': Recipe_Step.objects.filter(recipe_id=recipe_id), 'recipe_id': recipe_id})


def edit_recipe(request, recipe_id):
    if request.method == 'POST':
        recipe = Recipe.objects.get(id=recipe_id)
        recipe.title = request.POST['title']
        recipe.category_id = request.POST['category']
        recipe.description = request.POST['description']
        recipe.time_required = request.POST['time_required']
        recipe.calories = request.POST['calory_count']
        recipe.ingredients = request.POST['ingredients']
        recipe.photo = request.FILES.get('photo')
        recipe.video = request.POST['video']
        recipe.save()
        return redirect('view_recipe', recipe_id=recipe_id)
    else:
        recipe = Recipe.objects.get(id=recipe_id)
        return render(request, 'recipe/editrecipe.html', {'recipe': recipe, 'categories': Category.objects.all()})
    

def view_recipe(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    user = request.user
    all_comments = Review.objects.filter(recipe=recipe)
    # add the user to the list of users who have viewed the recipe
    recipe.viewed_by.add(user)
    # add the category of the recipe to the list of categories liked by the user
    user_favourites = UserFavourites.objects.get(user=user)
    user_favourites.favorite_categories.add(recipe.category)
    instructions = recipe.instructions.all()
    is_liked = recipe.is_liked(request.user)
    return render(request, 'recipe/viewrecipe.html', {'recipe': recipe, 'instructions': instructions, 'is_liked': is_liked, 'likes_count': recipe.total_likes(), 'comments': all_comments})


def delete_recipe(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    recipe.delete()
    return redirect('view_all_recipes')

def view_all_recipes(request):
    if request.method == 'POST':
        search_term = request.POST['search']
        # Get all recipes whose title or description or ingredients contains the search term
        recipes = Recipe.objects.filter(title__icontains=search_term) | Recipe.objects.filter(description__icontains=search_term) | Recipe.objects.filter(ingredients__icontains=search_term)
        return render(request, 'recipe/viewallrecipes.html', {'recipes': recipes, 'search_term': search_term})
    recipes = Recipe.objects.all()
    return render(request, 'recipe/viewallrecipes.html', {'recipes': recipes})


def view_user_recipes(request, username):
    user = User.objects.get(username=username)
    recipes = Recipe.objects.filter(author=user)
    return render(request, 'recipe/viewallrecipes.html', {'recipes': recipes, 'user': user})


def like_recipe(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    recipe.likes.add(request.user)
    return redirect('view_recipe', recipe_id=recipe_id)


def unlike_recipe(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    recipe.likes.remove(request.user)
    return redirect('view_recipe', recipe_id=recipe_id)


def add_review(request, recipe_id):
    if request.method == 'POST':
        review = Review(review=request.POST['review'], recipe_id=recipe_id, user=request.user)
        review.save()
        return redirect('view_recipe', recipe_id=recipe_id)
    else:
        return redirect('view_recipe', recipe_id=recipe_id)


def delete_review(request, review_id):
    review = Review.objects.get(id=review_id)
    recipe_id = review.recipe.id
    review.delete()
    return redirect('view_recipe', recipe_id=recipe_id)