from django.urls import path
from . import views

urlpatterns = [
    path('siignup/', views.signup,name='signup'),
    path('', views.login,name='login'),
    path('home/', views.home,name='home'),
    path('logout/', views.logout,name='logout'),
    path('myadmin/', views.myadmin,name='myadmin'),
    path('adduser/', views.adduser,name='adduser'),
    path('edituser/<int:id>', views.edituser,name='edituser'),
    path('deleteuser/<int:id>', views.deleteuser,name='deleteuser'),
    path('searchuser/', views.searchuser,name='searchuser'),
]