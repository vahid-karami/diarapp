from django import forms
from projects.models import Project
from expenses.models import Expense

class BootstrapForm(forms.ModelForm):
    """A custom base class that automatically adds Bootstrap CSS to all form fields"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input shadow-sm'
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select shadow-sm'
            else:
                field.widget.attrs['class'] = 'form-control shadow-sm'

class ProjectForm(BootstrapForm):
    class Meta:
        model = Project
        fields = ['name', 'customer', 'address', 'start_date', 'end_date', 'status', 'description']
        widgets = {
            'start_date': forms.TextInput(attrs={'placeholder': 'مثال: 1403-05-20', 'dir': 'ltr'}),
            'end_date': forms.TextInput(attrs={'placeholder': 'مثال: 1403-12-29', 'dir': 'ltr'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class ExpenseForm(BootstrapForm):
    class Meta:
        model = Expense
        fields = ['project', 'date', 'category', 'amount', 'description', 'receipt']
        widgets = {
            'date': forms.TextInput(attrs={'placeholder': 'مثال: 1403-05-20', 'dir': 'ltr'}),
            'description': forms.Textarea(attrs={'rows': 2}),
        }