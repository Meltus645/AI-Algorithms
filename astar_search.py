import sys
import queue
import heapq

get_filecontent =lambda path: open(path, 'r').read()

def unspervised_search(graph:dict, start:str, goal:str)->'tuple[float, list | None, dict[str, int | list[str]]]':
    nodes =[(0, start, [])]
    route_log =dict(popped =0, expanded =0, generated =1, explored =[])

    while nodes:
        distance, route, path = heapq.heappop(nodes)
        route_log['popped'] +=1

        if route not in route_log['explored']:
            if route == goal:  return distance, path, route_log
            route_log['expanded'] +=1
            route_log['explored'].append(route)

            for neighbor, cost in graph.get(route, {}).items():
                heapq.heappush(nodes, (distance +cost, neighbor, path +[(route, cost)]))
                route_log['generated'] +=1

    return float('inf'), None, route_log

def supervised_search(graph:dict, start:str, goal:str, heuristic_graph:dict)->'tuple[float, list | None, dict[str, int | list[str]]]':
    nodes =queue.PriorityQueue()
    route_log =dict(popped =0, expanded =0, generated =1, explored =[])
    nodes.put((heuristic_graph.get(start, 0), 0, start, []))
    
    while not nodes.empty():
        *_, h_value, route, path = nodes.get()
        route_log['popped'] +=1

        if not route in route_log.get('explored'):
            if route == goal: return h_value, path, route_log
            route_log['explored'].append(route)
            route_log['expanded'] +=1

            neighbors =graph.get(route, {})
            for neighbor, cost in neighbors.items():
                distance =h_value +cost
                if neighbor not in route_log.get('explored'): nodes.put((distance +heuristic_graph.get(neighbor, 0), distance, neighbor, path +[(route, cost)]))
                route_log['generated'] +=1

    return float('inf'), None, route_log
    
def build_routes_graph(src:str, end ='END OF INPUT')->'dict[str, dict[str, float]]':
    
    routes_graph ={}
    try:
        content =src.strip().split('\n')
        content =content[:content.index(end)]
        for line in content:
            frm, to, dst =line.strip().split()
            routes_graph[frm] =routes_graph.get(frm, {})
            routes_graph[to] =routes_graph.get(to, {})
            routes_graph[frm][to] =float(dst)
            routes_graph[to][frm] =float(dst)

    except Exception as e: print(f"Error: {e}")
    return routes_graph

def build_heuristic_graph(src:str, end ='END OF INPUT')->'dict[str, float]':

    heuristic_graph ={}
    try:
        content =src.strip().split('\n')
        content =content[:content.index(end)]
        for line in content:
            city, h_value =line.strip().split()
            heuristic_graph[city] =float(h_value)
    except Exception as e: print(f"Error: {e}")
    return heuristic_graph

def print_search_log(distance:float, path:'list | None', routes_log:'dict[str, int | list]', /)->None:
    
    nodes_popped =str(routes_log.get('popped'))
    nodes_expanded =str(routes_log.get('expanded'))
    nodes_generated =str(routes_log.get('generated'))

    print("Node Popped:", nodes_popped)
    print("Node Expanded:", nodes_expanded)
    print("Node Generated:", nodes_generated)
    print(f"Distance: {str(distance) + ' km' if not distance ==float('inf') else 'infinity'}")
    
    if not path:
        print(path)
        sys.exit(0)

    for i in range(len(path) -1):
        curr_city, curr_dst, *_ =path[i]
        next_city, next_dst, *_ =path[i +1]
        print(f"From {curr_city} to {next_city}, {curr_dst} km")
        if i+1 ==len(path) -1: 
            print(f"From {next_city} to {goal}, {next_dst} km")

def main(input_content_path:str, start:str, goal:str, heuristic_content_path:'str | None')->None:

    input_content =get_filecontent(input_content_path)
    graph =build_routes_graph(input_content)

    if heuristic_content_path: 
        heuristic_content =get_filecontent(heuristic_content_path)
        heuristic_graph =build_heuristic_graph(heuristic_content)
        logs =supervised_search(graph, start, goal, heuristic_graph)
    else: logs =unspervised_search(graph, start, goal)

    print_search_log(*logs)

if __name__ =='__main__':
    args =sys.argv[1:]
    if len(args) <3:
        print("Error: Atleast 3 arguments must be parsed")
        sys.exit(1)

    input_content_path, start, goal, *heuristic_content_path =args
    heuristic_content_path =heuristic_content_path[0] if len(heuristic_content_path) else None
    main(input_content_path, start, goal, heuristic_content_path)