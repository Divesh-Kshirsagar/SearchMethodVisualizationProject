from django.shortcuts import render
import json
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse
import asyncio
import random
import sys
import os
import time
from django_ratelimit.decorators import ratelimit
from django.views.decorators.cache import cache_page

# Add the Algorithms directory to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Algorithms'))

from search_algorithms import solve_graph, solve_graph_with_steps

# Configuration constants
MAX_NODES = 20
MAX_EDGES = 50


def index(request):
    return render(request,"Search/index.html")


@ratelimit(key='ip', rate='30/m', method='POST', block=True)
def search_path_sse(request):
    """Server-Sent Events endpoint for real-time algorithm visualization"""
    if request.method != 'POST':
        return HttpResponse(status=405)
    
    try:
        # Parse the JSON data from the request
        data = json.loads(request.body)
        
        # Extract required fields
        nodes = data.get('nodes', [])
        edges = data.get('edges', [])
        source = data.get('source')
        destination = data.get('destination')
        algorithm = data.get('algorithm', 'bfs')
        
        # Validate node and edge limits for performance and security
        if len(nodes) > MAX_NODES:
            return JsonResponse({
                'error': f'Too many nodes! Maximum allowed is {MAX_NODES} nodes for optimal performance. Please reduce the number of nodes.'
            }, status=400)
            
        if len(edges) > MAX_EDGES:
            return JsonResponse({
                'error': f'Too many edges! Maximum allowed is {MAX_EDGES} edges for optimal performance. Please reduce the number of edges.'
            }, status=400)
        
        # Validate required fields
        if not nodes or not edges or not source or not destination:
            return JsonResponse({'error': 'Missing required data'}, status=400)
        
        # Convert node IDs to labels for validation
        node_labels = {str(node['id']): node['label'] for node in nodes}
        source_label = node_labels.get(str(source))
        destination_label = node_labels.get(str(destination))
        
        if not source_label or not destination_label:
            return JsonResponse({'error': 'Invalid source or destination'}, status=400)
        
        # Prepare graph data for algorithms
        graph_data = {
            'nodes': nodes,
            'edges': edges
        }
        
        # Generate heuristics for informed search algorithms
        heuristic = {}
        if algorithm.lower() in ['a_star', 'astar', 'hill_climbing', 'best_first']:
            # Generate simple heuristic values for demo
            destination_id = None
            for node in nodes:
                if node['label'] == destination_label:
                    destination_id = node['id']
                    break
            
            if destination_id:
                for node in nodes:
                    if node['label'] == destination_label:
                        heuristic[node['label']] = 0
                    else:
                        heuristic[node['label']] = random.uniform(1, 10)
                
                if source_label in heuristic:
                    heuristic[source_label] = max(heuristic[source_label], 2)
        
        # Store steps for SSE streaming
        steps = []
        
        # Step callback function to collect steps
        def step_callback(step_data):
            # Ensure all numeric values are JSON serializable
            cleaned_step = {}
            for key, value in step_data.items():
                if isinstance(value, float):
                    # Handle NaN and infinity values
                    if not (value == value):  # NaN check
                        cleaned_step[key] = 0
                    elif value == float('inf'):
                        cleaned_step[key] = 999999
                    elif value == float('-inf'):
                        cleaned_step[key] = -999999
                    else:
                        cleaned_step[key] = round(value, 6)  # Limit precision
                else:
                    cleaned_step[key] = value
            steps.append(cleaned_step)
        
        # Solve the graph using the specified algorithm with steps
        result = solve_graph_with_steps(
            graph_data=graph_data,
            source=source_label,
            destination=destination_label,
            algorithm=algorithm,
            heuristic=heuristic,
            step_callback=step_callback
        )
        
        # Clean the result object for JSON serialization
        def clean_result_for_json(result_data):
            cleaned_result = {}
            for key, value in result_data.items():
                if isinstance(value, float):
                    if not (value == value):  # NaN check
                        cleaned_result[key] = 0
                    elif value == float('inf'):
                        cleaned_result[key] = 999999
                    elif value == float('-inf'):
                        cleaned_result[key] = -999999
                    else:
                        cleaned_result[key] = round(value, 6)
                else:
                    cleaned_result[key] = value
            return cleaned_result
        
        cleaned_result = clean_result_for_json(result)
        
        # Return steps and result for client-side animation
        return JsonResponse({
            'steps': steps,
            'result': cleaned_result
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def ratelimited(request, exception):
    """Rate limit exceeded error handler"""
    return JsonResponse({
        'error': 'Rate limit exceeded. Please wait before making more requests.',
        'status': 'rate_limited'
    }, status=429)


@ratelimit(key='ip', rate='30/m', method='POST', block=True)
def search_path(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request
            data = json.loads(request.body)
            
            # Extract required fields
            nodes = data.get('nodes', [])
            edges = data.get('edges', [])
            source = data.get('source')
            destination = data.get('destination')
            algorithm = data.get('algorithm', 'bfs')  # Default to BFS
            
            # Validate node and edge limits for performance and security
            if len(nodes) > MAX_NODES:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Too many nodes! Maximum allowed is {MAX_NODES} nodes for optimal performance. Please reduce the number of nodes.'
                }, status=400)
                
            if len(edges) > MAX_EDGES:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Too many edges! Maximum allowed is {MAX_EDGES} edges for optimal performance. Please reduce the number of edges.'
                }, status=400)
            
            # Validate required fields
            if not nodes:
                return JsonResponse({
                    'status': 'error', 
                    'message': 'No nodes provided'
                }, status=400)
            
            if not edges:
                return JsonResponse({
                    'status': 'error', 
                    'message': 'No edges provided'
                }, status=400)
            
            if not source or not destination:
                return JsonResponse({
                    'status': 'error', 
                    'message': 'Source and destination must be specified'
                }, status=400)
            
            # Convert node IDs to labels for validation
            node_labels = {str(node['id']): node['label'] for node in nodes}
            source_label = node_labels.get(str(source))
            destination_label = node_labels.get(str(destination))
            
            if not source_label or not destination_label:
                return JsonResponse({
                    'status': 'error', 
                    'message': 'Invalid source or destination node'
                }, status=400)
            
            # Prepare graph data for algorithms
            graph_data = {
                'nodes': nodes,
                'edges': edges
            }
            
            # Optional: Create a simple heuristic (can be enhanced later)
            heuristic = {}
            
            # For A* and Hill Climbing, generate simple heuristics based on node positions or random values
            if algorithm.lower() in ['a_star', 'astar', 'hill_climbing', 'best_first']:
                # Generate simple heuristic values (in practice, this would be distance to goal)
                # For demo purposes, we'll use random values that decrease towards the destination
                destination_id = None
                for node in nodes:
                    if node['label'] == destination_label:
                        destination_id = node['id']
                        break
                
                if destination_id:
                    # Create heuristic values - smaller values for nodes closer to destination
                    for node in nodes:
                        if node['label'] == destination_label:
                            heuristic[node['label']] = 0  # Goal has heuristic 0
                        else:
                            # Simple random heuristic (in practice, use actual distance)
                            heuristic[node['label']] = random.uniform(1, 10)
                    
                    # Ensure source has a reasonable heuristic
                    if source_label in heuristic:
                        heuristic[source_label] = max(heuristic[source_label], 2)
            
            # Solve the graph using the specified algorithm
            result = solve_graph(
                graph_data=graph_data,
                source=source_label,
                destination=destination_label,
                algorithm=algorithm,
                heuristic=heuristic
            )
            
            # Clean the result object for JSON serialization
            def clean_result_for_json(result_data):
                cleaned_result = {}
                for key, value in result_data.items():
                    if isinstance(value, float):
                        if not (value == value):  # NaN check
                            cleaned_result[key] = 0
                        elif value == float('inf'):
                            cleaned_result[key] = 999999
                        elif value == float('-inf'):
                            cleaned_result[key] = -999999
                        else:
                            cleaned_result[key] = round(value, 6)
                    else:
                        cleaned_result[key] = value
                return cleaned_result
            
            cleaned_result = clean_result_for_json(result)
            
            # Return the result
            if cleaned_result['success']:
                return JsonResponse({
                    'status': 'success',
                    'message': cleaned_result['message'],
                    'path': cleaned_result['path'],
                    'cost': cleaned_result['cost'],
                    'algorithm': cleaned_result['algorithm'],
                    'nodes_explored': cleaned_result.get('nodes_explored', 0)
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': cleaned_result['message'],
                    'error': cleaned_result['error'],
                    'algorithm': cleaned_result['algorithm']
                }, status=404)
                
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error', 
                'message': 'Invalid JSON data'
            }, status=400)
        except KeyError as e:
            return JsonResponse({
                'status': 'error', 
                'message': f'Missing key: {str(e)}'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Internal server error: {str(e)}'
            }, status=500)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid request method'
        }, status=405)