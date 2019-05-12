from django.shortcuts import render
from rest_framework import  viewsets
from .models import Graph, Node, Edge, File
from .serializers import GraphSerializer, NodeSerializer, EdgeSerializer, FileSerializer
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework import views, viewsets
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

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


class FileView(views.APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            file_object = File.objects.last()
            graph = file_object.graph
            with open('/home/nk/Projects/mavenoid/graphservice/graphservice'+file_object.file.url, 'r') as f:
                for line in f:
                    l = line.replace("\n", "").split(',')
                    Node.objects.create(graph=graph, iid=l[0], title=l[1],
                                       top=float(l[2]), left=float(l[3]), bottom=float(l[4]), right=float(l[5]))
                f.close()
            print(File.objects.last().file.url)
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class BoundingRectangle(views.APIView):
    queryset = Node.objects.all()
    serializers_class = NodeSerializer

    # def islands(request, graph_pk):
    # graph = get_object_or_404(Graph, pk=request.data.graph_pk)
    # return graph.islands()
