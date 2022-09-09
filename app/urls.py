from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('app/index/', views.index, name='index'),
    path('app/user/complete', views.move_to_output, name='user_input_complete'),
]