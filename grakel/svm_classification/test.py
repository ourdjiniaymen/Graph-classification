

import numpy as np

from grakel.svm_classification import GraphletSamplingStrategy
from grakel.svm_classification import UnifiedClassificationModel

if __name__ == '__main__':
    dataset_name = 'MUTAG'
    C = (10. ** np.arange(-7, 7, 1)).tolist()
    sigma = (2. ** np.arange(0, 1, 1)).tolist()
    normalize = [True, False]
    rbf = [False]
    model = UnifiedClassificationModel(GraphletSamplingStrategy(), kernel_configuration={'k': [3, 4]})
    result = model.tuning_classification(dataset_name)
    print(result)