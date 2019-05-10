from django.shortcuts import render
from rest_framework import  viewsets
from .models import Graph, Node, Edge
from .serializers import GraphSerializer, NodeSerializer, EdgeSerializer
from rest_framework import generics
from django.shortcuts import get_object_or_404
# Create your views here.


class NodeList(generics.ListCreateAPIView):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer


class NodeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer


class EdgeList(generics.ListCreateAPIView):
    queryset = Edge.objects.all()
    serializer_class = EdgeSerializer


class EdgeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Edge.objects.all()
    serializer_class = EdgeSerializer


class GraphList(generics.ListCreateAPIView):
    queryset = Graph.objects.all()
    serializer_class = GraphSerializer


class GraphDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Graph.objects.all()
    serializer_class = GraphSerializer


class WeaklyConnectedList(generics.ListAPIView):
    serializer_class = NodeSerializer

    def get_queryset(self):
        graph = get_object_or_404(Graph, pk=self.kwargs['graph_pk'])
        return set([node for node in graph.nodes.all() if node.weakly_connected()])


# def weakly_connected(request, graph_pk):
#     print(request)
#     graph = get_object_or_404(Graph, pk=graph_pk)
#     nodes = graph.nodes.all()
#     return set([node for node in nodes if node.weakly_connected()])






