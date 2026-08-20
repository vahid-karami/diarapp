from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from dashboard.views import CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Custom Login & Logout Routes
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(next_page='login'), name='logout'),
    
    # App Routes
    path('', include('dashboard.urls')),
    path('expenses/', include('expenses.urls')),  # NEW: Registered expenses namespace
    path('projects/', include('projects.urls')),  # NEW: Registered projects namespace
]

# Serve media files in development (and via Docker volume in production)
if settings.DEBUG or True: # Ensuring static/media resolve properly
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)