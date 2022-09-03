import enum
import errno
import os
import numpy as np
import ast


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def open_a(path, mode='a'):
    """ Open "path" for writing, creating any parent directories as needed.
    """
    mkdir_p(os.path.dirname(path))
    return open(path, mode)


def read_matrix_from_file(path):
    f = open(path, "r")
    content = f.read()
    matrix = np.array(ast.literal_eval(content))
    matrix = np.where(matrix == -1, float("Inf"), matrix)
    return matrix


def euclidean_distance(A, B):
    """
    :param A: vector
    :param B: vector
    :return: euclidean distance between A and B
    """
    diff = np.subtract(A, B)
    return np.sqrt(np.dot(diff, diff))


def normalized_distance_euclidean(x, y):
    return (np.linalg.norm((x - np.mean(x)) - (y - np.mean(y))) ** 2) / (
            np.linalg.norm(x - np.mean(x)) ** 2 + np.linalg.norm(y - np.mean(y)) ** 2)
