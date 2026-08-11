from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='index'),
    path('reports/', views.ReportView.as_view(), name='reports'),
    path('export/excel/', views.ExportExcelView.as_view(), name='export_excel'),
    
    # Form Routes (Phase 13)
    path('projects/new/', views.ProjectCreateView.as_view(), name='project_create'),
    path('expenses/new/', views.ExpenseCreateView.as_view(), name='expense_create'),
    
    # NEW: Project Detail & Expense Management (Phase 14)
    path('project/<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('expense/<int:pk>/edit/', views.ExpenseUpdateView.as_view(), name='expense_edit'),
    path('expense/<int:pk>/delete/', views.ExpenseDeleteView.as_view(), name='expense_delete'),
]