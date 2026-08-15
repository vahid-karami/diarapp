import openpyxl
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy, reverse
from projects.models import Project
from expenses.models import Expense
from .forms import ProjectForm, ExpenseForm
import jdatetime
from django.contrib.auth.views import LoginView  # NEW: Import Django LoginView

User = get_user_model()

# -----------------------------------------
# 1. MAIN DASHBOARD VIEW
# -----------------------------------------
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = jdatetime.date.today()
        
        total = Expense.objects.aggregate(Sum('amount'))['amount__sum']
        context['total_expenses'] = total or 0
        
        monthly = Expense.objects.filter(
            date__year=now.year, 
            date__month=now.month
        ).aggregate(Sum('amount'))['amount__sum']
        context['monthly_expenses'] = monthly or 0

        user_expenses = Expense.objects.values('user__username').annotate(
            total_spent=Sum('amount')
        ).order_by('-total_spent')
        context['user_expenses'] = user_expenses
        
        context['recent_expenses'] = Expense.objects.select_related(
            'project', 'user'
        ).order_by('-date')[:5]
        
        return context

# -----------------------------------------
# 2. REPORTS VIEW
# -----------------------------------------
class ReportView(LoginRequiredMixin, ListView):
    model = Expense
    template_name = 'dashboard/reports.html'
    context_object_name = 'expenses'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('project', 'user').order_by('-date')
        
        project_id = self.request.GET.get('project')
        category = self.request.GET.get('category')
        user_id = self.request.GET.get('user')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if project_id:
            queryset = queryset.filter(project_id=project_id)
        if category:
            queryset = queryset.filter(category=category)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)   
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.all()
        context['categories'] = Expense.Category.choices
        context['users'] = User.objects.all()
        
        total = self.get_queryset().aggregate(Sum('amount'))['amount__sum']
        context['filtered_total'] = total or 0
        return context

# -----------------------------------------
# 3. EXCEL EXPORT VIEW
# -----------------------------------------
class ExportExcelView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        queryset = Expense.objects.select_related('project', 'user').order_by('-date')
        
        project_id = request.GET.get('project')
        category = request.GET.get('category')
        user_id = request.GET.get('user')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if project_id:
            queryset = queryset.filter(project_id=project_id)
        if category:
            queryset = queryset.filter(category=category)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "گزارش هزینه‌ها" 

        headers = ['تاریخ', 'پروژه', 'کاربر', 'دسته‌بندی', 'شرح', 'مبلغ (تومان)']
        ws.append(headers)

        for expense in queryset:
            ws.append([
                str(expense.date),  
                expense.project.name,
                expense.user.username if expense.user else "نامشخص",
                expense.get_category_display(),
                expense.description,
                expense.amount
            ])

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="expenses_report.xlsx"'
        wb.save(response)
        return response

# -----------------------------------------
# 4. CREATE PROJECT & EXPENSE VIEWS
# -----------------------------------------
class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'dashboard/form.html'
    success_url = reverse_lazy('dashboard:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'ثبت پروژه جدید'
        return context

class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'dashboard/form.html'
    success_url = reverse_lazy('dashboard:index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'ثبت هزینه جدید'
        return context

# -----------------------------------------
# 5. PROJECT DETAIL & EXPENSE MANAGEMENT
# -----------------------------------------
class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'dashboard/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all expenses for this specific project
        context['expenses'] = self.object.expenses.select_related('user').order_by('-date')
        # Calculate the total cost of this specific project
        context['total_cost'] = self.object.expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        return context

class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'dashboard/form.html' # We reuse the beautiful form here!

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'ویرایش هزینه'
        return context

    def get_success_url(self):
        # After editing, go back to the specific project page
        return reverse('dashboard:project_detail', kwargs={'pk': self.object.project.pk})

class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    model = Expense
    template_name = 'dashboard/expense_confirm_delete.html'

    def get_success_url(self):
        # After deleting, go back to the specific project page
        return reverse('dashboard:project_detail', kwargs={'pk': self.object.project.pk})


# -----------------------------------------
# 6. CUSTOM LOGIN VIEW
# -----------------------------------------
class CustomLoginView(LoginView):
    template_name = 'dashboard/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('dashboard:index')