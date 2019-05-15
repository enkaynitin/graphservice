from django.db import models
from django.db.models import Q, Max
from django.core.validators import MaxValueValidator, MinValueValidator
from itertools import chain

# Create your models here.


class Graph(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return "{}".format(self.title)

    def edges(self):
        """get edges for the graph object.
         Look for edges that have source
         or destination having node belonging to the graph nodes.
        """
        edges = Edge.objects.none()
        for node in self.nodes.all().iterator(chunk_size=100):
            filered_edges = Edge.objects.filter(Q(source=node) | Q(target=node))
            edges = set(chain(edges, filered_edges))
        return edges


class Node(models.Model):

    graph = models.ForeignKey(Graph, related_name='nodes', on_delete=models.CASCADE, null=True)
    iid = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    top = models.FloatField(null=True)
    left = models.FloatField(null=True)
    bottom = models.FloatField(null=True)
    right = models.FloatField(null=True)

    def position(self):
        return {
            'top': self.top,
            'left': self.left,
            'bottom': self.bottom,
            'right': self.right
        }

    def weakly_connected(self):
        edges = Edge.objects.filter(Q(target=self))
        if edges.count()>0:
            if edges.aggregate(Max('weight'))['weight__max']< 0.5:
                return True
        else:
            return False

    def __str__(self):
        return "{} {}".format(self.iid, self.title)


class Edge(models.Model):

    source = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='node_source', null=True)
    target = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='node_target', null=True)
    weight = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)])

    def __str__(self):
        return "{} {} {}".format(self.source, self.target, self.weight)


class NodeTraversal(models.Model):

    nodes_to_traverse = models.ManyToManyField(Node, related_name='to_travers')
    traversed_nodes = models.ManyToManyField(Node, related_name='traversed')
    connected_nodes  = models.ManyToManyField(Node, related_name='connected')


class File(models.Model):

    title = models.CharField(max_length=50, null=True)
    file = models.FileField(upload_to='media', blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)



