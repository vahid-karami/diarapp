from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # The main dashboard page
    path('', views.DashboardView.as_view(), name='index'),
    
    # The reports page
    path('reports/', views.ReportsView.as_view(), name='reports'),
    
    # The Excel export feature
    path('export/excel/', views.ExportExcelView.as_view(), name='export_excel'),
]