from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Feedback
from .forms import UserRegistrationForm, UserProfileForm, ContactForm, FeedbackForm

# Home Page
def home(request):
    return render(request, 'main_app/home.html')

# Registration View
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.email = user_form.cleaned_data['email']
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.email = user.email
            profile.save()

            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()

    return render(request, 'main_app/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to the appropriate dashboard
            if user.is_superuser:
                return redirect('admin_dashboard')
            else:
                return redirect('user_dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'main_app/login.html')

# Logout View
def logout_user(request):
    logout(request)
    return redirect('home')

# User Dashboard
def user_dashboard(request):
    return render(request, 'main_app/user_dashboard.html')

# Admin Dashboard
def admin_dashboard(request):
    return render(request, 'main_app/admin_dashboard.html')

# About Us Page
def about_us(request):
    return render(request, 'main_app/about_us.html')

# Contact Us Page
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

# # Feedback Page
# def feedback(request):
#     if request.method == 'POST':
#         form = FeedbackForm(request.POST)
#         if form.is_valid():
#             feedback = form.save(commit=False)
#             feedback.user = request.user
#             feedback.save()
#             messages.success(request, 'Feedback submitted successfully!')
#             return redirect('home')
#     else:
#         form = FeedbackForm()
#     return render(request, 'main_app/feedback.html', {'form': form})


# #feedback
# def feedback(request):
#     if request.method == 'POST':
#         form = FeedbackForm(request.POST)
#         if form.is_valid():
#             feedback = form.save(commit=False)
#             feedback.user = None  # No user association, anyone can submit
#             feedback.save()
#             messages.success(request, "Thank you for your feedback!")
#             return redirect('feedback')
#         else:
#             messages.error(request, "Please correct the errors below.")
#     else:
#         form = FeedbackForm()
#     return render(request, 'main_app/feedback.html', {'form': form})






# Feedback Form
from django import forms

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'message']  # Update these fields as per your model
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message'}),
        }

def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('feedback')  # Redirect to the same page after saving
    else:
        form = FeedbackForm()
    return render(request, 'main_app/feedback.html', {'form': form})