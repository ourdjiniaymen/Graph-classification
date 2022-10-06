from dataclasses import fields
from rest_framework import serializers
from base.models import Dataset, Evaluation, Kernel, Parameter, Result


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ('id', 'name', 'number_graphs', 'number_classes','classes_imbalance', 'average_nodes','average_edges','labels_number','attribute_dimension')


class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ('name', 'values')

class KernelSerializer(serializers.ModelSerializer):
    parameter_list = serializers.PrimaryKeyRelatedField(many=True, queryset=Parameter.objects.all(), write_only=True)
    parameters = ParameterSerializer(many=True, read_only=True, source= 'parameter_set')

    class Meta:
        model = Kernel
        fields = ('id','name', 'use_node_labels', 'use_node_attributes', 'parameter_list', 'parameters')

    def update(self, instance, validated_data):

        parameter_list = validated_data.pop('parameter_list', None)

        instance = super().update(instance, validated_data)

        if parameter_list:
            for parameter in parameter_list:
                instance.parameters.add(parameter)
            instance.save()
        return instance



class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = '__all__'
        
class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ('id','kernel', 'dataset', 'accuracy', 'standard_deviation', 'running_time', 'rbf', 'sigma', 'normalize', 'c','cv','experiments', 'with_labels','with_labels', 'with_attributes', 'parameters')