from rest_framework import serializers
from .models import Graph, Node, NodePosition,  Edge
from rest_framework.parsers import JSONParser


class NodePositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodePosition
        fields = '__all__'


class NodeSerializer(serializers.ModelSerializer):
    position = NodePositionSerializer(many=True)

    class Meta:
        model = Node
        depth = 1
        fields = ('iid', 'title', 'position')


class EdgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edge
        depth = 1
        fields = '__all__'


class GraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = Graph   
        fields = '__all__'

    def create(self, request):
        validated_data = request
        node_data = validated_data.pop('nodes')
        edge_data = validated_data.pop('edges')

        for node_data in node_data:
            position_data = node_data.pop('position')
            node = Node.objects.create(**node_data)

            NodePosition.objects.create(node=node, **position_data)
        for edge_data in edge_data:
            Edge.objects.create(**edge_data)
        graph = Graph.objects.create(**validated_data)
        return graph



