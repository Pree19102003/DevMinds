from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('upload/', views.upload_resource, name='upload'),
    path('search/', views.search, name='search'),
    path('resource/<int:id>/', views.view_resource, name='view_resource'),

]
