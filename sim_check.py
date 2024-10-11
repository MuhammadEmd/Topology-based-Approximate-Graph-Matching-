import networkx as nx
import pygraphviz as pgv
import random
import time
from gen_graph_list import gen_graph_list   

def limit_generator(gen, limit):
    
    count = 0
    for item in gen:
        if count >= limit:
            break
        yield item
        count += 1

def limit_generator_by_time(gen, time_limit_ms):
    """
    Wrapper to limit the generator based on a time limit per item.
    
    :param gen: The original generator function.
    :param time_limit_ms: The time limit (in milliseconds) for each iteration.
    :return: A generator that stops if an iteration exceeds the time limit.
    """
    start_time = time.time()  # Record the start time
    for item in gen:
        yield item
        elapsed_time_ms = (time.time() - start_time) * 1000  # Convert to milliseconds
        if elapsed_time_ms > time_limit_ms:
            # print(f"Generation timed out after {elapsed_time_ms:.4f} ms")
            break

def find_distance(g1, g2):
    # DG1 = nx.drawing.nx_agraph.read_dot(g1) #"subGraph/output44.gv"
    # DG2 = nx.drawing.nx_agraph.read_dot(g2) #"subGraph/output64.gv"

    return nx.optimize_graph_edit_distance(g1, g2)#(DG1, DG2)

def comparison(graph, graph_list):
    best_match = float('inf') 
    # best_match_graph = ""
    best_match_graph = None
    cntr = 0
    for graph2 in graph_list:
        limited_gen = limit_generator_by_time(find_distance(graph, graph2), 100)
        print(cntr)
        cntr += 1
        cloeset = float('inf')
        for value in limited_gen:
            if value < cloeset:
                cloeset = value
        print(f'{cloeset=}')
        if cloeset < best_match :
            best_match_graph = graph2
            best_match = cloeset
            print(f'{best_match=}')
    
    return best_match_graph, best_match
        

def main():
    graph_list = gen_graph_list("mul_i8_o8.gv")
    graph = random.choice(graph_list)
    graph_list.remove(graph)

    # print(graph)
    # exit()
    # graph_list = ""
    best_graph_name, best_GED  = comparison(graph, graph_list)
    nx.drawing.nx_agraph.write_dot(graph, "choosen.gv")
    nx.drawing.nx_agraph.write_dot(best_graph_name, "best.gv")
    print(f'{best_GED}')
    print()
    print(f'{best_graph_name}')

if __name__ == "__main__":
    main()