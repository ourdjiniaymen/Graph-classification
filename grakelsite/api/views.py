from functools import reduce
from unittest import result
from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Dataset, Kernel, Result
from .serializers import DatasetSerializer, EvaluationSerializer, KernelSerializer, ResultSerializer
from grakel.svm_classification import GraphletSamplingStrategy, ShortestPathStrategy, VertexHistogramStrategy, WeisfeilerLehmanSubtreeStrategy, WeisfeilerLehmanOptimalAssignmentStrategy, RenyiStrategy, RandomWalkStrategy, NeighborhoodHashStrategy, NeighborhoodSubgraphPairwiseDistanceStrategy, GraphHopperStrategy, LabeledEntropyStrategy
from grakel.svm_classification import UnifiedClassificationModel

from api import serializers


@api_view(['GET'])
def getDatasets(request):
    datasets = Dataset.objects.all()
    serializer = DatasetSerializer(datasets, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getKernels(request):
    kernels = Kernel.objects.all()
    serializer = KernelSerializer(kernels, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getResults(request):
    results = Result.objects.all()
    serializer = ResultSerializer(results, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def addEvaluation(request):
    serializer = EvaluationSerializer(data=request.data)
    if serializer.is_valid():
        result_evaluation = run_evaluation(serializer.data)
        serializer = ResultSerializer(data=result_evaluation)
        if serializer.is_valid():
            serializer.save()
        else:
            print('not valid')
    else:
        print('not ok')
    return Response(serializer.data)


def run_evaluation(data):
    dataset_name = data['dataset']
    c = data['c']
    sigma = data['sigma']
    svm_configuration = {'C': c, 'sigma': sigma}
    normalize = data['normalize']
    rbf = data['rbf']
    cv = data['cv']
    experiments = data['experiments']
    with_labels = data['with_labels']
    with_attributes = data['with_attributes']
    kernel_strategy = get_kernel_strategy(data['kernel'])
    kernel_configuration = reduce(lambda r, d: r.update(d) or r, data['parameters'], {})
    model = UnifiedClassificationModel(kernel_strategy(), kernel_configuration=kernel_configuration, svm_configuration=svm_configuration,
                                       normalize=normalize, rbf=rbf, cv=cv, experiments=experiments, with_labels=with_labels, with_attributes=with_attributes)
    result = model.tuning_classification(dataset_name)
    params =  [{key:result['best params'][key]} for key in result['best params']]
    serializer = {'kernel': data['kernel'], 'dataset': dataset_name,
                  'accuracy': result['acc'], 'standard_deviation': result['std'], 'running_time': result['running_time'],
                  'rbf': result['rbf'], 'sigma': result['sigma'], 'normalize': result['normalize'],
                  'c': result['C'], 'cv': cv, 'experiments': experiments, 'with_labels': result['with_labels'], 'with_attributes': result['with_attributes'], 'parameters': params}
    return serializer


def get_kernel_strategy(kernel_name):
    if kernel_name == "SP" or kernel_name == "Shortest path":
        return ShortestPathStrategy
    elif kernel_name == "GS" or kernel_name == "Graphlet sampling":
        return GraphletSamplingStrategy
    elif kernel_name == "VH" or kernel_name == "Vertex histogram":
        return VertexHistogramStrategy
    elif kernel_name == "WL" or kernel_name == "WeisfeilerLehman subtree":
        return WeisfeilerLehmanSubtreeStrategy
    elif kernel_name == "WL-OA" or kernel_name == "WeisfeilerLehman optimal assignment":
        return WeisfeilerLehmanOptimalAssignmentStrategy
    elif kernel_name == "RE" or kernel_name == "Renyi entropy":
        return RenyiStrategy
    elif kernel_name == "RW" or kernel_name == "Random walk":
        return RandomWalkStrategy
    elif kernel_name == "NSPD" or kernel_name == "Neighborhood subgraph pairwise distance":
        return NeighborhoodSubgraphPairwiseDistanceStrategy
    elif kernel_name == "NH" or kernel_name == "Neighborhood hash":
        return NeighborhoodHashStrategy
    elif kernel_name == "GH" or kernel_name == "Graph hopper":
        return GraphHopperStrategy
    elif kernel_name == "LE" or kernel_name == "Labeled entropy":
        return LabeledEntropyStrategy
    else:
        return None


"""
@api_view(['POST'])
def addItem(request):
    serializer = ItemSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)"""
