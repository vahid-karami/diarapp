from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.utils import timezone
from expenses.models import Expense

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        
        # Calculate all-time total expenses
        total = Expense.objects.aggregate(Sum('amount'))['amount__sum']
        context['total_expenses'] = total or 0
        
        # Calculate this month's expenses
        monthly = Expense.objects.filter(
            date__year=now.year, 
            date__month=now.month
        ).aggregate(Sum('amount'))['amount__sum']
        context['monthly_expenses'] = monthly or 0
        
        # Fetch the 5 most recent expenses. 
        # select_related prevents the "N+1 query problem" by joining tables efficiently.
        context['recent_expenses'] = Expense.objects.select_related(
            'project', 'user'
        ).order_by('-date')[:5]
        
        return context