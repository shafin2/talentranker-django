from django.urls import path
from . import views

urlpatterns = [
    path('rank', views.rank_cvs, name='rank_cvs'),
    path('rank-with-files', views.rank_with_files, name='rank_with_files'),
    path('results', views.get_ranking_results, name='get_ranking_results'),
    path('results/<int:id>', views.get_ranking_result_by_id, name='get_ranking_result_by_id'),
    path('results/<int:id>', views.delete_ranking_result, name='delete_ranking_result'),
]
