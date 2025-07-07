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
        Width of the editor in pixels (constrained to 300-2000)
    height : int  
        Height of the editor in pixels (constrained to 400-1200)
    key : str or None
        Unique key for the component
        
    Returns:
    --------
    None (component-based editor)
    """
    
    # Input validation and sanitization
    try:
        # Validate dimensions
        width = max(300, min(width, 2000))
        height = max(400, min(height, 1200))
        
        # Initialize and validate data
        if data is None or not isinstance(data, list):
            # Initialize with empty 10x26 grid (A-Z columns)
            data = [["" for _ in range(26)] for _ in range(10)]
        else:
            # Sanitize data - ensure it's a proper 2D list of strings
            sanitized_data = []
            for row in data:
                if isinstance(row, list):
                    sanitized_row = [str(cell) if cell is not None else "" for cell in row]
                    # Ensure at least 26 columns (A-Z)
                    while len(sanitized_row) < 26:
                        sanitized_row.append("")
                    sanitized_data.append(sanitized_row[:26])  # Limit to 26 columns
                else:
                    sanitized_data.append(["" for _ in range(26)])
            data = sanitized_data
            
            # Ensure at least 10 rows
            while len(data) < 10:
                data.append(["" for _ in range(26)])
    
    except Exception as e:
        st.error(f"Error initializing spreadsheet editor: {e}")
        return None
    
    # Convert data to JSON for JavaScript with proper escaping
    try:
        data_json = json.dumps(data).replace('"', '\\"').replace("'", "\\'")
    except Exception as e:
        st.error(f"Error encoding spreadsheet data to JSON: {e}")
        return None
    
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
                try {{
                    const container = document.getElementById('spreadsheet');
                    if (!container) {{
                        throw new Error('Spreadsheet container not found');
                    }}
                    
                    container.innerHTML = '';
                    
                    // Empty top-left cell
                    const topLeft = document.createElement('div');
                    topLeft.className = 'header-cell';
                    topLeft.style.gridColumn = '1';
                    topLeft.style.gridRow = '1';
                    container.appendChild(topLeft);
                    
                    // Column headers
                    columnHeaders.forEach((header, index) => {{
                        const headerCell = document.createElement('div');
                        headerCell.className = 'header-cell';
                        headerCell.textContent = header;
                        headerCell.style.gridColumn = `${{index + 2}}`;
                        headerCell.style.gridRow = '1';
                        headerCell.onclick = () => selectColumn(index);
                        container.appendChild(headerCell);
                    }});
                    
                    // Ensure spreadsheetData is properly initialized
                    if (!Array.isArray(spreadsheetData)) {{
                        spreadsheetData = [];
                    }}
                    
                    // Ensure we have at least 100 rows for the grid
                    const maxRows = Math.max(100, spreadsheetData.length);
                    
                    // Rows
                    for (let row = 0; row < maxRows; row++) {{
                        // Row header
                        const rowHeader = document.createElement('div');
                        rowHeader.className = 'row-header';
                        rowHeader.textContent = row + 1;
                        rowHeader.style.gridColumn = '1';
                        rowHeader.style.gridRow = `${{row + 2}}`;
                        rowHeader.onclick = () => selectRow(row);
                        container.appendChild(rowHeader);
                        
                        // Data cells
                        for (let col = 0; col < 26; col++) {{
                            const cell = document.createElement('input');
                            cell.className = 'cell';
                            cell.type = 'text';
                            cell.dataset.row = row;
                            cell.dataset.col = col;
                            cell.style.gridColumn = `${{col + 2}}`;
                            cell.style.gridRow = `${{row + 2}}`;
                            
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
                }} catch (error) {{
                    console.error('Error initializing spreadsheet:', error);
                    alert('Error initializing spreadsheet. Please refresh the page.');
                }}
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
                try {{
                    const newRow = new Array(26).fill('');
                    spreadsheetData.push(newRow);
                    
                    // Add the new row to the existing grid
                    const container = document.getElementById('spreadsheet');
                    const rowIndex = spreadsheetData.length - 1;
                    
                    // Row header
                    const rowHeader = document.createElement('div');
                    rowHeader.className = 'row-header';
                    rowHeader.textContent = rowIndex + 1;
                    rowHeader.onclick = () => selectRow(rowIndex);
                    rowHeader.style.gridColumn = '1';
                    rowHeader.style.gridRow = `${{rowIndex + 2}}`;
                    container.appendChild(rowHeader);
                    
                    // Data cells
                    for (let col = 0; col < 26; col++) {{
                        const cell = document.createElement('input');
                        cell.className = 'cell';
                        cell.type = 'text';
                        cell.dataset.row = rowIndex;
                        cell.dataset.col = col;
                        cell.value = '';
                        cell.style.gridColumn = `${{col + 2}}`;
                        cell.style.gridRow = `${{rowIndex + 2}}`;
                        
                        cell.onfocus = () => selectCell(rowIndex, col);
                        cell.oninput = () => updateCell(rowIndex, col, cell.value);
                        cell.onkeydown = (e) => handleKeydown(e, rowIndex, col);
                        
                        container.appendChild(cell);
                    }}
                    
                    console.log('Row added successfully');
                }} catch (error) {{
                    console.error('Error adding row:', error);
                    alert('Error adding row. Please try again.');
                }}
            }}
            
            function addColumn() {{
                try {{
                    spreadsheetData.forEach(row => {{
                        if (Array.isArray(row)) {{
                            row.push('');
                        }}
                    }});
                    
                    // Re-initialize the spreadsheet to include the new column
                    initSpreadsheet();
                    console.log('Column added successfully');
                }} catch (error) {{
                    console.error('Error adding column:', error);
                    alert('Error adding column. Please try again.');
                }}
            }}
            
            function deleteRow() {{
                try {{
                    if (spreadsheetData.length > 1 && selectedCell.row >= 0) {{
                        spreadsheetData.splice(selectedCell.row, 1);
                        
                        // Re-initialize the spreadsheet to reflect the deletion
                        initSpreadsheet();
                        
                        // Adjust selected cell if needed
                        if (selectedCell.row >= spreadsheetData.length) {{
                            selectedCell.row = Math.max(0, spreadsheetData.length - 1);
                        }}
                        
                        selectCell(selectedCell.row, selectedCell.col);
                        console.log('Row deleted successfully');
                    }} else {{
                        alert('Please select a row to delete, and ensure at least one row remains.');
                    }}
                }} catch (error) {{
                    console.error('Error deleting row:', error);
                    alert('Error deleting row. Please try again.');
                }}
            }}
            
            function deleteColumn() {{
                try {{
                    if (selectedCell.col >= 0) {{
                        spreadsheetData.forEach(row => {{
                            if (Array.isArray(row) && row.length > 1) {{
                                row.splice(selectedCell.col, 1);
                            }}
                        }});
                        
                        // Re-initialize the spreadsheet to reflect the deletion
                        initSpreadsheet();
                        
                        // Adjust selected cell if needed
                        if (selectedCell.col >= (spreadsheetData[0] ? spreadsheetData[0].length : 26)) {{
                            selectedCell.col = Math.max(0, (spreadsheetData[0] ? spreadsheetData[0].length : 26) - 1);
                        }}
                        
                        selectCell(selectedCell.row, selectedCell.col);
                        console.log('Column deleted successfully');
                    }} else {{
                        alert('Please select a column to delete, and ensure at least one column remains.');
                    }}
                }} catch (error) {{
                    console.error('Error deleting column:', error);
                    alert('Error deleting column. Please try again.');
                }}
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