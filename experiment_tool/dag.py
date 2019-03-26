from hypothesis import given, strategies as st
import random


class DAG:
    def __init__(self, vertices, edges):
        self._graph = {}
        self._add_vertices(vertices)
        self._add_edges(edges)
        self._validate()

    def _add_vertices(self, vertices):
        """
        Add list of vertices to dag.
        """
        for v in vertices:
            self._graph.setdefault(v, [])

    def _add_edges(self, edges):
        """
        Add list of edges to dag.
        Throws exception if there is an end of an edge that is not in dag.
        """
        for (x, y) in edges:
            if (x not in self._graph) or (y not in self._graph):
                raise KeyError("No such vertex in a _graph")
            self._graph[x].append(y)

    def get_vertices(self):
        return self._graph.keys()

    def topological_sort(self) -> list:
        """
        Return a topological sort of dag.
        """
        res = []
        visited = set()

        def dfs(x):
            visited.add(x)
            for y in self._graph[x]:
                if y not in visited:
                    dfs(y)
            res.append(x)

        for v in self._graph:
            if v not in visited:
                dfs(v)
        res.reverse()
        return res

    def get_subgraph(self, metrics, modified):
        """
        Return subgraph that contains all vertices, functions in which should be recalculated
        in order to obtain desired metrics.
        """
        return self

    def _validate(self):
        """
        Check if dag is valid.
        Throws exception otherwise.
        """
        visited = {}  # values : 0 - not visited, 1 - in, 2 - out

        def dfs(x):
            visited[x] = 1
            for y in self._graph[x]:
                if visited[y] == 1:
                    return True
                if not visited[y]:
                    if dfs(y):
                        return True
            visited[x] = 2
            return False

        for v in self._graph:
            visited.setdefault(v, 0)
        for v in self._graph:
            if not visited[v]:
                if dfs(v):
                    raise Exception("Graph contains cycle")


max_vert = random.randint(0, 10)
# max_vert = st.integers(min_value=0, max_value=10)


@given(  # vertices=max_vert,
       edges=st.tuples(st.integers(min_value=0, max_value=max_vert),
                       st.integers(min_value=0, max_value=max_vert)))
def test_topological_sort(edges):
    dag = DAG(list(range(max_vert)), edges)
    assert check_topological_sort(dag, dag.topological_sort())


def check_topological_sort(dag, sorted_list):
    sorted_list.reverse()
    size = len(sorted_list)

    def dfs(v):
        res = set()
        for u in dag._graph[v]:
            res.add(u).add(dfs(u))
        return res

    for i in range(size):
        adjacent = dfs(sorted_list[i])
        for j in range(i + 1, size):
            if sorted_list[j] in adjacent:
                return False
    return True


test_topological_sort()
