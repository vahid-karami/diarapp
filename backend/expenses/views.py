from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Expense
from .forms import ExpenseForm

class ExpenseCreateView(CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expenses/expense_form.html'
    success_url = reverse_lazy('dashboard:index') # Redirects to dashboard after saving