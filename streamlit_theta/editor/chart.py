"""
Theta Chart Editor - Interactive data visualization creator for Streamlit
Provides a visual interface for creating charts and graphs.
"""

import streamlit as st
import streamlit.components.v1 as components
import json
from typing import Dict, List, Any, Optional

def theta_chart_editor(
    data: Optional[List[List[Any]]] = None,
    chart_type: str = "bar",
    width: int = 900,
    height: int = 600,
    key: Optional[str] = None
) -> None:
    """
    Create an interactive chart/graph editor.
    
    Parameters:
    -----------
    data : List[List[Any]]
        Data for the chart (first row should be headers)
    chart_type : str
        Type of chart (bar, line, pie, scatter, area)
    width : int
        Width of the editor in pixels
    height : int  
        Height of the editor in pixels
    key : str or None
        Unique key for the component
    
    Returns:
    --------
    Dict or None
        Chart configuration and data or None if no changes
    """
    
    # Default data if none provided
    if data is None:
        data = [
            ["Category", "Value 1", "Value 2"],
            ["Q1", "120", "100"],
            ["Q2", "150", "130"],
            ["Q3", "180", "160"],
            ["Q4", "200", "190"]
        ]
    
    # Convert data to JSON for JavaScript
    data_json = json.dumps(data).replace('"', '\\"')
    
    component_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Theta Chart Editor</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
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
            }}
            
            .chart-panel {{
                flex: 1;
                padding: 20px;
                display: flex;
                flex-direction: column;
            }}
            
            .controls-panel {{
                width: 300px;
                background: #f8f9fa;
                border-left: 1px solid #dee2e6;
                padding: 20px;
                overflow-y: auto;
            }}
            
            .chart-container {{
                flex: 1;
                position: relative;
                background: white;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                padding: 20px;
            }}
            
            .control-group {{
                margin-bottom: 20px;
                padding: 15px;
                background: white;
                border-radius: 6px;
                border: 1px solid #dee2e6;
            }}
            
            .control-group h4 {{
                margin: 0 0 10px 0;
                font-size: 14px;
                font-weight: 600;
                color: #495057;
            }}
            
            .control-row {{
                display: flex;
                flex-direction: column;
                margin-bottom: 10px;
            }}
            
            .control-row label {{
                font-size: 12px;
                color: #6c757d;
                margin-bottom: 5px;
            }}
            
            .control-row select, .control-row input {{
                padding: 6px 8px;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                font-size: 12px;
            }}
            
            .color-input {{
                width: 50px;
                height: 30px;
                border-radius: 4px;
                border: 1px solid #dee2e6;
            }}
            
            .data-table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
            }}
            
            .data-table th, .data-table td {{
                border: 1px solid #dee2e6;
                padding: 6px;
                text-align: center;
                font-size: 11px;
            }}
            
            .data-table input {{
                width: 100%;
                border: none;
                background: transparent;
                text-align: center;
                font-size: 11px;
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
            }}
            
            .btn:hover {{
                background: #0056b3;
            }}
            
            .toolbar {{
                display: flex;
                gap: 10px;
                margin-bottom: 15px;
                padding: 10px;
                background: #f8f9fa;
                border-radius: 6px;
            }}
            
            .toolbar button {{
                padding: 6px 12px;
                border: 1px solid #dee2e6;
                background: white;
                border-radius: 4px;
                cursor: pointer;
                font-size: 12px;
            }}
            
            .toolbar button.active {{
                background: #007bff;
                color: white;
                border-color: #007bff;
            }}
        </style>
    </head>
    <body>
        <div class="editor-container">
            <div class="chart-panel">
                <div class="toolbar">
                    <button onclick="setChartType('bar')" class="chart-type-btn active" data-type="bar">📊 Bar</button>
                    <button onclick="setChartType('line')" class="chart-type-btn" data-type="line">📈 Line</button>
                    <button onclick="setChartType('pie')" class="chart-type-btn" data-type="pie">🥧 Pie</button>
                    <button onclick="setChartType('doughnut')" class="chart-type-btn" data-type="doughnut">🍩 Doughnut</button>
                    <button onclick="setChartType('radar')" class="chart-type-btn" data-type="radar">🕸️ Radar</button>
                    <button onclick="setChartType('scatter')" class="chart-type-btn" data-type="scatter">⚪ Scatter</button>
                    <button onclick="exportChart()" class="btn">💾 Export</button>
                </div>
                
                <div class="chart-container">
                    <canvas id="chart-canvas"></canvas>
                </div>
            </div>
            
            <div class="controls-panel">
                <div class="control-group">
                    <h4>Chart Settings</h4>
                    <div class="control-row">
                        <label>Title:</label>
                        <input type="text" id="chart-title" value="My Chart" onchange="updateChart()">
                    </div>
                    <div class="control-row">
                        <label>X-Axis Label:</label>
                        <input type="text" id="x-label" value="Categories" onchange="updateChart()">
                    </div>
                    <div class="control-row">
                        <label>Y-Axis Label:</label>
                        <input type="text" id="y-label" value="Values" onchange="updateChart()">
                    </div>
                    <div class="control-row">
                        <label>Legend Position:</label>
                        <select id="legend-position" onchange="updateChart()">
                            <option value="top">Top</option>
                            <option value="bottom" selected>Bottom</option>
                            <option value="left">Left</option>
                            <option value="right">Right</option>
                        </select>
                    </div>
                </div>
                
                <div class="control-group">
                    <h4>Colors</h4>
                    <div class="control-row">
                        <label>Primary Color:</label>
                        <input type="color" id="primary-color" value="#007bff" class="color-input" onchange="updateChart()">
                    </div>
                    <div class="control-row">
                        <label>Secondary Color:</label>
                        <input type="color" id="secondary-color" value="#28a745" class="color-input" onchange="updateChart()">
                    </div>
                    <div class="control-row">
                        <label>Background:</label>
                        <input type="color" id="bg-color" value="#ffffff" class="color-input" onchange="updateChart()">
                    </div>
                </div>
                
                <div class="control-group">
                    <h4>Data</h4>
                    <button onclick="addDataRow()" class="btn">+ Add Row</button>
                    <button onclick="addDataColumn()" class="btn">+ Add Column</button>
                    <div id="data-editor">
                        <!-- Data table will be generated here -->
                    </div>
                </div>
                
                <div class="control-group">
                    <h4>Export</h4>
                    <button onclick="exportChart('png')" class="btn">📸 Export PNG</button>
                    <button onclick="exportChart('json')" class="btn">📄 Export Data</button>
                </div>
            </div>
        </div>
        
        <script>
            let chartData = {data_json};
            let currentChart = null;
            let currentChartType = '{chart_type}';
            
            function initChart() {{
                createDataTable();
                updateChart();
            }}
            
            function createDataTable() {{
                const container = document.getElementById('data-editor');
                let tableHTML = '<table class="data-table"><thead><tr>';
                
                // Headers
                if (chartData.length > 0) {{
                    chartData[0].forEach((header, index) => {{
                        tableHTML += `<th><input type="text" value="${{header}}" onchange="updateDataCell(0, ${{index}}, this.value)"></th>`;
                    }});
                }}
                tableHTML += '</tr></thead><tbody>';
                
                // Data rows
                for (let i = 1; i < chartData.length; i++) {{
                    tableHTML += '<tr>';
                    chartData[i].forEach((cell, colIndex) => {{
                        tableHTML += `<td><input type="text" value="${{cell}}" onchange="updateDataCell(${{i}}, ${{colIndex}}, this.value)"></td>`;
                    }});
                    tableHTML += '</tr>';
                }}
                
                tableHTML += '</tbody></table>';
                container.innerHTML = tableHTML;
            }}
            
            function updateDataCell(row, col, value) {{
                chartData[row][col] = value;
                updateChart();
            }}
            
            function setChartType(type) {{
                currentChartType = type;
                document.querySelectorAll('.chart-type-btn').forEach(btn => {{
                    btn.classList.remove('active');
                }});
                document.querySelector(`[data-type="${{type}}"]`).classList.add('active');
                updateChart();
            }}
            
            function updateChart() {{
                const ctx = document.getElementById('chart-canvas').getContext('2d');
                
                if (currentChart) {{
                    currentChart.destroy();
                }}
                
                const labels = chartData.slice(1).map(row => row[0]);
                const datasets = [];
                
                // Create datasets from data columns (skip first column which is labels)
                for (let i = 1; i < chartData[0].length; i++) {{
                    const data = chartData.slice(1).map(row => parseFloat(row[i]) || 0);
                    const colors = [
                        document.getElementById('primary-color').value,
                        document.getElementById('secondary-color').value,
                        '#ffc107', '#dc3545', '#17a2b8', '#6f42c1'
                    ];
                    
                    datasets.push({{
                        label: chartData[0][i],
                        data: data,
                        backgroundColor: currentChartType === 'pie' || currentChartType === 'doughnut' 
                            ? colors.slice(0, data.length)
                            : colors[i-1] + '80',
                        borderColor: colors[i-1],
                        borderWidth: 2,
                        fill: currentChartType === 'area'
                    }});
                }}
                
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
                                text: document.getElementById('chart-title').value,
                                font: {{ size: 16, weight: 'bold' }}
                            }},
                            legend: {{
                                position: document.getElementById('legend-position').value
                            }}
                        }},
                        scales: currentChartType !== 'pie' && currentChartType !== 'doughnut' ? {{
                            x: {{
                                title: {{
                                    display: true,
                                    text: document.getElementById('x-label').value
                                }}
                            }},
                            y: {{
                                title: {{
                                    display: true,
                                    text: document.getElementById('y-label').value
                                }}
                            }}
                        }} : {{}}
                    }}
                }};
                
                currentChart = new Chart(ctx, config);
            }}
            
            function addDataRow() {{
                const newRow = new Array(chartData[0].length).fill('0');
                chartData.push(newRow);
                createDataTable();
                updateChart();
            }}
            
            function addDataColumn() {{
                chartData.forEach(row => row.push('New Column'));
                chartData[0][chartData[0].length - 1] = 'New Series';
                createDataTable();
                updateChart();
            }}
            
            function exportChart(format = 'png') {{
                if (format === 'png') {{
                    const canvas = document.getElementById('chart-canvas');
                    const link = document.createElement('a');
                    link.download = `chart-${{new Date().toISOString().slice(0, 19).replace(/:/g, '-')}}.png`;
                    link.href = canvas.toDataURL();
                    link.click();
                }} else if (format === 'json') {{
                    const chartConfig = {{
                        type: currentChartType,
                        data: chartData,
                        settings: {{
                            title: document.getElementById('chart-title').value,
                            xLabel: document.getElementById('x-label').value,
                            yLabel: document.getElementById('y-label').value,
                            legendPosition: document.getElementById('legend-position').value,
                            primaryColor: document.getElementById('primary-color').value,
                            secondaryColor: document.getElementById('secondary-color').value,
                            backgroundColor: document.getElementById('bg-color').value
                        }}
                    }};
                    
                    const blob = new Blob([JSON.stringify(chartConfig, null, 2)], {{ type: 'application/json' }});
                    const link = document.createElement('a');
                    link.download = `chart-config-${{new Date().toISOString().slice(0, 19).replace(/:/g, '-')}}.json`;
                    link.href = URL.createObjectURL(blob);
                    link.click();
                }}
            }}
            
            // Initialize the chart editor
            initChart();
        </script>
    </body>
    </html>
    """
    
    # Use Streamlit's HTML component
    components.html(component_html, width=width, height=height)
    
    # Return None due to Streamlit version compatibility
    return None
