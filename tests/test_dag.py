from experiment_tool.dag import DAG
import random


def test_topological_sort():
    vertices = list(range(10))
    random.shuffle(vertices)
    edges = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 7),
             (2, 7), (3, 7), (4, 8), (5, 8), (6, 8), (7, 9), (8, 9)]
    dag = DAG(vertices, edges)
    assert check_topological_sort(dag, dag.topological_sort())


def check_topological_sort(dag, sorted_list):
    edges = dag.get_edges()
    order = {}
    for i in range(len(sorted_list)):
        order[sorted_list[i]] = i
    for e in edges:
        u, v = e
        if order[u] > order[v]:
            return False
    return True
