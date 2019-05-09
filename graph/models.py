from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class Graph(models.Model):
    title = models.CharField(max_length=100)
    nodes = models.ManyToManyField('Node', related_name='graphs')
    edges = models.ManyToManyField('Edge', related_name='graphs')

    def __str__(self):
        return "{} {} {}".format(self.title, self.nodes, self.edges)


class Node(models.Model):
    graph = models.ManyToManyField(Graph, related_name='graphs')
    iid = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    position = models.ForeignKey('NodePosition', on_delete=models.CASCADE, related_name='node_position', null=True)

    def __str__(self):
        return "{} {} {}".format(self.iid, self.title, self.position)


class NodePosition(models.Model):
    top = models.IntegerField()
    left = models.IntegerField()
    bottom = models.IntegerField()
    right = models.IntegerField()

    def __str__(self):
        return "{} {} {} {}".format(self.top, self.left, self.bottom, self.right)


class Edge(models.Model):
    graph = models.ManyToManyField(Graph, related_name='graph_edges')
    source = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='node_source', null=True)
    target = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='node_target', null=True)
    weight = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)])

    def __str__(self):
        return "{} {} {}".format(self.source, self.target, self.weight)


