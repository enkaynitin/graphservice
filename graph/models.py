from django.db import models
from django.db.models import Q
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class Graph(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return "{}".format(self.title)


    def islands(self):
        nodes = self.nodes.all()


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
        edges = Edge.objects.filter(Q(source=self) | Q(target=self))
        if len(edges) == 0:
            return True
        for edge in edges:
            if edge.weight > 0.5:
                return False
        return True

    def __str__(self):
        return "{} {}".format(self.iid, self.title)


class Edge(models.Model):
    graph = models.ForeignKey(Graph, related_name='edges', on_delete=models.CASCADE, null=True)
    source = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='node_source', null=True)
    target = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='node_target', null=True)
    weight = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)])

    def __str__(self):
        return "{} {} {}".format(self.source, self.target, self.weight)


class FindIsland(models.Model):
    nodes_to_traverse = models.ManyToManyField(Node, related_name='to_travers')
    traversed_nodes = models.ManyToManyField(Node, related_name='traversed')


class File(models.Model):
    graph = models.ForeignKey(Graph, on_delete=models.CASCADE)
    file = models.FileField(upload_to='media', blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)



