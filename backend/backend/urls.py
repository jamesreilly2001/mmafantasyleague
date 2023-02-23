"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.signIn, name="signIn"),
    path('postsign', views.postsign, name="postsign"),
    path('logout', views.logout, name="logout"),
    path('signup', views.signUp, name="signUp"),
    path('postsignup', views.postsignup, name="postsignup"),
    path('choosefighters', views.choosefighters, name="choosefighters"),
    path('joinleague', views.joinleague, name="joinleague" ),
    path('postjoinleague', views.postjoinleague, name="postjoinleague" ),
    path('createleague',views.createleague, name="createleague"),
    path('postcreateleague',views.postcreateleague, name="postcreateleague"),
    path('leaguetable',views.leaguetable, name="leaguetable"),
    path('save_choices',views.save_choices, name="save_choices"),
    path('fighter_selection',views.fighter_selection, name="fighter_selection"),
    path('home',views.home, name="home"),
    path('points_earned',views.points_earned, name="points_earned"),
    path('pointsystem',views.pointsystem, name="pointsystem"),
    path('andradre_blanchfield',views.andradre_blanchfield, name="andradre_blanchfield")




    









    ]
