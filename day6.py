from typing import Dict


class SpaceVertex:
    def __init__(self, name):
        self.name = name
        self.child_nodes = []
        self._parent = None

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent_vertex: 'SpaceVertex'):
        self._parent = parent_vertex

    @parent.deleter
    def parent(self):
        del self._parent

    def add_child(self, child_vertex: 'SpaceVertex'):
        self.child_nodes.append(child_vertex)

    def __repr__(self):
        return f"{self.name} => {[child.name for child in self.child_nodes]}"

    def get_all_parents(self):
        parents = []
        current_vertex = self

        while current_vertex.parent:
            current_vertex = current_vertex.parent
            parents.append(current_vertex)

        return parents

    def distance_to(self, other: 'SpaceVertex'):
        own_parents = self.get_all_parents()
        other_parents = other.get_all_parents()
        return len(set(own_parents).symmetric_difference(set(other_parents)))


class UniverseOrbitMap:
    def __init__(self):
        self.vertices: Dict[str, SpaceVertex] = {}

    def _add_vertex(self, name):
        if name not in self.vertices:
            self.vertices[name] = SpaceVertex(name)
        else:
            raise ValueError(f'Vertex {name} is already in the vertices map.')

    def add_edge(self, name_origin, name_dest):
        if name_origin not in self.vertices:
            self._add_vertex(name_origin)
        if name_dest not in self.vertices:
            self._add_vertex(name_dest)

        origin_vertex = self.vertices[name_origin]
        dest_vertex = self.vertices[name_dest]

        dest_vertex.parent = origin_vertex
        origin_vertex.add_child(dest_vertex)

    @classmethod
    def from_file(cls, filepath):
        instance = cls()
        with open(filepath, 'r') as f:
            lines = f.readlines()
            for line in lines:
                origin, dest = line.replace('\n', '').split(')')
                instance.add_edge(origin, dest)
        return instance

    @property
    def graph(self):
        return self.vertices['COM']


if __name__ == '__main__':
    universe_map = UniverseOrbitMap.from_file('./day6input')
    print(universe_map.graph)
    print(universe_map.vertices)

    total_distance = 0

    for vertex in universe_map.vertices.values():
        total_distance += len(vertex.get_all_parents())

    print(total_distance)

    you = universe_map.vertices.get('YOU')
    san = universe_map.vertices.get('SAN')
    print(you.distance_to(san))
    print(san.distance_to(you))
