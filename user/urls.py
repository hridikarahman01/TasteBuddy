from django.urls import path
from .views import *

urlpatterns = [
    path('login/', signin, name='signin'),
    path('logout/', signout, name='signout'),
    path('register/', signup, name='signup'),
    path('profile/<str:username>', profile, name='profile'),
    path('editprofile/', editprofile, name='editprofile'),

]