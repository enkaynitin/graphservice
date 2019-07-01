from django.urls import path
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from graph import views


urlpatterns = [
    path('graphs/', views.GraphList.as_view()),
    path('graphs/<int:pk>/', views.GraphDetail.as_view()),
    path('nodes/', views.NodeList.as_view()),
    path('nodes/<int:pk>/', views.NodeDetail.as_view()),
    path('edges/', views.EdgeList.as_view()),
    path('edges/<int:pk>/', views.EdgeDetail.as_view()),
    path('graphs/<int:graph_pk>/weakly-connected/', views.WeaklyConnectedList.as_view()),
    path('graphs/upload/', views.FileUploadView.as_view()),
    path('graphs/<int:graph_pk>/bounding-rectangle-incoming-nodes/',
         views.nodes_with_incoming_edge_from_source_node_overlapped_by_rectangle, name='rectangle'),
    path('graphs/<int:graph_pk>/groups/', views.get_groups, name='groups'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

