from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from graph import views


urlpatterns = [
    path('graphs/', views.GraphList.as_view()),
    path('graphs/<int:pk>/', views.GraphDetail.as_view()),
    path('nodes/', views.NodeList.as_view()),
    path('nodes/<int:pk>/', views.NodeDetail.as_view()),
    path('edges/', views.EdgeList.as_view()),
    path('edges/<int:pk>/', views.EdgeDetail.as_view()),
    path('graphs/<int:graph_pk>/weakly_connected/', views.WeaklyConnectedList.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)

