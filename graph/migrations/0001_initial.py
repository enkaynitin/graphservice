# Generated by Django 2.2.1 on 2019-05-08 19:32

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Edge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
            ],
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iid', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='NodePosition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('top', models.IntegerField()),
                ('left', models.IntegerField()),
                ('bottom', models.IntegerField()),
                ('right', models.IntegerField()),
                ('node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='position', to='graph.Node')),
            ],
        ),
        migrations.CreateModel(
            name='Graph',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('edges', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='graph.Edge')),
                ('nodes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='graph.Node')),
            ],
        ),
        migrations.AddField(
            model_name='edge',
            name='destination',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='node_destination', to='graph.Node'),
        ),
        migrations.AddField(
            model_name='edge',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='node_source', to='graph.Node'),
        ),
    ]
