from typing import List, Dict, Tuple, Optional, Callable
class Vertex:
    """
    Represents a vertex in a graph.

    Attributes:
        name (str): The label or identifier of the vertex.
        children (Dict[str, Tuple[str, str, float]]):
            A mapping between child vertex names and edges.
            Each edge is represented as a tuple:
                (source vertex name, child vertex name, edge weight).
    """

    def __init__(self, name: str, children: Optional[Dict[str, Tuple[str, str, float]]] = None):
        """
        Initializes a Vertex.

        Args:
            name (str): The label or identifier of the vertex.
            children (Optional[Dict[str, Tuple[str, str, float]]]):
                A mapping between child vertex names and edges.
        """
        self.name = name
        self.children: Dict[str, Tuple[str, str, float]] = children if children is not None else {}

    def get_children(self) -> List[Tuple[str, str, float]]:
        """
        Returns all edges from this vertex.

        Returns:
            List[Tuple[str, str, float]]: The list of edges from this vertex.
        """
        kids = []
        keys = []
        for key in self.children:
            keys.append(key)
        for i in range(len(self.children)):
            kids.append(self.children[keys[i]])

        return kids

class Graph:
    """
    Represents a graph consisting of multiple vertices.

    Attributes:
        vertices (List[Vertex]): The list of vertices in the graph.
    """

    def __init__(self, vertices: List[Vertex]):
        """
        Initializes a Graph.
        Args:
            vertices (List[Vertex]): The list of vertices that make up the graph.
        """
        self.vertices = vertices

    def get_vertices(self) -> List[Vertex]:
        """
        Returns all vertices in the graph.

        Returns:
            List[Vertex]: The list of vertices in the graph.
        """
        return self.vertices

    def is_child(self, u_name: str, v_name: str) -> bool:
        """
        Checks if vertex v_name is a child of vertex u_name.

        Args:
            u_name (str): The name of the parent vertex.
            v_name (str): The name of the potential child vertex.

        Returns:
            bool: True if the vertex v_name is a child of the vertex u_name, False otherwise.
        """
        kids = []
        for i in range(len(self.vertices)):
            #print(self.get_vertices()[i].name)
            if self.get_vertices()[i].name == u_name:
                kids = self.get_vertices()[i].get_children()
                #print(kids)

                for kid in kids:
                    if kid[1] == v_name:
                        return True
        return False

    def get_edge(self, u_name: str, v_name: str) -> Optional[Tuple[str, str, float]]:
        """
        Retrieves the edge between u_name and v_name.

        Args:
            u_name (str): The name of the parent vertex.
            v_name (str): The name of the child vertex.

        Returns:
            Optional[Tuple[str, str, float]]: The edge if it exists,
            or None if no such edge is found.
        """
        if self.is_child == False:
            return None
        kids = []
        for i in range(len(self.vertices)):
            if self.get_vertices()[i].name == u_name:
                kids = self.get_vertices()[i].get_children()

                for kid in kids:
                    if kid[1] == v_name:
                        return kid

class Device(Vertex):
    """
    Represents a network device, extending the Vertex class with
    device-specific functionality.

    Attributes:
        name (str): The label or identifier of the device.
        children (Dict[str, Tuple[str, str, float]]):
            A mapping between child device names and nearby devices.
        network (Graph): A graph representing this device's discovered network.
    """

    def __init__(self, name: str):
        """
        Initializes a Device.

        Args:
            name (str): The label or identifier of the device.
        """
        self.name = name
        self.children = {}
        self.network = Graph([self])

    def discover_network(self, find_devices_fn: Callable[[List[str]], List[Tuple[str, str, float]]]) -> None:
        """
        Discovers the surrounding network starting from this device. Once this
        function is called, self.network should contain a representation of the
        device's discovered network.

        Args:
            find_devices_fn (Callable[[List[str]], List[Tuple[str, str, float]]]):
                A function that takes an ordered list of device names (i.e., a path)
                and returns the edges from the last device in the path to its immediate children.
        """

        visited = []
        edges = []
        to_visit = [self.name]
        while len(to_visit) > 0:
            current = to_visit[-1]
            print("Now Visiting")
            print(current)
            edges = find_devices_fn([current])
            print(edges)
            to_visit.pop()
            visited.append(current)
            vertex_kids = {}
            for edge in edges:
                if edge[1] not in visited:
                    to_visit.append(edge[1])
                    vertex_kids[edge[1]] = (current, edge[1], edge[2])
            vertex = Vertex(current, vertex_kids)
            self.network.vertices.append(vertex)
            print("Visited")
            print(visited)
            print("To Visit")
            print(to_visit)
            print("\n")


# ----------------------------------------------------------------------
# Mock function for testing
# ----------------------------------------------------------------------
def find_devices_fn(path: List[str]) -> List[Tuple[str, str, float]]:
    """
    A mock function that simulates network discovery.

    Args:
        path (List[str]): The sequence of device names representing the discovery path.

    Returns:
        List[Tuple[str, str, float]]: A list of edges, where each tuple contains:
            - source device name (str),
            - child device name (str),
            - edge weight (float).
    """
    if not path:
        return []

    last_device = path[-1]

    mock_network = {
        "chandra-s25": [
            ("chandra-s25", "router-051797", 1.0),
            ("chandra-s25", "helen-pc", 2.0),
        ],
        "router-051797": [
            ("router-051797", "ws-102", 1.2),
            ("router-051797", "switch-12", 0.8),
            ("router-051797", "srv-07", 1.0),
        ],
        "helen-pc": [
            ("helen-pc", "ws-14", 1.5),
        ],
    }

    return mock_network.get(last_device, [])

def main():
    '''v1_dict = {
        "A": ("S", "A", 4),
        "B": ("S", "B", 8),
    }
    v1 = Vertex("S", v1_dict)
    v2_dict = {
        "B": ("A", "B", 11),
        "C": ("A", "C", 8),
    }
    v2 = Vertex("A", v2_dict)
    print(v1.get_children())
    Graph1 = Graph([v1, v2])
    print(Graph1.get_vertices())
    print(Graph1.is_child("A", "B"))
    print(Graph1.is_child("A", "S"))
    print(Graph1.get_edge("S", "A"))
    print(Graph1.get_edge("A", "S"))
    print(Graph1.get_edge("A", "C"))'''
    dev = Device("chandra-s25")
    dev.discover_network(find_devices_fn)



if __name__ == "__main__":
    main()