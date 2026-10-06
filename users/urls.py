from django.urls import path
from .views import home,index, profile, RegisterView,logout_view
from . import views

urlpatterns = [
    path('', home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    path('logout_view/',logout_view,name='logout_view'),
    path('index/', index, name='users-index'),
    path('Basic_report/',views.Basic_report,name='Basic_report'),
    path('Metrics_report/',views.Metrics_report,name='Metrics_report'),
    path('Deploy_8/',views.Deploy_8,name='Deploy_8'),
    path('Deploy_9/',views.Deploy_9,name='Deploy_9'),
    path('Crop',views.Crop,name='Crop'),
    path('Yield/', views.Yield, name='Yield'),
    path('Yield_report/',views.Yield_report,name='Yield_report'),
    path('timeline/', views.timeline, name='timeline'),
    
    path('profile_list/',views.profile_list,name='profile_list'),
    path('chatbot/', views.chatbot_response_view,name='chatbot'),
    path('map/', views.map_page, name='map_page'),
    path('fetch-crop-inputs/', views.fetch_crop_inputs, name='fetch_crop_inputs'),
    # path('fetch-crop-form-data/', views.fetch_crop_form_data, name='fetch_crop_form_data'),
   


    # path('set-language/', views.set_language, name='set_language'),








    
    
    ]


 