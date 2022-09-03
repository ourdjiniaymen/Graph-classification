"""Graph classification model as defined in :cite:`Errica2020AFAIR`."""
import itertools as it
import statistics as stat
from operator import itemgetter
import random
import numpy as np
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.svm import SVC

from grakel.datasets import fetch_dataset
from grakel.datasets import get_dataset_info
from grakel.svm_classification import KernelStrategy


class UnifiedClassificationModel:
    def __init__(self, kernel_strategy: KernelStrategy,
                 kernel_configuration=None, svm_configuration=None, with_labels=True, with_attributes=False,
                 normalize=True,
                 rbf=False, cv=10, experiments=10) -> None:
        self._kernel_strategy = kernel_strategy
        self.kernel_configuration = kernel_configuration
        self.svm_configuration = svm_configuration
        self.with_labels = with_labels
        self.with_attributes = with_attributes
        self.normalize = normalize
        self.rbf = rbf
        self.cv = cv
        self.experiments = experiments
        self.prev_kernel_configuration = None
        self.initialize()

    def initialize(self):
        if self.kernel_configuration is None:
            self.kernel_configuration = dict()
        if self.svm_configuration is None:
            self.svm_configuration = dict()
            self.svm_configuration['C'] = (10. ** np.arange(-7, 7, 1)).tolist()
            self.svm_configuration['sigma'] = (2. ** np.arange(-3, 3, 1)).tolist()
        if not self.rbf:
            self.svm_configuration['sigma'] = [0]
        if self.with_labels:
            self.with_attributes = False

    @property
    def kernel_strategy(self) -> KernelStrategy:
        return self._kernel_strategy

    @kernel_strategy.setter
    def kernel_strategy(self, kernel_strategy: KernelStrategy) -> None:
        self._kernel_strategy = kernel_strategy

    def cross_validation(self, K, y, C_value):
        y = np.array(y)
        kf = StratifiedKFold(n_splits=self.cv)
        accuracies = []
        self.arange = np.arange(len(y))
        for train_index, test_index in kf.split(self.arange, y):
            K_train = K[np.ix_(train_index, train_index)]
            K_test = K[np.ix_(test_index, train_index)]
            y_train = y[train_index]
            y_test = y[test_index]
            # Uses the SVM classifier to perform classification
            clf = SVC(kernel='precomputed', C=C_value).fit(K_train, y_train)
            acc = clf.score(K_test, y_test)
            # Computes and prints the classification accuracy
            accuracies.append(acc)
        return stat.mean(accuracies)

    def tuning_classification(self, dataset_name):
        info = get_dataset_info(dataset_name)
        has_labels = info['nl']
        has_attributes = info['na']

        if self.with_attributes and not has_attributes:
            self.with_attributes = False
            self.with_labels = True
        dataset = fetch_dataset(dataset_name, prefer_attr_nodes=self.with_attributes,
                                verbose=False)
        self.graphs = dataset.data
        self.y = dataset.target

        if self.with_labels and not has_labels:
            # add same label to all nodes in graphs
            self.graphs = add_labels_to_graphs(graphs=self.graphs, label='0')

        tuning_results = []
        kernel_param_combinations = list(it.product(*self.kernel_configuration.values()))
        svm_param_combinations = list(it.product(*self.svm_configuration.values()))
        all_possible_combinations = list(it.product(*[kernel_param_combinations, svm_param_combinations]))
        for combination in all_possible_combinations:
            kernel_configuration_tuple = combination[0]
            kernel_configuration = dict()
            for (idx, key) in enumerate(self.kernel_configuration.keys()):
                kernel_configuration[key] = kernel_configuration_tuple[idx]
            svm_configuration_tuple = combination[1]
            svm_configuration = dict()
            for (idx, key) in enumerate(self.svm_configuration.keys()):
                svm_configuration[key] = svm_configuration_tuple[idx]
            accuracies = []
            for i in range(self.experiments):
                if kernel_configuration != self.prev_kernel_configuration:
                    self.K = self._kernel_strategy.get_kernel_instance(kernel_configuration, self.with_labels,
                                                                       self.with_attributes).fit_transform(self.graphs)
                    print('check')
                K = self.K
                y = self.y
                self.prev_kernel_configuration = kernel_configuration
                K, y = random_shuffle(K, y)
                if self.normalize:
                    K = normalize_matrix(K)
                if self.rbf:
                    K = RBF_K_matrix(K, svm_configuration['sigma'])
                acc_mean = self.cross_validation(K, y, svm_configuration['C'])
                accuracies.append(acc_mean)
            tuning_results.append((stat.mean(accuracies), stat.stdev(accuracies), kernel_configuration,
                                   svm_configuration))
        result = max(tuning_results, key=itemgetter(0))
        result = {'acc': round(result[0] * 100, 2), 'std': round(result[1] * 100, 2), 'best params': result[2],
                  'C': result[3]['C'], 'sigma': result[3]['sigma'], 'normalize': self.normalize, 'rbf': self.rbf,
                  'with_labels': self.with_labels, 'with_attributes': self.with_attributes}
        save_results(result, dataset_name, self.kernel_strategy)
        return result


def save_results(result, dataset_name, kernel):
    with open('../../../Results/Classification plateform/' + str(kernel) + '_' + dataset_name, 'w+') as f:
        f.write('Accuracy Mean :' + str(result['acc']) + '%\n')
        f.write('Accuracy Std :' + str(result['std']) + '%\n')
        f.write('Best kernel configuration : \n')
        for param, value in result['best params'].items():
            f.write('\t' + str(param) + ' : ' + str(value) + '\n')
        f.write('Best C value : ' + str(result['C']) + '\n')
        f.write('best Sigma value : ' + str(result['sigma']) + '\n')
        f.write('Normalize value : ' + str(result['normalize']) + '\n')
        f.write('Rbf value : ' + str(result['rbf']) + '\n')
        f.write('With labels : ' + str(result['with_labels']) + '\n')
        f.write('With attributes : ' + str(result['with_attributes']) + '\n')


def random_shuffle(K, y):
    # y = np.array(y)
    ids = np.arange(0, len(y))
    random.shuffle(ids)
    y_copy = y[ids]
    K_copy = K[ids]
    K_copy = np.transpose(np.transpose(K_copy)[ids])
    return K_copy, y_copy


def RBF_K_matrix(K, sigma):
    k_yy = np.repeat(np.diag(K)[None, :], np.shape(K)[0], axis=0)
    k_xx = np.transpose(k_yy)
    return np.exp(-1 * (k_xx - 2 * K + k_yy) / (2 * pow(sigma, 2)))


def normalize_matrix(K):
    X_diag = np.diagonal(K)
    return np.divide(K, np.sqrt(np.outer(X_diag, X_diag)))


def get_nodes(edges):
    nodes = set()
    for edge in edges:
        nodes.add(edge[0])
        nodes.add(edge[1])
    return nodes


def add_labels_to_graphs(graphs, label):
    for graph in graphs:
        edges = graph[0]
        nodes = get_nodes(edges)
        labeled_nodes = dict()
        for node in nodes:
            labeled_nodes[node] = label
        graph[1] = labeled_nodes
    return graphs
