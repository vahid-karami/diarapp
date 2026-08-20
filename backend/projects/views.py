from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Project
from .forms import ProjectForm

class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('dashboard:index')