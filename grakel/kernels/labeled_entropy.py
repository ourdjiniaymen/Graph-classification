import warnings
from collections.abc import Iterable
from grakel.graph import Graph
from grakel.kernels import Kernel
import numpy as np
from sklearn.utils.validation import check_is_fitted
from sklearn.exceptions import NotFittedError


class LabeledEntropy(Kernel):
    def __init__(self, n_jobs=None,
                 normalize=False,
                 verbose=False,
                 k=1,
                 entropy_type='von_neumann_entropy'):
        super(LabeledEntropy, self).__init__(
            n_jobs=n_jobs, normalize=normalize, verbose=verbose)
        self.attributed = False
        self.k = k
        self.entropy_type = entropy_type
        self._initialized.update({"k": False, 'entropy_type': False})

    def initialize(self):
        """Initialize all transformer arguments, needing initialization."""
        super(LabeledEntropy, self).initialize()
        if not self._initialized['entropy_type']:
            if self.entropy_type == 'renyi_entropy':
                self.entropy_method = labeled_renyi_entropy
            elif self.entropy_type == 'von_neumann_entropy':
                self.entropy_method = labeled_von_neumann_entropy
            else:
                raise ValueError('Unsupported "entropy_type"')

    def parse_input(self, X):
        """Parse and create features for "labeled entropy" kernel.

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
            i = -1
            entropy_representation = dict()
            if self._method_calling == 1:
                self._enum = dict()
            elif self._method_calling == 3:
                self._Y_enum = dict()
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
                i += 1
                try:
                    node_labels = x.get_labels(purpose=x.format)
                except:
                    node_labels = dict(zip(x.vertices, [0] * len(x.vertices)))
                entropy_representation[i] = dict()
                for v in x.vertices:
                    labeled_entropy = (
                        neighborhood_distribution_entropy(x, v, self.k, self.entropy_method), node_labels[v])
                    if labeled_entropy not in self._enum:
                        if self._method_calling == 1:
                            idx = len(self._enum)
                            self._enum[labeled_entropy] = idx
                        elif self._method_calling == 3:
                            if labeled_entropy not in self._Y_enum:
                                idx = len(self._enum) + len(self._Y_enum)
                                self._Y_enum[labeled_entropy] = idx
                            else:
                                idx = self._Y_enum[labeled_entropy]
                    else:
                        idx = self._enum[labeled_entropy]
                    if idx in entropy_representation[i]:
                        entropy_representation[i][idx] += 1
                    else:
                        entropy_representation[i][idx] = 1
            if i == -1:
                raise ValueError('parsed input is empty')

            if self._method_calling == 1:
                self._nx = i + 1
            elif self._method_calling == 3:
                self._ny = i + 1
            return entropy_representation

    def transform(self, X):
        """Calculate the kernel matrix, between given and fitted dataset.

        Parameters
        ----------
        X : iterable
            Each element must be an iterable with at most three features and at
            least one. The first that is obligatory is a valid graph structure
            (adjacency matrix or edge_dictionary) while the second is
            node_labels and the third edge_labels (that fitting the given graph
            format). If None the kernel matrix is calculated upon fit data.
            The test samples.

        Returns
        -------
        K : numpy array, shape = [n_targets, n_input_graphs]
            corresponding to the kernel matrix, a calculation between
            all pairs of graphs between target an features

        """
        self._method_calling = 3
        # Check is fit had been called
        check_is_fitted(self, ['X', '_nx', '_enum'])

        # Input validation and parsing
        if X is None:
            raise ValueError('transform input cannot be None')
        else:
            Y = self.parse_input(X)

        # Transform - calculate kernel matrix
        try:
            check_is_fitted(self, ['_phi_X'])
            phi_x = self._phi_X
        except NotFittedError:
            phi_x = np.zeros(shape=(self._nx, len(self._enum)))
            for i in self.X.keys():
                for j in self.X[i].keys():
                    phi_x[i, j] = self.X[i][j]
            self._phi_X = phi_x

        phi_y = np.zeros(shape=(self._ny, len(self._enum) + len(self._Y_enum)))
        for i in Y.keys():
            for j in Y[i].keys():
                phi_y[i, j] = Y[i][j]

        # store _phi_Y for independent (of normalization arg diagonal-calls)
        self._phi_Y = phi_y
        km = np.dot(phi_y[:, :len(self._enum)], phi_x.T)
        self._is_transformed = True
        if self.normalize:
            X_diag, Y_diag = self.diagonal()
            return km / np.sqrt(np.outer(Y_diag, X_diag))
        else:
            return km

    def diagonal(self):
        """Calculate the kernel matrix diagonal for fitted data.

        A funtion called on transform on a seperate dataset to apply
        normalization on the exterior.

        Parameters
        ----------
        None.

        Returns
        -------
        X_diag : np.array
            The diagonal of the kernel matrix, of the fitted data.
            This consists of kernel calculation for each element with itself.

        Y_diag : np.array
            The diagonal of the kernel matrix, of the transformed data.
            This consists of kernel calculation for each element with itself.

        """
        # Check is fit and transform had been called
        try:
            check_is_fitted(self, ['_phi_X'])
        except NotFittedError:
            check_is_fitted(self, ['X'])
            # calculate feature matrices.
            phi_x = np.zeros(shape=(self._nx, len(self._enum)))

            for i in self.X.keys():
                for j in self.X[i].keys():
                    phi_x[i, j] = self.X[i][j]
                    # Transform - calculate kernel matrix
            self._phi_X = phi_x

        try:
            check_is_fitted(self, ['X_diag'])
        except NotFittedError:
            # Calculate diagonal of X
            self._X_diag = np.sum(np.square(self._phi_X), axis=1)
            self._X_diag = np.reshape(self._X_diag, (self._X_diag.shape[0], 1))

        try:
            check_is_fitted(self, ['_phi_Y'])
            # Calculate diagonal of Y
            Y_diag = np.sum(np.square(self._phi_Y), axis=1)
            return self._X_diag, Y_diag
        except NotFittedError:
            return self._X_diag

    def fit_transform(self, X, y=None):
        """Fit and transform, on the same dataset.

        Parameters
        ----------
        X : iterable
            Each element must be an iterable with at most three features and at
            least one. The first that is obligatory is a valid graph structure
            (adjacency matrix or edge_dictionary) while the second is
            node_labels and the third edge_labels (that fitting the given graph
            format).

        y : Object, default=None
            Ignored argument, added for the pipeline.

        Returns
        -------
        K : numpy array, shape = [n_targets, n_input_graphs]
            corresponding to the kernel matrix, a calculation between
            all pairs of graphs between target an features

        """
        self._method_calling = 2
        self.fit(X)
        # calculate feature matrices.
        phi_x = np.zeros(shape=(self._nx, len(self._enum)))

        for i in self.X.keys():
            for j in self.X[i].keys():
                phi_x[i, j] = self.X[i][j]

        # Transform - calculate kernel matrix
        self._phi_X = phi_x
        km = np.dot(phi_x, phi_x.T)

        self._X_diag = np.diagonal(km)
        if self.normalize:
            return np.divide(km, np.sqrt(np.outer(self._X_diag, self._X_diag)))
        else:
            return km


class LabeledEntropyAttr(Kernel):
    def __init__(self, n_jobs=None,
                 normalize=False,
                 verbose=False,
                 k=1,
                 entropy_type='von_neumann_entropy',
                 metric=np.dot):
        super(LabeledEntropyAttr, self).__init__(
            n_jobs=n_jobs, normalize=normalize, verbose=verbose)
        self.attributed = False
        self.k = k
        self.entropy_type = entropy_type
        self.metric = metric
        self._initialized.update({"k": False, 'entropy_type': False, 'metric': False})

    def initialize(self):
        """Initialize all transformer arguments, needing initialization."""
        super(LabeledEntropyAttr, self).initialize()
        if not self._initialized["metric"]:
            if not callable(self.metric):
                raise TypeError('"metric" must be callable')
            self._initialized["metric"] = True
        if not self._initialized['entropy_type']:
            if self.entropy_type == 'renyi_entropy':
                self.entropy_method = labeled_renyi_entropy
            elif self.entropy_type == 'von_neumann_entropy':
                self.entropy_method = labeled_von_neumann_entropy
            else:
                raise ValueError('Unsupported "entropy_type"')

    def parse_input(self, X):
        """Parse and create features for "labeled entropy" kernel.

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
                if is_iter and len(x) in [0, 2, 3]:
                    if len(x) == 0:
                        warnings.warn('Ignoring empty element on index: '
                                      + str(idx))
                        continue
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
                    graph_entropy_representation.append(
                        (neighborhood_distribution_entropy(x, v, self.k, self.entropy_method), labels[v]))
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
                    kernel += self.metric(x_label, y_label)
        return kernel


def labeled_renyi_entropy(G, center):
    """
    :param G: undirected unweighted graph
    :return: labeled renyi entropy of G
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


def labeled_von_neumann_entropy(G, center):
    """
    :param G: undirected unweighted graph
    :return: von neumann entropy of G
    """
    degrees = G.degrees()
    vertices = G.vertices
    try:
        labels = G.get_labels(purpose="dictionary")
    except ValueError:
        labels = dict.fromkeys(G.vertices, 0)

    l = list(labels.values()).count(labels[center])
    sum = 0
    for v in vertices:
        if labels[v] == labels[center]:
            sum += 1 / ((l ** 2) * degrees[v] * degrees[center])
    return 1 - (1 / l) - sum


def label_sum_degrees(G, degrees, labels, center):
    sum = 0
    center_label = labels[center]
    for v in G.vertices:
        if labels[v] == center_label:
            sum += degrees[v]
    return sum


def r_radius_subgraph(G, source, r):
    """
    :param G: undirected unweighted graph
    :param source: int, node in G
    :param r: int, layer depth
    :return: the induced subgraph on the r expansion nodes
    """
    r_radius_neighborhood = G.r_radius_neighborhood(source, r)
    return G.get_subgraph(r_radius_neighborhood)


def neighborhood_distribution_entropy(G, source, k, entropy_method):
    """
    :param G: undirected unweighted graph
    :param source: int, node in G
    :return: neighborhood distribution entropy
    """
    subgraph = r_radius_subgraph(G, source, k)
    return entropy_method(subgraph, source)
