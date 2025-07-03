"""
Theta Spreadsheet Editor - Visual spreadsheet editor for Streamlit
Provides a grid interface for creating and editing spreadsheets.
"""

import streamlit as st
import streamlit.components.v1 as components
import json
from typing import Dict, List, Any, Optional

def theta_spreadsheet_editor(
    data: Optional[List[List[str]]] = None,
    width: int = 900,
    height: int = 600,
    key: Optional[str] = None
) -> None:
    """
    Create a spreadsheet-style spreadsheet editor.
    
    Parameters:
    -----------
    data : List[List[str]] or None
        Initial spreadsheet data as 2D array
    width : int
        Width of the editor in pixels
    height : int  
        Height of the editor in pixels
    key : str or None
        Unique key for the component
        
    Returns:
    --------
    List[List[str]] or None
        Updated spreadsheet data or None if no changes
    """
    
    if data is None:
        # Initialize with empty 10x26 grid (A-Z columns)
        data = [["" for _ in range(26)] for _ in range(10)]
    
    # Safety check: ensure data is a proper list, not a DeltaGenerator
    if not isinstance(data, list):
        data = [["" for _ in range(26)] for _ in range(10)]
    
    # Convert data to JSON for JavaScript
    data_json = json.dumps(data).replace('"', '\\"')
    
    # Component HTML/CSS/JS for spreadsheet-like editor
    component_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Theta Excel Editor</title>
        <style>
            body {{
                margin: 0;
                padding: 10px;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: #f5f5f5;
                overflow: hidden;
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
            }}
            
            .formula-bar {{
                height: 30px;
                background: white;
                border-bottom: 1px solid #e9ecef;
                display: flex;
                align-items: center;
                padding: 0 10px;
                gap: 10px;
            }}
            
            .cell-ref {{
                min-width: 80px;
                padding: 4px 8px;
                border: 1px solid #dee2e6;
                border-radius: 3px;
                font-size: 12px;
                font-weight: bold;
            }}
            
            .formula-input {{
                flex: 1;
                padding: 4px 8px;
                border: 1px solid #dee2e6;
                border-radius: 3px;
                font-size: 12px;
                font-family: monospace;
            }}
            
            .spreadsheet-container {{
                flex: 1;
                overflow: auto;
                background: white;
            }}
            
            .spreadsheet {{
                display: grid;
                grid-template-columns: 40px repeat(26, 80px);
                grid-template-rows: 30px repeat(100, 25px);
                font-size: 12px;
                font-family: 'Segoe UI', sans-serif;
            }}
            
            .cell {{
                border: 1px solid #e0e0e0;
                padding: 2px 4px;
                outline: none;
                background: white;
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
            }}
            
            .cell:focus {{
                border: 2px solid #007bff;
                z-index: 1;
                position: relative;
            }}
            
            .header-cell {{
                background: #f8f9fa;
                font-weight: bold;
                text-align: center;
                display: flex;
                align-items: center;
                justify-content: center;
                border: 1px solid #dee2e6;
                color: #495057;
            }}
            
            .row-header {{
                background: #f8f9fa;
                font-weight: bold;
                text-align: center;
                display: flex;
                align-items: center;
                justify-content: center;
                border: 1px solid #dee2e6;
                color: #495057;
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
            
            .selected {{
                background: #e3f2fd !important;
            }}
        </style>
    </head>
    <body>
        <div class="editor-container">
            <!-- Toolbar -->
            <div class="toolbar">
                <button onclick="addRow()">+ Row</button>
                <button onclick="addColumn()">+ Column</button>
                <button onclick="deleteRow()">- Row</button>
                <button onclick="deleteColumn()">- Column</button>
                <button onclick="formatBold()">B</button>
                <button onclick="formatItalic()">I</button>
                <button onclick="saveSpreadsheet()">💾 Save</button>
            </div>
            
            <!-- Formula Bar -->
            <div class="formula-bar">
                <input type="text" class="cell-ref" id="cell-ref" readonly value="A1">
                <input type="text" class="formula-input" id="formula-input" placeholder="Enter formula or value">
            </div>
            
            <!-- Spreadsheet -->
            <div class="spreadsheet-container">
                <div class="spreadsheet" id="spreadsheet">
                    <!-- Grid will be generated by JavaScript -->
                </div>
            </div>
        </div>
        
        <script>
            // Theta Excel Editor JavaScript
            let spreadsheetData = {data_json};
            let currentCell = null;
            let selectedCell = {{ row: 0, col: 0 }};
            
            // Column headers A-Z
            const columnHeaders = Array.from({{length: 26}}, (_, i) => String.fromCharCode(65 + i));
            
            function initSpreadsheet() {{
                const container = document.getElementById('spreadsheet');
                container.innerHTML = '';
                
                // Empty top-left cell
                const topLeft = document.createElement('div');
                topLeft.className = 'header-cell';
                container.appendChild(topLeft);
                
                // Column headers
                columnHeaders.forEach((header, index) => {{
                    const headerCell = document.createElement('div');
                    headerCell.className = 'header-cell';
                    headerCell.textContent = header;
                    headerCell.onclick = () => selectColumn(index);
                    container.appendChild(headerCell);
                }});
                
                // Rows
                for (let row = 0; row < 100; row++) {{
                    // Row header
                    const rowHeader = document.createElement('div');
                    rowHeader.className = 'row-header';
                    rowHeader.textContent = row + 1;
                    rowHeader.onclick = () => selectRow(row);
                    container.appendChild(rowHeader);
                    
                    // Data cells
                    for (let col = 0; col < 26; col++) {{
                        const cell = document.createElement('input');
                        cell.className = 'cell';
                        cell.type = 'text';
                        cell.dataset.row = row;
                        cell.dataset.col = col;
                        
                        // Set initial value
                        if (spreadsheetData[row] && spreadsheetData[row][col]) {{
                            cell.value = spreadsheetData[row][col];
                        }}
                        
                        // Event listeners
                        cell.onfocus = () => selectCell(row, col);
                        cell.oninput = () => updateCell(row, col, cell.value);
                        cell.onkeydown = (e) => handleKeydown(e, row, col);
                        
                        container.appendChild(cell);
                    }}
                }}
                
                updateFormulaBar();
            }}
            
            function selectCell(row, col) {{
                selectedCell = {{ row, col }};
                currentCell = document.querySelector(`[data-row="${{row}}"][data-col="${{col}}"]`);
                
                // Update visual selection
                document.querySelectorAll('.cell').forEach(c => c.classList.remove('selected'));
                if (currentCell) {{
                    currentCell.classList.add('selected');
                }}
                
                updateFormulaBar();
            }}
            
            function updateCell(row, col, value) {{
                // Ensure data structure exists
                while (spreadsheetData.length <= row) {{
                    spreadsheetData.push(new Array(26).fill(''));
                }}
                while (spreadsheetData[row].length <= col) {{
                    spreadsheetData[row].push('');
                }}
                
                spreadsheetData[row][col] = value;
                updateFormulaBar();
            }}
            
            function updateFormulaBar() {{
                const cellRef = document.getElementById('cell-ref');
                const formulaInput = document.getElementById('formula-input');
                
                const col = columnHeaders[selectedCell.col] || 'A';
                const row = selectedCell.row + 1;
                cellRef.value = col + row;
                
                const cellValue = (spreadsheetData[selectedCell.row] && 
                                 spreadsheetData[selectedCell.row][selectedCell.col]) || '';
                formulaInput.value = cellValue;
                
                formulaInput.onchange = () => {{
                    updateCell(selectedCell.row, selectedCell.col, formulaInput.value);
                    if (currentCell) {{
                        currentCell.value = formulaInput.value;
                    }}
                }};
            }}
            
            function handleKeydown(e, row, col) {{
                switch(e.key) {{
                    case 'ArrowUp':
                        e.preventDefault();
                        if (row > 0) selectCell(row - 1, col);
                        break;
                    case 'ArrowDown':
                        e.preventDefault();
                        selectCell(row + 1, col);
                        break;
                    case 'ArrowLeft':
                        e.preventDefault();
                        if (col > 0) selectCell(row, col - 1);
                        break;
                    case 'ArrowRight':
                        e.preventDefault();
                        if (col < 25) selectCell(row, col + 1);
                        break;
                    case 'Enter':
                        e.preventDefault();
                        selectCell(row + 1, col);
                        break;
                    case 'Tab':
                        e.preventDefault();
                        if (col < 25) selectCell(row, col + 1);
                        break;
                }}
            }}
            
            function addRow() {{
                spreadsheetData.push(new Array(26).fill(''));
                // Re-render would be needed for dynamic rows
                console.log('Row added');
            }}
            
            function addColumn() {{
                spreadsheetData.forEach(row => row.push(''));
                console.log('Column added');
            }}
            
            function deleteRow() {{
                if (spreadsheetData.length > 1) {{
                    spreadsheetData.splice(selectedCell.row, 1);
                    console.log('Row deleted');
                }}
            }}
            
            function deleteColumn() {{
                spreadsheetData.forEach(row => {{
                    if (row.length > 1) {{
                        row.splice(selectedCell.col, 1);
                    }}
                }});
                console.log('Column deleted');
            }}
            
            function formatBold() {{
                if (currentCell) {{
                    currentCell.style.fontWeight = 
                        currentCell.style.fontWeight === 'bold' ? 'normal' : 'bold';
                }}
            }}
            
            function formatItalic() {{
                if (currentCell) {{
                    currentCell.style.fontStyle = 
                        currentCell.style.fontStyle === 'italic' ? 'normal' : 'italic';
                }}
            }}
            
            function saveSpreadsheet() {{
                // Clean up empty trailing rows and columns
                const cleanData = spreadsheetData
                    .filter(row => row.some(cell => cell.trim() !== ''))
                    .map(row => {{
                        const lastIndex = row.findLastIndex(cell => cell.trim() !== '');
                        return row.slice(0, Math.max(0, lastIndex + 1));
                    }});
                
                // Create CSV content
                let csvContent = '';
                cleanData.forEach(row => {{
                    csvContent += row.map(cell => `"${{cell.replace(/"/g, '""')}}"`).join(',') + '\\n';
                }});
                
                const blob = new Blob([csvContent], {{ type: 'text/csv' }});
                
                // Create download link
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `spreadsheet_${{new Date().toISOString().slice(0,19).replace(/:/g,'-')}}.csv`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
                
                alert('Spreadsheet downloaded successfully!');
            }}
            
            // Initialize when page loads
            document.addEventListener('DOMContentLoaded', () => {{
                initSpreadsheet();
                selectCell(0, 0);
            }});
        </script>
    </body>
    </html>
    """
    
    # Create the component
    component_value = components.html(
        component_html,
        width=width + 50,
        height=height + 50
    )
    
    # Component doesn't return data due to Streamlit version compatibility
    return None