// UI and Styling Module
// Handles all user interface updates, message displays, 
// and visual feedback elements

// Algorithm explanations
function updateAlgorithmExplanation() {
    const algorithmSelect = document.getElementById("algorithmSelect");
    const descriptionElement = document.getElementById("algorithmDescription");
    
    if (!algorithmSelect || !descriptionElement) return;
    
    const selectedAlgorithm = algorithmSelect.value;
    
    const explanations = {
        bfs: "<strong>Breadth-First Search (BFS):</strong> Explores nodes level by level, guaranteeing the shortest path in unweighted graphs. Uses a queue (FIFO) to process nodes in the order they were discovered. Time complexity: O(V + E).",
        
        dfs: "<strong>Depth-First Search (DFS):</strong> Explores as far as possible along each branch before backtracking. Uses a stack (LIFO) or recursion. Does not guarantee the shortest path but uses less memory. Time complexity: O(V + E).",
        
        dijkstra: "<strong>Dijkstra's Algorithm:</strong> Finds the shortest path in weighted graphs with non-negative weights. Uses a priority queue to always explore the node with the smallest distance first. Guarantees optimal solution. Time complexity: O((V + E) log V).",
        
        a_star: "<strong>A* Search:</strong> Combines the benefits of Dijkstra's algorithm and Best-First Search using f(n) = g(n) + h(n). Guarantees optimal solution if heuristic is admissible. More efficient than Dijkstra's when good heuristics are available. Time complexity: O(b^d) where b is branching factor and d is depth.",
        
        best_first: "<strong>Best-First Search:</strong> Uses a heuristic function to guide the search toward the goal. Explores nodes that appear most promising first. May not find the optimal path but can be faster than uninformed searches. Time complexity varies based on heuristic.",
        
        hill_climbing: "<strong>Hill Climbing:</strong> Local search algorithm that moves to the best neighboring state. Terminates when no better neighbor exists (local optimum). Fast but may get stuck in local optima. Does not guarantee optimal or complete solution. Time complexity: O(∞) in worst case."
    };
    
    descriptionElement.innerHTML = explanations[selectedAlgorithm] || explanations.bfs;
}

// Initialize algorithm explanation on page load
document.addEventListener('DOMContentLoaded', function() {
    // Small delay to ensure the dropdown is populated
    setTimeout(updateAlgorithmExplanation, 200);
});

function displayStepInfo(message) {
    let stepInfoDiv = document.getElementById("stepInfo");
    if (!stepInfoDiv) {
        stepInfoDiv = document.createElement("div");
        stepInfoDiv.id = "stepInfo";
        stepInfoDiv.className = "step-info";
        document.body.insertBefore(stepInfoDiv, document.getElementById("searchResult"));
        
        // Add a header for the step info
        const headerElement = document.createElement("div");
        headerElement.className = "step-info-header";
        headerElement.innerHTML = "<strong>Algorithm Steps:</strong>";
        stepInfoDiv.appendChild(headerElement);
    }
    
    // Create a new message element
    const messageElement = document.createElement("p");
    messageElement.innerHTML = `${message}`;
    
    // Add timestamp for better tracking
    const timestamp = new Date().toLocaleTimeString();
    messageElement.innerHTML += ` <span class="timestamp">[${timestamp}]</span>`;
    
    // Append the new message to existing content
    stepInfoDiv.appendChild(messageElement);
    
    // Update step counter in header
    const stepCount = stepInfoDiv.querySelectorAll('p').length;
    const header = stepInfoDiv.querySelector('.step-info-header');
    if (header) {
        header.innerHTML = `<strong>Algorithm Steps (${stepCount}):</strong>`;
    }
    
    // Auto-scroll to the bottom to show latest message
    stepInfoDiv.scrollTop = stepInfoDiv.scrollHeight;
}

function displayFinalResult(stepData) {
    let timeText = '';
    if (stepData.execution_time !== undefined) {
        if (stepData.execution_time < 0.001) {
            timeText = ` (Time: ${(stepData.execution_time * 1000000).toFixed(0)} μs)`;
        } else if (stepData.execution_time < 1) {
            timeText = ` (Time: ${(stepData.execution_time * 1000).toFixed(2)} ms)`;
        } else {
            timeText = ` (Time: ${stepData.execution_time.toFixed(3)} s)`;
        }
    }
    
    displayStepInfo(`Path found: ${stepData.path.join(' → ')} (Cost: ${stepData.cost.toFixed(2)})${timeText}`);
}

function displayError(message) {
    let resultDiv = document.getElementById("searchResult");
    if (!resultDiv) {
        resultDiv = document.createElement("div");
        resultDiv.id = "searchResult";
        document.body.insertBefore(resultDiv, document.getElementById("network"));
    }
    
    resultDiv.innerHTML = `
        <div class="error-message">
            <strong>Error:</strong> ${message}
        </div>
    `;
}

function displayResultInfo(result) {
    let resultDiv = document.getElementById("searchResult");
    if (!resultDiv) {
        resultDiv = document.createElement("div");
        resultDiv.id = "searchResult";
        document.body.insertBefore(resultDiv, document.getElementById("network"));
    }
    
    // Format execution time
    let executionTimeText = '';
    if (result.execution_time !== undefined) {
        if (result.execution_time < 0.001) {
            executionTimeText = `<p><strong>Execution Time:</strong> ${(result.execution_time * 1000000).toFixed(0)} μs</p>`;
        } else if (result.execution_time < 1) {
            executionTimeText = `<p><strong>Execution Time:</strong> ${(result.execution_time * 1000).toFixed(2)} ms</p>`;
        } else {
            executionTimeText = `<p><strong>Execution Time:</strong> ${result.execution_time.toFixed(3)} s</p>`;
        }
    }
    
    resultDiv.innerHTML = `
        <div class="success-message">
            <h3>Path Found!</h3>
            <p><strong>Algorithm:</strong> ${result.algorithm}</p>
            <p><strong>Path:</strong> ${result.path.join(' → ')}</p>
            <p><strong>Total Cost:</strong> ${result.cost.toFixed(2)}</p>
            <p><strong>Nodes Explored:</strong> ${result.nodes_explored}</p>
            ${executionTimeText}
        </div>
    `;
}

// Utility functions for UI management
function showLoadingState(buttonElement, loadingText = "Searching...") {
    if (buttonElement) {
        buttonElement.originalText = buttonElement.textContent;
        buttonElement.textContent = loadingText;
        buttonElement.disabled = true;
    }
}

function hideLoadingState(buttonElement) {
    if (buttonElement && buttonElement.originalText) {
        buttonElement.textContent = buttonElement.originalText;
        buttonElement.disabled = false;
        delete buttonElement.originalText;
    }
}

function clearAllMessages() {
    // Clear result display
    let resultDiv = document.getElementById("searchResult");
    if (resultDiv) {
        resultDiv.innerHTML = '';
    }
    
    // Clear step info
    let stepInfoDiv = document.getElementById("stepInfo");
    if (stepInfoDiv) {
        stepInfoDiv.innerHTML = '';
    }
}

function clearStepInfo() {
    // Clear only step info messages
    let stepInfoDiv = document.getElementById("stepInfo");
    if (stepInfoDiv) {
        stepInfoDiv.innerHTML = '';
    }
}

function showVisualizationLegend() {
    let legend = document.getElementById("visualizationLegend");
    if (legend) {
        legend.style.display = 'block';
    }
}

function hideVisualizationLegend() {
    let legend = document.getElementById("visualizationLegend");
    if (legend) {
        legend.style.display = 'none';
    }
}

// Form validation and user feedback
function validateGraphInput() {
    const nodes = window.nodes ? window.nodes.get() : [];
    const edges = window.edges ? window.edges.get() : [];
    
    if (nodes.length === 0) {
        displayError("Please add at least one node to the graph.");
        return false;
    }
    
    if (nodes.length === 1) {
        displayError("Please add at least two nodes to create a meaningful graph.");
        return false;
    }
    
    return true;
}

function showSuccessMessage(message, duration = 3000) {
    // Create a temporary success message
    let successDiv = document.createElement("div");
    successDiv.className = "success-notification";
    successDiv.innerHTML = `
        <div class="success-message">
            ${message}
        </div>
    `;
    successDiv.style.position = "fixed";
    successDiv.style.top = "20px";
    successDiv.style.right = "20px";
    successDiv.style.zIndex = "1000";
    successDiv.style.padding = "10px";
    successDiv.style.borderRadius = "4px";
    successDiv.style.maxWidth = "300px";
    
    document.body.appendChild(successDiv);
    
    // Auto-remove after duration
    setTimeout(() => {
        if (successDiv.parentNode) {
            successDiv.parentNode.removeChild(successDiv);
        }
    }, duration);
}

function showErrorMessage(message, duration = 5000) {
    // Create a temporary error message
    let errorDiv = document.createElement("div");
    errorDiv.className = "error-notification";
    errorDiv.innerHTML = `
        <div class="error-message">
            <strong>Error:</strong> ${message}
        </div>
    `;
    errorDiv.style.position = "fixed";
    errorDiv.style.top = "20px";
    errorDiv.style.right = "20px";
    errorDiv.style.zIndex = "1000";
    errorDiv.style.padding = "10px";
    errorDiv.style.borderRadius = "4px";
    errorDiv.style.maxWidth = "300px";
    
    document.body.appendChild(errorDiv);
    
    // Auto-remove after duration
    setTimeout(() => {
        if (errorDiv.parentNode) {
            errorDiv.parentNode.removeChild(errorDiv);
        }
    }, duration);
}
