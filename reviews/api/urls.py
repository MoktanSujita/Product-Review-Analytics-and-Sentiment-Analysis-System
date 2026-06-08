from django.urls import path
from .api import views

urlpatterns = [  

    path('', views.analyze_review, name='home'), 
    path('chart/', views.chart_page, name='chart_page'),
]