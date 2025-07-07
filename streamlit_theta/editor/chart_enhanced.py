"""
Enhanced Chart Editor - Interactive data visualization creator with advanced features

Provides comprehensive chart creation with:
- Multiple chart types (bar, line, pie, scatter, area, histogram, heatmap)
- Real-time data editing and preview
- Multiple view modes (edit, preview, split)
- Theme support
- Template system
- Export capabilities
- Collaboration features
"""

import streamlit as st
import streamlit.components.v1 as components
import json
from typing import Dict, List, Any, Optional
import sys
import os

# Add the parent directory to sys.path to import theme_manager
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from theme_manager import ThemeManager

def theta_chart_editor_enhanced(
    data: Optional[List[List[Any]]] = None,
    chart_type: str = "bar",
    width: int = 900,
    height: int = 600,
    theme: str = "light",
    mode: str = "edit",  # edit, preview, split
    enable_animations: bool = True,
    enable_interactivity: bool = True,
    templates: Optional[List[Dict[str, Any]]] = None,
    key: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    Enhanced chart editor with advanced features and modes.
    
    Parameters:
    -----------
    data : List[List[Any]]
        Data for the chart (first row should be headers)
    chart_type : str
        Type of chart (bar, line, pie, scatter, area, histogram, heatmap)
    width : int
        Width of the editor in pixels
    height : int  
        Height of the editor in pixels
    theme : str
        Theme name (light, dark, blue, green, purple)
    mode : str
        Editor mode (edit, preview, split)
    enable_animations : bool
        Enable chart animations
    enable_interactivity : bool
        Enable interactive features
    templates : List[Dict[str, Any]]
        Chart templates
    key : str or None
        Unique key for the component
    
    Returns:
    --------
    Dict[str, Any] or None
        Chart configuration and data
    """
    
    # Default data if none provided
    if data is None:
        data = [
            ["Month", "Sales", "Marketing", "Support"],
            ["Jan", 120, 80, 60],
            ["Feb", 150, 95, 75],
            ["Mar", 180, 110, 85],
            ["Apr", 200, 125, 95],
            ["May", 220, 140, 105],
            ["Jun", 250, 160, 120]
        ]
    
    # Default templates
    if templates is None:
        templates = [
            {
                "name": "Sales Dashboard",
                "type": "bar",
                "data": [
                    ["Quarter", "Q1", "Q2", "Q3", "Q4"],
                    ["Sales", 120000, 150000, 180000, 200000],
                    ["Target", 100000, 140000, 170000, 190000]
                ],
                "config": {
                    "colors": ["#3498db", "#e74c3c"],
                    "showLegend": True,
                    "showGrid": True
                }
            },
            {
                "name": "Website Analytics",
                "type": "line",
                "data": [
                    ["Date", "Visitors", "Page Views", "Bounce Rate"],
                    ["Mon", 1200, 2400, 35],
                    ["Tue", 1500, 2800, 32],
                    ["Wed", 1800, 3200, 28],
                    ["Thu", 2100, 3600, 25],
                    ["Fri", 2500, 4000, 22],
                    ["Sat", 1800, 2800, 40],
                    ["Sun", 1200, 2000, 45]
                ],
                "config": {
                    "colors": ["#2ecc71", "#f39c12", "#e74c3c"],
                    "smooth": True,
                    "showDataPoints": True
                }
            },
            {
                "name": "Market Share",
                "type": "pie",
                "data": [
                    ["Company", "Market Share"],
                    ["Company A", 35],
                    ["Company B", 25],
                    ["Company C", 20],
                    ["Company D", 15],
                    ["Others", 5]
                ],
                "config": {
                    "colors": ["#3498db", "#e74c3c", "#2ecc71", "#f39c12", "#9b59b6"],
                    "showLabels": True,
                    "showPercentages": True
                }
            },
            {
                "name": "Correlation Analysis",
                "type": "scatter",
                "data": [
                    ["X", "Y", "Size"],
                    [10, 20, 5],
                    [15, 25, 8],
                    [20, 30, 12],
                    [25, 35, 15],
                    [30, 40, 18],
                    [35, 45, 22]
                ],
                "config": {
                    "colors": ["#3498db"],
                    "showTrendline": True,
                    "bubbleSize": True
                }
            }
        ]
    
    # Get theme CSS
    theme_css = ThemeManager.generate_css(theme)
    theme_switcher_html = ThemeManager.get_theme_switcher_html(theme)
    theme_switcher_js = ThemeManager.get_theme_switcher_js()
    
    # Convert data and templates to JSON
    data_json = json.dumps(data)
    templates_json = json.dumps(templates)
    
    component_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Enhanced Chart Editor</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            {theme_css}
            
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
                background: var(--secondary-bg);
                color: var(--text-primary);
                overflow: hidden;
            }}
            
            .chart-editor {{
                width: 100%;
                height: 100vh;
                display: flex;
                flex-direction: column;
                background: var(--primary-bg);
                border-radius: 8px;
                box-shadow: var(--shadow);
                overflow: hidden;
                position: relative;
            }}
            
            .header {{
                background: var(--secondary-bg);
                border-bottom: 1px solid var(--border-color);
                padding: 12px 16px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                flex-wrap: wrap;
                gap: 12px;
                min-height: 60px;
            }}
            
            .header-left {{
                display: flex;
                align-items: center;
                gap: 12px;
            }}
            
            .header-right {{
                display: flex;
                align-items: center;
                gap: 12px;
            }}
            
            .mode-switcher {{
                display: flex;
                background: var(--tertiary-bg);
                border-radius: 6px;
                padding: 2px;
                gap: 2px;
            }}
            
            .mode-btn {{
                background: transparent;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                cursor: pointer;
                color: var(--text-secondary);
                font-size: 14px;
                transition: all 0.2s ease;
            }}
            
            .mode-btn.active {{
                background: var(--accent-color);
                color: var(--primary-bg);
            }}
            
            .chart-type-selector {{
                display: flex;
                gap: 4px;
                align-items: center;
            }}
            
            .chart-type-btn {{
                background: var(--tertiary-bg);
                border: 1px solid var(--border-color);
                border-radius: 4px;
                padding: 8px 12px;
                cursor: pointer;
                transition: all 0.2s ease;
                font-size: 12px;
                color: var(--text-secondary);
            }}
            
            .chart-type-btn.active {{
                background: var(--accent-color);
                color: var(--primary-bg);
                border-color: var(--accent-color);
            }}
            
            .content-area {{
                flex: 1;
                display: flex;
                overflow: hidden;
            }}
            
            .data-panel {{
                width: 300px;
                background: var(--secondary-bg);
                border-right: 1px solid var(--border-color);
                display: flex;
                flex-direction: column;
                overflow: hidden;
            }}
            
            .data-panel.hidden {{
                display: none;
            }}
            
            .chart-area {{
                flex: 1;
                display: flex;
                flex-direction: column;
                overflow: hidden;
            }}
            
            .chart-container {{
                flex: 1;
                padding: 20px;
                display: flex;
                align-items: center;
                justify-content: center;
                background: var(--primary-bg);
                position: relative;
            }}
            
            .chart-canvas {{
                max-width: 100%;
                max-height: 100%;
            }}
            
            .data-table {{
                flex: 1;
                overflow: auto;
                padding: 16px;
            }}
            
            .data-table table {{
                width: 100%;
                border-collapse: collapse;
                font-size: 12px;
            }}
            
            .data-table th,
            .data-table td {{
                border: 1px solid var(--border-color);
                padding: 6px 8px;
                text-align: left;
            }}
            
            .data-table th {{
                background: var(--tertiary-bg);
                color: var(--text-primary);
                font-weight: 600;
            }}
            
            .data-table input {{
                width: 100%;
                border: none;
                background: transparent;
                color: var(--text-primary);
                font-size: 12px;
                padding: 2px;
            }}
            
            .data-table input:focus {{
                outline: 2px solid var(--accent-color);
                outline-offset: -2px;
            }}
            
            .data-controls {{
                padding: 16px;
                border-top: 1px solid var(--border-color);
                display: flex;
                gap: 8px;
                flex-wrap: wrap;
            }}
            
            .data-controls .theta-button {{
                font-size: 12px;
                padding: 6px 12px;
                height: auto;
                min-width: auto;
            }}
            
            .config-panel {{
                width: 280px;
                background: var(--secondary-bg);
                border-left: 1px solid var(--border-color);
                display: flex;
                flex-direction: column;
                overflow-y: auto;
                padding: 16px;
            }}
            
            .config-panel.hidden {{
                display: none;
            }}
            
            .config-section {{
                margin-bottom: 20px;
            }}
            
            .config-section h3 {{
                color: var(--text-primary);
                margin-bottom: 12px;
                font-size: 14px;
                font-weight: 600;
            }}
            
            .config-option {{
                margin-bottom: 12px;
            }}
            
            .config-option label {{
                display: block;
                margin-bottom: 4px;
                color: var(--text-secondary);
                font-size: 12px;
            }}
            
            .config-option input,
            .config-option select {{
                width: 100%;
                padding: 6px 8px;
                border: 1px solid var(--border-color);
                border-radius: 4px;
                background: var(--primary-bg);
                color: var(--text-primary);
                font-size: 12px;
            }}
            
            .config-option input[type="checkbox"] {{
                width: auto;
                margin-right: 8px;
            }}
            
            .color-picker {{
                display: flex;
                gap: 4px;
                flex-wrap: wrap;
                margin-top: 8px;
            }}
            
            .color-option {{
                width: 24px;
                height: 24px;
                border-radius: 4px;
                cursor: pointer;
                border: 2px solid transparent;
                transition: all 0.2s ease;
            }}
            
            .color-option.selected {{
                border-color: var(--accent-color);
                transform: scale(1.1);
            }}
            
            .templates-panel {{
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.5);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 1000;
            }}
            
            .templates-content {{
                background: var(--primary-bg);
                border: 1px solid var(--border-color);
                border-radius: 8px;
                padding: 24px;
                max-width: 800px;
                max-height: 600px;
                overflow-y: auto;
                box-shadow: var(--shadow-hover);
            }}
            
            .templates-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
                gap: 16px;
                margin-top: 16px;
            }}
            
            .template-card {{
                background: var(--secondary-bg);
                border: 1px solid var(--border-color);
                border-radius: 6px;
                padding: 16px;
                cursor: pointer;
                transition: all 0.2s ease;
                text-align: center;
            }}
            
            .template-card:hover {{
                background: var(--tertiary-bg);
                border-color: var(--accent-color);
                transform: translateY(-2px);
            }}
            
            .template-preview {{
                width: 100%;
                height: 100px;
                background: var(--tertiary-bg);
                border-radius: 4px;
                margin-bottom: 8px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 24px;
            }}
            
            .template-name {{
                font-weight: 600;
                color: var(--text-primary);
                margin-bottom: 4px;
            }}
            
            .template-type {{
                font-size: 12px;
                color: var(--text-secondary);
                background: var(--tertiary-bg);
                padding: 2px 6px;
                border-radius: 3px;
                display: inline-block;
            }}
            
            .status-bar {{
                background: var(--secondary-bg);
                border-top: 1px solid var(--border-color);
                padding: 8px 16px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 12px;
                color: var(--text-secondary);
            }}
            
            .export-menu {{
                position: absolute;
                top: 100%;
                right: 0;
                background: var(--primary-bg);
                border: 1px solid var(--border-color);
                border-radius: 4px;
                box-shadow: var(--shadow-hover);
                z-index: 100;
                min-width: 150px;
            }}
            
            .export-option {{
                padding: 8px 12px;
                cursor: pointer;
                transition: background 0.2s ease;
                font-size: 12px;
            }}
            
            .export-option:hover {{
                background: var(--tertiary-bg);
            }}
            
            .hidden {{
                display: none !important;
            }}
            
            /* Responsive design */
            @media (max-width: 768px) {{
                .header {{
                    flex-direction: column;
                    align-items: stretch;
                }}
                
                .content-area {{
                    flex-direction: column;
                }}
                
                .data-panel,
                .config-panel {{
                    width: 100%;
                    max-height: 200px;
                }}
                
                .chart-type-selector {{
                    flex-wrap: wrap;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="chart-editor theta-editor" data-theme="{theme}">
            {theme_switcher_html}
            
            <div class="header">
                <div class="header-left">
                    <h3>📊 Enhanced Chart Editor</h3>
                    <div class="mode-switcher">
                        <button class="mode-btn active" data-mode="edit">✏️ Edit</button>
                        <button class="mode-btn" data-mode="preview">👁️ Preview</button>
                        <button class="mode-btn" data-mode="split">↔️ Split</button>
                    </div>
                </div>
                <div class="header-right">
                    <button class="theta-button" onclick="showTemplates()">📋 Templates</button>
                    <button class="theta-button" onclick="toggleDataPanel()">📊 Data</button>
                    <button class="theta-button" onclick="toggleConfigPanel()">⚙️ Config</button>
                    <div style="position: relative;">
                        <button class="theta-button" onclick="toggleExportMenu()">📤 Export</button>
                        <div class="export-menu hidden" id="export-menu">
                            <div class="export-option" onclick="exportChart('png')">📸 PNG Image</div>
                            <div class="export-option" onclick="exportChart('json')">📋 JSON Data</div>
                            <div class="export-option" onclick="exportChart('csv')">📊 CSV Data</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="chart-type-selector" style="padding: 12px 16px; border-bottom: 1px solid var(--border-color);">
                <button class="chart-type-btn active" data-type="bar">📊 Bar</button>
                <button class="chart-type-btn" data-type="line">📈 Line</button>
                <button class="chart-type-btn" data-type="pie">🥧 Pie</button>
                <button class="chart-type-btn" data-type="scatter">⚫ Scatter</button>
                <button class="chart-type-btn" data-type="area">📉 Area</button>
                <button class="chart-type-btn" data-type="doughnut">🍩 Doughnut</button>
                <button class="chart-type-btn" data-type="radar">🕸️ Radar</button>
            </div>
            
            <div class="content-area">
                <div class="data-panel" id="data-panel">
                    <div class="data-table">
                        <table id="data-table">
                            <!-- Data table will be populated by JavaScript -->
                        </table>
                    </div>
                    <div class="data-controls">
                        <button class="theta-button" onclick="addRow()">➕ Row</button>
                        <button class="theta-button" onclick="addColumn()">➕ Column</button>
                        <button class="theta-button" onclick="deleteRow()">➖ Row</button>
                        <button class="theta-button" onclick="deleteColumn()">➖ Column</button>
                    </div>
                </div>
                
                <div class="chart-area">
                    <div class="chart-container">
                        <canvas id="chart-canvas" class="chart-canvas"></canvas>
                    </div>
                </div>
                
                <div class="config-panel" id="config-panel">
                    <div class="config-section">
                        <h3>🎨 Appearance</h3>
                        <div class="config-option">
                            <label>Chart Title</label>
                            <input type="text" id="chart-title" value="My Chart" onchange="updateChart()">
                        </div>
                        <div class="config-option">
                            <label>Color Scheme</label>
                            <div class="color-picker" id="color-picker">
                                <!-- Color options will be populated by JavaScript -->
                            </div>
                        </div>
                        <div class="config-option">
                            <label>
                                <input type="checkbox" id="show-legend" checked onchange="updateChart()">
                                Show Legend
                            </label>
                        </div>
                        <div class="config-option">
                            <label>
                                <input type="checkbox" id="show-grid" checked onchange="updateChart()">
                                Show Grid
                            </label>
                        </div>
                    </div>
                    
                    <div class="config-section">
                        <h3>📐 Layout</h3>
                        <div class="config-option">
                            <label>Width</label>
                            <input type="range" id="chart-width" min="300" max="800" value="600" onchange="updateChart()">
                        </div>
                        <div class="config-option">
                            <label>Height</label>
                            <input type="range" id="chart-height" min="200" max="600" value="400" onchange="updateChart()">
                        </div>
                        <div class="config-option">
                            <label>Legend Position</label>
                            <select id="legend-position" onchange="updateChart()">
                                <option value="top">Top</option>
                                <option value="bottom">Bottom</option>
                                <option value="left">Left</option>
                                <option value="right">Right</option>
                            </select>
                        </div>
                    </div>
                    
                    <div class="config-section">
                        <h3>🎭 Animation</h3>
                        <div class="config-option">
                            <label>
                                <input type="checkbox" id="enable-animation" {"checked" if enable_animations else ""} onchange="updateChart()">
                                Enable Animations
                            </label>
                        </div>
                        <div class="config-option">
                            <label>Animation Duration</label>
                            <input type="range" id="animation-duration" min="0" max="3000" value="1000" onchange="updateChart()">
                        </div>
                    </div>
                    
                    <div class="config-section">
                        <h3>🖱️ Interaction</h3>
                        <div class="config-option">
                            <label>
                                <input type="checkbox" id="enable-hover" {"checked" if enable_interactivity else ""} onchange="updateChart()">
                                Enable Hover Effects
                            </label>
                        </div>
                        <div class="config-option">
                            <label>
                                <input type="checkbox" id="enable-click" {"checked" if enable_interactivity else ""} onchange="updateChart()">
                                Enable Click Events
                            </label>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="status-bar">
                <div>
                    <span>Data Points: <span id="data-points">0</span></span>
                    <span style="margin-left: 16px;">Series: <span id="series-count">0</span></span>
                </div>
                <div>
                    <span>Mode: <span id="current-mode">Edit</span></span>
                </div>
            </div>
        </div>
        
        <div class="templates-panel hidden" id="templates-panel">
            <div class="templates-content">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                    <h2>📋 Chart Templates</h2>
                    <button class="theta-button" onclick="hideTemplates()">✕ Close</button>
                </div>
                <div class="templates-grid" id="templates-grid">
                    <!-- Templates will be populated by JavaScript -->
                </div>
            </div>
        </div>
        
        <script>
            {theme_switcher_js}
            
            // Global variables
            let currentMode = 'edit';
            let currentChartType = '{chart_type}';
            let chartData = {data_json};
            let templates = {templates_json};
            let chart = null;
            let chartConfig = {{
                title: 'My Chart',
                colors: ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c', '#34495e', '#f1c40f'],
                showLegend: true,
                showGrid: true,
                legendPosition: 'top',
                enableAnimation: {str(enable_animations).lower()},
                animationDuration: 1000,
                enableHover: {str(enable_interactivity).lower()},
                enableClick: {str(enable_interactivity).lower()}
            }};
            
            // Initialize editor
            document.addEventListener('DOMContentLoaded', function() {{
                setupEventListeners();
                populateDataTable();
                populateTemplates();
                setupColorPicker();
                updateChart();
                updateStats();
            }});
            
            function setupEventListeners() {{
                // Mode switching
                document.querySelectorAll('.mode-btn').forEach(btn => {{
                    btn.addEventListener('click', function() {{
                        switchMode(this.dataset.mode);
                    }});
                }});
                
                // Chart type switching
                document.querySelectorAll('.chart-type-btn').forEach(btn => {{
                    btn.addEventListener('click', function() {{
                        switchChartType(this.dataset.type);
                    }});
                }});
                
                // Close export menu when clicking outside
                document.addEventListener('click', function(e) {{
                    if (!e.target.closest('.export-menu') && !e.target.closest('button[onclick="toggleExportMenu()"]')) {{
                        document.getElementById('export-menu').classList.add('hidden');
                    }}
                }});
            }}
            
            function switchMode(mode) {{
                currentMode = mode;
                document.querySelectorAll('.mode-btn').forEach(btn => {{
                    btn.classList.toggle('active', btn.dataset.mode === mode);
                }});
                
                const dataPanel = document.getElementById('data-panel');
                const configPanel = document.getElementById('config-panel');
                
                switch(mode) {{
                    case 'edit':
                        dataPanel.classList.remove('hidden');
                        configPanel.classList.remove('hidden');
                        break;
                    case 'preview':
                        dataPanel.classList.add('hidden');
                        configPanel.classList.add('hidden');
                        break;
                    case 'split':
                        dataPanel.classList.add('hidden');
                        configPanel.classList.remove('hidden');
                        break;
                }}
                
                document.getElementById('current-mode').textContent = mode.charAt(0).toUpperCase() + mode.slice(1);
            }}
            
            function switchChartType(type) {{
                currentChartType = type;
                document.querySelectorAll('.chart-type-btn').forEach(btn => {{
                    btn.classList.toggle('active', btn.dataset.type === type);
                }});
                updateChart();
            }}
            
            function populateDataTable() {{
                const table = document.getElementById('data-table');
                table.innerHTML = '';
                
                chartData.forEach((row, rowIndex) => {{
                    const tr = document.createElement('tr');
                    
                    row.forEach((cell, colIndex) => {{
                        const cellElement = rowIndex === 0 ? document.createElement('th') : document.createElement('td');
                        
                        if (rowIndex === 0) {{
                            cellElement.textContent = cell;
                        }} else {{
                            const input = document.createElement('input');
                            input.type = typeof cell === 'number' ? 'number' : 'text';
                            input.value = cell;
                            input.addEventListener('change', function() {{
                                const value = this.type === 'number' ? parseFloat(this.value) || 0 : this.value;
                                chartData[rowIndex][colIndex] = value;
                                updateChart();
                                updateStats();
                            }});
                            cellElement.appendChild(input);
                        }}
                        
                        tr.appendChild(cellElement);
                    }});
                    
                    table.appendChild(tr);
                }});
            }}
            
            function populateTemplates() {{
                const grid = document.getElementById('templates-grid');
                grid.innerHTML = '';
                
                templates.forEach(template => {{
                    const card = document.createElement('div');
                    card.className = 'template-card';
                    
                    const preview = document.createElement('div');
                    preview.className = 'template-preview';
                    preview.textContent = getChartEmoji(template.type);
                    
                    const name = document.createElement('div');
                    name.className = 'template-name';
                    name.textContent = template.name;
                    
                    const type = document.createElement('div');
                    type.className = 'template-type';
                    type.textContent = template.type.charAt(0).toUpperCase() + template.type.slice(1);
                    
                    card.appendChild(preview);
                    card.appendChild(name);
                    card.appendChild(type);
                    
                    card.addEventListener('click', function() {{
                        loadTemplate(template);
                    }});
                    
                    grid.appendChild(card);
                }});
            }}
            
            function getChartEmoji(type) {{
                const emojis = {{
                    'bar': '📊',
                    'line': '📈',
                    'pie': '🥧',
                    'scatter': '⚫',
                    'area': '📉',
                    'doughnut': '🍩',
                    'radar': '🕸️'
                }};
                return emojis[type] || '📊';
            }}
            
            function loadTemplate(template) {{
                chartData = template.data;
                currentChartType = template.type;
                
                // Update chart type buttons
                document.querySelectorAll('.chart-type-btn').forEach(btn => {{
                    btn.classList.toggle('active', btn.dataset.type === template.type);
                }});
                
                // Update config if provided
                if (template.config) {{
                    Object.assign(chartConfig, template.config);
                    updateConfigUI();
                }}
                
                populateDataTable();
                updateChart();
                updateStats();
                hideTemplates();
            }}
            
            function updateConfigUI() {{
                document.getElementById('chart-title').value = chartConfig.title;
                document.getElementById('show-legend').checked = chartConfig.showLegend;
                document.getElementById('show-grid').checked = chartConfig.showGrid;
                document.getElementById('legend-position').value = chartConfig.legendPosition;
                document.getElementById('enable-animation').checked = chartConfig.enableAnimation;
                document.getElementById('animation-duration').value = chartConfig.animationDuration;
                document.getElementById('enable-hover').checked = chartConfig.enableHover;
                document.getElementById('enable-click').checked = chartConfig.enableClick;
            }}
            
            function setupColorPicker() {{
                const colorPicker = document.getElementById('color-picker');
                const colorSchemes = [
                    ['#3498db', '#e74c3c', '#2ecc71', '#f39c12'],
                    ['#9b59b6', '#1abc9c', '#34495e', '#f1c40f'],
                    ['#e67e22', '#95a5a6', '#16a085', '#27ae60'],
                    ['#2980b9', '#8e44ad', '#c0392b', '#d35400'],
                    ['#7f8c8d', '#ecf0f1', '#bdc3c7', '#95a5a6']
                ];
                
                colorSchemes.forEach((scheme, index) => {{
                    const colorDiv = document.createElement('div');
                    colorDiv.className = 'color-option';
                    colorDiv.style.background = `linear-gradient(45deg, ${{scheme[0]}} 25%, ${{scheme[1]}} 25%, ${{scheme[1]}} 50%, ${{scheme[2]}} 50%, ${{scheme[2]}} 75%, ${{scheme[3]}} 75%)`;
                    colorDiv.addEventListener('click', function() {{
                        chartConfig.colors = scheme;
                        updateChart();
                        
                        // Update selection
                        document.querySelectorAll('.color-option').forEach(opt => opt.classList.remove('selected'));
                        this.classList.add('selected');
                    }});
                    
                    if (index === 0) {{
                        colorDiv.classList.add('selected');
                    }}
                    
                    colorPicker.appendChild(colorDiv);
                }});
            }}
            
            function updateChart() {{
                const ctx = document.getElementById('chart-canvas').getContext('2d');
                
                // Read config from UI
                chartConfig.title = document.getElementById('chart-title').value;
                chartConfig.showLegend = document.getElementById('show-legend').checked;
                chartConfig.showGrid = document.getElementById('show-grid').checked;
                chartConfig.legendPosition = document.getElementById('legend-position').value;
                chartConfig.enableAnimation = document.getElementById('enable-animation').checked;
                chartConfig.animationDuration = parseInt(document.getElementById('animation-duration').value);
                chartConfig.enableHover = document.getElementById('enable-hover').checked;
                chartConfig.enableClick = document.getElementById('enable-click').checked;
                
                // Prepare data for Chart.js
                const labels = chartData[0].slice(1);
                const datasets = [];
                
                for (let i = 1; i < chartData.length; i++) {{
                    const row = chartData[i];
                    datasets.push({{
                        label: row[0],
                        data: row.slice(1),
                        backgroundColor: currentChartType === 'pie' || currentChartType === 'doughnut' ? 
                            chartConfig.colors.slice(0, row.slice(1).length) : 
                            chartConfig.colors[(i - 1) % chartConfig.colors.length],
                        borderColor: chartConfig.colors[(i - 1) % chartConfig.colors.length],
                        borderWidth: 2,
                        fill: currentChartType === 'area'
                    }});
                }}
                
                // Chart configuration
                const config = {{
                    type: currentChartType,
                    data: {{
                        labels: labels,
                        datasets: datasets
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{
                            title: {{
                                display: true,
                                text: chartConfig.title,
                                font: {{
                                    size: 16,
                                    weight: 'bold'
                                }}
                            }},
                            legend: {{
                                display: chartConfig.showLegend,
                                position: chartConfig.legendPosition
                            }},
                            tooltip: {{
                                enabled: chartConfig.enableHover
                            }}
                        }},
                        scales: currentChartType === 'pie' || currentChartType === 'doughnut' ? {{}} : {{
                            y: {{
                                grid: {{
                                    display: chartConfig.showGrid
                                }},
                                beginAtZero: true
                            }},
                            x: {{
                                grid: {{
                                    display: chartConfig.showGrid
                                }}
                            }}
                        }},
                        animation: {{
                            duration: chartConfig.enableAnimation ? chartConfig.animationDuration : 0
                        }},
                        onHover: chartConfig.enableHover ? null : function() {{}},
                        onClick: chartConfig.enableClick ? function(event, elements) {{
                            if (elements.length > 0) {{
                                const element = elements[0];
                                const datasetIndex = element.datasetIndex;
                                const index = element.index;
                                console.log('Clicked:', datasets[datasetIndex].label, labels[index]);
                            }}
                        }} : null
                    }}
                }};
                
                // Destroy existing chart
                if (chart) {{
                    chart.destroy();
                }}
                
                // Create new chart
                chart = new Chart(ctx, config);
            }}
            
            function updateStats() {{
                const dataPoints = (chartData.length - 1) * (chartData[0].length - 1);
                const seriesCount = chartData.length - 1;
                
                document.getElementById('data-points').textContent = dataPoints;
                document.getElementById('series-count').textContent = seriesCount;
            }}
            
            function addRow() {{
                const newRow = ['Series ' + chartData.length];
                for (let i = 1; i < chartData[0].length; i++) {{
                    newRow.push(0);
                }}
                chartData.push(newRow);
                populateDataTable();
                updateChart();
                updateStats();
            }}
            
            function addColumn() {{
                const newLabel = 'Column ' + chartData[0].length;
                chartData[0].push(newLabel);
                for (let i = 1; i < chartData.length; i++) {{
                    chartData[i].push(0);
                }}
                populateDataTable();
                updateChart();
                updateStats();
            }}
            
            function deleteRow() {{
                if (chartData.length > 2) {{
                    chartData.pop();
                    populateDataTable();
                    updateChart();
                    updateStats();
                }}
            }}
            
            function deleteColumn() {{
                if (chartData[0].length > 2) {{
                    for (let i = 0; i < chartData.length; i++) {{
                        chartData[i].pop();
                    }}
                    populateDataTable();
                    updateChart();
                    updateStats();
                }}
            }}
            
            function toggleDataPanel() {{
                const panel = document.getElementById('data-panel');
                panel.classList.toggle('hidden');
            }}
            
            function toggleConfigPanel() {{
                const panel = document.getElementById('config-panel');
                panel.classList.toggle('hidden');
            }}
            
            function showTemplates() {{
                document.getElementById('templates-panel').classList.remove('hidden');
            }}
            
            function hideTemplates() {{
                document.getElementById('templates-panel').classList.add('hidden');
            }}
            
            function toggleExportMenu() {{
                const menu = document.getElementById('export-menu');
                menu.classList.toggle('hidden');
            }}
            
            function exportChart(format) {{
                const exportData = {{
                    type: currentChartType,
                    data: chartData,
                    config: chartConfig,
                    format: format,
                    timestamp: new Date().toISOString()
                }};
                
                let filename, content, mimeType;
                
                switch(format) {{
                    case 'png':
                        const canvas = document.getElementById('chart-canvas');
                        const imageData = canvas.toDataURL('image/png');
                        filename = `chart-${{new Date().toISOString().slice(0, 19).replace(/:/g, '-')}}.png`;
                        downloadFile(imageData, filename);
                        break;
                    case 'json':
                        content = JSON.stringify(exportData, null, 2);
                        filename = `chart-${{new Date().toISOString().slice(0, 19).replace(/:/g, '-')}}.json`;
                        mimeType = 'application/json';
                        downloadFile('data:' + mimeType + ';charset=utf-8,' + encodeURIComponent(content), filename);
                        break;
                    case 'csv':
                        content = chartData.map(row => row.join(',')).join('\\n');
                        filename = `chart-data-${{new Date().toISOString().slice(0, 19).replace(/:/g, '-')}}.csv`;
                        mimeType = 'text/csv';
                        downloadFile('data:' + mimeType + ';charset=utf-8,' + encodeURIComponent(content), filename);
                        break;
                }}
                
                // Send to Streamlit
                window.parent.postMessage({{
                    type: 'streamlit:setComponentValue',
                    value: exportData
                }}, '*');
                
                document.getElementById('export-menu').classList.add('hidden');
            }}
            
            function downloadFile(data, filename) {{
                const link = document.createElement('a');
                link.download = filename;
                link.href = data;
                link.click();
            }}
        </script>
    </body>
    </html>
    """
    
    # Create component with the generated HTML
    component_value = components.html(
        component_html,
        width=width,
        height=height,
        key=key
    )
    
    return component_value