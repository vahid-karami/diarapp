from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from expenses.models import Expense
import jdatetime  # NEW: Import Jalali datetime

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Grab the current Shamsi date (e.g., 1403-05-20)
        now = jdatetime.date.today()
        
        # 1. Calculate all-time total expenses
        total = Expense.objects.aggregate(Sum('amount'))['amount__sum']
        context['total_expenses'] = total or 0
        
        # 2. Calculate this month's expenses using the Shamsi year and month
        monthly = Expense.objects.filter(
            date__year=now.year, 
            date__month=now.month
        ).aggregate(Sum('amount'))['amount__sum']
        context['monthly_expenses'] = monthly or 0

        # 3. NEW: Group expenses by User
        # This translates to: SELECT user, SUM(amount) GROUP BY user
        user_expenses = Expense.objects.values('user__username').annotate(
            total_spent=Sum('amount')
        ).order_by('-total_spent')
        
        context['user_expenses'] = user_expenses
        
        # 4. Fetch the 5 most recent expenses
        context['recent_expenses'] = Expense.objects.select_related(
            'project', 'user'
        ).order_by('-date')[:5]
        
        return context