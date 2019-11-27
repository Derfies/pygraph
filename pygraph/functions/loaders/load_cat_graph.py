from ...classes import DirectedGraph, UndirectedGraph


def load_cat_graph(file_path):
    """
    Reads in a graph from file fileName. File-format is supposed to be from old 
    CATBOX++ (*.cat)

    """
    def _read_cat_line(line):
        split_line = filter(None, line.strip().split(';'))
        return {
            key_value.split(':')[0].strip(): key_value.split(':')[1].strip()
            for key_value in split_line
        }

    graph = None
    
    with open(file_path, 'r') as f:
        line_id = 1
        first_vert_line = -1
        last_vert_line = -1
        first_edge_line = -1
        last_edge_line = -1
        done = False
        while not done:

            line = f.readline()
            if not line:
                break

            if line_id == 2:
                graph_data = _read_cat_line(line)
                cls = DirectedGraph if int(graph_data['dir']) else UndirectedGraph
                graph = cls()

            if line_id == 5:
                num_verts = int(_read_cat_line(line)['vertices'])
                first_vert_line = line_id + 1
                last_vert_line = line_id + num_verts

            if first_vert_line <= line_id <= last_vert_line:
                node_id = graph.new_node()
                node_data = _read_cat_line(line)
                node_data.pop('n')
                graph.nodes[node_id]['data'] = node_data

            if line_id == last_vert_line + 1:
                num_edges = int(_read_cat_line(line)['edges'])
                first_edge_line = line_id + 1
                last_edge_line = line_id + num_edges

            if first_edge_line <= line_id <= last_edge_line:
                edge_data = _read_cat_line(line)
                h = int(edge_data['h'])
                t = int(edge_data['t'])
                w = float(edge_data['w'])   # Only supports single weight value.
                edge_id = graph.new_edge(h, t, w)

            line_id += 1

    return graph