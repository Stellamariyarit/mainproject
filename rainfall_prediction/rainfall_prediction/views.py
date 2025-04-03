import joblib
import numpy as np
from tensorflow import keras
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Feedback, RainfallPrediction
from .forms import UserRegistrationForm, UserProfileForm, ContactForm, FeedbackForm
from .utils import get_weather_data


import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rf_model = joblib.load(os.path.join(BASE_DIR, 'main_app/ml_model/random_forest_model.pkl'))
svm_model = joblib.load(os.path.join(BASE_DIR, 'main_app/ml_model/svm_model.pkl'))
lstm_model = keras.models.load_model(os.path.join(BASE_DIR, 'main_app/ml_model/lstm_model.keras'))


# Home Page
def home(request):
    forecast = RainfallPrediction.objects.all().order_by('date')[:5]
    return render(request, 'main_app/home.html', {'forecast': forecast})


# Registration
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()

    return render(request, 'main_app/register.html', {'user_form': user_form, 'profile_form': profile_form})

# Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_dashboard' if user.is_superuser else 'user_dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'main_app/login.html')

# Logout
def logout_user(request):
    logout(request)
    return redirect('home')

import matplotlib.pyplot as plt
import io
import base64

# Load the model
try:
    rf_model = joblib.load('main_app/ml_model/random_forest_model.pkl')
    # rf_model = joblib.load(os.path.join(BASE_DIR, 'main_app/ml_model/random_forest_model.pkl'))

    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {str(e)}")
    rf_model = None

# def user_dashboard(request):
#     rainfall_forecast = []
#     alert_levels = []
#     graph_base64 = None

#     if request.method == 'POST':
#         try:
#             # Extracting feature inputs for five-day prediction
#             features = [float(request.POST.get(f'feature{i}', 0)) for i in range(1, 19)]

#             if rf_model is None:
#                 return render(request, 'main_app/user_dashboard.html', {'error': 'Model not loaded.'})

#             if len(features) != rf_model.n_features_in_:
#                 return render(request, 'main_app/user_dashboard.html', {'error': 'Invalid number of features.'})

#             # Convert features to NumPy array for prediction
#             features_array = np.array(features).reshape(1, -1)

#             # Generate rainfall predictions for the next 5 days
#             for i in range(5):
#                 predicted_rainfall = rf_model.predict(features_array)[0]
#                 rainfall_forecast.append(predicted_rainfall)

#                 # Determine Alert Level
#                 if predicted_rainfall < 20:
#                     alert_levels.append("Green")
#                 elif 20 <= predicted_rainfall < 50:
#                     alert_levels.append("Yellow")
#                 elif 50 <= predicted_rainfall < 100:
#                     alert_levels.append("Orange")
#                 else:
#                     alert_levels.append("Red")

#             # Generate Graph for the Five-Day Forecast
#             plt.figure(figsize=(8, 5))
#             plt.bar(["Day 1", "Day 2", "Day 3", "Day 4", "Day 5"], rainfall_forecast, color=['green', 'yellow', 'orange', 'red', 'red'])
#             plt.xlabel('Days')
#             plt.ylabel('Predicted Rainfall (mm)')
#             plt.title('Five-Day Rainfall Forecast')

#             # Save graph to base64
#             buf = io.BytesIO()
#             plt.savefig(buf, format='png')
#             buf.seek(0)
#             graph_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
#             buf.close()

#         except Exception as e:
#             return render(request, 'main_app/user_dashboard.html', {'error': str(e)})

#     return render(request, 'main_app/user_dashboard.html', {
#         'rainfall_forecast': rainfall_forecast,
#         'alert_levels': alert_levels,
#         'graph': graph_base64,
#     })

from .models import Alert

def user_dashboard(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Get JSON data from request
            features = [float(data.get(f'feature{i}', 0)) for i in range(1, 19)]

            if rf_model is None:
                return JsonResponse({"error": "Model not loaded."}, status=400)

            if len(features) != rf_model.n_features_in_:
                return JsonResponse({"error": "Invalid number of features."}, status=400)

            # Convert features to NumPy array
            features_array = np.array(features).reshape(1, -1)

            # Generate rainfall predictions for the next 5 days
            rainfall_forecast = [rf_model.predict(features_array)[0] for _ in range(5)]
            alert_levels = [
                "Green" if r < 20 else "Yellow" if r < 50 else "Orange" if r < 100 else "Red"
                for r in rainfall_forecast
            ]

            return JsonResponse({
                "rainfall_forecast": rainfall_forecast,
                "alert_levels": alert_levels,
                "rainfall_amount": rainfall_forecast[0],  # Today's rainfall
                "alert_level": alert_levels[0]  # Today's alert level
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # **GET request: Fetch alerts for the logged-in user**
    alerts = Alert.objects.filter(user=request.user).order_by('-created_at')  
    return render(request, "main_app/user_dashboard.html", {"alerts": alerts})
def admin_dashboard(request):
    return render(request, 'main_app/admin_dashboard.html')

# About Us Page
def about_us(request):
    return render(request, 'main_app/about_us.html')

# Contact Us
def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Message sent successfully!')
            return redirect('home')
    else:
        form = ContactForm()
    return render(request, 'main_app/contact_us.html', {'form': form})

# Feedback
def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Feedback submitted successfully!')
            return redirect('feedback')
    else:
        form = FeedbackForm()
    return render(request, 'main_app/feedback.html', {'form': form})

# Predict Rainfall using User Input
def predict_rainfall(request):
    if request.method == 'POST':
        try:
            temperature = float(request.POST.get('temperature'))
            humidity = float(request.POST.get('humidity'))
            wind_speed = float(request.POST.get('wind_speed'))

            input_data = np.array([[temperature, humidity, wind_speed]])

            # Predictions
            rf_prediction = rf_model.predict(input_data)[0]
            svm_prediction = svm_model.predict(input_data)[0]
            lstm_input = np.reshape(input_data, (1, input_data.shape[1], 1))
            lstm_prediction = lstm_model.predict(lstm_input)[0][0]

            final_prediction = (rf_prediction + svm_prediction + lstm_prediction) / 3

            # Alert determination
            if final_prediction < 10:
                alert = "Green (No Rain)"
            elif 10 <= final_prediction < 20:
                alert = "Yellow (Light Rain)"
            elif 20 <= final_prediction < 30:
                alert = "Orange (Heavy Rain)"
            else:
                alert = "Red (Very Heavy Rain)"

            return JsonResponse({'rainfall_mm': final_prediction, 'alert_level': alert})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    return render(request, 'main_app/prediction.html')


def predict_rainfall_api(request):
    try:
        # Ensure model is available
        if 'rf_model' not in globals():
            return JsonResponse({'error': 'Random Forest model not loaded.'}, status=500)

        # Extract and validate features from request
        features = [float(request.GET.get(f'feature_{i}', 0)) for i in range(18)]
        print("Received Features:", features)
        
        # Check if feature count matches model expectation
        expected_features = rf_model.n_features_in_
        print("Model expects features:", expected_features)

        if len(features) != expected_features:
            return JsonResponse({'error': f'Invalid input. Expected {expected_features} features.'}, status=400)

        # Convert to NumPy array for prediction
        features = np.array(features).reshape(1, -1)

        # Predict using Random Forest model
        rf_prediction = rf_model.predict(features)[0]
        print("Prediction Result:", rf_prediction)
        
        return JsonResponse({'prediction': float(rf_prediction)})

    except ValueError as ve:
        print("ValueError:", str(ve))
        return JsonResponse({'error': 'Invalid input values. Ensure all features are valid numbers.'}, status=400)

    except Exception as e:
        print("Error:", str(e))
        return JsonResponse({'error': str(e)}, status=500)




from django.http import JsonResponse
import json

def save_location(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            print(f"Location Received: Latitude={latitude}, Longitude={longitude}")
            return JsonResponse({"message": "Location saved successfully!"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


from django.http import JsonResponse
import random
from datetime import datetime, timedelta

def get_prediction(request):
    if request.method == "GET":
        try:
            # Simulating a 5-day forecast
            forecast_data = []
            alert_levels = ["Green", "Yellow", "Orange", "Red"]

            for i in range(5):
                date = (datetime.today() + timedelta(days=i)).strftime("%Y-%m-%d")
                predicted_rainfall = round(random.uniform(0, 100), 2)  # Random rainfall values
                alert_level = (
                    "Green" if predicted_rainfall < 20 else
                    "Yellow" if predicted_rainfall < 50 else
                    "Orange" if predicted_rainfall < 80 else
                    "Red"
                )
                forecast_data.append({
                    "date": date,
                    "predicted_rainfall": predicted_rainfall,
                    "alert_level": alert_level
                })

            # Get the highest alert level for display
            highest_alert = max(forecast_data, key=lambda x: ["Green", "Yellow", "Orange", "Red"].index(x["alert_level"]))

            return JsonResponse({
                "success": True,
                "forecast": forecast_data,
                "alert_level": highest_alert["alert_level"]
            })

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request method"})








# from django.core.mail import send_mail
# from django.http import JsonResponse
# from django.contrib.auth.decorators import user_passes_test
# from .models import User  # Adjust based on your user model
# from django.conf import settings

# # Check if user is admin
# def is_admin(user):
#     return user.is_staff  # Only admin can trigger alerts

# @user_passes_test(is_admin)
# def send_email_alerts(request):
#     if request.method == "POST":
#         users = User.objects.all()
#         email_list = [user.email for user in users if user.email]

#         alert_message = "⚠️ Rainfall Alert: Heavy rain expected! Stay safe. ☔"

#         send_mail(
#             "Rainfall Alert 🌧️",
#             alert_message,
#             settings.EMAIL_HOST_USER,
#             email_list,
#             fail_silently=False,
#         )

#         return JsonResponse({"message": "Email alerts sent successfully!"})

#     return JsonResponse({"error": "Invalid request"}, status=400)




from django.core.mail import send_mail
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from .models import User, AlertLog  # Ensure AlertLog exists

# Check if user is admin
def is_admin(user):
    return user.is_staff  # Only admin can trigger alerts

@user_passes_test(is_admin)
def send_email_alerts(request):
    if request.method == "POST":
        users = User.objects.all()
        email_list = [user.email for user in users if user.email]

        alert_message = "⚠️ Rainfall Alert: Heavy rain expected! Stay safe. ☔"

        # Send email alerts
        send_mail(
            "Rainfall Alert 🌧️",
            alert_message,
            settings.EMAIL_HOST_USER,
            email_list,
            fail_silently=False,
        )

        # Store alerts in database
        alerted_users = []
        for user in users:
            if user.email:  # Only log users with emails
                alert = AlertLog.objects.create(
                    user=user,
                    alert_type="Email"
                )
                alerted_users.append({
                    "name": user.username,
                    "email": user.email,
                    "alert_type": "Email",
                    "timestamp": alert.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                })

        return JsonResponse({"message": "Email alerts sent successfully!", "users": alerted_users})

    return JsonResponse({"error": "Invalid request"}, status=400)







# from django.http import JsonResponse
# from .models import AlertLog  # Make sure you have a model that stores alerts

# def get_alerted_users(request):
#     """Fetch users who received alerts."""
#     alerted_users = AlertLog.objects.all().order_by('-timestamp')[:10]  # Fetch last 10 alerts

#     data = {
#         "users": [
#             {
#                 "name": alert.user.name,
#                 "email": alert.user.email,
#                 "alert_type": alert.alert_type,
#                 "timestamp": alert.timestamp.strftime("%Y-%m-%d %H:%M:%S")
#             }
#             for alert in alerted_users
#         ]
#     }
#     return JsonResponse(data)




from django.http import JsonResponse
from .models import AlertLog

def get_alerted_users(request):
    alerts = AlertLog.objects.select_related("user").order_by("-timestamp")  # Get recent alerts
    users_data = [
        {
            "name": alert.user.username,
            "email": alert.user.email,
            "alert_type": alert.alert_type,
            "timestamp": alert.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for alert in alerts
    ]
    return JsonResponse({"users": users_data})
