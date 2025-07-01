from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('process_graph/', views.search_path, name='process_graph'),
    path('search_sse/', views.search_path_sse, name='search_sse')
]
