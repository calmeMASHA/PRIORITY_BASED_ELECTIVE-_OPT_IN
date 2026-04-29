from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_preference, name='submit_preference'),
    path('api/seats/<int:elective_id>/', views.seat_count, name='seat_count'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('export/', views.export_allocations, name='export_allocations'),
]
