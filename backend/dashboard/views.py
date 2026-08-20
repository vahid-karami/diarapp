from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Sum
from expenses.models import Expense
from projects.models import Project
import csv
from django.http import HttpResponse
from django.views import View
class CustomLoginView(LoginView):
    template_name = 'dashboard/login.html'
    redirect_authenticated_user = True

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # FIX: Query all records instead of filtering by the deleted 'user' field
        context['recent_expenses'] = Expense.objects.all()[:5]
        context['active_projects'] = Project.objects.exclude(status='canceled')[:5]
        
        # Calculate total expenses safely
        total = Expense.objects.aggregate(total_sum=Sum('amount'))['total_sum']
        context['total_expenses'] = total if total else 0
        
        return context

class ReportsView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/reports.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch all expenses for the reports page
        context['expenses'] = Expense.objects.all()
        return context


class ExportExcelView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # We use utf-8-sig so Microsoft Excel reads Persian characters correctly!
        response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
        response['Content-Disposition'] = 'attachment; filename="expenses_report.csv"'
        
        writer = csv.writer(response)
        
        # Write the header row in Persian
        writer.writerow(['عنوان هزینه', 'پروژه', 'مبلغ (تومان)', 'تاریخ', 'توضیحات'])
        
        # Fetch all expenses and write them to the file
        expenses = Expense.objects.all().select_related('project')
        for expense in expenses:
            writer.writerow([
                expense.title,
                expense.project.name if expense.project else '---',
                expense.amount,
                expense.date,
                expense.description or ''
            ])
            
        return response