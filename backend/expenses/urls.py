from django.urls import path
from .views import ExpenseCreateView

app_name = 'expenses'
urlpatterns = [
    path('new/', ExpenseCreateView.as_view(), name='create'),
]