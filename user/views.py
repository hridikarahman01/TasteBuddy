from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from home.views import home
from recipe.models import *

# Create your views here.

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(home)
        else:
            return render(request, 'userauth/login.html', {'error': 'Invalid username or password'})
    else:
        redirected_from = request.session.get('redirected_from')
        if redirected_from:
            del request.session['redirected_from']
            print(redirected_from)
            return render(request, 'userauth/login.html', {'success': 'Account created successfully. Please login to continue'})
        return render(request, 'userauth/login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password != password2:
            return render(request, 'userauth/signup.html', {'error': 'Passwords do not match'})
        elif User.objects.filter(username=username).exists():
            return render(request, 'userauth/signup.html', {'error': 'Username already exists'})
        elif User.objects.filter(email=email).exists():
            return render(request, 'userauth/signup.html', {'error': 'Email already exists'})

        user = User.objects.create_user(username, email, password)
        user.save()
        request.session['redirected_from'] = 'signup'
        return redirect(signin)
    else:
        return render(request, 'userauth/signup.html')

def signout(request):
    logout(request)
    return redirect(signin)


def profile(request, username):
    user = User.objects.get(username=username)
    recipes = Recipe.objects.filter(author=user)
    # get the user's liked recipes
    liked_recipes = []
    for recipe in Recipe.objects.all():
        if recipe.is_liked(user):
            liked_recipes.append(recipe)
    return render(request, 'userauth/userprofile.html', {'user': user, 'recipes': recipes, 'liked_recipes': liked_recipes})

def editprofile(request):
    user = request.user
    if not user.is_authenticated:
        return redirect(signin)
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        if request.POST.get('password') != '' and request.POST.get('password') == request.POST.get('password2'):
            user.set_password(request.POST.get('password'))
        user.save()
        return redirect(profile, user.username)
    else:
        return render(request, 'userauth/editprofile.html', {'user': user})





