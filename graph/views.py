from django.shortcuts import render
from rest_framework import  viewsets
from .models import Graph
from .serializers import GraphSerializer
from rest_framework import generics
# Create your views here.





class GraphList(generics.ListCreateAPIView):
    queryset = Graph.objects.all()
    serializer_class = GraphSerializer


class GraphDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Graph.objects.all()
    serializer_class = GraphSerializer


