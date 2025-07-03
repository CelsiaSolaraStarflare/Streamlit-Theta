import streamlit as st
import streamlit.components.v1 as components
from typing import Dict, List, Any, Optional

def theta_document_editor(
    content: str = "",
    width: int = 800,
    height: int = 600,
    key: Optional[str] = None
) -> Optional[str]:
    """
    Create a document-style editor.
    
    Parameters:
    -----------
    content : str
        Initial document content (HTML format)
    width : int
        Width of the editor in pixels
    height : int  
        Height of the editor in pixels
    key : str, optional
        Unique key for the component
        
    Returns:
    --------
    str or None
        Updated document content if save button is clicked
    """
    
    component_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: #f8f9fa;
                color: #212529;
            }}
            
            .editor-container {{
                width: 100%;
                height: 100vh;
                display: flex;
                flex-direction: column;
                background: white;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                overflow: hidden;
            }}
            
            .toolbar {{
                background: #ffffff;
                border-bottom: 1px solid #e9ecef;
                padding: 12px 16px;
                display: flex;
                gap: 12px;
                align-items: center;
                flex-wrap: wrap;
                min-height: 60px;
            }}
            
            .toolbar-group {{
                display: flex;
                gap: 4px;
                align-items: center;
                border-right: 1px solid #e9ecef;
                padding-right: 12px;
            }}
            
            .toolbar-group:last-child {{
                border-right: none;
            }}
            
            .toolbar button {{
                background: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 8px 12px;
                cursor: pointer;
                transition: all 0.2s;
                font-size: 14px;
                min-width: 36px;
                height: 36px;
            }}
            
            .toolbar button:hover {{
                background: #e9ecef;
                border-color: #adb5bd;
            }}
            
            .toolbar button.active {{
                background: #0d6efd;
                color: white;
                border-color: #0d6efd;
            }}
            
            .toolbar select {{
                background: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 8px;
                cursor: pointer;
                font-size: 14px;
                height: 36px;
            }}
            
            .editor-main {{
                flex: 1;
                display: flex;
                overflow: hidden;
            }}
            
            .document-area {{
                flex: 1;
                padding: 40px;
                background: white;
                overflow-y: auto;
                display: flex;
                justify-content: center;
            }}
            
            .document {{
                width: 100%;
                max-width: 8.5in;
                min-height: 11in;
                background: white;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
                border: 1px solid #e9ecef;
                border-radius: 4px;
                padding: 1in;
                outline: none;
                font-family: 'Times New Roman', serif;
                font-size: 12pt;
                line-height: 1.5;
            }}
            
            .properties-panel {{
                width: 250px;
                background: #f8f9fa;
                border-left: 1px solid #e9ecef;
                padding: 16px;
                overflow-y: auto;
            }}
            
            .property-group {{
                margin-bottom: 20px;
            }}
            
            .property-group h4 {{
                font-size: 14px;
                margin-bottom: 8px;
                color: #495057;
            }}
            
            .property-item {{
                margin-bottom: 8px;
            }}
            
            .property-item label {{
                display: block;
                font-size: 12px;
                color: #6c757d;
                margin-bottom: 4px;
            }}
            
            .property-item input, .property-item select {{
                width: 100%;
                padding: 6px 8px;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                font-size: 12px;
            }}
            
            .stats {{
                background: #e9ecef;
                padding: 12px;
                border-radius: 4px;
                font-size: 12px;
                text-align: center;
            }}
            
            .stats div {{
                margin-bottom: 4px;
            }}
        </style>
        <script src="https://cdn.jsdelivr.net/npm/docx@7.3.0/build/index.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/FileSaver.js/2.0.5/FileSaver.min.js"></script>
    </head>
    <body>
        <div class="editor-container">
            <!-- Toolbar -->
            <div class="toolbar">
                <div class="toolbar-group">
                    <button id="bold" title="Bold">B</button>
                    <button id="italic" title="Italic">I</button>
                    <button id="underline" title="Underline">U</button>
                </div>
                
                <div class="toolbar-group">
                    <select id="font-family">
                        <option value="Times New Roman">Times New Roman</option>
                        <option value="Arial">Arial</option>
                        <option value="Calibri">Calibri</option>
                        <option value="Georgia">Georgia</option>
                    </select>
                    <select id="font-size">
                        <option value="10">10</option>
                        <option value="11">11</option>
                        <option value="12" selected>12</option>
                        <option value="14">14</option>
                        <option value="16">16</option>
                        <option value="18">18</option>
                        <option value="20">20</option>
                        <option value="24">24</option>
                    </select>
                </div>
                
                <div class="toolbar-group">
                    <button id="align-left" title="Align Left">⬅</button>
                    <button id="align-center" title="Center">🔘</button>
                    <button id="align-right" title="Align Right">➡</button>
                    <button id="justify" title="Justify">⬛</button>
                </div>
                
                <div class="toolbar-group">
                    <button id="bullet-list" title="Bullet List">• List</button>
                    <button id="number-list" title="Numbered List">1. List</button>
                </div>
                
                <div class="toolbar-group">
                    <button id="save-doc" title="Save Document">💾 Save</button>
                    <button id="save-docx" title="Save as DOCX">💾 Save DOCX</button>
                </div>
            </div>
            
            <!-- Main Editor -->
            <div class="editor-main">
                <!-- Document Area -->
                <div class="document-area">
                    <div class="document" id="document" contenteditable="true">
                        {content or "Start typing your document here..."}
                    </div>
                </div>
                
                <!-- Properties Panel -->
                <div class="properties-panel">
                    <div class="property-group">
                        <h4>Document Properties</h4>
                        <div class="property-item">
                            <label>Margin</label>
                            <select id="margin-size">
                                <option value="0.5in">Narrow (0.5")</option>
                                <option value="1in" selected>Normal (1")</option>
                                <option value="1.25in">Wide (1.25")</option>
                            </select>
                        </div>
                        <div class="property-item">
                            <label>Orientation</label>
                            <select id="orientation">
                                <option value="portrait" selected>Portrait</option>
                                <option value="landscape">Landscape</option>
                            </select>
                        </div>
                    </div>
                    
                    <div class="property-group">
                        <h4>Statistics</h4>
                        <div class="stats">
                            <div>Words: <span id="word-count">0</span></div>
                            <div>Characters: <span id="char-count">0</span></div>
                            <div>Pages: <span id="page-count">1</span></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            // Theta Document Editor JavaScript
            let documentContent = `{content}`;
            let isModified = false;
            
            function initEditor() {{
                const doc = document.getElementById('document');
                
                // Set initial content
                if (documentContent && documentContent !== "Start typing your document here...") {{
                    doc.innerHTML = documentContent;
                }}
                
                updateStatistics();
                setupToolbarEvents();
                setupDocumentEvents();
            }}
            
            function setupToolbarEvents() {{
                // Formatting buttons
                document.getElementById('bold').onclick = () => document.execCommand('bold');
                document.getElementById('italic').onclick = () => document.execCommand('italic');
                document.getElementById('underline').onclick = () => document.execCommand('underline');
                
                // Alignment buttons
                document.getElementById('align-left').onclick = () => document.execCommand('justifyLeft');
                document.getElementById('align-center').onclick = () => document.execCommand('justifyCenter');
                document.getElementById('align-right').onclick = () => document.execCommand('justifyRight');
                document.getElementById('justify').onclick = () => document.execCommand('justifyFull');
                
                // List buttons
                document.getElementById('bullet-list').onclick = () => document.execCommand('insertUnorderedList');
                document.getElementById('number-list').onclick = () => document.execCommand('insertOrderedList');
                
                // Font family and size
                document.getElementById('font-family').onchange = (e) => {{
                    document.execCommand('fontName', false, e.target.value);
                }};
                
                document.getElementById('font-size').onchange = (e) => {{
                    document.execCommand('fontSize', false, e.target.value);
                }};
            }}
            
            function setupDocumentEvents() {{
                const doc = document.getElementById('document');
                
                doc.oninput = () => {{
                    updateStatistics();
                    documentContent = doc.innerHTML;
                    isModified = true;
                }};
                
                // Save button
                document.getElementById('save-doc').onclick = saveDocument;
                
                // Save document as DOCX
                document.getElementById('save-docx').onclick = () => {{
                    const contentEl = document.getElementById('document');
                    const content = contentEl.innerHTML || contentEl.textContent || 'No content';
                    
                    // Create a simple HTML version for download
                    const htmlContent = '<!DOCTYPE html><html><head><title>Document</title><style>body {{font-family: Arial, sans-serif; margin: 40px; line-height: 1.6;}} .document {{max-width: 800px; margin: 0 auto;}}</style></head><body><div class="document">' + content + '</div></body></html>';
                    
                    const blob = new Blob([htmlContent], {{type: 'text/html'}});
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'document_' + new Date().toISOString().slice(0,19).replace(/:/g,'-') + '.html';
                    a.click();
                    URL.revokeObjectURL(url);
                }};
            }}
            
            function updateStatistics() {{
                const doc = document.getElementById('document');
                const text = doc.textContent || doc.innerText || '';
                const words = text.trim() ? text.trim().split(/\\s+/).length : 0;
                const chars = text.length;
                
                document.getElementById('word-count').textContent = words;
                document.getElementById('char-count').textContent = chars;
            }}
            
            function saveDocument() {{
                const doc = document.getElementById('document');
                documentContent = doc.innerHTML;
                isModified = false;
                
                // Send data back to Streamlit
                window.parent.postMessage({{
                    type: 'streamlit:setComponentValue',
                    value: documentContent
                }}, '*');
            }}
            
            // Initialize when page loads
            window.onload = initEditor;
        </script>
    </body>
    </html>
    """
    
    # Create the component
    result = components.html(
        component_html,
        width=width + 50,
        height=height + 50
    )
    
    return result


def document_editor(content="", width=800, height=600, key=None):
    """Alias for theta_document_editor for convenience."""
    return theta_document_editor(content, width, height, key)
