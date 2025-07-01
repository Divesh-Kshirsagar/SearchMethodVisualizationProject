# 🚀 Search Method Showcase

A Django web application that demonstrates various graph search algorithms with an interactive visualization interface. Built for educational purposes to help students and developers understand how different pathfinding algorithms work.

[![Django](https://img.shields.io/badge/Django-5.1.6-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

## 🎯 Features

### 🔍 **Comprehensive Search Algorithms**
- **Breadth-First Search (BFS)** - Level-by-level exploration, guarantees shortest path in unweighted graphs
- **Depth-First Search (DFS)** - Deep exploration along branches before backtracking
- **Dijkstra's Algorithm** - Optimal pathfinding in weighted graphs using actual edge costs
- **A* Search** - Intelligent pathfinding using heuristics for faster optimal solutions
- **Best-First Search** - Greedy approach using heuristic guidance
- **Hill Climbing** - Local search optimization algorithm

### 🎨 **Interactive Visualization Interface**
- **Dual View Modes**: Switch between **Graph View** 📊 and **Tree View** 🌳
- **Real-time Graph Editor**: Add nodes and edges with custom labels and weights
- **Step-by-Step Visualization**: Watch algorithms explore nodes with color-coded progress
- **Interactive Controls**: Toggle visualization modes, clear paths, reset graphs
- **City-Based Examples**: Pre-loaded with realistic city networks and distances

### 🛡️ **Performance & Safety Features**
- **Smart Limits**: Maximum 20 nodes and 50 edges for optimal performance
- **Rate Limiting**: 30 requests per minute per IP to prevent abuse
- **Input Validation**: Comprehensive frontend and backend validation
- **Error Handling**: User-friendly error messages and graceful failure handling

### � **Educational Tools**
- **Algorithm Explanations**: Dynamic descriptions that update based on selected algorithm
- **Step-by-Step Log**: Scrollable, timestamped execution steps with persistent history
- **Visual Legend**: Color-coded visualization guide for different node states
- **Tree Structure Display**: Hierarchical view showing graph relationships
- **Performance Metrics**: View path costs, nodes explored, and execution details

### 🎛️ **Modern User Experience**
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Modular Architecture**: Clean, maintainable CSS and JavaScript modules
- **Professional UI**: Modern styling with hover effects, transitions, and visual feedback
- **Accessibility**: Keyboard navigation and screen reader friendly

## 🏗️ Project Structure

```
SearchMethodShowcase/
├── Search/                          # Main Django app
│   ├── templates/Search/      
│   │   └── index.html              # Interactive web interface
│   ├── views.py                    # Request handlers & validation
│   ├── urls.py                     # URL routing
│   ├── models.py                   # Data models
│   └── admin.py                    # Admin interface
├── SearchMethods/                   # Django project settings
│   ├── settings.py                 # Configuration
│   ├── urls.py                     # Main URL config
│   └── wsgi.py                     # WSGI application
├── Algorithms/                      # Search algorithm implementations
│   └── search_algorithms.py        # Unified algorithm module
├── static/                         # Static files (modular architecture)
│   ├── css/
│   │   ├── main.css               # Entry point (imports all modules)
│   │   ├── base.css               # Foundation styles & layout
│   │   ├── forms.css              # Form controls & buttons
│   │   ├── ui-components.css      # Messages & notifications
│   │   ├── visualization.css      # Graph visualization
│   │   ├── tree-view.css          # Tree structure display
│   │   └── step-info.css          # Algorithm step tracking
│   └── js/                        # Modular JavaScript
│       ├── visualization.js        # Graph & tree logic
│       ├── request-handler.js      # API calls & animation
│       └── ui-manager.js           # UI controls & styling
├── staticfiles/                    # Collected static files for production
├── db.sqlite3                      # SQLite database
└── manage.py                       # Django management commands
```

## 🚀 Quick Start

### **Prerequisites**
- Python 3.8 or higher
- Django 5.1.6
- Modern web browser with JavaScript enabled

### **Installation**

1. **Download or clone the project**
   ```bash
   # If you have git installed
   git clone [repository-url]
   cd SearchMethodShowcase
   
   # Or download as ZIP and extract
   ```

2. **Install dependencies**
   ```bash
   pip install django
   pip install django-ratelimit
   ```

3. **Set up the database**
   ```bash
   python manage.py migrate
   ```

4. **Collect static files**
   ```bash
   python manage.py collectstatic --noinput
   ```

5. **Start the development server**
   ```bash
   python manage.py runserver
   ```

6. **Open your browser**
   Navigate to `http://127.0.0.1:8000` and start exploring!

## 💡 Usage Guide

### **🎮 Getting Started**
1. **Explore the Default Graph**: A sample city network is pre-loaded
2. **Try Different Algorithms**: Select from 6 different search algorithms
3. **Watch the Visualization**: Enable step-by-step visualization to see how algorithms work
4. **Switch Views**: Toggle between Graph View 📊 and Tree View 🌳

### **🛠️ Building Custom Graphs**
1. **Add Nodes**: Enter city names or labels and click "Add Node"
2. **Connect Nodes**: Select source and destination, enter weight, click "Add Edge"
3. **Set Search Parameters**: Choose start and goal nodes
4. **Run Algorithm**: Select algorithm and click "Find Path"
5. **Analyze Results**: View path, cost, and execution steps

### **📊 View Modes**
- **Graph View**: Interactive network visualization with drag-and-drop nodes
- **Tree View**: Hierarchical structure showing graph relationships and connectivity
- **Step Log**: Real-time algorithm execution with timestamps and detailed steps

### **🎯 Algorithm Comparison**
- Run multiple algorithms on the same graph
- Compare path optimality, execution speed, and nodes explored
- Use "Clear Path" to reset and try different approaches

## 🧠 Algorithm Details

### **Breadth-First Search (BFS)**
- **Time Complexity**: O(V + E)
- **Space Complexity**: O(V)
- **Optimal**: Yes (for unweighted graphs)
- **Use Case**: Finding shortest path in unweighted graphs, level-order traversal
- **How it works**: Explores nodes level by level using a queue (FIFO)

### **Depth-First Search (DFS)**
- **Time Complexity**: O(V + E)
- **Space Complexity**: O(V)
- **Optimal**: No (may not find shortest path)
- **Use Case**: Path existence, maze solving, topological sorting
- **How it works**: Explores as deep as possible before backtracking using a stack

### **Dijkstra's Algorithm**
- **Time Complexity**: O((V + E) log V)
- **Space Complexity**: O(V)
- **Optimal**: Yes (for non-negative weights)
- **Use Case**: GPS navigation, network routing, shortest path in weighted graphs
- **How it works**: Uses a priority queue to always explore the closest unvisited node

### **A* Search**
- **Time Complexity**: O(b^d) where b is branching factor, d is depth
- **Space Complexity**: O(b^d)
- **Optimal**: Yes (with admissible heuristic)
- **Use Case**: Game AI, robotics, optimal pathfinding with heuristics
- **How it works**: Combines Dijkstra's with heuristic guidance (f = g + h)

### **Best-First Search**
- **Time Complexity**: O(b^d)
- **Space Complexity**: O(b^d)
- **Optimal**: No (greedy approach)
- **Use Case**: When a good heuristic is available but optimality isn't critical
- **How it works**: Always chooses the node that appears best according to heuristic

### **Hill Climbing**
- **Time Complexity**: O(∞) in worst case (can get stuck)
- **Space Complexity**: O(1)
- **Optimal**: No (local search algorithm)
- **Use Case**: Optimization problems, when local optimum is acceptable
- **How it works**: Always moves to the neighbor with the best heuristic value

## 🔧 API Reference

### **POST /process_graph/**
Processes graph data and returns search results with step-by-step execution.

**Request Body:**
```json
{
  "nodes": [
    {"id": 1, "label": "New York"}, 
    {"id": 2, "label": "Philadelphia"}
  ],
  "edges": [
    {"from": 1, "to": 2, "label": "5"}
  ],
  "source": "1",
  "destination": "2",
  "algorithm": "dijkstra",
  "visualization": true
}
```

**Success Response:**
```json
{
  "status": "success",
  "path": ["New York", "Philadelphia", "Washington"],
  "cost": 7.5,
  "algorithm": "Dijkstra's Algorithm",
  "nodes_explored": 3,
  "steps": [
    "Starting Dijkstra's algorithm from New York",
    "Exploring node: New York (cost: 0)",
    "Found path to goal: Washington"
  ],
  "message": "Path found using Dijkstra's Algorithm"
}
```

**Error Response:**
```json
{
  "status": "error",
  "error": "No path found between the specified nodes",
  "algorithm": "Dijkstra's Algorithm"
}
```

### **Rate Limiting**
- **Limit**: 30 requests per minute per IP address
- **Purpose**: Prevents abuse and ensures fair usage
- **Response**: HTTP 429 when limit exceeded

## 🛠️ Development & Contributing

### **Architecture**
- **Backend**: Django 5.1.6 with modular view handling
- **Frontend**: Vanilla JavaScript with modular ES6 architecture
- **Visualization**: Vis.js for interactive graph rendering
- **Styling**: Modular CSS with component-based organization
- **Security**: Rate limiting, input validation, CSRF protection

### **Adding New Algorithms**
1. Implement in `Algorithms/search_algorithms.py`
2. Add to the algorithm selection in `solve_graph()` function
3. Update the frontend dropdown in `index.html`
4. Add algorithm description in `ui-manager.js`

### **CSS Architecture**
The project uses a modular CSS architecture:
```
static/css/
├── main.css              # Entry point
├── base.css              # Layout & typography
├── forms.css             # Form controls
├── ui-components.css     # Messages & notifications
├── visualization.css     # Graph components
├── tree-view.css         # Tree structure
└── step-info.css         # Algorithm steps
```

### **JavaScript Modules**
```
static/js/
├── visualization.js      # Graph & tree logic
├── request-handler.js    # API calls & animation
└── ui-manager.js         # UI controls & styling
```

### **Testing**
```bash
# Run Django tests
python manage.py test

# Collect static files after changes
python manage.py collectstatic --noinput

# Check for common issues
python manage.py check
```

### **Contributing**
This is a personal educational project by Divesh Sanjay Kshirsagar. If you'd like to suggest improvements or report issues, feel free to reach out!

## � Contact & Support

**Developer**: Divesh Sanjay Kshirsagar  
**Role**: Software Developer  
**Project**: Educational demonstration of graph search algorithms

### **About This Project**
This project was created as an educational tool to demonstrate various pathfinding algorithms with interactive visualization. It showcases modern web development practices using Django and JavaScript.

---

**Created with ❤️ by Divesh Sanjay Kshirsagar**  
*Software Developer passionate about algorithms and education*

## 🎓 Educational Use Cases

1. **Computer Science Education**: Learn how pathfinding algorithms work
2. **Algorithm Comparison**: Compare performance on different graph structures  
3. **Interactive Learning**: Visual understanding of search strategies
4. **Research Projects**: Foundation for advanced pathfinding research
5. **Interview Preparation**: Practice with common algorithm questions
6. **Game Development**: Understanding AI pathfinding for games

## 🔮 Future Enhancements

- [ ] **Advanced Algorithms**: Bidirectional search, Jump Point Search
- [ ] **Interactive Tutorial**: Guided walkthrough for beginners
- [ ] **Graph Import/Export**: Save and load custom graph configurations
- [ ] **Performance Benchmarking**: Detailed timing and memory usage analytics
- [ ] **3D Visualization**: Three-dimensional graph representation
- [ ] **Multi-language Support**: Interface translations
- [ ] **Algorithm Animation Speed Control**: Adjustable visualization speed
- [ ] **Custom Heuristics**: User-defined heuristic functions for A*
- [ ] **Graph Generators**: Automatic generation of common graph types
- [ ] **Collaborative Features**: Share graphs and results with others

## 🤝 Acknowledgments

- **Vis.js Community**: For the excellent graph visualization library
- **Django Team**: For the robust web framework
- **Open Source Community**: For inspiration and best practices
- **Computer Science Educators**: For feedback on educational value

## 📞 Contact & Support

**Developer**: Divesh Sanjay Kshirsagar  
**Role**: Software Developer  
**Project**: Educational demonstration of graph search algorithms

### **Questions or Feedback?**
If you have questions about the project or suggestions for improvements, feel free to reach out!

---

**⭐ Thank you for checking out this project!**

**Created with ❤️ by Divesh Sanjay Kshirsagar**  
*Software Developer passionate about algorithms and education*
