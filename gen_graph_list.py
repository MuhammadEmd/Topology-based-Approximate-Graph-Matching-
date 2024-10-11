import networkx as nx
import pygraphviz as pgv
import random


def find_predecessors(graph, node, depth_now, max_depth):
    # Base case: if depth_now is 0, stop recursion
    if depth_now == 0:
        return {node}, max_depth -1
    
    # Get predecessors of the current node
    predecessors = list(graph.predecessors(node))

    # If no predecessors, stop recursion (dead end)
    if not predecessors:
        return {node}, max_depth - 1
    
    # Recursively find predecessors of current node
    max_depth_through = 0
    result = set()
    for pred in predecessors:
        # Add the predecessor to the set
        result.add(pred)
        # Recursively find predecessors of this predecessor
        node, max_depth_through = find_predecessors(graph, pred, depth_now - 1, max_depth )
        result.update(node)

    if max_depth < max_depth_through:
        max_depth = max_depth_through

    return result, max_depth +1

def gen_sub_graph(graph, depth, name):
    check_mark = True
    iteration = 0
    
    while check_mark == True:
        node = random.choice(list(graph.nodes()))
        sub_DG_nodes, max_depth = find_predecessors(graph, node, depth, 0)
        iteration += 1
        if max_depth == depth:
            sub_DG_nodes.add(node)
            sub_DG = nx.subgraph(graph, sub_DG_nodes)
            nx.drawing.nx_agraph.write_dot(sub_DG, name)
            check_mark = False

        if iteration > 30:
            print("Timeout reached, exiting loop.")
            break

    return sub_DG

def gen_graph_list(sample):
    DG = nx.drawing.nx_agraph.read_dot(sample)#"mul_i8_o8.gv"
    
    sub_graph_list = []

    for i in range(30):
        depth = 3
        sub_graph_list.append(gen_sub_graph(DG, depth, f"./subGraph{depth}/output{i}.gv"))

    return sub_graph_list

if __name__ == "__main__":
    main()