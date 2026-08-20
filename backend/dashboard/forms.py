from django import forms
from expenses.models import Expense
from projects.models import Project

class BootstrapForm(forms.ModelForm):
    """
    Base form to automatically apply Bootstrap CSS classes to all fields.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            old_class = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'form-control {old_class}'.strip()

class ExpenseForm(BootstrapForm):
    class Meta:
        model = Expense
        # Removed 'category' and updated to match the real Expense model
        fields = ['title', 'project', 'amount', 'date', 'receipt', 'description']

class ProjectForm(BootstrapForm):
    class Meta:
        model = Project
        # Updated to match the real Project model
        fields = ['name', 'customer', 'address', 'start_date', 'end_date', 'status', 'description']