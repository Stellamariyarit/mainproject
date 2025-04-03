# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('register/', views.register, name='register'),
#     path('login/', views.login_view, name='login'),
#         path('logout/', views.logout_user, name='logout'),

#     path('about_us/', views.about_us, name='about_us'),
#     path('feedback/', views.feedback, name='feedback'),
#     path('contact_us/', views.contact_us, name='contact_us'),
#      path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
#     path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
# ]


from django.urls import path
from . import views
# from .views import predict_rainfall
from .views import save_location
from .views import send_email_alerts
from .views import get_alerted_users



urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('about-us/', views.about_us, name='about_us'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('feedback/', views.feedback, name='feedback'),
    path('predict-rainfall/', views.predict_rainfall, name='predict_rainfall'),

    # path('predict/', predict_rainfall, name='predict_rainfall'),
    path('save-location/', save_location, name='save_location'),


    path('predict_rainfall_api/', views.predict_rainfall_api, name='predict_rainfall_api'),
    path('get-prediction/', views.get_prediction, name='get_prediction'),
    # path("send-email-alerts/", send_email_alerts, name="send_email_alerts"),
    path("send_email_alerts/", send_email_alerts, name="send_email_alerts"),
    path("get_alerted_users/", get_alerted_users, name="get_alerted_users"),

]


