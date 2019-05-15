from rest_framework import serializers
from .models import Graph, Node,  Edge, File
from rest_framework.parsers import JSONParser




class NodeSerializer(serializers.ModelSerializer):
    queryset = Node.objects.all()

    class Meta:
        model = Node
        fields = ('iid', 'title', 'top', 'left', 'bottom', 'right', 'position')


class EdgeSerializer(serializers.ModelSerializer):
    queryset = Edge.objects.all()

    class Meta:
        model = Edge
        fields = ('source', 'target', 'weight')


class GraphSerializer(serializers.ModelSerializer):
    queryset = Graph.objects.all()
    nodes = NodeSerializer(many=True)
    edges = EdgeSerializer(many=True)

    class Meta:
        model = Graph
        fields = ('title', 'nodes', 'edges')

    # def create(self, validated_data):
    #     node_data = validated_data.pop('node')
    #     edge_data = validated_data.pop('edge')
    #
    #     for node_data in node_data:
    #         node = Node.objects.create(**node_data)
    #     for edge_data in edge_data:
    #         Edge.objects.create(**edge_data)
    #     graph = Graph.objects.create(**validated_data)
    #     return graph


class FileSerializer(serializers.ModelSerializer):
    class Meta():
        model = File
        fields = ('file', 'timestamp', 'title')


class BoundingRectagleAndGraphSerializer(serializers.Serializer):

    top = serializers.FloatField()
    left = serializers.FloatField()
    bottom = serializers.FloatField()
    right = serializers.FloatField()
    graph = serializers.IntegerField()



