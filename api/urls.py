# api/urls.py

"""
URL routing for API endpoints
"""

from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('health/', views.health_check, name='health'),
    path('signatures/', views.get_signatures, name='signatures'),
    path('scan/text/', views.scan_text, name='scan_text'),
    path('scan/file/', views.scan_file_upload, name='scan_file'),
    path('stats/', views.get_stats, name='stats'),
]
