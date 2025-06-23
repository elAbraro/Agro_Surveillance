from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Farm, PestDisease, SurveillanceRecord
from .forms import FarmForm, PestDiseaseForm, SurveillanceForm, RegisterForm
from django.contrib.auth.forms import UserCreationForm

# Dashboard View
@login_required
def dashboard(request):
    farms = Farm.objects.filter(grower=request.user)
    recent_surveillance = SurveillanceRecord.objects.filter(farm__grower=request.user).order_by('-date')[:5]
    
    # Calculate statistics
    total_farms = farms.count()
    total_surveillance = SurveillanceRecord.objects.filter(farm__grower=request.user).count()
    total_pests = PestDisease.objects.count()
    
    context = {
        'farms': farms,
        'recent_surveillance': recent_surveillance,
        'total_farms': total_farms,
        'total_surveillance': total_surveillance,
        'total_pests': total_pests,
    }
    return render(request, 'dashboard.html', context)

# Farm Views
class FarmListView(LoginRequiredMixin, ListView):
    model = Farm
    template_name = 'farms/list.html'
    context_object_name = 'farms'
    
    def get_queryset(self):
        return Farm.objects.filter(grower=self.request.user)

class FarmDetailView(LoginRequiredMixin, DetailView):
    model = Farm
    template_name = 'farms/detail.html'
    
    def get_queryset(self):
        return Farm.objects.filter(grower=self.request.user)

class FarmCreateView(LoginRequiredMixin, CreateView):
    model = Farm
    form_class = FarmForm
    template_name = 'farms/form.html'
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self, form):
        form.instance.grower = self.request.user
        messages.success(self.request, 'Farm added successfully!')
        return super().form_valid(form)

class FarmUpdateView(LoginRequiredMixin, UpdateView):
    model = Farm
    form_class = FarmForm
    template_name = 'farms/form.html'
    
    def get_queryset(self):
        return Farm.objects.filter(grower=self.request.user)
    
    def get_success_url(self):
        messages.success(self.request, 'Farm updated successfully!')
        return reverse_lazy('farm-detail', kwargs={'pk': self.object.pk})

class FarmDeleteView(LoginRequiredMixin, DeleteView):
    model = Farm
    template_name = 'farms/delete.html'
    success_url = reverse_lazy('dashboard')
    
    def get_queryset(self):
        return Farm.objects.filter(grower=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Farm deleted successfully!')
        return super().delete(request, *args, **kwargs)

# Pest/Disease Views
class PestDiseaseListView(LoginRequiredMixin, ListView):
    model = PestDisease
    template_name = 'pests/list.html'
    context_object_name = 'pests'

class PestDiseaseDetailView(LoginRequiredMixin, DetailView):
    model = PestDisease
    template_name = 'pests/detail.html'

class PestDiseaseCreateView(LoginRequiredMixin, CreateView):
    model = PestDisease
    form_class = PestDiseaseForm
    template_name = 'pests/form.html'
    success_url = reverse_lazy('pest-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Pest/Disease added successfully!')
        return super().form_valid(form)

class PestDiseaseUpdateView(LoginRequiredMixin, UpdateView):
    model = PestDisease
    form_class = PestDiseaseForm
    template_name = 'pests/form.html'
    
    def get_success_url(self):
        messages.success(self.request, 'Pest/Disease updated successfully!')
        return reverse_lazy('pest-detail', kwargs={'pk': self.object.pk})

class PestDiseaseDeleteView(LoginRequiredMixin, DeleteView):
    model = PestDisease
    template_name = 'pests/delete.html'
    success_url = reverse_lazy('pest-list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Pest/Disease deleted successfully!')
        return super().delete(request, *args, **kwargs)

# Surveillance Views
class SurveillanceRecordListView(LoginRequiredMixin, ListView):
    model = SurveillanceRecord
    template_name = 'surveillance/list.html'
    context_object_name = 'records'
    
    def get_queryset(self):
        return SurveillanceRecord.objects.filter(farm__grower=self.request.user)

class SurveillanceRecordDetailView(LoginRequiredMixin, DetailView):
    model = SurveillanceRecord
    template_name = 'surveillance/detail.html'
    
    def get_queryset(self):
        return SurveillanceRecord.objects.filter(farm__grower=self.request.user)

class SurveillanceRecordCreateView(LoginRequiredMixin, CreateView):
    model = SurveillanceRecord
    form_class = SurveillanceForm
    template_name = 'surveillance/form.html'
    success_url = reverse_lazy('surveillance-list')
    
    def form_valid(self, form):
        form.instance.farm = Farm.objects.get(grower=self.request.user, pk=self.kwargs.get('farm_id'))
        messages.success(self.request, 'Surveillance record added successfully!')
        return super().form_valid(form)

class SurveillanceRecordUpdateView(LoginRequiredMixin, UpdateView):
    model = SurveillanceRecord
    form_class = SurveillanceForm
    template_name = 'surveillance/form.html'
    
    def get_queryset(self):
        return SurveillanceRecord.objects.filter(farm__grower=self.request.user)
    
    def get_success_url(self):
        messages.success(self.request, 'Surveillance record updated successfully!')
        return reverse_lazy('surveillance-detail', kwargs={'pk': self.object.pk})

class SurveillanceRecordDeleteView(LoginRequiredMixin, DeleteView):
    model = SurveillanceRecord
    template_name = 'surveillance/delete.html'
    success_url = reverse_lazy('surveillance-list')
    
    def get_queryset(self):
        return SurveillanceRecord.objects.filter(farm__grower=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Surveillance record deleted successfully!')
        return super().delete(request, *args, **kwargs)

# Surveillance Calculator View
@login_required
def surveillance_calculator(request, farm_id):
    farm = get_object_or_404(Farm, id=farm_id, grower=request.user)
    recommended_plants = farm.calculate_surveillance_effort()
    
    if request.method == 'POST':
        form = SurveillanceForm(request.POST, request.FILES)
        if form.is_valid():
            surveillance = form.save(commit=False)
            surveillance.farm = farm
            surveillance.save()
            messages.success(request, 'Surveillance record added successfully!')
            return redirect('dashboard')
    else:
        form = SurveillanceForm()
    
    context = {
        'farm': farm,
        'recommended_plants': recommended_plants,
        'form': form,
    }
    return render(request, 'surveillance/calculator.html', context)

# User Registration View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})