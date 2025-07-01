// Graph Visualization Module
// Handles all visualization-related functionality including node/edge manipulation,
// color updates, highlighting, and visual feedback

// Global variables for visualization
let nodes = new vis.DataSet([]);
let edges = new vis.DataSet([]);
let container = document.getElementById("network");
let data = { nodes: nodes, edges: edges };
let options = { edges: { arrows: "to" } };
let network = new vis.Network(container, data, options);

// Initialize with default graph
function initializeDefaultGraph() {
    // Add default nodes with city names
    const defaultNodes = [
        { id: 1, label: 'New York', color: { background: '#e1f5fe' } },
        { id: 2, label: 'Philadelphia', color: { background: '#f3e5f5' } },
        { id: 3, label: 'Boston', color: { background: '#e8f5e8' } },
        { id: 4, label: 'Washington', color: { background: '#fff3e0' } },
        { id: 5, label: 'Chicago', color: { background: '#fce4ec' } },
        { id: 6, label: 'Atlanta', color: { background: '#e0f2f1' } },
        { id: 7, label: 'Miami', color: { background: '#fff8e1' } },
        { id: 8, label: 'Dallas', color: { background: '#f1f8e9' } }
    ];
    
    // Add default edges with weights (representing distances in hundreds of miles)
    const defaultEdges = [
        { from: 1, to: 2, label: '1' },    // New York to Philadelphia
        { from: 1, to: 3, label: '2' },    // New York to Boston
        { from: 2, to: 4, label: '1' },    // Philadelphia to Washington
        { from: 2, to: 5, label: '8' },    // Philadelphia to Chicago
        { from: 3, to: 5, label: '10' },   // Boston to Chicago
        { from: 4, to: 6, label: '4' },    // Washington to Atlanta
        { from: 4, to: 5, label: '7' },    // Washington to Chicago
        { from: 5, to: 8, label: '9' },    // Chicago to Dallas
        { from: 6, to: 7, label: '7' },    // Atlanta to Miami
        { from: 6, to: 8, label: '8' },    // Atlanta to Dallas
        { from: 7, to: 8, label: '13' }    // Miami to Dallas
    ];
    
    // Add nodes and edges to the datasets
    nodes.add(defaultNodes);
    edges.add(defaultEdges);
    
    // Update dropdowns
    updateDropdowns();
    
    // Set default source and destination
    setTimeout(() => {
        document.getElementById("sourceNode").value = "1";
        document.getElementById("destinationNode").value = "6";
    }, 100);
    
    console.log("Default graph initialized with sample pathfinding scenario");
}

// Initialize the default graph when the page loads
document.addEventListener('DOMContentLoaded', function() {
    initializeDefaultGraph();
});

// Tree Visualization Functions
function generateTreeStructure(graphNodes, graphEdges) {
    if (!graphNodes || graphNodes.length === 0) {
        return null;
    }
    
    // Build adjacency list
    const adjacencyList = {};
    graphNodes.forEach(node => {
        adjacencyList[node.label] = [];
    });
    
    graphEdges.forEach(edge => {
        const fromLabel = graphNodes.find(n => n.id === edge.from)?.label;
        const toLabel = graphNodes.find(n => n.id === edge.to)?.label;
        if (fromLabel && toLabel) {
            adjacencyList[fromLabel].push(toLabel);
            adjacencyList[toLabel].push(fromLabel); // Undirected graph
        }
    });
    
    // Find a root node (preferably the first node or one with most connections)
    const rootNode = graphNodes[0].label;
    
    // Build tree structure using BFS to avoid cycles
    const visited = new Set();
    const tree = { label: rootNode, children: [], level: 0 };
    const queue = [{ node: rootNode, parent: tree, level: 0 }];
    visited.add(rootNode);
    
    while (queue.length > 0) {
        const { node, parent, level } = queue.shift();
        
        adjacencyList[node].forEach(neighbor => {
            if (!visited.has(neighbor)) {
                visited.add(neighbor);
                const childNode = { label: neighbor, children: [], level: level + 1 };
                parent.children.push(childNode);
                queue.push({ node: neighbor, parent: childNode, level: level + 1 });
            }
        });
    }
    
    return tree;
}

function renderTreeView(tree) {
    const treeContent = document.getElementById('treeContent');
    if (!tree) {
        treeContent.innerHTML = '<p class="tree-placeholder">Add nodes and edges to see the tree structure</p>';
        return;
    }
    
    let html = '';
    
    function renderNode(node, isRoot = false) {
        const levelClass = node.level <= 5 ? `tree-level-${node.level}` : 'tree-level-5';
        const rootClass = isRoot ? 'root' : '';
        const prefix = '├─ ';
        const displayLabel = isRoot ? `🌲 ${node.label} (Root)` : `${prefix}${node.label}`;
        
        html += `<div class="tree-node ${levelClass} ${rootClass}" data-node="${node.label}">
            ${displayLabel}
        </div>`;
        
        node.children.forEach(child => renderNode(child));
    }
    
    renderNode(tree, true);
    treeContent.innerHTML = html;
}

function highlightTreeNode(nodeLabel, className = 'highlighted') {
    // Remove previous highlights
    document.querySelectorAll('.tree-node').forEach(node => {
        node.classList.remove('highlighted', 'exploring');
    });
    
    // Add new highlight
    const treeNode = document.querySelector(`.tree-node[data-node="${nodeLabel}"]`);
    if (treeNode) {
        treeNode.classList.add(className);
        // Scroll into view
        treeNode.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

function updateTreeView() {
    const currentNodes = nodes.get();
    const currentEdges = edges.get();
    const tree = generateTreeStructure(currentNodes, currentEdges);
    renderTreeView(tree);
}

// Toggle functionality
function setupVisualizationToggle() {
    const graphViewRadio = document.getElementById('graphView');
    const treeViewRadio = document.getElementById('treeView');
    
    // If toggle elements don't exist, don't try to set up event listeners
    if (!graphViewRadio || !treeViewRadio) {
        console.log("Visualization toggle elements not found, skipping setup");
        return;
    }
    
    const networkDiv = document.getElementById('network');
    const treeDiv = document.getElementById('treeContainer');
    
    function toggleView() {
        if (graphViewRadio.checked) {
            networkDiv.style.display = 'block';
            treeDiv.style.display = 'none';
        } else {
            networkDiv.style.display = 'none';
            treeDiv.style.display = 'block';
            updateTreeView(); // Refresh tree view when switching
        }
    }
    
    graphViewRadio.addEventListener('change', toggleView);
    treeViewRadio.addEventListener('change', toggleView);
    
    // Initial state
    toggleView();
}

// Initialize toggle on page load
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(() => {
        setupVisualizationToggle();
    }, 500);
});

function addNode() {
    // Check node limit before adding
    const MAX_NODES = 20;
    const currentNodeCount = nodes.get().length;
    
    if (currentNodeCount >= MAX_NODES) {
        alert(`Maximum node limit reached! You cannot add more than ${MAX_NODES} nodes for optimal performance and learning experience.`);
        return;
    }
    
    let nodeLabel = document.getElementById("nodeLabel").value;
    if (nodeLabel) {
        // Check if label already exists
        let existingNode = nodes.get().find(node => node.label === nodeLabel);
        if (existingNode) {
            alert("A node with this label already exists!");
            return;
        }
        
        let nodeId = Math.max(...nodes.get().map(n => n.id), 0) + 1;
        nodes.add({ id: nodeId, label: nodeLabel });
        updateDropdowns();
        updateTreeView(); // Update tree view
        document.getElementById("nodeLabel").value = ""; // Clear input after adding
        
        // Show helpful message when approaching limit
        if (currentNodeCount >= MAX_NODES - 3) {
            const remaining = MAX_NODES - currentNodeCount - 1;
            if (remaining > 0) {
                console.log(`Note: You can add ${remaining} more node(s) before reaching the limit of ${MAX_NODES}.`);
            }
        }
    }
}

function addEdge() {
    // Check edge limit before adding
    const MAX_EDGES = 50;
    const currentEdgeCount = edges.get().length;
    
    if (currentEdgeCount >= MAX_EDGES) {
        alert(`Maximum edge limit reached! You cannot add more than ${MAX_EDGES} edges for optimal performance and learning experience.`);
        return;
    }
    
    let fromNode = parseInt(document.getElementById("fromNode").value);
    let toNode = parseInt(document.getElementById("toNode").value);
    let edgeWeight = document.getElementById("edgeWeight").value;

    if (fromNode && toNode && edgeWeight) {
        if (fromNode === toNode) {
            alert("Cannot create an edge from a node to itself!");
            return;
        }
        let existingEdge = edges.get().find(edge =>
            (edge.from === fromNode && edge.to === toNode) ||
            (edge.from === toNode && edge.to === fromNode)
        );

        if (!existingEdge) {
            edges.add({ from: fromNode, to: toNode, label: edgeWeight });
            updateTreeView(); // Update tree view
            document.getElementById("edgeWeight").value = ""; // Clear input after adding
            
            // Show helpful message when approaching limit
            if (currentEdgeCount >= MAX_EDGES - 5) {
                const remaining = MAX_EDGES - currentEdgeCount - 1;
                if (remaining > 0) {
                    console.log(`Note: You can add ${remaining} more edge(s) before reaching the limit of ${MAX_EDGES}.`);
                }
            }
        } else {
            alert("Edge already exists!");
        }
    }
}

function updateDropdowns() {
    let dropdowns = ["fromNode", "toNode", "sourceNode", "destinationNode"];
    dropdowns.forEach(id => {
        let select = document.getElementById(id);
        select.innerHTML = "";
        nodes.forEach(node => {
            let option = document.createElement("option");
            option.value = node.id;
            option.text = node.label;
            select.appendChild(option);
        });
    });
}

function highlightNodeExploring(nodeLabel) {
    // First, mark previous exploring nodes as explored (red)
    markPreviousExploredNodes();
    // Then highlight current node as exploring (yellow)
    updateNodeColor(nodeLabel, '#ffeb3b', '#f57f17'); // Yellow - currently exploring
}

function markPreviousExploredNodes() {
    // Mark all currently yellow nodes as red (explored but not in final path)
    let updatedNodes = nodes.get().map(node => {
        if (node.color && node.color.background === '#ffeb3b') {
            return { ...node, color: { background: '#f44336', border: '#c62828' } }; // Red - explored/rejected
        }
        return node;
    });
    nodes.update(updatedNodes);
}

function highlightNodeInFrontier(nodeLabel) {
    updateNodeColor(nodeLabel, '#ff9800', '#e65100'); // Orange - in frontier
}

function highlightNodeFound(nodeLabel) {
    updateNodeColor(nodeLabel, '#4caf50', '#1b5e20'); // Green - goal found
}

function highlightFinalPath(path) {
    // Clear all previous colors but preserve step info
    clearVisualHighlights();
    
    // Get node labels to ID mapping
    let nodeMap = {};
    nodes.forEach(node => {
        nodeMap[node.label] = node.id;
    });
    
    // Highlight path nodes in green
    let pathNodeIds = path.map(label => nodeMap[label]).filter(id => id !== undefined);
    
    let updatedNodes = nodes.get().map(node => {
        if (pathNodeIds.includes(node.id)) {
            return { ...node, color: { background: '#90EE90', border: '#228B22' } };
        }
        return node;
    });
    nodes.update(updatedNodes);
    
    // Highlight path edges in green
    let pathEdges = [];
    for (let i = 0; i < path.length - 1; i++) {
        let fromId = nodeMap[path[i]];
        let toId = nodeMap[path[i + 1]];
        
        let edge = edges.get().find(e => 
            (e.from === fromId && e.to === toId) || 
            (e.from === toId && e.to === fromId)
        );
        
        if (edge) {
            pathEdges.push(edge.id);
        }
    }
    
    let updatedEdges = edges.get().map(edge => {
        if (pathEdges.includes(edge.id)) {
            return { ...edge, color: { color: '#228B22' }, width: 4 };
        }
        return edge;
    });
    edges.update(updatedEdges);
}

function updateNodeColor(nodeLabel, backgroundColor, borderColor) {
    let nodeMap = {};
    nodes.forEach(node => {
        nodeMap[node.label] = node.id;
    });
    
    let nodeId = nodeMap[nodeLabel];
    if (nodeId) {
        let node = nodes.get(nodeId);
        if (node) {
            nodes.update({
                ...node,
                color: { background: backgroundColor, border: borderColor }
            });
        }
    }
}

function highlightPath(path) {
    if (!path || path.length < 2) return;
    
    // Get node labels to ID mapping
    let nodeMap = {};
    nodes.forEach(node => {
        nodeMap[node.label] = node.id;
    });
    
    // Highlight nodes in the path
    let pathNodeIds = path.map(label => nodeMap[label]).filter(id => id !== undefined);
    
    // Update nodes with highlighting
    let updatedNodes = nodes.get().map(node => {
        if (pathNodeIds.includes(node.id)) {
            return { ...node, color: { background: '#90EE90', border: '#228B22' } };
        }
        return { ...node, color: undefined };
    });
    nodes.update(updatedNodes);
    
    // Highlight edges in the path
    let pathEdges = [];
    for (let i = 0; i < path.length - 1; i++) {
        let fromId = nodeMap[path[i]];
        let toId = nodeMap[path[i + 1]];
        
        // Find the edge between these nodes
        let edge = edges.get().find(e => 
            (e.from === fromId && e.to === toId) || 
            (e.from === toId && e.to === fromId)
        );
        
        if (edge) {
            pathEdges.push(edge.id);
        }
    }
    
    // Update edges with highlighting
    let updatedEdges = edges.get().map(edge => {
        if (pathEdges.includes(edge.id)) {
            return { ...edge, color: { color: '#228B22' }, width: 3 };
        }
        return { ...edge, color: undefined, width: undefined };
    });
    edges.update(updatedEdges);
}

function clearVisualHighlights() {
    // Reset node colors only
    let updatedNodes = nodes.get().map(node => ({
        ...node, 
        color: undefined
    }));
    nodes.update(updatedNodes);
    
    // Reset edge colors only
    let updatedEdges = edges.get().map(edge => ({
        ...edge, 
        color: undefined, 
        width: undefined
    }));
    edges.update(updatedEdges);
    
    // Clear only result display (not step info)
    let resultDiv = document.getElementById("searchResult");
    if (resultDiv) {
        resultDiv.innerHTML = '';
    }
    
    // Hide legend
    let legend = document.getElementById("visualizationLegend");
    if (legend) {
        legend.style.display = 'none';
    }
}

function clearHighlights() {
    // Reset node colors
    let updatedNodes = nodes.get().map(node => ({
        ...node, 
        color: undefined
    }));
    nodes.update(updatedNodes);
    
    // Reset edge colors
    let updatedEdges = edges.get().map(edge => ({
        ...edge, 
        color: undefined, 
        width: undefined
    }));
    edges.update(updatedEdges);
    
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
    
    // Hide legend
    let legend = document.getElementById("visualizationLegend");
    if (legend) {
        legend.style.display = 'none';
    }
}

function resetToDefaultGraph() {
    // Clear existing graph
    clearHighlights();
    nodes.clear();
    edges.clear();
    
    // Reinitialize with default graph
    initializeDefaultGraph();
    
    // Update tree view
    updateTreeView();
    
    // Clear any previous results
    let resultDiv = document.getElementById("searchResult");
    if (resultDiv) {
        resultDiv.innerHTML = '';
    }
    
    console.log("Graph reset to default state");
}

function clearAllGraph() {
    // Clear everything
    clearHighlights();
    nodes.clear();
    edges.clear();
    updateDropdowns();
    
    // Update tree view
    updateTreeView();
    
    // Clear any previous results
    let resultDiv = document.getElementById("searchResult");
    if (resultDiv) {
        resultDiv.innerHTML = '';
    }
    
    console.log("All graph data cleared");
}
