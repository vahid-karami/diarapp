from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'project', 'amount', 'date', 'receipt', 'description']
        labels = {
            'title': 'عنوان هزینه',
            'project': 'پروژه مربوطه',
            'amount': 'مبلغ (تومان/ریال)',
            'date': 'تاریخ پرداخت',
            'receipt': 'تصویر فاکتور / رسید',
            'description': 'توضیحات',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 1. Make Amount and Description optional on the frontend
        if 'amount' in self.fields:
            self.fields['amount'].required = False
        if 'description' in self.fields:
            self.fields['description'].required = False
            self.fields['description'].widget = forms.Textarea(attrs={'rows': 3})
            
        # 2. Attach the Persian calendar class to the date field
        if 'date' in self.fields:
            self.fields['date'].widget.attrs['class'] = 'persian-date-picker'
            
        # 3. Add Bootstrap styling to all fields dynamically
        for field_name, field in self.fields.items():
            old_class = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'form-control {old_class}'.strip()

    def clean_amount(self):
        # If the user leaves the amount blank, safely save it as 0
        amount = self.cleaned_data.get('amount')
        return amount if amount else 0