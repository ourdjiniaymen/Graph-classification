import warnings
from collections.abc import Iterable

from grakel.kernels import Kernel
from grakel.graph import Graph
import numpy as np
from scipy.optimize import linear_sum_assignment

from grakel.utilities import euclidean_distance


class RenyiEntropy(Kernel):
    def __init__(self, n_jobs=None,
                 normalize=False,
                 verbose=False,
                 depth=3,
                 entropy_type='renyi'):
        super(RenyiEntropy, self).__init__(
            n_jobs=n_jobs, normalize=normalize, verbose=verbose)

        self.depth = depth
        self.entropy_type = entropy_type
        self._initialized.update({"depth": False, "entropy_type": False})

    def initialize(self):
        """Initialize all transformer arguments, needing initialization."""
        super(RenyiEntropy, self).initialize()
        if not self._initialized["entropy_type"]:
            if self.entropy_type == 'renyi':
                self.entropy_method = renyi_entropy
            elif self.entropy_type == 'shanon':
                self.entropy_method = shanon_entropy
            else:
                raise ValueError('Unsupported value ' + str(self.entropy_method) + ' for "entropy_type"')

    def h_layer_entropy_representation(self, G, S, v):
        """
        :param G: undirected unweighted graph
        :param S: shortest path matrix of G
        :param v: int, node in G
        :return: h-dimensional vector which is the h-layer entropy representation of G
        """
        h_layer_entropy_vector = list()
        for k in range(1, self.depth + 1):
            subgraph = k_layer_expansion_subgraph(G, S, v, k)
            h_layer_entropy_vector.append(self.entropy_method(subgraph))
        return h_layer_entropy_vector

    def parse_input(self, X):
        """Parse and create features for "renyi entropy" kernel.

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
                if is_iter:
                    if len(x) == 0:
                        warnings.warn('Ignoring empty element on index: '
                                      + str(idx))
                        continue
                    else:
                        x = Graph(x[0], {}, {}, graph_format='auto')
                elif type(x) is not Graph:
                    raise TypeError('each element of X must have at least' +
                                    ' one and at most 3 elements\n')
                spm_data = x.nx_shortest_path_matrix()
                G_vector = list()
                for v in x.vertices:
                    G_vector.append(self.h_layer_entropy_representation(x, spm_data, v))

                ni += 1
                entropy_representation.append(G_vector)
            if ni == 0:
                raise ValueError('parsed input is empty')
            return entropy_representation

    def pairwise_operation(self, x, y):
        R = affinity_matrix(x, y)
        C = correspondence_matrix(R)
        return np.sum(C)


def shanon_entropy(G):
    """
    :param G: undirected unweighted graph
    :return: shanon entropy of G
    """
    degrees = list(G.degrees().values())
    entropy = 0
    sum_degrees = sum(degrees)
    if sum_degrees == 0:
        return 0
    for d in degrees:
        p = d / sum_degrees
        entropy += p * np.log(p)
    return -1 * entropy


def renyi_entropy(G):
    """
    :param G: undirected unweighted graph
    :return: renyi entropy of G
    """
    degrees = list(G.degrees().values())
    entropy = 0
    sum_degrees = sum(degrees)
    if sum_degrees == 0:
        return 0
    for d in degrees:
        p = d / sum_degrees
        entropy += p ** 2
    return -1 * np.log(entropy)


"""def correspondence_matrix(R):
    n, m = np.shape(R)
    C = np.zeros((n, m))
    for i in range(n):
        for j in range(m):
            if R[i, j] == np.amin(R[i, :]) and R[i, j] == np.amin(R[:, j]):
                C[i, j] = 1

    for i in range(n):
        for j in range(m):
            if 1 in C[i, 0:j] or 1 in C[0:i, j]:
                C[i, j] = 0
    return C"""


def correspondence_matrix(R):
    n, m = np.shape(R)
    C = np.zeros((n, m))
    i = 0
    exception = []
    while i < n:
        j = 0
        while j < m:
            if j in exception:
                j += 1
                continue
            if R[i, j] == np.amin(R[i, :]) and R[i, j] == np.amin(R[:, j]):
                C[i, j] = 1
                exception.append(j)
                break
            j += 1
        i += 1
    return C


"""def correspondence_matrix(R):
    row_ind, col_ind = linear_sum_assignment(R)
    C = np.zeros(R.shape)
    C[row_ind, col_ind] = 1
    return C"""


def affinity_matrix(G1_vector, G2_vector):
    """
    :param index_G1: int
    :param index_G2: int
    :return: the affinity matrix between G_1 and G_2
    """
    n = len(G1_vector)
    m = len(G2_vector)
    R = np.empty((n, m))
    for v in range(n):
        A = G1_vector[v]
        for u in range(m):
            B = G2_vector[u]
            R[v, u] = euclidean_distance(A, B)
    return R


def k_layer_expansion_nodes(G, S, v, k):
    """
    :param S: shortest path matrix of G=(V,E)
    :param v: int, node in graph G
    :param k: int, layer depth
    :return: N âŠ‚ V and N = {u âˆˆ V|S(v, u) â‰¤ K}
    """
    N = list()
    l = list(G.vertices)
    id_v = l.index(v)
    for (idx, u) in enumerate(G.vertices):
        if S[id_v][idx] <= k:
            N.append(u)
    return N


def k_layer_expansion_subgraph(G, S, v, k):
    """
    :param G: undirected unweighted graph
    :param S: shortest path matrix of G
    :param v: int, node in G
    :param k: int, layer depth
    :return: the induced subgraph on the k expansion nodes
    """
    N = k_layer_expansion_nodes(G, S, v, k)

    return G.get_subgraph(N)
