from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('user/complete', views.move_to_output, name='user_input_complete'),
]