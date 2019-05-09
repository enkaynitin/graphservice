from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from graph import views


urlpatterns = [
    path('graphs/', views.GraphList.as_view()),
    path('graphs/<int:pk>/', views.GraphDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

