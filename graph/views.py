from django.shortcuts import render
from rest_framework import  viewsets
from .models import Graph, Node, Edge, File
from .serializers import GraphSerializer, NodeSerializer, EdgeSerializer, FileSerializer, BoundingRectagleAndGraphSerializer
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework import views, viewsets
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from itertools import chain
from rest_framework.decorators import api_view
from django.db.models import Q

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


class FileUploadView(views.APIView):
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
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def nodes_incoming_edge_from_source_overlap_by_rectangle(request, *args, **kwargs):
    """
    Given a rectangle specified in the request and a graph identifier, returns all nodes that have
    an incoming edge whose source node overlaps with that rectangle
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    graph = get_object_or_404(Graph, pk=kwargs['graph_pk'])
    top = float(request.data['top'])
    left = float(request.data['left'])
    bottom = float(request.data['bottom'])
    right = float(request.data['right'])
    all_overlapping_nodes = graph.nodes.filter(
        top__gte=top,
        left__gte=left,
        bottom__gte=bottom,
        right__gte=right
    )
    node_with_incoming_edge_with_source_overlapping_rectaangle = Node.objects.none()
    for node in all_overlapping_nodes.iterator():
        edge_with_source_node_overlapped = Edge.objects.filter(source=node)
        for edge in edge_with_source_node_overlapped:
            node_with_incoming_edge_with_source_overlapping_rectaangle\
                = set(chain(node_with_incoming_edge_with_source_overlapping_rectaangle, Node.objects.filter(pk=edge.target.pk)))

    serializer = NodeSerializer(node_with_incoming_edge_with_source_overlapping_rectaangle, many=True)
    return Response(serializer.data)

    # def islands(request, graph_pk):
    # graph = get_object_or_404(Graph, pk=request.data.graph_pk)
    # return graph.islands()
