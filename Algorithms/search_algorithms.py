"""
Unified search algorithms module for the Django web interface.
This module adapts the original algorithms to work with the graph data from the web interface
and provides step-by-step visualization support.
"""

from queue import Queue
import heapq
from typing import Dict, List, Tuple, Optional, Any, Callable
import time


class Node:
    """Node class for search algorithms"""
    def __init__(self, state: str, parent=None, action=None, path_cost: float = 0):
        self.state = state
        self.action = action
        self.parent = parent
        self.path_cost = path_cost
        
    def __lt__(self, other):
        return self.path_cost < other.path_cost


class GraphProblem:
    """Problem class that adapts web interface graph data for search algorithms"""
    
    def __init__(self, graph_data: Dict, start: str, end: str, heuristic: Dict = None):
        self.start = start
        self.end = end
        self.heuristic = heuristic if heuristic else {}
        
        # Convert web interface graph data to algorithm-compatible format
        self.graph = self._convert_graph_data(graph_data)
        
    def _convert_graph_data(self, graph_data: Dict) -> Dict:
        """Convert graph data from web interface to algorithm format"""
        nodes = graph_data.get('nodes', [])
        edges = graph_data.get('edges', [])
        
        # Create a mapping from node IDs to labels
        node_map = {node['id']: node['label'] for node in nodes}
        
        # Build adjacency list
        graph = {node['label']: [] for node in nodes}
        
        for edge in edges:
            from_label = node_map[edge['from']]
            to_label = node_map[edge['to']]
            weight = float(edge['label']) if edge['label'] else 1.0
            
            # Add edge in both directions (undirected graph)
            graph[from_label].append((to_label, weight))
            graph[to_label].append((from_label, weight))
            
        return graph
        
    def is_goal(self, state: str) -> bool:
        return state == self.end
        
    def get_neighbors(self, state: str) -> List[str]:
        """Get neighbors for simple algorithms (BFS, DFS)"""
        return [neighbor[0] for neighbor in self.graph.get(state, [])]
        
    def get_actions(self, state: str) -> List[Tuple[str, float]]:
        """Get actions with costs for informed search"""
        return self.graph.get(state, [])
        
    def action_cost(self, state: str, action: Tuple[str, float]) -> float:
        """Get the cost of an action"""
        return action[1]
        
    def heuristic_cost(self, state: str) -> float:
        """Get heuristic cost (for informed search)"""
        return self.heuristic.get(state, 0)


def breadth_first_search(problem: GraphProblem, step_callback: Callable = None) -> Optional[Node]:
    """Breadth-First Search algorithm with step-by-step visualization"""
    node = Node(state=problem.start)
    if problem.is_goal(node.state):
        return node
    
    frontier = Queue()
    reached = {problem.start}
    frontier.put(node)
    
    step_count = 0
    
    while not frontier.empty():
        node = frontier.get()
        step_count += 1
        
        # Send exploration step
        if step_callback:
            step_callback({
                'type': 'exploring',
                'node': node.state,
                'step': step_count,
                'algorithm': 'BFS',
                'frontier_size': frontier.qsize()
            })
        
        for action in problem.get_actions(node.state):
            neighbor, cost = action
            if neighbor not in reached:
                child_cost = node.path_cost + cost
                child = Node(state=neighbor, parent=node, action=action, path_cost=child_cost)
                
                if problem.is_goal(child.state):
                    # Send success step
                    if step_callback:
                        step_callback({
                            'type': 'found',
                            'node': child.state,
                            'step': step_count + 1,
                            'algorithm': 'BFS'
                        })
                    return child
                    
                reached.add(neighbor)
                frontier.put(child)
                
                # Send added to frontier step
                if step_callback:
                    step_callback({
                        'type': 'added_to_frontier',
                        'node': neighbor,
                        'step': step_count,
                        'parent': node.state,
                        'algorithm': 'BFS',
                        'cost': child_cost
                    })
    
    return None


def depth_first_search(problem: GraphProblem, step_callback: Callable = None) -> Optional[Node]:
    """Depth-First Search algorithm with step-by-step visualization"""
    node = Node(state=problem.start)
    if problem.is_goal(node.state):
        return node
    
    frontier = []
    reached = {problem.start}
    frontier.append(node)
    
    step_count = 0
    
    while frontier:
        node = frontier.pop()
        step_count += 1
        
        # Send exploration step
        if step_callback:
            step_callback({
                'type': 'exploring',
                'node': node.state,
                'step': step_count,
                'algorithm': 'DFS',
                'frontier_size': len(frontier)
            })
        
        for action in problem.get_actions(node.state):
            neighbor, cost = action
            if neighbor not in reached:
                child_cost = node.path_cost + cost
                child = Node(state=neighbor, parent=node, action=action, path_cost=child_cost)
                
                if problem.is_goal(child.state):
                    # Send success step
                    if step_callback:
                        step_callback({
                            'type': 'found',
                            'node': child.state,
                            'step': step_count + 1,
                            'algorithm': 'DFS'
                        })
                    return child
                    
                reached.add(neighbor)
                frontier.append(child)
                
                # Send added to frontier step
                if step_callback:
                    step_callback({
                        'type': 'added_to_frontier',
                        'node': neighbor,
                        'step': step_count,
                        'parent': node.state,
                        'algorithm': 'DFS',
                        'cost': child_cost
                    })
    
    return None


def dijkstra_search(problem: GraphProblem, step_callback: Callable = None) -> Optional[Node]:
    """Dijkstra's algorithm for shortest path with step-by-step visualization"""
    node = Node(problem.start, path_cost=0)
    frontier = []
    heapq.heappush(frontier, node)
    reached = {problem.start: 0}
    
    step_count = 0
    
    while frontier:
        node = heapq.heappop(frontier)
        step_count += 1
        
        # Send exploration step
        if step_callback:
            step_callback({
                'type': 'exploring',
                'node': node.state,
                'step': step_count,
                'cost': node.path_cost,
                'algorithm': 'Dijkstra',
                'frontier_size': len(frontier)
            })
        
        if problem.is_goal(node.state):
            # Send success step
            if step_callback:
                step_callback({
                    'type': 'found',
                    'node': node.state,
                    'step': step_count,
                    'cost': node.path_cost,
                    'algorithm': 'Dijkstra'
                })
            return node
            
        for action in problem.get_actions(node.state):
            child_state = action[0]
            child_cost = node.path_cost + problem.action_cost(node.state, action)
            
            if child_state not in reached or child_cost < reached[child_state]:
                reached[child_state] = child_cost
                child = Node(state=child_state, parent=node, action=action, path_cost=child_cost)
                heapq.heappush(frontier, child)
                
                # Send added to frontier step
                if step_callback:
                    step_callback({
                        'type': 'added_to_frontier',
                        'node': child_state,
                        'step': step_count,
                        'parent': node.state,
                        'cost': child_cost,
                        'algorithm': 'Dijkstra'
                    })
    
    return None


def best_first_search(problem: GraphProblem, step_callback: Callable = None) -> Optional[Node]:
    """Best-First Search algorithm with step-by-step visualization"""
    node = Node(problem.start, path_cost=problem.heuristic_cost(problem.start))
    frontier = []
    heapq.heappush(frontier, node)
    reached = {problem.start: node.path_cost}
    
    step_count = 0
    
    while frontier:
        node = heapq.heappop(frontier)
        step_count += 1
        
        # Send exploration step
        if step_callback:
            step_callback({
                'type': 'exploring',
                'node': node.state,
                'step': step_count,
                'cost': node.path_cost,
                'algorithm': 'Best-First',
                'frontier_size': len(frontier)
            })
        
        if problem.is_goal(node.state):
            # Send success step
            if step_callback:
                step_callback({
                    'type': 'found',
                    'node': node.state,
                    'step': step_count,
                    'cost': node.path_cost,
                    'algorithm': 'Best-First'
                })
            return node
            
        for action in problem.get_actions(node.state):
            child_state = action[0]
            child_cost = (node.path_cost - problem.heuristic_cost(node.state) + 
                         problem.action_cost(node.state, action) + 
                         problem.heuristic_cost(child_state))
            
            if child_state not in reached or child_cost < reached[child_state]:
                reached[child_state] = child_cost
                child = Node(state=child_state, parent=node, action=action, path_cost=child_cost)
                heapq.heappush(frontier, child)
                
                # Send added to frontier step
                if step_callback:
                    step_callback({
                        'type': 'added_to_frontier',
                        'node': child_state,
                        'step': step_count,
                        'parent': node.state,
                        'cost': child_cost,
                        'algorithm': 'Best-First'
                    })
    
    return None


def a_star_search(problem: GraphProblem, step_callback: Callable = None) -> Optional[Node]:
    """A* Search algorithm with step-by-step visualization"""
    node = Node(problem.start, path_cost=0)
    # For A*, the priority is f(n) = g(n) + h(n)
    node.f_cost = node.path_cost + problem.heuristic_cost(problem.start)
    frontier = []
    heapq.heappush(frontier, (node.f_cost, node))
    reached = {problem.start: node.path_cost}
    
    step_count = 0
    
    while frontier:
        f_cost, node = heapq.heappop(frontier)
        step_count += 1
        
        # Send exploration step
        if step_callback:
            step_callback({
                'type': 'exploring',
                'node': node.state,
                'step': step_count,
                'g_cost': node.path_cost,
                'h_cost': problem.heuristic_cost(node.state),
                'f_cost': f_cost,
                'algorithm': 'A*',
                'frontier_size': len(frontier)
            })
        
        if problem.is_goal(node.state):
            # Send success step
            if step_callback:
                step_callback({
                    'type': 'found',
                    'node': node.state,
                    'step': step_count,
                    'g_cost': node.path_cost,
                    'f_cost': f_cost,
                    'algorithm': 'A*'
                })
            return node
            
        for action in problem.get_actions(node.state):
            child_state = action[0]
            child_g_cost = node.path_cost + problem.action_cost(node.state, action)
            child_h_cost = problem.heuristic_cost(child_state)
            child_f_cost = child_g_cost + child_h_cost
            
            if child_state not in reached or child_g_cost < reached[child_state]:
                reached[child_state] = child_g_cost
                child = Node(state=child_state, parent=node, action=action, path_cost=child_g_cost)
                child.f_cost = child_f_cost
                heapq.heappush(frontier, (child_f_cost, child))
                
                # Send added to frontier step
                if step_callback:
                    step_callback({
                        'type': 'added_to_frontier',
                        'node': child_state,
                        'step': step_count,
                        'parent': node.state,
                        'g_cost': child_g_cost,
                        'h_cost': child_h_cost,
                        'f_cost': child_f_cost,
                        'algorithm': 'A*'
                    })
    
    return None


def hill_climbing_search(problem: GraphProblem, step_callback: Callable = None) -> Optional[Node]:
    """Hill Climbing Search algorithm with step-by-step visualization"""
    current = Node(problem.start, path_cost=0)
    step_count = 0
    visited = set()  # Track visited nodes to prevent infinite loops
    max_steps = 100  # Safety limit to prevent infinite loops
    
    while step_count < max_steps:
        step_count += 1
        visited.add(current.state)
        
        # Send exploration step
        if step_callback:
            heuristic_value = problem.heuristic_cost(current.state)
            step_callback({
                'type': 'exploring',
                'node': current.state,
                'step': step_count,
                'heuristic': float(heuristic_value) if heuristic_value is not None else 0.0,
                'algorithm': 'Hill Climbing'
            })
        
        if problem.is_goal(current.state):
            # Send success step
            if step_callback:
                heuristic_value = problem.heuristic_cost(current.state)
                step_callback({
                    'type': 'found',
                    'node': current.state,
                    'step': step_count,
                    'heuristic': float(heuristic_value) if heuristic_value is not None else 0.0,
                    'algorithm': 'Hill Climbing'
                })
            return current
        
        # Find the best neighbor that hasn't been visited
        neighbors = []
        for action in problem.get_actions(current.state):
            neighbor_state = action[0]
            if neighbor_state not in visited:  # Only consider unvisited neighbors
                neighbor_heuristic = problem.heuristic_cost(neighbor_state)
                neighbor_cost = current.path_cost + problem.action_cost(current.state, action)
                neighbors.append((neighbor_heuristic, neighbor_state, action, neighbor_cost))
        
        if not neighbors:
            # No unvisited neighbors available
            if step_callback:
                step_callback({
                    'type': 'no_path',
                    'node': current.state,
                    'step': step_count,
                    'algorithm': 'Hill Climbing',
                    'reason': 'No unvisited neighbors available'
                })
            return None
        
        # Sort by heuristic value (lower is better for goal-seeking)
        neighbors.sort(key=lambda x: x[0])
        best_heuristic, best_neighbor, best_action, best_cost = neighbors[0]
        
        # If no neighbor is better than current, we're stuck (local optimum)
        if best_heuristic >= problem.heuristic_cost(current.state):
            if step_callback:
                current_heuristic = problem.heuristic_cost(current.state)
                step_callback({
                    'type': 'local_optimum',
                    'node': current.state,
                    'step': step_count,
                    'heuristic': float(current_heuristic) if current_heuristic is not None else 0.0,
                    'algorithm': 'Hill Climbing',
                    'reason': 'Local optimum reached - no better neighbors'
                })
            return None
        
        # Move to the best neighbor
        current = Node(state=best_neighbor, parent=current, action=best_action, path_cost=best_cost)
        
        if step_callback:
            step_callback({
                'type': 'move_to_neighbor',
                'node': best_neighbor,
                'step': step_count,
                'parent': current.parent.state if current.parent else None,
                'heuristic': float(best_heuristic) if best_heuristic is not None else 0.0,
                'algorithm': 'Hill Climbing'
            })
    
    # If we reach here, we've exceeded max steps
    if step_callback:
        step_callback({
            'type': 'no_path',
            'node': current.state,
            'step': step_count,
            'algorithm': 'Hill Climbing',
            'reason': 'Maximum steps reached'
        })
    return None


def get_path(node: Optional[Node]) -> List[str]:
    """Extract path from solution node"""
    if not node:
        return []
    
    path = []
    current = node
    while current:
        path.append(current.state)
        current = current.parent
    
    return path[::-1]


def get_path_with_costs(node: Optional[Node]) -> Tuple[List[str], float]:
    """Extract path and total cost from solution node"""
    if not node:
        return [], float('inf')
    
    path = get_path(node)
    total_cost = node.path_cost if hasattr(node, 'path_cost') else 0
    
    return path, total_cost


def solve_graph_with_steps(graph_data: Dict, source: str, destination: str, algorithm: str = 'bfs', 
                          heuristic: Dict = None, step_callback: Callable = None) -> Dict:
    """
    Solve graph problems using different algorithms with step-by-step visualization
    
    Args:
        graph_data: Graph data from web interface
        source: Starting node label
        destination: Goal node label
        algorithm: Algorithm to use ('bfs', 'dfs', 'best_first', 'dijkstra')
        heuristic: Heuristic values for informed search (optional)
        step_callback: Function to call for each step of the algorithm
    
    Returns:
        Dictionary with solution path, cost, and algorithm info
    """
    import time
    
    try:
        # Start timing
        start_time = time.time()
        
        # Create problem instance
        problem = GraphProblem(graph_data, source, destination, heuristic)
        
        # Send start step
        if step_callback:
            step_callback({
                'type': 'start',
                'source': source,
                'destination': destination,
                'algorithm': algorithm,
                'step': 0
            })
        
        # Select and run algorithm
        if algorithm.lower() == 'bfs':
            solution = breadth_first_search(problem, step_callback)
            algorithm_name = "Breadth-First Search"
        elif algorithm.lower() == 'dfs':
            solution = depth_first_search(problem, step_callback)
            algorithm_name = "Depth-First Search"
        elif algorithm.lower() == 'best_first':
            solution = best_first_search(problem, step_callback)
            algorithm_name = "Best-First Search"
        elif algorithm.lower() == 'dijkstra':
            solution = dijkstra_search(problem, step_callback)
            algorithm_name = "Dijkstra's Algorithm"
        elif algorithm.lower() == 'a_star':
            solution = a_star_search(problem, step_callback)
            algorithm_name = "A* Search"
        elif algorithm.lower() == 'hill_climbing':
            solution = hill_climbing_search(problem, step_callback)
            algorithm_name = "Hill Climbing Search"
        else:
            return {
                'success': False,
                'error': f"Unknown algorithm: {algorithm}",
                'path': [],
                'cost': float('inf'),
                'algorithm': algorithm
            }
        
        # Extract results
        if solution:
            path, cost = get_path_with_costs(solution)
            end_time = time.time()
            execution_time = end_time - start_time
            
            # Send final path step
            if step_callback:
                step_callback({
                    'type': 'final_path',
                    'path': path,
                    'cost': cost,
                    'algorithm': algorithm_name,
                    'execution_time': execution_time
                })
            
            return {
                'success': True,
                'path': path,
                'cost': cost,
                'algorithm': algorithm_name,
                'nodes_explored': len(path),
                'execution_time': execution_time,
                'message': f"Path found using {algorithm_name}"
            }
        else:
            end_time = time.time()
            execution_time = end_time - start_time
            
            # Send no path found step
            if step_callback:
                step_callback({
                    'type': 'no_path',
                    'algorithm': algorithm_name,
                    'execution_time': execution_time
                })
            
            return {
                'success': False,
                'error': "No path found",
                'path': [],
                'cost': float('inf'),
                'algorithm': algorithm_name,
                'message': f"No path exists between {source} and {destination}"
            }
            
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'path': [],
            'cost': float('inf'),
            'algorithm': algorithm,
            'message': f"Error during search: {str(e)}"
        }


def solve_graph(graph_data: Dict, source: str, destination: str, algorithm: str = 'bfs', heuristic: Dict = None) -> Dict:
    """
    Main function to solve graph problems using different algorithms (legacy version without steps)
    """
    return solve_graph_with_steps(graph_data, source, destination, algorithm, heuristic, None)
