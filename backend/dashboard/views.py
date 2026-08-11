from django.views.generic import TemplateView, ListView  # NEW: Import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.contrib.auth import get_user_model       # NEW: Fetch CustomUser securely
from projects.models import Project                  # NEW: Import Project model
from expenses.models import Expense
import jdatetime

User = get_user_model()

# ... (Keep your existing DashboardView code here) ...

class ReportView(LoginRequiredMixin, ListView):
    model = Expense
    template_name = 'dashboard/reports.html'
    context_object_name = 'expenses'

    def get_queryset(self):
        # Start with all expenses, highly optimized
        queryset = super().get_queryset().select_related('project', 'user').order_by('-date')
        
        # Capture the form inputs from the URL (e.g., ?project=1&category=WK)
        project_id = self.request.GET.get('project')
        category = self.request.GET.get('category')
        user_id = self.request.GET.get('user')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        # Apply database filters dynamically
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        if category:
            queryset = queryset.filter(category=category)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if start_date:
            queryset = queryset.filter(date__gte=start_date) # gte = Greater Than or Equal
        if end_date:
            queryset = queryset.filter(date__lte=end_date)   # lte = Less Than or Equal
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Pass the database options to populate our HTML dropdowns
        context['projects'] = Project.objects.all()
        context['categories'] = Expense.Category.choices
        context['users'] = User.objects.all()
        
        # Calculate the dynamic total for the filtered results
        total = self.get_queryset().aggregate(Sum('amount'))['amount__sum']
        context['filtered_total'] = total or 0
        
        return context