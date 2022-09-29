from django.contrib import messages
from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Dataset, Kernel, Parameter, Result
from grakel.datasets import fetch_dataset, get_dataset_info
from grakel.graph import Graph
import numpy as np
# Register your models here.
admin.site.unregister(Group)
admin.site.site_header = "Graph kernels admin panel"
admin.site.site_title = "Graph kernels admin panel"


class DatasetAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('id', 'name', 'number_graphs', 'number_classes', 'classes_imbalance',
                    'average_nodes', 'average_edges', 'labels_number', 'attribute_dimension')
    list_display_links = ('id', 'name')
    list_filter = []
    search_fields = ('id', 'name')
    #list_editable = ()

    def has_change_permission(self, request, obj=None):
        if obj is not None:
            return False
        return super().has_change_permission(request, obj=obj)

    def remove_default_message(self, request):
        storage = messages.get_messages(request)
        try:
            del storage._queued_messages[-1]
        except KeyError:
            pass
        return True

    def response_add(self, request, obj, post_url_continue=None):
        """override"""
        response = super().response_add(request, obj, post_url_continue)
        self.remove_default_message(request)
        return response

    def save_model(self, request, obj, form, change):
        dataset_name = form.cleaned_data.get('name')
        try:
            dataset_info = get_dataset_information(dataset_name=dataset_name)
            obj.name = dataset_name
            obj.number_graphs = dataset_info['num_graphs']
            obj.number_classes = dataset_info['num_classes']
            obj.classes_imbalance = dataset_info['class_imbalance']
            obj.average_nodes = dataset_info['avg_nodes']
            obj.average_edges = dataset_info['avg_edges']
            obj.labels_number = dataset_info['num_labels']
            obj.attribute_dimension = dataset_info['dim_attribute']
            messages.add_message(request, messages.SUCCESS, dataset_name+' has been successfully added')
            return super(DatasetAdmin, self).save_model(request, obj, form, change)
        except:
            messages.add_message(request, messages.ERROR, 'Dataset not found')
            return False


class ParameterAdmin(admin.ModelAdmin):
    fields = ('name', 'values', 'kernel')
    list_display = ('id', 'name', 'values', 'kernel_name')
    list_display_links = ('id',)
    search_fields = ('id', 'name')
    list_editable = ('name', 'values')


class InlineParameter(admin.TabularInline):
    model = Parameter
    extra = 1


class KernelAdmin(admin.ModelAdmin):
    fields = ('name', 'use_node_labels', 'use_node_attributes')
    list_display = ('id', 'name', 'use_node_labels', 'use_node_attributes')
    list_display_links = ('id',)
    list_filter = ['use_node_labels', 'use_node_attributes']
    search_fields = ('id', 'name')
    list_editable = ('name', 'use_node_labels', 'use_node_attributes')
    inlines = [InlineParameter, ]

    def remove_default_message(self, request):
        storage = messages.get_messages(request)
        try:
            del storage._queued_messages[-1]
        except KeyError:
            pass
        return True

    def response_add(self, request, obj, post_url_continue=None):
        """override"""
        response = super().response_add(request, obj, post_url_continue)
        self.remove_default_message(request)
        messages.add_message(request, messages.SUCCESS, obj.name+' has been successfully added')
        return response

    def response_change(self, request, obj):
        """override"""
        response = super().response_change(request, obj)
        self.remove_default_message(request)
        messages.add_message(request, messages.SUCCESS, 'kernel has been successfully updated')
        return response


class ResultAdmin(admin.ModelAdmin):
    fields = []
    list_display = ('id', 'kernel', 'dataset', 'accuracy', 'standard_deviation',
                    'running_time', 'rbf', 'sigma', 'normalize', 'c', 'cv', 'experiments', 'with_labels', 'with_attributes', 'parameters')
    list_display_links = ('id',)
    list_filter = ['dataset', 'kernel', 'normalize','rbf','with_labels', 'with_attributes']
    search_fields = ('id', 'dataset', 'kernel')
    
    def has_change_permission(self, request, obj=None):
        if obj is not None:
            return False
        return super().has_change_permission(request, obj=obj)
    
    def has_add_permission(self, request):
        return False

admin.site.register(Dataset, DatasetAdmin)
admin.site.register(Kernel, KernelAdmin)
admin.site.register(Parameter, ParameterAdmin)
admin.site.register(Result, ResultAdmin)

########################################################################################


def get_number_graphs(data):
    return len(data)


def get_number_classes(y):
    return len(set(y))


def get_max_class_imbalance(y):
    class_count = [np.count_nonzero(y == x) for x in set(y)]
    max_item = max(class_count)
    min_item = min(class_count)
    max_class_imbalance = round(max_item/min_item, 2)
    return f'1 : {max_class_imbalance}'


def get_avg_nodes(data):
    all_nodes = 0
    l = len(data)
    for g in data:
        graph = Graph(g[0])
        all_nodes += len(graph.vertices)
    return round(all_nodes/l, 2)


def get_avg_edges(data):
    all_edges = 0
    l = len(data)
    for g in data:
        all_edges += len(g[0])
    return round(all_edges/(l*2), 2)


def get_number_labels(data, dataset_name):
    if not get_dataset_info(dataset_name)['nl']:
        return '-'
    else:
        list_labels = []
        for g in data:
            list_labels += list(g[1].values())
        label_number = len(set(list_labels))
        return f'+ ({label_number})'


def get_attribute_dimension(dataset_name):
    if not get_dataset_info(dataset_name)['na']:
        return '-'
    else:
        data = fetch_dataset(dataset_name, prefer_attr_nodes=True, verbose=False).data
        dimension = len(data[0][1][1])
        return f'+ ({dimension})'


def get_dataset_information(dataset_name):
    dataset = fetch_dataset(dataset_name, verbose=False)
    data = dataset.data
    y = dataset.target
    data_info = dict()
    data_info['num_graphs'] = get_number_graphs(data)
    data_info['num_classes'] = get_number_classes(y)
    data_info['class_imbalance'] = get_max_class_imbalance(y)
    data_info['avg_nodes'] = get_avg_nodes(data)
    data_info['avg_edges'] = get_avg_edges(data)
    data_info['num_labels'] = get_number_labels(data, dataset_name)
    data_info['dim_attribute'] = get_attribute_dimension(dataset_name)
    # return f'{get_number_graphs(data)} & {get_number_classes(y)} & {get_max_class_imbalance(y)} & {get_avg_nodes(data)} & {get_avg_edges(data)} & {get_number_labels(data, dataset_name)} & {get_attribute_dimension(dataset_name)}'
    return data_info
