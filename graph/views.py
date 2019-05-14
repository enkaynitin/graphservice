from django.shortcuts import render
from rest_framework import  viewsets
from .models import Graph, Node, Edge, File, NodeTraversal
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


class IslandsList(generics.ListAPIView):
    serializer_class = NodeSerializer

    def get_queryset(self):
        """
        traversed_nodes = []
nodes_to_traverse = []
initialize traversed_nodes with any node
i.e. traversed_nodes = [v1]


nodes_to_traverse=[v1]
traversed_nodes = []
2nd step
traversed_nodes = [v1]
nodes_to_traverse=[nodes_connected_to_v1] + nodes_to_traverse
you can use this line to get the first element at each step
ele, nodes_to_traverse = nodes_to_traverse[0] + nodes_to_traverse[1:]
if nodes_to_traverse is empty
algo has finished
you have found one disjoint set
then you mark in database that these nodes are traversed
and re-initialise with a new node that has yet not been traversed to get the 2nd disjoint set
and so on and so on
this will give you all disjoint set



1) Initialize all vertices as not visited.
2) Do following for every vertex 'v'.
       (a) If 'v' is not visited before, call DFSUtil(v)
       (b) Print new line character

DFSUtil(v)
1) Mark 'v' as visited.
2) Print 'v'
3) Do following for every adjacent 'u' of 'v'.
     If 'u' is not visited, then recursively call DFSUtil(u)

        :return:
        """
        graph = get_object_or_404(Graph, pk=self.kwargs['graph_pk'])
        node_traversal = NodeTraversal.object.create()
        node_traversal.traversed_nodes = Node.objects.none()
        node_traversal.nodes_to_traverse = Node.objects.none()
        nodes = graph.nodes.all()
        node_traversal.nodes_to_traverse = set(chain(node_traversal.nodes_to_traverse,
                                                     self.connected_nodes(node_traversal.nodes_to_traverse)))

    @staticmethod
    def connected_nodes(node):
        node_connected_to = Node.object.none()
        for e in Edge.objects.filter(Q(source=node) | Q(target=node)):
            if e.source == node:
                node_connected_to = set(chain(node_connected_to, Node.objects.filter(pk=e.target.pk)))
            else:
                node_connected_to = set(chain(node_connected_to, Node.objects.filter(pk=e.source.pk)))
        return node_connected_to







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
            graph = get_object_or_404(Graph, title=file_object.title)
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



