// Request Handling Module
// Handles all HTTP requests, API calls, and data processing
// between the frontend and Django backend

function sendDataToDjango() {
    let csrftoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    let algorithmSelect = document.getElementById("algorithmSelect");
    let selectedAlgorithm = algorithmSelect ? algorithmSelect.value : 'bfs';

    let sourceNode = document.getElementById("sourceNode").value;
    let destinationNode = document.getElementById("destinationNode").value;

    // Validate selection
    if (!sourceNode || !destinationNode) {
        alert("Please select both source and destination nodes!");
        return;
    }

    if (sourceNode === destinationNode) {
        alert("Source and destination cannot be the same!");
        return;
    }

    let graphData = {
        nodes: nodes.get(),
        edges: edges.get(),
        source: sourceNode,
        destination: destinationNode,
        algorithm: selectedAlgorithm
    };
    
    console.log("Starting algorithm visualization:", graphData);
    
    // Show loading state
    let findPathButton = document.querySelector('button[onclick="sendDataToDjango()"]');
    let originalText = findPathButton.textContent;
    findPathButton.textContent = "Searching...";
    findPathButton.disabled = true;
    
    // Clear previous results and step info
    clearHighlights();
    clearStepInfo();
    
    // Check if we should use SSE visualization
    let useVisualization = document.getElementById("useVisualization").checked;
    
    if (useVisualization) {
        startSSEVisualization(graphData, csrftoken, findPathButton, originalText);
    } else {
        // Use regular fetch for instant results
        startRegularSearch(graphData, csrftoken, findPathButton, originalText);
    }
}

function startSSEVisualization(graphData, csrftoken, findPathButton, originalText) {
    // Send the graph data to get all steps at once
    fetch('/search_sse/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(graphData),
    })
    .then(response => {
        console.log('Response status:', response.status);
        console.log('Response headers:', response.headers);
        
        if (!response.ok) {
            return response.text().then(errorText => {
                console.error('Error response text:', errorText);
                try {
                    const errorData = JSON.parse(errorText);
                    throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
                } catch (parseError) {
                    throw new Error(`HTTP error! status: ${response.status}. Response: ${errorText}`);
                }
            });
        }
        
        return response.text().then(text => {
            console.log('Raw response text:', text);
            try {
                return JSON.parse(text);
            } catch (parseError) {
                console.error('JSON parse error:', parseError);
                console.error('Failed to parse:', text);
                throw new Error(`Invalid JSON response: ${parseError.message}`);
            }
        });
    })
    .then(data => {
        console.log('Received steps:', data);
        
        if (data.error) {
            displayError(data.error);
            resetButton(findPathButton, originalText);
            return;
        }
        
        // Animate the steps
        animateAlgorithmSteps(data.steps, data.result, findPathButton, originalText);
    })
    .catch(error => {
        console.error('Error in visualization:', error);
        
        // Handle specific error types
        if (error.message.includes('Rate limit exceeded') || error.message.includes('429')) {
            displayError('Rate limit exceeded. Please wait a moment before trying again.');
        } else if (error.message.includes('Too many nodes')) {
            displayError('Too many nodes! Please reduce the number of nodes to 20 or fewer for optimal performance.');
        } else if (error.message.includes('Too many edges')) {
            displayError('Too many edges! Please reduce the number of edges to 50 or fewer for optimal performance.');
        } else {
            displayError(error.message);
        }
        
        resetButton(findPathButton, originalText);
    });
}

function animateAlgorithmSteps(steps, finalResult, findPathButton, originalText) {
    let currentStep = 0;
    
    // Show the legend during visualization
    let legend = document.getElementById("visualizationLegend");
    if (legend) {
        legend.style.display = 'block';
    }
    
    function playNextStep() {
        if (currentStep >= steps.length) {
            // Animation complete, show final result
            if (finalResult.success) {
                displaySearchResult(finalResult);
            } else {
                displayError(finalResult.message);
            }
            resetButton(findPathButton, originalText);
            return;
        }
        
        const step = steps[currentStep];
        handleAlgorithmStep(step);
        currentStep++;
        
        // Continue to next step after delay
        setTimeout(playNextStep, 800); // 800ms delay between steps
    }
    
    // Start the animation
    playNextStep();
}

function startRegularSearch(graphData, csrftoken, findPathButton, originalText) {
    // Hide legend for instant results
    let legend = document.getElementById("visualizationLegend");
    if (legend) {
        legend.style.display = 'none';
    }
    
    fetch('/process_graph/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(graphData),
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(errorData => {
                throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
            });
        }
        return response.json();
    })
    .then(responseData => {
        console.log('Response from Django:', responseData);
        displaySearchResult(responseData);
    })
    .catch(error => {
        console.error('Error sending data:', error);
        
        // Handle specific error types
        if (error.message.includes('Rate limit exceeded') || error.message.includes('429')) {
            displayError('Rate limit exceeded. Please wait a moment before trying again.');
        } else if (error.message.includes('Too many nodes')) {
            displayError('Too many nodes! Please reduce the number of nodes to 20 or fewer for optimal performance.');
        } else if (error.message.includes('Too many edges')) {
            displayError('Too many edges! Please reduce the number of edges to 50 or fewer for optimal performance.');
        } else {
            displayError(error.message);
        }
    })
    .finally(() => {
        resetButton(findPathButton, originalText);
    });
}

function resetButton(button, originalText) {
    button.textContent = originalText;
    button.disabled = false;
}

function handleAlgorithmStep(stepData) {
    console.log('Algorithm step:', stepData);
    
    switch (stepData.type) {
        case 'start':
            displayStepInfo(`🚀 Starting ${stepData.algorithm} from ${stepData.source} to ${stepData.destination}`);
            break;
            
        case 'exploring':
            highlightNodeExploring(stepData.node);
            let frontierSize = stepData.frontier_size ? ` | Frontier size: ${stepData.frontier_size}` : '';
            displayStepInfo(`🔍 Step ${stepData.step}: Exploring node "${stepData.node}" (${stepData.algorithm})${frontierSize}`);
            break;
            
        case 'added_to_frontier':
            highlightNodeInFrontier(stepData.node);
            let costInfo = stepData.cost ? ` (Cost: ${stepData.cost.toFixed(2)})` : '';
            displayStepInfo(`➕ Step ${stepData.step}: Added "${stepData.node}" to frontier from "${stepData.parent}"${costInfo}`);
            break;
            
        case 'found':
            highlightNodeFound(stepData.node);
            displayStepInfo(`🎯 Step ${stepData.step}: Found goal "${stepData.node}"!`);
            break;
            
        case 'local_optimum':
            highlightNodeExploring(stepData.node);
            displayStepInfo(`🚫 Step ${stepData.step}: Local optimum reached at "${stepData.node}" (Hill Climbing stuck)`);
            break;
            
        case 'move_to_neighbor':
            highlightNodeExploring(stepData.node);
            let heuristicInfo = stepData.heuristic ? ` (Heuristic: ${stepData.heuristic.toFixed(2)})` : '';
            displayStepInfo(`➡️ Step ${stepData.step}: Moving to better neighbor "${stepData.node}"${heuristicInfo}`);
            break;
            
        case 'final_path':
            highlightFinalPath(stepData.path);
            displayFinalResult(stepData);
            break;
            
        case 'no_path':
            displayStepInfo(`❌ No path found using ${stepData.algorithm}`);
            break;
            
        case 'complete':
            if (stepData.result.success) {
                displaySearchResult(stepData.result);
            } else {
                displayError(stepData.result.message);
            }
            break;
            
        case 'error':
            displayError(stepData.message);
            break;
    }
}

function displaySearchResult(result) {
    // Clear only visual highlights, preserve step info
    clearVisualHighlights();
    
    if (result.success) {
        // Add completion message to step info
        displayStepInfo(`🏁 Search completed! Path found with cost ${result.cost.toFixed(2)}`);
        
        // Highlight the path
        highlightPath(result.path);
        
        // Display result information
        displayResultInfo(result);
    } else {
        // Add failure message to step info
        displayStepInfo(`❌ Search completed: ${result.message || result.error || 'No path found'}`);
        displayError(result.message || result.error || 'Search failed');
    }
}
