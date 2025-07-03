"""
Theta Diagram Editor - Flowcharts, org charts, and wireframes
Provides a visual interface for creating diagrams.
"""

import streamlit as st
import streamlit.components.v1 as components
import json
from typing import Dict, List, Any, Optional

def theta_diagram_editor(
    diagram_data: Optional[Dict[str, Any]] = None,
    diagram_type: str = "flowchart",
    width: int = 900,
    height: int = 600,
    key: Optional[str] = None
) -> None:
    """
    Create a diagram editor for flowcharts, org charts, and wireframes.
    
    Parameters:
    -----------
    diagram_data : Dict[str, Any]
        Diagram data with shapes and connections
    diagram_type : str
        Type of diagram (flowchart, orgchart, wireframe)
    width : int
        Width of the editor in pixels
    height : int  
        Height of the editor in pixels
    key : str or None
        Unique key for the component
    
    Returns:
    --------
    Dict with diagram data or None
    """
    
    # Default diagram data if none provided
    if diagram_data is None:
        diagram_data = {
            "title": "Sample Flowchart",
            "type": diagram_type,
            "shapes": [
                {
                    "id": "start",
                    "type": "oval",
                    "text": "Start",
                    "x": 200,
                    "y": 50,
                    "width": 100,
                    "height": 60,
                    "color": "#28a745",
                    "borderColor": "#1e7e34"
                },
                {
                    "id": "process1",
                    "type": "rectangle",
                    "text": "Process Data",
                    "x": 150,
                    "y": 150,
                    "width": 120,
                    "height": 80,
                    "color": "#007bff",
                    "borderColor": "#0056b3"
                },
                {
                    "id": "decision",
                    "type": "diamond",
                    "text": "Valid?",
                    "x": 175,
                    "y": 270,
                    "width": 100,
                    "height": 80,
                    "color": "#ffc107",
                    "borderColor": "#e0a800"
                },
                {
                    "id": "end",
                    "type": "oval",
                    "text": "End",
                    "x": 200,
                    "y": 400,
                    "width": 100,
                    "height": 60,
                    "color": "#dc3545",
                    "borderColor": "#c82333"
                }
            ],
            "connections": [
                {
                    "id": "conn1",
                    "from": "start",
                    "to": "process1",
                    "label": "",
                    "style": "solid"
                },
                {
                    "id": "conn2",
                    "from": "process1",
                    "to": "decision",
                    "label": "",
                    "style": "solid"
                },
                {
                    "id": "conn3",
                    "from": "decision",
                    "to": "end",
                    "label": "Yes",
                    "style": "solid"
                }
            ]
        }
    
    # Convert data to JSON for JavaScript
    data_json = json.dumps(diagram_data).replace('"', '\\"')
    
    component_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Theta Diagram Editor</title>
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
                height: 60px;
                background: #f8f9fa;
                border-bottom: 1px solid #dee2e6;
                border-radius: 8px 8px 0 0;
                display: flex;
                align-items: center;
                padding: 0 15px;
                gap: 10px;
                overflow-x: auto;
            }}
            
            .toolbar-section {{
                display: flex;
                gap: 5px;
                padding-right: 15px;
                border-right: 1px solid #dee2e6;
            }}
            
            .toolbar button {{
                padding: 6px 12px;
                border: 1px solid #dee2e6;
                background: white;
                border-radius: 4px;
                cursor: pointer;
                font-size: 11px;
                transition: all 0.2s;
                white-space: nowrap;
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
            
            .editor-content {{
                flex: 1;
                display: flex;
            }}
            
            .shapes-panel {{
                width: 200px;
                background: #f8f9fa;
                border-right: 1px solid #dee2e6;
                padding: 15px;
                overflow-y: auto;
            }}
            
            .diagram-canvas {{
                flex: 1;
                position: relative;
                overflow: hidden;
                background: white;
                background-image: 
                    linear-gradient(rgba(0,0,0,.1) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(0,0,0,.1) 1px, transparent 1px);
                background-size: 20px 20px;
            }}
            
            .properties-panel {{
                width: 250px;
                background: #f8f9fa;
                border-left: 1px solid #dee2e6;
                padding: 15px;
                overflow-y: auto;
            }}
            
            .shape-library h4 {{
                margin: 0 0 15px 0;
                font-size: 14px;
                color: #495057;
            }}
            
            .shape-item {{
                display: flex;
                align-items: center;
                padding: 10px;
                margin-bottom: 8px;
                background: white;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                cursor: pointer;
                transition: all 0.2s;
            }}
            
            .shape-item:hover {{
                border-color: #007bff;
                background: #f8f9ff;
            }}
            
            .shape-icon {{
                width: 30px;
                height: 20px;
                margin-right: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 16px;
            }}
            
            .shape {{
                position: absolute;
                cursor: move;
                user-select: none;
                border: 2px solid;
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
                font-size: 12px;
                font-weight: 500;
                transition: all 0.2s;
                z-index: 10;
            }}
            
            .shape:hover {{
                transform: scale(1.02);
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            }}
            
            .shape.selected {{
                border-width: 3px;
                box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.25);
            }}
            
            .shape.rectangle {{
                border-radius: 4px;
            }}
            
            .shape.oval {{
                border-radius: 50%;
            }}
            
            .shape.diamond {{
                transform: rotate(45deg);
                border-radius: 8px;
            }}
            
            .shape.diamond .shape-text {{
                transform: rotate(-45deg);
            }}
            
            .shape.parallelogram {{
                transform: skew(-15deg);
                border-radius: 4px;
            }}
            
            .shape.parallelogram .shape-text {{
                transform: skew(15deg);
            }}
            
            .shape.hexagon {{
                clip-path: polygon(25% 0%, 75% 0%, 100% 50%, 75% 100%, 25% 100%, 0% 50%);
                border: none;
                border-radius: 0;
            }}
            
            .connection {{
                position: absolute;
                pointer-events: none;
                z-index: 5;
            }}
            
            .connection line {{
                stroke: #6c757d;
                stroke-width: 2;
                marker-end: url(#arrowhead);
            }}
            
            .connection.dashed line {{
                stroke-dasharray: 5,5;
            }}
            
            .connection-label {{
                position: absolute;
                background: white;
                padding: 2px 6px;
                border: 1px solid #dee2e6;
                border-radius: 3px;
                font-size: 10px;
                color: #495057;
                z-index: 15;
            }}
            
            .shape-controls {{
                position: absolute;
                top: -20px;
                right: -20px;
                display: none;
                gap: 3px;
            }}
            
            .shape:hover .shape-controls,
            .shape.selected .shape-controls {{
                display: flex;
            }}
            
            .control-btn {{
                width: 18px;
                height: 18px;
                border: none;
                border-radius: 50%;
                cursor: pointer;
                font-size: 9px;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 1px 3px rgba(0,0,0,0.2);
            }}
            
            .control-btn.connect {{ background: #28a745; color: white; }}
            .control-btn.edit {{ background: #007bff; color: white; }}
            .control-btn.delete {{ background: #dc3545; color: white; }}
            
            .property-group {{
                margin-bottom: 20px;
                padding: 15px;
                background: white;
                border-radius: 6px;
                border: 1px solid #dee2e6;
            }}
            
            .property-group h4 {{
                margin: 0 0 10px 0;
                font-size: 14px;
                font-weight: 600;
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
            
            .property-row input, .property-row select, .property-row textarea {{
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
                padding: 8px 16px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 12px;
                margin: 5px 0;
                width: 100%;
                transition: background 0.3s;
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
            
            .connecting-mode {{
                cursor: crosshair !important;
            }}
            
            .temp-connection {{
                position: absolute;
                pointer-events: none;
                z-index: 20;
            }}
            
            .zoom-controls {{
                position: absolute;
                bottom: 20px;
                right: 20px;
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
        </style>
    </head>
    <body>
        <div class="editor-container">
            <div class="toolbar">
                <div class="toolbar-section">
                    <button onclick="setTool('select')" class="tool-btn active" data-tool="select">👆 Select</button>
                    <button onclick="setTool('connect')" class="tool-btn" data-tool="connect">🔗 Connect</button>
                    <button onclick="setTool('pan')" class="tool-btn" data-tool="pan">✋ Pan</button>
                </div>
                
                <div class="toolbar-section">
                    <button onclick="addShape('rectangle')">⬜ Rectangle</button>
                    <button onclick="addShape('oval')">⭕ Oval</button>
                    <button onclick="addShape('diamond')">💎 Diamond</button>
                    <button onclick="addShape('parallelogram')">📐 Parallel</button>
                </div>
                
                <div class="toolbar-section">
                    <button onclick="alignShapes('left')">⬅️ Left</button>
                    <button onclick="alignShapes('center')">🔘 Center</button>
                    <button onclick="alignShapes('right')">➡️ Right</button>
                    <button onclick="distributeShapes()">📏 Distribute</button>
                </div>
                
                <div class="toolbar-section">
                    <button onclick="exportDiagram()">💾 Export</button>
                    <button onclick="resetView()">🎯 Reset View</button>
                </div>
            </div>
            
            <div class="editor-content">
                <div class="shapes-panel">
                    <div class="shape-library">
                        <h4>📐 Shape Library</h4>
                        
                        <div class="shape-item" onclick="addShape('rectangle')">
                            <div class="shape-icon">⬜</div>
                            <span>Rectangle</span>
                        </div>
                        
                        <div class="shape-item" onclick="addShape('oval')">
                            <div class="shape-icon">⭕</div>
                            <span>Oval</span>
                        </div>
                        
                        <div class="shape-item" onclick="addShape('diamond')">
                            <div class="shape-icon">💎</div>
                            <span>Diamond</span>
                        </div>
                        
                        <div class="shape-item" onclick="addShape('parallelogram')">
                            <div class="shape-icon">📐</div>
                            <span>Parallelogram</span>
                        </div>
                        
                        <div class="shape-item" onclick="addShape('hexagon')">
                            <div class="shape-icon">⬡</div>
                            <span>Hexagon</span>
                        </div>
                        
                        <div class="shape-item" onclick="addShape('triangle')">
                            <div class="shape-icon">🔺</div>
                            <span>Triangle</span>
                        </div>
                        
                        <div class="shape-item" onclick="addShape('cylinder')">
                            <div class="shape-icon">🗃️</div>
                            <span>Cylinder</span>
                        </div>
                        
                        <div class="shape-item" onclick="addShape('document')">
                            <div class="shape-icon">📄</div>
                            <span>Document</span>
                        </div>
                    </div>
                </div>
                
                <div class="diagram-canvas" id="diagram-canvas">
                    <svg class="connections" id="connections-svg">
                        <defs>
                            <marker id="arrowhead" markerWidth="10" markerHeight="7" 
                                refX="9" refY="3.5" orient="auto">
                                <polygon points="0 0, 10 3.5, 0 7" fill="#6c757d" />
                            </marker>
                        </defs>
                    </svg>
                    
                    <div class="zoom-controls">
                        <button class="zoom-btn" onclick="zoom(1.2)">+</button>
                        <button class="zoom-btn" onclick="zoom(0.8)">-</button>
                        <button class="zoom-btn" onclick="resetZoom()">⚫</button>
                    </div>
                </div>
                
                <div class="properties-panel">
                    <div class="property-group">
                        <h4>📊 Diagram Settings</h4>
                        <div class="property-row">
                            <label>Title:</label>
                            <input type="text" id="diagram-title" value="Sample Flowchart" onchange="updateDiagramSettings()">
                        </div>
                        <div class="property-row">
                            <label>Type:</label>
                            <select id="diagram-type" onchange="updateDiagramSettings()">
                                <option value="flowchart">Flowchart</option>
                                <option value="orgchart">Org Chart</option>
                                <option value="wireframe">Wireframe</option>
                                <option value="network">Network</option>
                            </select>
                        </div>
                    </div>
                    
                    <div class="property-group" id="shape-properties" style="display: none;">
                        <h4>🔧 Shape Properties</h4>
                        <div class="property-row">
                            <label>Text:</label>
                            <textarea id="shape-text" onchange="updateSelectedShape()"></textarea>
                        </div>
                        <div class="property-row">
                            <label>Width:</label>
                            <input type="number" id="shape-width" onchange="updateSelectedShape()">
                        </div>
                        <div class="property-row">
                            <label>Height:</label>
                            <input type="number" id="shape-height" onchange="updateSelectedShape()">
                        </div>
                        <div class="property-row">
                            <label>Fill Color:</label>
                            <input type="color" id="shape-color" class="color-input" onchange="updateSelectedShape()">
                        </div>
                        <div class="property-row">
                            <label>Border Color:</label>
                            <input type="color" id="shape-border" class="color-input" onchange="updateSelectedShape()">
                        </div>
                        <button onclick="deleteSelectedShape()" class="btn danger">🗑️ Delete Shape</button>
                    </div>
                    
                    <div class="property-group">
                        <h4>💾 Export</h4>
                        <button onclick="exportDiagram('json')" class="btn">📄 Export JSON</button>
                        <button onclick="exportDiagram('svg')" class="btn">🖼️ Export SVG</button>
                        <button onclick="exportDiagram('png')" class="btn">📸 Export PNG</button>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            let diagramData = {data_json};
            let selectedShape = null;
            let currentTool = 'select';
            let isDragging = false;
            let dragOffset = {{ x: 0, y: 0 }};
            let canvasOffset = {{ x: 0, y: 0 }};
            let zoomLevel = 1;
            let shapeCounter = 4;
            let connectionMode = false;
            let connectionStart = null;
            
            function initDiagramEditor() {{
                renderDiagram();
                setupEventListeners();
                updateDiagramSettings();
            }}
            
            function renderDiagram() {{
                const canvas = document.getElementById('diagram-canvas');
                
                // Clear existing shapes
                const existingShapes = canvas.querySelectorAll('.shape');
                existingShapes.forEach(shape => shape.remove());
                
                // Render shapes
                diagramData.shapes.forEach(shapeData => {{
                    const shape = createShapeElement(shapeData);
                    canvas.appendChild(shape);
                }});
                
                // Render connections
                renderConnections();
            }}
            
            function createShapeElement(shapeData) {{
                const shape = document.createElement('div');
                shape.className = `shape ${{shapeData.type}}`;
                shape.id = shapeData.id;
                
                shape.style.left = shapeData.x + 'px';
                shape.style.top = shapeData.y + 'px';
                shape.style.width = shapeData.width + 'px';
                shape.style.height = shapeData.height + 'px';
                shape.style.backgroundColor = shapeData.color;
                shape.style.borderColor = shapeData.borderColor;
                
                const textElement = document.createElement('div');
                textElement.className = 'shape-text';
                textElement.textContent = shapeData.text;
                shape.appendChild(textElement);
                
                // Add controls
                const controls = document.createElement('div');
                controls.className = 'shape-controls';
                controls.innerHTML = `
                    <button class="control-btn connect" onclick="startConnection('${{shapeData.id}}')" title="Connect">🔗</button>
                    <button class="control-btn edit" onclick="editShape('${{shapeData.id}}')" title="Edit">✏️</button>
                    <button class="control-btn delete" onclick="deleteShape('${{shapeData.id}}')" title="Delete">×</button>
                `;
                shape.appendChild(controls);
                
                // Add event listeners
                shape.addEventListener('click', (e) => {{
                    e.stopPropagation();
                    if (connectionMode && connectionStart && connectionStart !== shapeData.id) {{
                        createConnection(connectionStart, shapeData.id);
                        endConnectionMode();
                    }} else {{
                        selectShape(shapeData.id);
                    }}
                }});
                
                shape.addEventListener('mousedown', (e) => {{
                    if (currentTool === 'select' && !connectionMode) {{
                        startDragShape(e, shapeData.id);
                    }}
                }});
                
                return shape;
            }}
            
            function renderConnections() {{
                const svg = document.getElementById('connections-svg');
                const canvas = document.getElementById('diagram-canvas');
                
                svg.style.width = canvas.offsetWidth + 'px';
                svg.style.height = canvas.offsetHeight + 'px';
                svg.innerHTML = svg.innerHTML.replace(/<(?!defs|marker)[^>]*>/g, '');
                
                diagramData.connections.forEach(conn => {{
                    const fromShape = diagramData.shapes.find(s => s.id === conn.from);
                    const toShape = diagramData.shapes.find(s => s.id === conn.to);
                    
                    if (fromShape && toShape) {{
                        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                        line.setAttribute('x1', fromShape.x + fromShape.width / 2);
                        line.setAttribute('y1', fromShape.y + fromShape.height / 2);
                        line.setAttribute('x2', toShape.x + toShape.width / 2);
                        line.setAttribute('y2', toShape.y + toShape.height / 2);
                        line.className = conn.style === 'dashed' ? 'dashed' : '';
                        svg.appendChild(line);
                        
                        // Add label if exists
                        if (conn.label) {{
                            const labelX = (fromShape.x + toShape.x + fromShape.width + toShape.width) / 4;
                            const labelY = (fromShape.y + toShape.y + fromShape.height + toShape.height) / 4;
                            
                            const label = document.createElement('div');
                            label.className = 'connection-label';
                            label.textContent = conn.label;
                            label.style.left = labelX + 'px';
                            label.style.top = labelY + 'px';
                            canvas.appendChild(label);
                        }}
                    }}
                }});
            }}
            
            function setupEventListeners() {{
                const canvas = document.getElementById('diagram-canvas');
                
                // Canvas interaction
                canvas.addEventListener('mousedown', (e) => {{
                    if (currentTool === 'pan') {{
                        startPanCanvas(e);
                    }} else if (connectionMode) {{
                        endConnectionMode();
                    }}
                }});
                
                canvas.addEventListener('click', (e) => {{
                    if (e.target === canvas) {{
                        deselectShape();
                    }}
                }});
                
                document.addEventListener('mousemove', handleMouseMove);
                document.addEventListener('mouseup', handleMouseUp);
                
                // Keyboard shortcuts
                document.addEventListener('keydown', (e) => {{
                    if (e.key === 'Delete' && selectedShape) {{
                        deleteSelectedShape();
                    }} else if (e.key === 'Escape') {{
                        endConnectionMode();
                        deselectShape();
                    }}
                }});
            }}
            
            function setTool(tool) {{
                currentTool = tool;
                document.querySelectorAll('.tool-btn').forEach(btn => {{
                    btn.classList.remove('active');
                }});
                document.querySelector(`[data-tool="${{tool}}"]`).classList.add('active');
                
                const canvas = document.getElementById('diagram-canvas');
                canvas.className = 'diagram-canvas';
                if (tool === 'pan') {{
                    canvas.style.cursor = 'grab';
                }} else if (tool === 'connect') {{
                    canvas.classList.add('connecting-mode');
                }} else {{
                    canvas.style.cursor = 'default';
                }}
            }}
            
            function addShape(type) {{
                shapeCounter++;
                const newShape = {{
                    id: `shape_${{shapeCounter}}`,
                    type: type,
                    text: `New ${{type.charAt(0).toUpperCase() + type.slice(1)}}`,
                    x: 100 + Math.random() * 200,
                    y: 100 + Math.random() * 200,
                    width: type === 'diamond' ? 100 : 120,
                    height: type === 'oval' ? 60 : 80,
                    color: '#e3f2fd',
                    borderColor: '#1976d2'
                }};
                
                diagramData.shapes.push(newShape);
                renderDiagram();
                selectShape(newShape.id);
            }}
            
            function selectShape(shapeId) {{
                selectedShape = shapeId;
                
                // Update visual selection
                document.querySelectorAll('.shape').forEach(shape => {{
                    shape.classList.remove('selected');
                }});
                document.getElementById(shapeId).classList.add('selected');
                
                // Show properties panel
                const shapeData = diagramData.shapes.find(s => s.id === shapeId);
                if (shapeData) {{
                    document.getElementById('shape-text').value = shapeData.text;
                    document.getElementById('shape-width').value = shapeData.width;
                    document.getElementById('shape-height').value = shapeData.height;
                    document.getElementById('shape-color').value = shapeData.color;
                    document.getElementById('shape-border').value = shapeData.borderColor;
                    document.getElementById('shape-properties').style.display = 'block';
                }}
            }}
            
            function deselectShape() {{
                selectedShape = null;
                document.querySelectorAll('.shape').forEach(shape => {{
                    shape.classList.remove('selected');
                }});
                document.getElementById('shape-properties').style.display = 'none';
            }}
            
            function updateSelectedShape() {{
                if (!selectedShape) return;
                
                const shapeData = diagramData.shapes.find(s => s.id === selectedShape);
                if (shapeData) {{
                    shapeData.text = document.getElementById('shape-text').value;
                    shapeData.width = parseInt(document.getElementById('shape-width').value);
                    shapeData.height = parseInt(document.getElementById('shape-height').value);
                    shapeData.color = document.getElementById('shape-color').value;
                    shapeData.borderColor = document.getElementById('shape-border').value;
                    
                    renderDiagram();
                    selectShape(selectedShape);
                }}
            }}
            
            function deleteSelectedShape() {{
                if (!selectedShape) return;
                
                if (confirm('Delete this shape and its connections?')) {{
                    // Remove shape
                    diagramData.shapes = diagramData.shapes.filter(s => s.id !== selectedShape);
                    
                    // Remove related connections
                    diagramData.connections = diagramData.connections.filter(c => 
                        c.from !== selectedShape && c.to !== selectedShape
                    );
                    
                    selectedShape = null;
                    document.getElementById('shape-properties').style.display = 'none';
                    renderDiagram();
                }}
            }}
            
            function startConnection(shapeId) {{
                connectionMode = true;
                connectionStart = shapeId;
                setTool('connect');
                document.getElementById('diagram-canvas').classList.add('connecting-mode');
            }}
            
            function endConnectionMode() {{
                connectionMode = false;
                connectionStart = null;
                document.getElementById('diagram-canvas').classList.remove('connecting-mode');
                setTool('select');
            }}
            
            function createConnection(fromId, toId) {{
                const connId = `conn_${{Date.now()}}`;
                const newConnection = {{
                    id: connId,
                    from: fromId,
                    to: toId,
                    label: '',
                    style: 'solid'
                }};
                
                diagramData.connections.push(newConnection);
                renderDiagram();
            }}
            
            function startDragShape(e, shapeId) {{
                const shapeData = diagramData.shapes.find(s => s.id === shapeId);
                isDragging = true;
                dragOffset = {{
                    x: e.clientX - shapeData.x,
                    y: e.clientY - shapeData.y
                }};
                selectShape(shapeId);
            }}
            
            function handleMouseMove(e) {{
                if (!isDragging) return;
                
                if (currentTool === 'pan') {{
                    // Pan canvas
                    canvasOffset.x = e.clientX - dragOffset.x;
                    canvasOffset.y = e.clientY - dragOffset.y;
                    document.getElementById('diagram-canvas').style.transform = 
                        `translate(${{canvasOffset.x}}px, ${{canvasOffset.y}}px) scale(${{zoomLevel}})`;
                }} else if (selectedShape) {{
                    // Drag shape
                    const shapeData = diagramData.shapes.find(s => s.id === selectedShape);
                    if (shapeData) {{
                        shapeData.x = e.clientX - dragOffset.x;
                        shapeData.y = e.clientY - dragOffset.y;
                        
                        const shapeElement = document.getElementById(selectedShape);
                        shapeElement.style.left = shapeData.x + 'px';
                        shapeElement.style.top = shapeData.y + 'px';
                        
                        renderConnections();
                    }}
                }}
            }}
            
            function handleMouseUp() {{
                isDragging = false;
            }}
            
            function alignShapes(alignment) {{
                const selectedShapes = document.querySelectorAll('.shape.selected');
                if (selectedShapes.length < 2) return;
                
                const shapes = Array.from(selectedShapes).map(el => 
                    diagramData.shapes.find(s => s.id === el.id)
                );
                
                if (alignment === 'left') {{
                    const leftX = Math.min(...shapes.map(s => s.x));
                    shapes.forEach(s => s.x = leftX);
                }} else if (alignment === 'right') {{
                    const rightX = Math.max(...shapes.map(s => s.x + s.width));
                    shapes.forEach(s => s.x = rightX - s.width);
                }} else if (alignment === 'center') {{
                    const centerX = shapes.reduce((sum, s) => sum + s.x + s.width/2, 0) / shapes.length;
                    shapes.forEach(s => s.x = centerX - s.width/2);
                }}
                
                renderDiagram();
            }}
            
            function zoom(factor) {{
                zoomLevel *= factor;
                zoomLevel = Math.max(0.1, Math.min(3, zoomLevel));
                document.getElementById('diagram-canvas').style.transform = 
                    `translate(${{canvasOffset.x}}px, ${{canvasOffset.y}}px) scale(${{zoomLevel}})`;
            }}
            
            function resetZoom() {{
                zoomLevel = 1;
                canvasOffset = {{ x: 0, y: 0 }};
                document.getElementById('diagram-canvas').style.transform = 'translate(0px, 0px) scale(1)';
            }}
            
            function resetView() {{
                resetZoom();
                deselectShape();
                endConnectionMode();
            }}
            
            function updateDiagramSettings() {{
                diagramData.title = document.getElementById('diagram-title').value;
                diagramData.type = document.getElementById('diagram-type').value;
            }}
            
            function exportDiagram(format = 'json') {{
                if (format === 'json') {{
                    const exportData = {{
                        ...diagramData,
                        export_date: new Date().toISOString(),
                        version: '1.0'
                    }};
                    
                    const blob = new Blob([JSON.stringify(exportData, null, 2)], {{ type: 'application/json' }});
                    const link = document.createElement('a');
                    link.download = `diagram-${{new Date().toISOString().slice(0, 19).replace(/:/g, '-')}}.json`;
                    link.href = URL.createObjectURL(blob);
                    link.click();
                }} else if (format === 'svg') {{
                    // Create SVG export
                    const svgContent = generateSVGExport();
                    const blob = new Blob([svgContent], {{ type: 'image/svg+xml' }});
                    const link = document.createElement('a');
                    link.download = `diagram-${{new Date().toISOString().slice(0, 19).replace(/:/g, '-')}}.svg`;
                    link.href = URL.createObjectURL(blob);
                    link.click();
                }}
            }}
            
            function generateSVGExport() {{
                let svg = `<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600">`;
                
                // Add shapes
                diagramData.shapes.forEach(shape => {{
                    if (shape.type === 'rectangle') {{
                        svg += `<rect x="${{shape.x}}" y="${{shape.y}}" width="${{shape.width}}" height="${{shape.height}}" 
                                fill="${{shape.color}}" stroke="${{shape.borderColor}}" stroke-width="2"/>`;
                    }} else if (shape.type === 'oval') {{
                        svg += `<ellipse cx="${{shape.x + shape.width/2}}" cy="${{shape.y + shape.height/2}}" 
                                rx="${{shape.width/2}}" ry="${{shape.height/2}}" 
                                fill="${{shape.color}}" stroke="${{shape.borderColor}}" stroke-width="2"/>`;
                    }}
                    
                    svg += `<text x="${{shape.x + shape.width/2}}" y="${{shape.y + shape.height/2}}" 
                            text-anchor="middle" dominant-baseline="middle" 
                            font-family="Arial" font-size="12">${{shape.text}}</text>`;
                }});
                
                // Add connections
                diagramData.connections.forEach(conn => {{
                    const fromShape = diagramData.shapes.find(s => s.id === conn.from);
                    const toShape = diagramData.shapes.find(s => s.id === conn.to);
                    if (fromShape && toShape) {{
                        svg += `<line x1="${{fromShape.x + fromShape.width/2}}" y1="${{fromShape.y + fromShape.height/2}}" 
                                x2="${{toShape.x + toShape.width/2}}" y2="${{toShape.y + toShape.height/2}}" 
                                stroke="#6c757d" stroke-width="2" marker-end="url(#arrowhead)"/>`;
                    }}
                }});
                
                svg += '</svg>';
                return svg;
            }}
            
            function editShape(shapeId) {{
                const shapeData = diagramData.shapes.find(s => s.id === shapeId);
                if (shapeData) {{
                    const newText = prompt('Edit shape text:', shapeData.text);
                    if (newText !== null) {{
                        shapeData.text = newText;
                        renderDiagram();
                        selectShape(shapeId);
                    }}
                }}
            }}
            
            // Initialize the diagram editor
            initDiagramEditor();
        </script>
    </body>
    </html>
    """
    
    # Use Streamlit's HTML component
    components.html(component_html, width=width, height=height)
    
    # Return None due to Streamlit version compatibility
    return None
