from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'customer', 'address', 'start_date', 'end_date', 'status', 'description']
        labels = {
            'name': 'نام پروژه',
            'customer': 'مشتری / کارفرما',
            'address': 'آدرس',
            'start_date': 'تاریخ شروع',
            'end_date': 'تاریخ پایان',
            'status': 'وضعیت پروژه',
            'description': 'توضیحات',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # اختیاری کردن فیلدها
        self.fields['address'].required = False
        self.fields['end_date'].required = False
        self.fields['description'].required = False
        if 'description' in self.fields:
            self.fields['description'].widget = forms.Textarea(attrs={'rows': 3})

        # افزودن تقویم فارسی به فیلدهای تاریخ
        if 'start_date' in self.fields:
            self.fields['start_date'].widget.attrs['class'] = 'persian-date-picker'
        if 'end_date' in self.fields:
            self.fields['end_date'].widget.attrs['class'] = 'persian-date-picker'
            
        # اعمال استایل بوت‌استرپ روی تمام فیلدها
        for field_name, field in self.fields.items():
            old_class = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'form-control {old_class}'.strip()