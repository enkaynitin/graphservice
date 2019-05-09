from django.contrib import admin
from .models import Graph, Node, NodePosition, Edge
# Register your models here.


admin.site.register(Graph)
admin.site.register(Node)
admin.site.register(NodePosition)
admin.site.register(Edge)