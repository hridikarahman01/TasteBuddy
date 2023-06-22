from django.shortcuts import render, redirect, reverse
from recipe.models import recommend_recipes
from user.models import UserFavourites

# Create your views here.



def home(request):
    if request.user.is_authenticated:
        try:
            recommended_recipes = recommend_recipes(request.user)
        except:
            UserFavourites.objects.create(user=request.user)
            recommended_recipes = recommend_recipes(request.user)
        return render(request, 'home/index.html',{'user':request.user, 'recommended_recipes':recommended_recipes})
    else:
        return redirect(reverse('signin'))