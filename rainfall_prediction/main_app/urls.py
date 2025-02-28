from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
        path('logout/', views.logout_user, name='logout'),

    path('about_us/', views.about_us, name='about_us'),
    path('feedback/', views.feedback, name='feedback'),
    path('contact_us/', views.contact_us, name='contact_us'),
     path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
]



