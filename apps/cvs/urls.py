from django.urls import path
from . import views

urlpatterns = [
    path('upload', views.upload_cvs, name='upload_cvs'),
    path('', views.get_all_cvs, name='get_all_cvs'),
    path('<int:id>', views.get_cv_by_id, name='get_cv_by_id'),
    path('<int:id>', views.delete_cv, name='delete_cv'),
]
