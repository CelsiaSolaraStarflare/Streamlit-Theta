"""
Theta CSV Editor - Data table editor for CSV files
"""

import streamlit as st
import streamlit.components.v1 as components
import json
import csv
import io
from typing import Dict, List, Any, Optional

def theta_csv_editor(
    data: Optional[List[List[str]]] = None,
    headers: Optional[List[str]] = None,
    width: int = 900,
    height: int = 600,
    key: Optional[str] = None
) -> None:
    """
    Create a CSV/data table editor.
    
    Parameters:
    -----------
    data : List[List[str]] or None
        Initial CSV data as 2D array
    headers : List[str] or None
        Column headers
    width : int
        Width of the editor in pixels
    height : int  
        Height of the editor in pixels
        
    Returns:
    --------
    Dict containing 'data' and 'headers' keys or None
    """
    
    if data is None:
        data = [["" for _ in range(5)] for _ in range(5)]
    if headers is None:
        headers = [f"Column {i+1}" for i in range(len(data[0]) if data else 5)]
    
    # Safety checks: ensure data and headers are proper types, not DeltaGenerators
    if not isinstance(data, list):
        data = [["" for _ in range(5)] for _ in range(5)]
    if not isinstance(headers, list):
        headers = [f"Column {i+1}" for i in range(len(data[0]) if data else 5)]
    
    # Convert to JSON for JavaScript
    data_json = json.dumps(data).replace('"', '\\"')
    headers_json = json.dumps(headers).replace('"', '\\"')
    
    component_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Theta CSV Editor</title>
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
                border-bottom: 1px solid #e9ecef;
                border-radius: 8px 8px 0 0;
                display: flex;
                align-items: center;
                padding: 0 15px;
                gap: 10px;
                flex-wrap: wrap;
            }}
            
            .data-info {{
                height: 30px;
                background: #e9ecef;
                border-bottom: 1px solid #dee2e6;
                display: flex;
                align-items: center;
                padding: 0 15px;
                font-size: 12px;
                color: #6c757d;
            }}
            
            .table-container {{
                flex: 1;
                overflow: auto;
                padding: 10px;
            }}
            
            .data-table {{
                width: 100%;
                border-collapse: collapse;
                font-size: 13px;
                background: white;
            }}
            
            .data-table th {{
                background: #f8f9fa;
                border: 1px solid #dee2e6;
                padding: 8px;
                font-weight: 600;
                text-align: left;
                position: sticky;
                top: 0;
                z-index: 10;
            }}
            
            .data-table td {{
                border: 1px solid #dee2e6;
                padding: 4px;
            }}
            
            .data-table input {{
                width: 100%;
                border: none;
                outline: none;
                padding: 4px;
                font-size: 13px;
                background: transparent;
            }}
            
            .data-table input:focus {{
                background: #fff3cd;
                border-radius: 3px;
            }}
            
            .header-input {{
                font-weight: 600;
                background: #f8f9fa;
            }}
            
            .row-number {{
                background: #e9ecef;
                text-align: center;
                font-weight: 600;
                color: #6c757d;
                min-width: 40px;
            }}
            
            .toolbar button {{
                background: #fff;
                border: 1px solid #dee2e6;
                padding: 6px 12px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 12px;
                transition: all 0.2s;
            }}
            
            .toolbar button:hover {{
                background: #e9ecef;
                border-color: #adb5bd;
            }}
            
            .toolbar button.primary {{
                background: #007bff;
                color: white;
                border-color: #007bff;
            }}
            
            .toolbar input[type="file"] {{
                display: none;
            }}
            
            .file-label {{
                background: #28a745;
                color: white;
                border: 1px solid #28a745;
                padding: 6px 12px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 12px;
                transition: all 0.2s;
            }}
            
            .file-label:hover {{
                background: #218838;
                border-color: #1e7e34;
            }}
        </style>
    </head>
    <body>
        <div class="editor-container">
            <!-- Toolbar -->
            <div class="toolbar">
                <button onclick="addRow()">+ Add Row</button>
                <button onclick="addColumn()">+ Add Column</button>
                <button onclick="deleteRow()">- Delete Row</button>
                <button onclick="deleteColumn()">- Delete Column</button>
                <label for="file-input" class="file-label">📁 Load CSV</label>
                <input type="file" id="file-input" accept=".csv" onchange="loadCSV(event)">
                <button onclick="exportCSV()">💾 Export CSV</button>
                <button onclick="saveData()" class="primary">💾 Save</button>
            </div>
            
            <!-- Data Info -->
            <div class="data-info">
                <span id="data-stats">Rows: 0, Columns: 0</span>
            </div>
            
            <!-- Table -->
            <div class="table-container">
                <table class="data-table" id="data-table">
                    <!-- Table will be generated by JavaScript -->
                </table>
            </div>
        </div>
        
        <script>
            let csvData = {data_json};
            let csvHeaders = {headers_json};
            let selectedRow = -1;
            let selectedCol = -1;
            
            function initTable() {{
                renderTable();
                updateStats();
            }}
            
            function renderTable() {{
                const table = document.getElementById('data-table');
                table.innerHTML = '';
                
                // Header row
                const headerRow = document.createElement('tr');
                
                // Row number header
                const rowNumHeader = document.createElement('th');
                rowNumHeader.className = 'row-number';
                rowNumHeader.textContent = '#';
                headerRow.appendChild(rowNumHeader);
                
                // Column headers
                csvHeaders.forEach((header, index) => {{
                    const th = document.createElement('th');
                    const input = document.createElement('input');
                    input.className = 'header-input';
                    input.value = header;
                    input.onchange = () => updateHeader(index, input.value);
                    th.appendChild(input);
                    headerRow.appendChild(th);
                }});
                
                table.appendChild(headerRow);
                
                // Data rows
                csvData.forEach((row, rowIndex) => {{
                    const tr = document.createElement('tr');
                    
                    // Row number
                    const rowNumCell = document.createElement('td');
                    rowNumCell.className = 'row-number';
                    rowNumCell.textContent = rowIndex + 1;
                    rowNumCell.onclick = () => selectRow(rowIndex);
                    tr.appendChild(rowNumCell);
                    
                    // Data cells
                    row.forEach((cell, colIndex) => {{
                        const td = document.createElement('td');
                        const input = document.createElement('input');
                        input.value = cell;
                        input.dataset.row = rowIndex;
                        input.dataset.col = colIndex;
                        input.oninput = () => updateCell(rowIndex, colIndex, input.value);
                        input.onfocus = () => selectCell(rowIndex, colIndex);
                        input.onkeydown = (e) => handleKeydown(e, rowIndex, colIndex);
                        td.appendChild(input);
                        tr.appendChild(td);
                    }});
                    
                    table.appendChild(tr);
                }});
            }}
            
            function updateHeader(index, value) {{
                csvHeaders[index] = value;
                updateStats();
            }}
            
            function updateCell(row, col, value) {{
                csvData[row][col] = value;
            }}
            
            function selectCell(row, col) {{
                selectedRow = row;
                selectedCol = col;
            }}
            
            function selectRow(row) {{
                selectedRow = row;
                selectedCol = -1;
            }}
            
            function handleKeydown(e, row, col) {{
                switch(e.key) {{
                    case 'ArrowUp':
                        e.preventDefault();
                        if (row > 0) {{
                            const nextInput = document.querySelector(`[data-row="${{row-1}}"][data-col="${{col}}"]`);
                            if (nextInput) nextInput.focus();
                        }}
                        break;
                    case 'ArrowDown':
                        e.preventDefault();
                        if (row < csvData.length - 1) {{
                            const nextInput = document.querySelector(`[data-row="${{row+1}}"][data-col="${{col}}"]`);
                            if (nextInput) nextInput.focus();
                        }}
                        break;
                    case 'ArrowLeft':
                        e.preventDefault();
                        if (col > 0) {{
                            const nextInput = document.querySelector(`[data-row="${{row}}"][data-col="${{col-1}}"]`);
                            if (nextInput) nextInput.focus();
                        }}
                        break;
                    case 'ArrowRight':
                        e.preventDefault();
                        if (col < csvData[row].length - 1) {{
                            const nextInput = document.querySelector(`[data-row="${{row}}"][data-col="${{col+1}}"]`);
                            if (nextInput) nextInput.focus();
                        }}
                        break;
                    case 'Enter':
                        e.preventDefault();
                        if (row < csvData.length - 1) {{
                            const nextInput = document.querySelector(`[data-row="${{row+1}}"][data-col="${{col}}"]`);
                            if (nextInput) nextInput.focus();
                        }}
                        break;
                    case 'Tab':
                        e.preventDefault();
                        if (col < csvData[row].length - 1) {{
                            const nextInput = document.querySelector(`[data-row="${{row}}"][data-col="${{col+1}}"]`);
                            if (nextInput) nextInput.focus();
                        }} else if (row < csvData.length - 1) {{
                            const nextInput = document.querySelector(`[data-row="${{row+1}}"][data-col="0"]`);
                            if (nextInput) nextInput.focus();
                        }}
                        break;
                }}
            }}
            
            function addRow() {{
                const newRow = new Array(csvHeaders.length).fill('');
                csvData.push(newRow);
                renderTable();
                updateStats();
            }}
            
            function addColumn() {{
                csvHeaders.push(`Column ${{csvHeaders.length + 1}}`);
                csvData.forEach(row => row.push(''));
                renderTable();
                updateStats();
            }}
            
            function deleteRow() {{
                if (selectedRow >= 0 && csvData.length > 1) {{
                    csvData.splice(selectedRow, 1);
                    renderTable();
                    updateStats();
                }}
            }}
            
            function deleteColumn() {{
                if (selectedCol >= 0 && csvHeaders.length > 1) {{
                    csvHeaders.splice(selectedCol, 1);
                    csvData.forEach(row => row.splice(selectedCol, 1));
                    renderTable();
                    updateStats();
                }}
            }}
            
            function loadCSV(event) {{
                const file = event.target.files[0];
                if (!file) return;
                
                const reader = new FileReader();
                reader.onload = function(e) {{
                    const csv = e.target.result;
                    const lines = csv.split('\\n').filter(line => line.trim());
                    
                    if (lines.length > 0) {{
                        // First line as headers
                        csvHeaders = lines[0].split(',').map(h => h.trim().replace(/"/g, ''));
                        
                        // Remaining lines as data
                        csvData = lines.slice(1).map(line => 
                            line.split(',').map(cell => cell.trim().replace(/"/g, ''))
                        );
                        
                        renderTable();
                        updateStats();
                    }}
                }};
                reader.readAsText(file);
            }}
            
            function exportCSV() {{
                let csvContent = '';
                
                // Add headers
                csvContent += csvHeaders.map(h => `"${{h}}"`).join(',') + '\\n';
                
                // Add data
                csvData.forEach(row => {{
                    csvContent += row.map(cell => `"${{cell}}"`).join(',') + '\\n';
                }});
                
                // Download file
                const blob = new Blob([csvContent], {{ type: 'text/csv' }});
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'data.csv';
                a.click();
                URL.revokeObjectURL(url);
            }}
            
            function updateStats() {{
                const stats = document.getElementById('data-stats');
                stats.textContent = `Rows: ${{csvData.length}}, Columns: ${{csvHeaders.length}}`;
            }}
            
            function saveData() {{
                // Create CSV content with headers
                let csvContent = '';
                
                // Add headers
                csvContent += csvHeaders.map(h => `"${{h.replace(/"/g, '""')}}"`).join(',') + '\\n';
                
                // Add data rows
                csvData.forEach(row => {{
                    csvContent += row.map(cell => `"${{cell.replace(/"/g, '""')}}"`).join(',') + '\\n';
                }});
                
                const blob = new Blob([csvContent], {{ type: 'text/csv' }});
                
                // Create download link
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `data_${{new Date().toISOString().slice(0,19).replace(/:/g,'-')}}.csv`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
                
                alert('CSV data downloaded successfully!');
            }}
            
            // Initialize when page loads
            document.addEventListener('DOMContentLoaded', initTable);
        </script>
    </body>
    </html>
    """
    
    # Create the component - note: components.html doesn't support key parameter
    component_value = components.html(
        component_html,
        width=width + 50,
        height=height + 50
    )
    
    # Component doesn't return data due to Streamlit version compatibility
    return None