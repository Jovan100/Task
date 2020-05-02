from django.urls import path
from .views import *

urlpatterns = [
    path('add/', AddView.as_view({'post':'create'}), name='add'),
    path('calculate/', CalculateView.as_view({'get':'retrieve'}), name='calculate'),
    path('calculate/<str:all>/', CalculateView.as_view({'get':'list'}), name='calculate'),
    path('reset/', ResetView.as_view({'post':'create'}), name='reset'),
    path('history/', HistoryView.as_view({'get':'list'}), name='history'),
    path('history/<int:pk>/', HistoryView.as_view({'get':'retrieve'}), name='history'),
]
