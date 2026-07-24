from django.urls import path
from . import views

urlpatterns = [  

    path('', views.analyze_review, name='home'), 
    path('dashboard/', views.chart_page, name='chart_page'),
]