from django.test import TestCase
from .models import Graph, Node, Edge
# Create your tests here.


class GraphTest(TestCase):
    """
    Test for model Graph
    """

    def setUp(self):
        self.before_count = Graph.objects.count()
        self.graph = Graph.objects.create(title='Grapb123')
        self.count = Graph.objects.count()
        self.assertNotEqual(self.before_count, self.count)

    def test_string_representation(self):
        self.assertEqual(str(self.graph), self.graph.title)


class NodeTest(TestCase):
    """
    Test for model Node
    """
    def setUp(self):
        self.g = Graph.objects.create(title='test1')
        self.before_count = Node.objects.count()
        self.node = Node.objects.create(graph=self.g, iid='v1', top=10, left=20, bottom=30, right=50)
        self.count = Node.objects.count()
        self.assertNotEqual(self.before_count, self.count)

    def test_position(self):
        self.node_ostion = self.node.position()
        self.assertEqual(self.node_ostion, {
            'top': 10,
            'left': 20,
            'bottom': 30,
            'right': 50
        })

    def test_string_representation(self):
        self.assertEqual(str(self.node), "{} {}".format(self.node.iid, self.node.title))




