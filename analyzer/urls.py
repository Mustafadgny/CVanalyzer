from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('upload/', views.upload_cv, name='upload_cv'),
    path('cvs/', views.cv_list, name='cv_list'),
    path('analyze/<int:cv_id>/', views.analyze_cv, name='analyze_cv'),
    path('help_me/', views.help_me, name='help_me'),
    path('delete/<int:cv_id>/', views.delete_cv, name='delete_cv'),
    path('analyze_image/<int:cv_id>/', views.analyze_image, name='analyze_image'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
