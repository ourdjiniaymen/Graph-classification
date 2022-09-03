"""
Creates graphs from kernel databases to test shortest motif path on them
"""
from utilities import open_a
from grakel.datasets import fetch_dataset
from grakel import Graph

GRAPHS_PATH = '../../../data/graphs/'
GRAPHS_FOR_VISUALIZATION_PATH = '../../../data/graphs_for_visualization/'
datasets = ['AIDS', 'DD', 'ENZYMES', 'IMDB-BINARY', 'IMDB-MULTI', 'MSRC_9', 'MSRC_21', 'MSRC_21C', 'NCI1', 'PROTEINS',
            'PTC_MR', 'SYNTHETICnew', 'Synthie']


def write_graph(graph, graph_id, dataset_name):
    n = graph.nv()
    m = len(graph.get_edges())
    d = graph.diameter()
    degree = graph.average_degree()
    first_line = f'#NodeNum:{n}\tedgNum:{m}\tave.degree:{degree}\tdiameter:{d}'
    file = open_a(GRAPHS_PATH + dataset_name + '/' + str(graph_id))
    file.write(first_line)
    for edge in graph.get_edges():
        ne = normalize_edge(edge)
        file.write('\n' + str(ne[0]) + ',' + str(ne[1]))
    file.close()


def write_graph_for_visualisation(graph_core, graph_id, class_id, dataset_name):
    m = len(graph_core.get_edges())
    i = 1
    file = open_a(GRAPHS_FOR_VISUALIZATION_PATH + dataset_name + '/' + str(graph_id) + '_' + str(class_id))
    for edge in graph_core.get_edges():
        ne = normalize_edge(edge)
        file.write(str(ne[0]) + '\t' + str(ne[1]))
        if not (i == m):
            file.write('\n')
        i += 1
    file.close()


def normalize_edge(edge):
    return edge[0] + 1, edge[1] + 1


def normalize_graph(edges):
    normalized_edges = list()
    for edge in edges:
        if edge[0] < edge[1]:
            normalized_edges.append(edge)
    return normalized_edges


def build_datasets(datasets):
    for dataset in datasets:
        print("start building", dataset, ' ...')
        fetched_data = fetch_dataset(dataset, verbose=False)
        graphs = fetched_data.data
        file = open_a(GRAPHS_PATH + dataset + '/M.txt')
        file.write(str(len(graphs)))
        for idx, graph in enumerate(graphs):
            list_edges = normalize_graph(graph[0])
            G = Graph(list_edges)
            write_graph(G, idx, dataset)
        print('------building of ', dataset, ' ends with success------')


def build_datasets_for_visualization(datasets):
    for dataset in datasets:
        print("start building", dataset, ' ...')
        fetched_data = fetch_dataset(dataset, verbose=False)
        graphs = fetched_data.data
        y = fetched_data.target
        for idx, graph in enumerate(graphs):
            list_edges = normalize_graph(graph[0])
            G = Graph(list_edges)
            write_graph_for_visualisation(G, idx, y[idx], dataset)
        print('------building of ', dataset, ' ends with success------')


if __name__ == '__main__':
    build_datasets_for_visualization(['MUTAG'])
