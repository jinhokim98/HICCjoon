"""HICCjoon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from . import views

app_name = 'PSP'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('lobby/', views.lobby, name='lobby'),
    path('task/<int:number>/', views.task_detail, name='task_detail'),
    path('task/', views.task_list, name='task_list'),
    path('monitoring/', views.monitoring, name='monitoring'),
    path('end/', views.end, name='end'),
    path('enroll/', views.enroll, name='enroll'),
    path('test/', views.test, name='test'),
    path('test_back/', views.test_back, name='test_back'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('task_timecheck/', views.task_timecheck, name='task_timecheck'),
    path('get_score/', views.get_score, name='get_score'),
]
