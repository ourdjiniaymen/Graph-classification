import warnings
from collections.abc import Iterable
from grakel import Kernel, Graph
import numpy as np


class LabeledEntropy(Kernel):
    def __init__(self, n_jobs=None,
                 normalize=False,
                 verbose=False,
                 k=1):
        super(LabeledEntropy, self).__init__(
            n_jobs=n_jobs, normalize=normalize, verbose=verbose)
        self.attributed = False
        self.k = k
        self._initialized.update({"k": False})

    def initialize(self):
        """Initialize all transformer arguments, needing initialization."""
        super(LabeledEntropy, self).initialize()

    def neighborhood_distribution_entropy(self, G, source):
        """
        :param G: undirected unweighted graph
        :param source: int, node in G
        :return: neighborhood distribution entropy
        """
        subgraph = r_radius_subgraph(G, source, self.k)
        return labeled_entropy(subgraph, source)

    def parse_input(self, X):
        """Parse and create features for "deep renyi entropy" kernel.

        Parameters
        ----------
        X : iterable
            For the input to pass the test, we must have:
            Each element must be an iterable with at most three features and at
            least one. The first that is obligatory is a valid graph structure
            (adjacency matrix or edge_dictionary) while the second is
            node_labels and the third edge_labels (that correspond to the given
            graph format). A valid input also consists of graph type objects.

        Returns
        -------
        entropy_representation : list
            A list that for each vertex in each graph holds the h layer entropy representation.

        """
        if not isinstance(X, Iterable):
            raise TypeError('input must be an iterable\n')
            # Not a dictionary
        else:
            entropy_representation = list()
            ni = 0
            for (idx, x) in enumerate(iter(X)):
                is_iter = isinstance(x, Iterable)
                if is_iter:
                    x = list(x)
                if is_iter and (len(x) == 0 or
                                len(x) in [1, 2, 3]):
                    if len(x) == 0:
                        warnings.warn('Ignoring empty element on index: '
                                      + str(idx))
                        continue
                    elif len(x) == 1:
                        x = Graph(x[0], {}, {}, 'auto')
                    else:
                        x = Graph(x[0], x[1], {}, 'auto')
                elif type(x) is not Graph:
                    raise TypeError('each element of X must have at least' +
                                    ' one and at most 3 elements\n')
                try:
                    labels = x.get_labels(purpose=x.format)
                    if type(list(labels.values())[0]) == list:
                        self.attributed = True
                except:
                    labels = dict(zip(x.vertices, [0] * len(x.vertices)))
                graph_entropy_representation = list()
                for v in x.vertices:
                    graph_entropy_representation.append((self.neighborhood_distribution_entropy(x, v), labels[v]))
                ni += 1
                entropy_representation.append(graph_entropy_representation)
            if ni == 0:
                raise ValueError('parsed input is empty')
            return entropy_representation

    def pairwise_operation(self, x, y):
        kernel = 0
        for (x_entropy, x_label) in x:
            for (y_entropy, y_label) in y:
                if x_entropy == y_entropy:
                    if self.attributed:
                        kernel += np.dot(x_label, y_label)
                    elif x_label == y_label:
                        kernel += 1
        return kernel


def labeled_entropy(G, center):
    """
    :param G: undirected unweighted graph
    :return: renyi entropy of G
    """
    degrees = G.degrees()
    try:
        labels = G.get_labels(purpose="dictionary")
    except ValueError:
        labels = dict.fromkeys(G.vertices, 0)
    entropy = 0
    sum_degrees = label_sum_degrees(G, degrees, labels, center)
    if sum_degrees == 0:
        return 0
    for v in G.vertices:
        if labels[v] == labels[center]:
            p = degrees[v] / sum_degrees
            entropy += p ** 2
    return -1 * np.log(entropy)


def r_radius_subgraph(G, source, r):
    """
    :param G: undirected unweighted graph
    :param source: int, node in G
    :param r: int, layer depth
    :return: the induced subgraph on the r expansion nodes
    """
    r_radius_neighborhood = G.r_radius_neighborhood(source, r)
    return G.get_subgraph(r_radius_neighborhood)


def label_sum_degrees(G, degrees, labels, center):
    sum = 0
    center_label = labels[center]
    for v in G.vertices:
        if labels[v] == center_label:
            sum += degrees[v]
    return sum
