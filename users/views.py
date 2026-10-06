from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import logout as auth_logout
import numpy as np
import joblib
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm
from .models import UserPredictModel,yield_db
from .forms import UserPredictDataForm

# Static seasonal crop data
SEASONAL_CROPS = {
    "Spring": ["Wheat", "Barley", "Peas"],
    "Summer": ["Maize", "Tomatoes", "Cotton"],
    "Monsoon": ["Rice", "Sugarcane", "Millets"],
    "Autumn": ["Chickpeas", "Mustard", "Sunflower"],
    "Winter": ["Potatoes", "Carrots", "Onion"]
}





def home(request):
    return render(request, 'users/home.html')

@login_required(login_url='users-register')


def timeline(request):
    context = {"seasonal_crops": SEASONAL_CROPS}
    return render(request, "app/timeline.html", context)

def index(request):
    return render(request, 'app/index.html')

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

from django.contrib.auth import logout as auth_logout

class CustomLoginView(LoginView):
    form_class = LoginForm

    def dispatch(self, request, *args, **kwargs):
        # ✅ Force logout any user who visits the login page
        if request.user.is_authenticated:
            auth_logout(request)

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()

        if hasattr(user, 'customerprofile'):
            auth_logout(self.request)
            messages.error(self.request, "Please Enter valid user account.")
            return redirect(reverse('login'))

     
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(0)  
            self.request.session.modified = True

        return super().form_valid(form)




class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})


from django.http import JsonResponse
import openmeteo_requests
import requests_cache
from retry_requests import retry
import pandas as pd

def fetch_crop_inputs(request):
    # Open-Meteo setup
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 12.963,
        "longitude": 80.1767,
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation"  # for rainfall
        ]
    }

    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    hourly = response.Hourly()

    # Weather-based fields
    temperature = float(hourly.Variables(0).ValuesAsNumpy()[0])
    humidity = float(hourly.Variables(1).ValuesAsNumpy()[0])
    rainfall = float(hourly.Variables(2).ValuesAsNumpy()[0])

    # Example fixed nutrient & pH values (replace with your logic if needed)
    nitrogen = 90
    phosphorus = 42
    potassium = 37
    ph_value = 6.4

    crop_data = {
        "nitrogen": nitrogen,
        "phosphorus": phosphorus,
        "potassium": potassium,
        "temperature": temperature,
        "humidity": humidity,
        "ph": ph_value,
        "rainfall": rainfall
    }

    return JsonResponse(crop_data)




Model07 = joblib.load('users/crop1.pkl')
def Deploy_8(request):
    if request.method == 'POST':
        form = UserPredictDataForm(request.POST)
        if form.is_valid():
            # Extract cleaned data from form
            nitrogen = form.cleaned_data['nitrogen']
            phosphorus = form.cleaned_data['phosphorus']
            potassium = form.cleaned_data['potassium']
            temperature = form.cleaned_data['temperature']
            humidity = form.cleaned_data['humidity']
            ph = form.cleaned_data['ph']
            rainfall = form.cleaned_data['rainfall']
            
            # Prepare features for prediction
            features = np.array([[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]])
            
            # Predict using the loaded model
            prediction = Model07.predict(features)
            prediction = prediction[0]
            
            # Determine the result based on prediction
            crops = ['Apple', 'Banana', 'BlackGram', 'Chickpea', 'Coconut', 'Coffee', 'Cotton', 'Grapes', 'Jute', 'KidneyBeans', 
                     'Lentil', 'Maize', 'Mango', 'MothBeans', 'MungBean', 'Musk melon', 'Orange', 'Papaya', 'Pigeonpeas', 
                     'Pomegranate', 'Rice', 'Watermelon']
            result = crops[prediction]
            
            # Save data to database
            instance = form.save(commit=False)
            instance.label = result
            instance.save()
            
            # Render output page with prediction result
            return render(request, 'app/output1.html', {'prediction_text': result})
    else:
        form = UserPredictDataForm()
    
    return render(request, 'app/deploy_8.html', {'form': form})


Model2 = joblib.load('users/YIELD.pkl')  


import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO
from django.shortcuts import render
from .models import yield_db


def Deploy_9(request): 
    if request.method == "POST":
        # Extract features from the POST request
        int_features = [x for x in request.POST.values()]
        int_features = int_features[1:]  # Assuming the first value is not needed

        # Convert features to numpy array
        final_features = [np.array(int_features, dtype=object)]
        
        # Make prediction using the model
        prediction = Model2.predict(final_features)
        output = prediction[0]

        # Save the data to the database
        yield_instance = yield_db(
            crop=request.POST['crop'],
            season=request.POST['season'],
            area=request.POST['area'],
            area_units=request.POST['area_units'],
            production=request.POST['production'],
            production_units=request.POST['production_units'],
            yield_value=output
        )
        yield_instance.save()

        # Generate plot
        categories = ['crop', 'season', 'area', 'area_units', 'production', 'production_units', 'yield_value']
        values = [request.POST['crop'], request.POST['season'], request.POST['area'], 
                  request.POST['area_units'], request.POST['production'], 
                  request.POST['production_units'], output]

        # Convert categorical data to strings for plotting
        str_values = [str(value) for value in values]

        plt.figure(figsize=(10, 6))
        plt.plot(categories, str_values, marker='o', color='red')
        
        plt.xlabel('Categories')
        plt.ylabel('Values')
        plt.title('Crop Yield Prediction')

        # Save the plot to a buffer
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        # Encode plot to base64 string
        plot_base64 = base64.b64encode(buffer.read()).decode('utf-8')

        # Create context for rendering the template
        context = {
            'plot_base64': plot_base64,
            'prediction_text1': f'The yield is {output}, indicating the amount of agricultural product harvested.'
        }

        return render(request, 'app/output.html', context)
    else:
        return render(request, 'app/Deploy_9.html')


from django.http import JsonResponse
import openmeteo_requests
import requests_cache
from retry_requests import retry

def fetch_crop_form_data(request):
    # Set up caching & retries
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 12.963,
        "longitude": 80.1767,
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation"
        ]
    }

    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    hourly = response.Hourly()

    temperature = float(hourly.Variables(0).ValuesAsNumpy()[0])
    rainfall = float(hourly.Variables(2).ValuesAsNumpy()[0])

    # Example fixed values for nutrients & pH
    nitrogen = 90
    phosphorus = 42
    potassium = 37
    ph_value = 6.4

    data = {
        "Soil_color": "Red",  # Example default
        "Nitrogen": nitrogen,
        "Phosphorus": phosphorus,
        "Potassium": potassium,
        "pH": ph_value,
        "Rainfall": rainfall,
        "Temperature": temperature,
        "Crop": "Wheat"  # Example default
    }

    return JsonResponse(data)



def Basic_report(request):
    return render(request,'app/Basic_report.html')

def Metrics_report(request):
    return render(request,'app/Metrics_report.html')

def Yield_report(request):
    return render(request,'app/Yield_report.html')

def Crop(request):
    data = UserPredictModel.objects.all()
    return render(request, 'app/crop_db.html', {'data': data})

def Yield(request):
    data = yield_db.objects.all()
    return render(request, 'app/yield_db.html', {'data': data})

from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
import numpy as np

import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras import layers, models

from PIL import Image, ImageOps
from . import forms
import joblib
from . models import UserPredictModel

    







def logout_view(request):  
    auth_logout(request)
    return redirect('/')




def weather_db(request):
    data = FatModel.objects.all()
    return render(request, 'app/weather_db.html', {'data': data})
from .models import Profile

def profile_list(request):
    # Fetch all profile objects from the database
    profiles = Profile.objects.all()
    
    # Pass the profiles data to the template
    return render(request, 'app/profile_list.html', {'profiles': profiles})


   


from django.shortcuts import render
from django.http import JsonResponse
# import random
# import json
import numpy as np
# from nltk.tokenize import word_tokenize
# from nltk.stem import WordNetLemmatizer
#from .models import Response, models
from Chatbot.processor import chatbot_response
# Remove the comments to download additional nltk packages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

@require_POST
@csrf_exempt
def chatbot_response_view(request):
    if request.method == 'POST':
        the_question = request.POST.get('question', '')

        response = chatbot_response(the_question)
        print(response)

        return JsonResponse({"response": response})
    else:
        
        return JsonResponse({"message": "This endpoint only accepts POST requests."})
 
 
def map_page(request):
    return render(request, 'app/map.html')







from django.utils import translation
from django.shortcuts import redirect

def set_language(request):
    if request.method == 'POST':
        lang_code = request.POST.get('language')
        if lang_code:
            translation.activate(lang_code)
            request.session['django_language'] = lang_code
    return redirect(request.META.get('HTTP_REFERER', '/'))


