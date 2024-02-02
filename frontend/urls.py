from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('process_transcript/', views.process_transcript, name='process_transcript'),
    path('requirements/', views.requirements, name="requirements"),
    path('contact/', views.contact, name="contact"),
    path('dataTeam/', views.dataTeam, name="dataTeam"),
    path('negotiationTeam/', views.negotiationTeam, name="negotiationTeam"),
    path('aiTranscript/', views.aiTranscript, name="aiTranscript"),
    path('aiQuasi/', views.aiQuasi, name="aiQuasi"),
]