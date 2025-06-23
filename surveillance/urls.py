# surveillance/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Authentication
    path('register/', views.register, name='register'),
    
    # Farms
    path('farms/', views.FarmListView.as_view(), name='farm-list'),
    path('farms/<int:pk>/', views.FarmDetailView.as_view(), name='farm-detail'),
    path('farms/new/', views.FarmCreateView.as_view(), name='farm-create'),
    path('farms/<int:pk>/update/', views.FarmUpdateView.as_view(), name='farm-update'),
    path('farms/<int:pk>/delete/', views.FarmDeleteView.as_view(), name='farm-delete'),
    
    # Pests & Diseases
    path('pests/', views.PestDiseaseListView.as_view(), name='pest-list'),
    path('pests/<int:pk>/', views.PestDiseaseDetailView.as_view(), name='pest-detail'),
    path('pests/new/', views.PestDiseaseCreateView.as_view(), name='pest-create'),
    path('pests/<int:pk>/update/', views.PestDiseaseUpdateView.as_view(), name='pest-update'),
    path('pests/<int:pk>/delete/', views.PestDiseaseDeleteView.as_view(), name='pest-delete'),
    
    # Surveillance
    path('surveillance/', views.SurveillanceRecordListView.as_view(), name='surveillance-list'),
    path('surveillance/<int:pk>/', views.SurveillanceRecordDetailView.as_view(), name='surveillance-detail'),
    path('surveillance/new/', views.SurveillanceRecordCreateView.as_view(), name='surveillance-create'),
    path('surveillance/<int:pk>/update/', views.SurveillanceRecordUpdateView.as_view(), name='surveillance-update'),
    path('surveillance/<int:pk>/delete/', views.SurveillanceRecordDeleteView.as_view(), name='surveillance-delete'),
    path('farms/<int:farm_id>/calculator/', views.surveillance_calculator, name='surveillance-calculator'),
]