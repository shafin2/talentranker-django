from django.urls import path
from . import views

urlpatterns = [
    path('upload', views.upload_jd, name='upload_jd'),
    path('', views.get_all_jds, name='get_all_jds'),
    path('<int:id>', views.get_jd_by_id, name='get_jd_by_id'),
    path('<int:id>', views.delete_jd, name='delete_jd'),
]
