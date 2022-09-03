from abc import ABC, abstractmethod

from grakel.svm_classification import KernelException


class KernelStrategy(ABC):

    @abstractmethod
    def get_kernel_instance(self, configuration, with_labels, with_attributes):
        pass


class ShortestPathStrategy(KernelStrategy):

    def get_kernel_instance(self, configuration: dict, with_labels, with_attributes):
        from grakel.kernels import ShortestPath
        from grakel.kernels import ShortestPathAttr
        if with_attributes:
            return ShortestPathAttr()
        return ShortestPath(with_labels=with_labels)

    def __str__(self) -> str:
        return 'SPK'


class GraphletSamplingStrategy(KernelStrategy):

    def get_kernel_instance(self, configuration: dict, *args):
        from grakel.kernels import GraphletSampling
        return GraphletSampling(k=configuration['k'])

    def __str__(self) -> str:
        return 'GR'


class VertexHistogramStrategy(KernelStrategy):

    def get_kernel_instance(self, configuration, with_labels, *args):
        from grakel.kernels import VertexHistogram
        if not with_labels:
            raise KernelException('Vertex Histogram kernel uses node labels')
        return VertexHistogram()

    def __str__(self) -> str:
        return 'VH'


class WeisfeilerLehmanSubtreeStrategy(KernelStrategy):
    def get_kernel_instance(self, configuration, with_labels, *args):
        from grakel.kernels import WeisfeilerLehman
        if not with_labels:
            raise KernelException('WeisfeilerLehman Subtree kernel uses node labels')
        return WeisfeilerLehman(n_iter=configuration['n_iter'])

    def __str__(self) -> str:
        return 'WL-ST'


class WeisfeilerLehmanOptimalAssignmentStrategy(KernelStrategy):
    def get_kernel_instance(self, configuration, with_labels, *args):
        from grakel.kernels import WeisfeilerLehmanOptimalAssignment
        if not with_labels:
            raise KernelException('WeisfeilerLehman Optimal Assignment kernel uses node labels')
        return WeisfeilerLehmanOptimalAssignment(n_iter=configuration['n_iter'])

    def __str__(self) -> str:
        return 'WL-OA'


class RenyiStrategy(KernelStrategy):
    def get_kernel_instance(self, configuration, *args):
        from grakel.kernels import RenyiEntropy
        return RenyiEntropy(depth=configuration['depth'])

    def __str__(self) -> str:
        return 'RE'


class NeighborhoodHashStrategy(KernelStrategy):
    def get_kernel_instance(self, configuration, with_labels, *args):
        from grakel.kernels import NeighborhoodHash
        if not with_labels:
            raise KernelException('Neighborhood Hash  kernel uses node labels')
        return NeighborhoodHash(R=configuration['R'], nh_type=configuration['nh_type'])

    def __str__(self) -> str:
        return 'NH'


class GraphHopperStrategy(KernelStrategy):
    def get_kernel_instance(self, configuration, with_labels, with_attributes):
        from grakel.kernels import GraphHopper
        if not with_labels and not with_attributes:
            raise KernelException('Graph Hopper kernel uses either node labels or node attributes')
        else:
            return GraphHopper(kernel_type=configuration['kernel_type'])

    def __str__(self) -> str:
        return 'GH'


class RandomWalkStrategy(KernelStrategy):
    def get_kernel_instance(self, configuration, with_labels, *args):
        from grakel.kernels import RandomWalk
        from grakel.kernels import RandomWalkLabeled
        if with_labels:
            return RandomWalkLabeled(lamda=configuration['lambda'], p=configuration['p'])
        else:
            return RandomWalk(lamda=configuration['lambda'], p=configuration['p'])

    def __str__(self) -> str:
        return 'RW'


class NeighborhoodSubgraphPairwiseDistanceStrategy(KernelStrategy):
    def get_kernel_instance(self, configuration, with_labels, *args):
        from grakel.kernels import NeighborhoodSubgraphPairwiseDistance
        if not with_labels:
            raise KernelException('Neighborhood Subgraph Pairwise Distance kernel uses node labels')
        else:
            return NeighborhoodSubgraphPairwiseDistance(r=configuration['r'], d=configuration['d'])

    def __str__(self) -> str:
        return 'NSPD'
