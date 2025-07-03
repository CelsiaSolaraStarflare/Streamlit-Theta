"""
Theta Mind Map Editor - Interactive mind mapping tool
Provides a visual interface for creating mind maps.
"""

import streamlit as st
import streamlit.components.v1 as components
import json
from typing import Dict, List, Any, Optional

def theta_mindmap_editor(
    mindmap_data: Optional[Dict[str, Any]] = None,
    width: int = 900,
    height: int = 600,
    key: Optional[str] = None
) -> None:
    """
    Create an interactive mind map editor.
    
    Parameters:
    -----------
    mindmap_data : Dict[str, Any]
        Mind map data with nodes and connections
    width : int
        Width of the editor in pixels
    height : int  
        Height of the editor in pixels
    key : str or None
        Unique key for the component
    
    Returns:
    --------
    Dict with mind map data or None
    """
    
    # Default mind map data if none provided
    if mindmap_data is None:
        mindmap_data = {
            "title": "My Mind Map",
            "nodes": [
                {
                    "id": "root",
                    "text": "Central Idea",
                    "x": 400,
                    "y": 250,
                    "color": "#007bff",
                    "level": 0,
                    "parent": None
                },
                {
                    "id": "node_1",
                    "text": "Branch 1",
                    "x": 200,
                    "y": 150,
                    "color": "#28a745",
                    "level": 1,
                    "parent": "root"
                },
                {
                    "id": "node_2",
                    "text": "Branch 2",
                    "x": 600,
                    "y": 150,
                    "color": "#ffc107",
                    "level": 1,
                    "parent": "root"
                },
                {
                    "id": "node_3",
                    "text": "Sub-branch",
                    "x": 150,
                    "y": 80,
                    "color": "#17a2b8",
                    "level": 2,
                    "parent": "node_1"
                }
            ]
        }
    
    # Convert data to JSON for JavaScript
    data_json = json.dumps(mindmap_data).replace('"', '\\"')
    
    component_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Theta Mind Map Editor</title>
        <style>
            body {{
                margin: 0;
                padding: 10px;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: #f5f5f5;
            }}
            
            .editor-container {{
                width: {width}px;
                height: {height}px;
                background: white;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                display: flex;
                flex-direction: column;
            }}
            
            .toolbar {{
                height: 50px;
                background: #f8f9fa;
                border-bottom: 1px solid #dee2e6;
                border-radius: 8px 8px 0 0;
                display: flex;
                align-items: center;
                padding: 0 15px;
                gap: 10px;
            }}
            
            .toolbar button {{
                padding: 6px 12px;
                border: 1px solid #dee2e6;
                background: white;
                border-radius: 4px;
                cursor: pointer;
                font-size: 12px;
                transition: all 0.2s;
            }}
            
            .toolbar button:hover {{
                background: #e9ecef;
                border-color: #adb5bd;
            }}
            
            .toolbar button.active {{
                background: #007bff;
                color: white;
                border-color: #007bff;
            }}
            
            .mindmap-container {{
                flex: 1;
                position: relative;
                overflow: hidden;
                background: linear-gradient(45deg, #f8f9fa 25%, transparent 25%, transparent 75%, #f8f9fa 75%, #f8f9fa),
                           linear-gradient(45deg, #f8f9fa 25%, transparent 25%, transparent 75%, #f8f9fa 75%, #f8f9fa);
                background-size: 20px 20px;
                background-position: 0 0, 10px 10px;
            }}
            
            .mindmap-canvas {{
                width: 100%;
                height: 100%;
                position: absolute;
                cursor: grab;
            }}
            
            .mindmap-canvas.dragging {{
                cursor: grabbing;
            }}
            
            .node {{
                position: absolute;
                min-width: 120px;
                padding: 10px 15px;
                background: white;
                border: 2px solid #007bff;
                border-radius: 20px;
                text-align: center;
                cursor: move;
                user-select: none;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                transition: all 0.2s;
                font-size: 14px;
                font-weight: 500;
                z-index: 10;
            }}
            
            .node:hover {{
                transform: scale(1.05);
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            }}
            
            .node.selected {{
                border-width: 3px;
                box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.25);
            }}
            
            .node.root {{
                font-size: 16px;
                font-weight: 600;
                min-width: 150px;
                padding: 15px 20px;
            }}
            
            .node.level-1 {{
                font-size: 14px;
                min-width: 130px;
            }}
            
            .node.level-2 {{
                font-size: 12px;
                min-width: 110px;
                padding: 8px 12px;
            }}
            
            .connection {{
                position: absolute;
                pointer-events: none;
                z-index: 1;
            }}
            
            .connection line {{
                stroke: #6c757d;
                stroke-width: 2;
                stroke-linecap: round;
            }}
            
            .node-controls {{
                position: absolute;
                top: -15px;
                right: -15px;
                display: none;
                gap: 5px;
            }}
            
            .node:hover .node-controls,
            .node.selected .node-controls {{
                display: flex;
            }}
            
            .control-btn {{
                width: 20px;
                height: 20px;
                border: none;
                border-radius: 50%;
                cursor: pointer;
                font-size: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 1px 3px rgba(0,0,0,0.2);
            }}
            
            .control-btn.add {{ background: #28a745; color: white; }}
            .control-btn.edit {{ background: #007bff; color: white; }}
            .control-btn.delete {{ background: #dc3545; color: white; }}
            
            .properties-panel {{
                position: absolute;
                top: 60px;
                right: 10px;
                width: 250px;
                background: white;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                padding: 15px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                display: none;
                z-index: 100;
            }}
            
            .properties-panel h4 {{
                margin: 0 0 10px 0;
                font-size: 14px;
                color: #495057;
            }}
            
            .property-row {{
                display: flex;
                flex-direction: column;
                margin-bottom: 10px;
            }}
            
            .property-row label {{
                font-size: 12px;
                color: #6c757d;
                margin-bottom: 5px;
            }}
            
            .property-row input, .property-row select {{
                padding: 6px 8px;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                font-size: 12px;
            }}
            
            .color-input {{
                width: 50px;
                height: 30px;
                border-radius: 4px;
            }}
            
            .btn {{
                background: #007bff;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 12px;
                margin: 5px 0;
                width: 100%;
            }}
            
            .btn:hover {{
                background: #0056b3;
            }}
            
            .btn.danger {{
                background: #dc3545;
            }}
            
            .btn.danger:hover {{
                background: #c82333;
            }}
            
            .minimap {{
                position: absolute;
                bottom: 10px;
                right: 10px;
                width: 150px;
                height: 100px;
                background: rgba(255,255,255,0.9);
                border: 1px solid #dee2e6;
                border-radius: 4px;
                overflow: hidden;
                z-index: 50;
            }}
            
            .zoom-controls {{
                position: absolute;
                bottom: 120px;
                right: 10px;
                display: flex;
                flex-direction: column;
                gap: 5px;
                z-index: 50;
            }}
            
            .zoom-btn {{
                width: 30px;
                height: 30px;
                border: 1px solid #dee2e6;
                background: white;
                border-radius: 4px;
                cursor: pointer;
                font-size: 14px;
                font-weight: bold;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            
            .zoom-btn:hover {{
                background: #f8f9fa;
            }}
            
            .context-menu {{
                position: absolute;
                background: white;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                padding: 5px 0;
                display: none;
                z-index: 200;
            }}
            
            .context-menu-item {{
                padding: 8px 15px;
                cursor: pointer;
                font-size: 12px;
                border: none;
                background: none;
                width: 100%;
                text-align: left;
            }}
            
            .context-menu-item:hover {{
                background: #f8f9fa;
            }}
        </style>
    </head>
    <body>
        <div class="editor-container">
            <div class="toolbar">
                <button onclick="addNode()" title="Add Node">➕ Add Node</button>
                <button onclick="setTool('select')" class="tool-btn active" data-tool="select" title="Select">👆 Select</button>
                <button onclick="setTool('pan')" class="tool-btn" data-tool="pan" title="Pan">✋ Pan</button>
                <button onclick="centerView()" title="Center View">🎯 Center</button>
                <button onclick="autoLayout()" title="Auto Layout">🔀 Layout</button>
                <button onclick="exportMindMap()" title="Export">💾 Export</button>
                <button onclick="toggleFullscreen()" title="Fullscreen">🔍 Zoom</button>
            </div>
            
            <div class="mindmap-container" id="mindmap-container">
                <div class="mindmap-canvas" id="mindmap-canvas">
                    <svg class="connections" id="connections-svg">
                        <!-- Connections will be drawn here -->
                    </svg>
                    <!-- Nodes will be added here -->
                </div>
                
                <div class="properties-panel" id="properties-panel">
                    <h4>📝 Node Properties</h4>
                    <div class="property-row">
                        <label>Text:</label>
                        <input type="text" id="node-text" onchange="updateSelectedNode()">
                    </div>
                    <div class="property-row">
                        <label>Color:</label>
                        <input type="color" id="node-color" class="color-input" onchange="updateSelectedNode()">
                    </div>
                    <div class="property-row">
                        <label>Font Size:</label>
                        <select id="node-fontsize" onchange="updateSelectedNode()">
                            <option value="12">Small</option>
                            <option value="14" selected>Medium</option>
                            <option value="16">Large</option>
                            <option value="18">Extra Large</option>
                        </select>
                    </div>
                    <button onclick="addChildNode()" class="btn">➕ Add Child</button>
                    <button onclick="deleteSelectedNode()" class="btn danger">🗑️ Delete Node</button>
                </div>
                
                <div class="zoom-controls">
                    <button class="zoom-btn" onclick="zoom(1.2)" title="Zoom In">+</button>
                    <button class="zoom-btn" onclick="zoom(0.8)" title="Zoom Out">-</button>
                    <button class="zoom-btn" onclick="resetZoom()" title="Reset Zoom">⚫</button>
                </div>
                
                <div class="minimap" id="minimap">
                    <!-- Minimap content -->
                </div>
                
                <div class="context-menu" id="context-menu">
                    <button class="context-menu-item" onclick="addNodeAtPosition()">➕ Add Node Here</button>
                    <button class="context-menu-item" onclick="addChildNode()">🌳 Add Child Node</button>
                    <button class="context-menu-item" onclick="changeNodeColor()">🎨 Change Color</button>
                    <button class="context-menu-item" onclick="deleteSelectedNode()">🗑️ Delete Node</button>
                </div>
            </div>
        </div>
        
        <script>
            let mindmapData = {data_json};
            let selectedNode = null;
            let currentTool = 'select';
            let isDragging = false;
            let dragOffset = {{ x: 0, y: 0 }};
            let canvasOffset = {{ x: 0, y: 0 }};
            let zoomLevel = 1;
            let nodeCounter = 4;
            let contextMenuPosition = {{ x: 0, y: 0 }};
            
            function initMindMap() {{
                renderMindMap();
                setupEventListeners();
                centerView();
            }}
            
            function renderMindMap() {{
                const canvas = document.getElementById('mindmap-canvas');
                
                // Clear existing nodes
                const existingNodes = canvas.querySelectorAll('.node');
                existingNodes.forEach(node => node.remove());
                
                // Render nodes
                mindmapData.nodes.forEach(nodeData => {{
                    const node = createNodeElement(nodeData);
                    canvas.appendChild(node);
                }});
                
                // Render connections
                renderConnections();
            }}
            
            function createNodeElement(nodeData) {{
                const node = document.createElement('div');
                node.className = `node level-${{nodeData.level}}`;
                if (nodeData.level === 0) node.classList.add('root');
                node.id = nodeData.id;
                node.textContent = nodeData.text;
                
                node.style.left = nodeData.x + 'px';
                node.style.top = nodeData.y + 'px';
                node.style.borderColor = nodeData.color;
                node.style.color = nodeData.color;
                
                // Add controls
                const controls = document.createElement('div');
                controls.className = 'node-controls';
                controls.innerHTML = `
                    <button class="control-btn add" onclick="addChildToNode('${{nodeData.id}}')" title="Add Child">+</button>
                    <button class="control-btn edit" onclick="editNode('${{nodeData.id}}')" title="Edit">✏️</button>
                    <button class="control-btn delete" onclick="deleteNode('${{nodeData.id}}')" title="Delete">×</button>
                `;
                node.appendChild(controls);
                
                // Add event listeners
                node.addEventListener('click', (e) => {{
                    e.stopPropagation();
                    selectNode(nodeData.id);
                }});
                
                node.addEventListener('mousedown', (e) => {{
                    if (currentTool === 'select') {{
                        startDragNode(e, nodeData.id);
                    }}
                }});
                
                node.addEventListener('contextmenu', (e) => {{
                    e.preventDefault();
                    showContextMenu(e.clientX, e.clientY, nodeData.id);
                }});
                
                return node;
            }}
            
            function renderConnections() {{
                const svg = document.getElementById('connections-svg');
                const container = document.getElementById('mindmap-container');
                
                svg.style.width = container.offsetWidth + 'px';
                svg.style.height = container.offsetHeight + 'px';
                svg.innerHTML = '';
                
                mindmapData.nodes.forEach(node => {{
                    if (node.parent) {{
                        const parentNode = mindmapData.nodes.find(n => n.id === node.parent);
                        if (parentNode) {{
                            const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                            line.setAttribute('x1', parentNode.x + 75); // Center of parent node
                            line.setAttribute('y1', parentNode.y + 25);
                            line.setAttribute('x2', node.x + 75); // Center of child node  
                            line.setAttribute('y2', node.y + 25);
                            line.setAttribute('stroke', node.color);
                            line.setAttribute('stroke-width', '2');
                            svg.appendChild(line);
                        }}
                    }}
                }});
            }}
            
            function setupEventListeners() {{
                const canvas = document.getElementById('mindmap-canvas');
                const container = document.getElementById('mindmap-container');
                
                // Canvas panning
                canvas.addEventListener('mousedown', (e) => {{
                    if (currentTool === 'pan' || e.ctrlKey) {{
                        startPanCanvas(e);
                    }}
                }});
                
                document.addEventListener('mousemove', handleMouseMove);
                document.addEventListener('mouseup', handleMouseUp);
                
                // Context menu
                canvas.addEventListener('contextmenu', (e) => {{
                    e.preventDefault();
                    contextMenuPosition = {{ x: e.offsetX, y: e.offsetY }};
                    showContextMenu(e.clientX, e.clientY);
                }});
                
                // Hide context menu on click
                document.addEventListener('click', () => {{
                    document.getElementById('context-menu').style.display = 'none';
                }});
                
                // Keyboard shortcuts
                document.addEventListener('keydown', (e) => {{
                    if (e.key === 'Delete' && selectedNode) {{
                        deleteSelectedNode();
                    }} else if (e.key === 'Tab' && selectedNode) {{
                        e.preventDefault();
                        addChildNode();
                    }} else if (e.key === 'Enter' && selectedNode) {{
                        editNode(selectedNode);
                    }}
                }});
            }}
            
            function selectNode(nodeId) {{
                selectedNode = nodeId;
                
                // Update visual selection
                document.querySelectorAll('.node').forEach(node => {{
                    node.classList.remove('selected');
                }});
                document.getElementById(nodeId).classList.add('selected');
                
                // Show properties panel
                const nodeData = mindmapData.nodes.find(n => n.id === nodeId);
                if (nodeData) {{
                    document.getElementById('node-text').value = nodeData.text;
                    document.getElementById('node-color').value = nodeData.color;
                    document.getElementById('properties-panel').style.display = 'block';
                }}
            }}
            
            function setTool(tool) {{
                currentTool = tool;
                document.querySelectorAll('.tool-btn').forEach(btn => {{
                    btn.classList.remove('active');
                }});
                document.querySelector(`[data-tool="${{tool}}"]`).classList.add('active');
                
                const canvas = document.getElementById('mindmap-canvas');
                if (tool === 'pan') {{
                    canvas.style.cursor = 'grab';
                }} else {{
                    canvas.style.cursor = 'default';
                }}
            }}
            
            function addNode() {{
                nodeCounter++;
                const newNode = {{
                    id: `node_${{nodeCounter}}`,
                    text: 'New Node',
                    x: 300 + Math.random() * 200,
                    y: 200 + Math.random() * 200,
                    color: '#' + Math.floor(Math.random()*16777215).toString(16),
                    level: 1,
                    parent: 'root'
                }};
                
                mindmapData.nodes.push(newNode);
                renderMindMap();
                selectNode(newNode.id);
            }}
            
            function addChildNode() {{
                if (!selectedNode) return;
                
                nodeCounter++;
                const parentNode = mindmapData.nodes.find(n => n.id === selectedNode);
                const newNode = {{
                    id: `node_${{nodeCounter}}`,
                    text: 'New Child',
                    x: parentNode.x + 150,
                    y: parentNode.y + 50,
                    color: parentNode.color,
                    level: parentNode.level + 1,
                    parent: selectedNode
                }};
                
                mindmapData.nodes.push(newNode);
                renderMindMap();
                selectNode(newNode.id);
            }}
            
            function addChildToNode(nodeId) {{
                selectNode(nodeId);
                addChildNode();
            }}
            
            function deleteSelectedNode() {{
                if (!selectedNode || selectedNode === 'root') return;
                
                if (confirm('Delete this node and all its children?')) {{
                    deleteNodeAndChildren(selectedNode);
                    selectedNode = null;
                    document.getElementById('properties-panel').style.display = 'none';
                    renderMindMap();
                }}
            }}
            
            function deleteNodeAndChildren(nodeId) {{
                // Find and delete all children first
                const children = mindmapData.nodes.filter(n => n.parent === nodeId);
                children.forEach(child => deleteNodeAndChildren(child.id));
                
                // Delete the node itself
                mindmapData.nodes = mindmapData.nodes.filter(n => n.id !== nodeId);
            }}
            
            function updateSelectedNode() {{
                if (!selectedNode) return;
                
                const nodeData = mindmapData.nodes.find(n => n.id === selectedNode);
                if (nodeData) {{
                    nodeData.text = document.getElementById('node-text').value;
                    nodeData.color = document.getElementById('node-color').value;
                    nodeData.fontSize = document.getElementById('node-fontsize').value;
                    
                    renderMindMap();
                    selectNode(selectedNode);
                }}
            }}
            
            function startDragNode(e, nodeId) {{
                const nodeData = mindmapData.nodes.find(n => n.id === nodeId);
                isDragging = true;
                dragOffset = {{
                    x: e.clientX - nodeData.x,
                    y: e.clientY - nodeData.y
                }};
                selectNode(nodeId);
            }}
            
            function startPanCanvas(e) {{
                isDragging = true;
                dragOffset = {{
                    x: e.clientX - canvasOffset.x,
                    y: e.clientY - canvasOffset.y
                }};
                document.getElementById('mindmap-canvas').classList.add('dragging');
            }}
            
            function handleMouseMove(e) {{
                if (!isDragging) return;
                
                if (currentTool === 'pan' || e.ctrlKey) {{
                    // Pan canvas
                    canvasOffset.x = e.clientX - dragOffset.x;
                    canvasOffset.y = e.clientY - dragOffset.y;
                    document.getElementById('mindmap-canvas').style.transform = 
                        `translate(${{canvasOffset.x}}px, ${{canvasOffset.y}}px) scale(${{zoomLevel}})`;
                }} else if (selectedNode) {{
                    // Drag node
                    const nodeData = mindmapData.nodes.find(n => n.id === selectedNode);
                    if (nodeData) {{
                        nodeData.x = e.clientX - dragOffset.x;
                        nodeData.y = e.clientY - dragOffset.y;
                        
                        const nodeElement = document.getElementById(selectedNode);
                        nodeElement.style.left = nodeData.x + 'px';
                        nodeElement.style.top = nodeData.y + 'px';
                        
                        renderConnections();
                    }}
                }}
            }}
            
            function handleMouseUp() {{
                isDragging = false;
                document.getElementById('mindmap-canvas').classList.remove('dragging');
            }}
            
            function centerView() {{
                canvasOffset = {{ x: 0, y: 0 }};
                zoomLevel = 1;
                document.getElementById('mindmap-canvas').style.transform = 'translate(0px, 0px) scale(1)';
            }}
            
            function zoom(factor) {{
                zoomLevel *= factor;
                zoomLevel = Math.max(0.1, Math.min(3, zoomLevel));
                document.getElementById('mindmap-canvas').style.transform = 
                    `translate(${{canvasOffset.x}}px, ${{canvasOffset.y}}px) scale(${{zoomLevel}})`;
            }}
            
            function resetZoom() {{
                zoomLevel = 1;
                document.getElementById('mindmap-canvas').style.transform = 
                    `translate(${{canvasOffset.x}}px, ${{canvasOffset.y}}px) scale(1)`;
            }}
            
            function autoLayout() {{
                // Simple radial layout
                const root = mindmapData.nodes.find(n => n.level === 0);
                const level1Nodes = mindmapData.nodes.filter(n => n.level === 1);
                
                level1Nodes.forEach((node, index) => {{
                    const angle = (2 * Math.PI * index) / level1Nodes.length;
                    node.x = root.x + Math.cos(angle) * 200;
                    node.y = root.y + Math.sin(angle) * 200;
                    
                    // Position children of this node
                    const children = mindmapData.nodes.filter(n => n.parent === node.id);
                    children.forEach((child, childIndex) => {{
                        const childAngle = angle + (childIndex - children.length/2) * 0.5;
                        child.x = node.x + Math.cos(childAngle) * 150;
                        child.y = node.y + Math.sin(childAngle) * 150;
                    }});
                }});
                
                renderMindMap();
            }}
            
            function showContextMenu(x, y, nodeId = null) {{
                const menu = document.getElementById('context-menu');
                menu.style.left = x + 'px';
                menu.style.top = y + 'px';
                menu.style.display = 'block';
                
                if (nodeId) {{
                    selectNode(nodeId);
                }}
            }}
            
            function addNodeAtPosition() {{
                nodeCounter++;
                const newNode = {{
                    id: `node_${{nodeCounter}}`,
                    text: 'New Node',
                    x: contextMenuPosition.x - 60,
                    y: contextMenuPosition.y - 20,
                    color: '#' + Math.floor(Math.random()*16777215).toString(16),
                    level: 1,
                    parent: 'root'
                }};
                
                mindmapData.nodes.push(newNode);
                renderMindMap();
                selectNode(newNode.id);
                document.getElementById('context-menu').style.display = 'none';
            }}
            
            function exportMindMap() {{
                const exportData = {{
                    ...mindmapData,
                    export_date: new Date().toISOString(),
                    version: '1.0'
                }};
                
                const blob = new Blob([JSON.stringify(exportData, null, 2)], {{ type: 'application/json' }});
                const link = document.createElement('a');
                link.download = `mindmap-${{new Date().toISOString().slice(0, 19).replace(/:/g, '-')}}.json`;
                link.href = URL.createObjectURL(blob);
                link.click();
            }}
            
            function editNode(nodeId) {{
                const nodeData = mindmapData.nodes.find(n => n.id === nodeId);
                if (nodeData) {{
                    const newText = prompt('Edit node text:', nodeData.text);
                    if (newText !== null) {{
                        nodeData.text = newText;
                        renderMindMap();
                        selectNode(nodeId);
                    }}
                }}
            }}
            
            function toggleFullscreen() {{
                const container = document.getElementById('mindmap-container');
                if (!document.fullscreenElement) {{
                    container.requestFullscreen();
                }} else {{
                    document.exitFullscreen();
                }}
            }}
            
            // Initialize the mind map editor
            initMindMap();
        </script>
    </body>
    </html>
    """
    
    # Use Streamlit's HTML component
    components.html(component_html, width=width, height=height)
    
    # Return None due to Streamlit version compatibility
    return None
