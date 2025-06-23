from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class Farm(models.Model):
    grower = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    total_plants = models.PositiveIntegerField()
    area_hectares = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.location})"
    
    def get_absolute_url(self):
        return reverse('farm-detail', kwargs={'pk': self.pk})
    
    def calculate_surveillance_effort(self):
        """Calculate recommended surveillance effort based on farm size"""
        # Basic formula: 1 plant per 0.1 hectare + 5% of total plants
        base_plants = self.area_hectares * 10
        percentage_plants = self.total_plants * 0.05
        return round(max(base_plants, percentage_plants))

class PestDisease(models.Model):
    PLANT_PARTS = [
        ('leaf', 'Leaf'),
        ('stem', 'Stem'),
        ('fruit', 'Fruit'),
        ('root', 'Root'),
        ('flower', 'Flower'),
    ]
    
    name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=100)
    affected_plant_part = models.CharField(max_length=50, choices=PLANT_PARTS)
    description = models.TextField()
    symptoms = models.TextField()
    treatment = models.TextField()
    image = models.ImageField(upload_to='pests/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('pest-detail', kwargs={'pk': self.pk})

class SurveillanceRecord(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    pest_disease = models.ForeignKey(PestDisease, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    plants_checked = models.PositiveIntegerField()
    infected_plants = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)
    location_in_farm = models.CharField(max_length=100)
    image_evidence = models.ImageField(upload_to='surveillance/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def infection_percentage(self):
        if self.plants_checked > 0:
            return round((self.infected_plants / self.plants_checked) * 100, 2)
        return 0
    
    def get_absolute_url(self):
        return reverse('surveillance-detail', kwargs={'pk': self.pk})
    
    def __str__(self):
        return f"{self.farm} - {self.pest_disease} on {self.date}"