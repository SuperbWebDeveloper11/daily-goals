from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

def index(request):
    return redirect("goals:daily_goals_list")

urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('goals/', include('goals.urls', namespace='goals')),
]

# serving media files only during developement
# if settings.DEBUG:
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
