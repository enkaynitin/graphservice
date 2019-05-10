# Generated by Django 2.2.1 on 2019-05-09 22:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('graph', '0012_auto_20190509_1405'),
    ]

    operations = [
        migrations.AddField(
            model_name='edge',
            name='graph',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='edges', to='graph.Graph'),
        ),
        migrations.CreateModel(
            name='FindIsland',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nodes_to_traverse', models.ManyToManyField(related_name='to_travers', to='graph.Node')),
                ('traversed_nodes', models.ManyToManyField(related_name='traversed', to='graph.Node')),
            ],
        ),
    ]
