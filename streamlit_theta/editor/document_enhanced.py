import streamlit as st
import streamlit.components.v1 as components
from typing import Dict, List, Any, Optional
import json
import sys
import os

# Add the parent directory to sys.path to import theme_manager
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from theme_manager import ThemeManager

def theta_document_editor_enhanced(
    content: str = "",
    width: int = 800,
    height: int = 600,
    theme: str = "light",
    mode: str = "edit",  # edit, preview, split
    enable_autosave: bool = True,
    enable_collaboration: bool = False,
    templates: Optional[List[Dict[str, Any]]] = None,
    key: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    Enhanced document editor with new modes and features.
    
    Parameters:
    -----------
    content : str
        Initial document content (HTML format)
    width : int
        Width of the editor in pixels
    height : int  
        Height of the editor in pixels
    theme : str
        Theme name (light, dark, blue, green, purple)
    mode : str
        Editor mode (edit, preview, split)
    enable_autosave : bool
        Enable automatic saving
    enable_collaboration : bool
        Enable collaboration features
    templates : List[Dict[str, Any]]
        Document templates
    key : str, optional
        Unique key for the component
        
    Returns:
    --------
    Dict[str, Any] or None
        Updated document data with content, mode, and metadata
    """
    
    # Default templates
    if templates is None:
        templates = [
            {
                "name": "Blank Document",
                "content": "<h1>New Document</h1><p>Start writing here...</p>",
                "category": "Basic"
            },
            {
                "name": "Business Letter",
                "content": """
                <div style="margin-bottom: 20px;">
                    <div style="text-align: right; margin-bottom: 20px;">
                        <p>[Your Name]<br>[Your Address]<br>[City, State ZIP Code]<br>[Email Address]<br>[Phone Number]</p>
                        <p>[Date]</p>
                    </div>
                    <p>[Recipient Name]<br>[Title]<br>[Company Name]<br>[Address]<br>[City, State ZIP Code]</p>
                    <p>Dear [Recipient Name],</p>
                    <p>I am writing to...</p>
                    <p>Thank you for your time and consideration.</p>
                    <p>Sincerely,<br>[Your Name]</p>
                </div>
                """,
                "category": "Business"
            },
            {
                "name": "Resume",
                "content": """
                <div style="max-width: 800px; margin: 0 auto; font-family: Arial, sans-serif;">
                    <h1 style="text-align: center; color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;">[Your Name]</h1>
                    <p style="text-align: center; color: #7f8c8d; margin-bottom: 20px;">[Your Title] | [Email] | [Phone] | [Location]</p>
                    
                    <h2 style="color: #2c3e50; border-bottom: 1px solid #bdc3c7; padding-bottom: 5px;">Professional Summary</h2>
                    <p>Brief overview of your experience and key skills...</p>
                    
                    <h2 style="color: #2c3e50; border-bottom: 1px solid #bdc3c7; padding-bottom: 5px;">Work Experience</h2>
                    <h3>[Job Title] - [Company Name]</h3>
                    <p style="color: #7f8c8d; font-style: italic;">[Start Date] - [End Date]</p>
                    <ul>
                        <li>Key achievement or responsibility</li>
                        <li>Another important accomplishment</li>
                    </ul>
                    
                    <h2 style="color: #2c3e50; border-bottom: 1px solid #bdc3c7; padding-bottom: 5px;">Education</h2>
                    <h3>[Degree] - [University Name]</h3>
                    <p style="color: #7f8c8d; font-style: italic;">[Graduation Year]</p>
                    
                    <h2 style="color: #2c3e50; border-bottom: 1px solid #bdc3c7; padding-bottom: 5px;">Skills</h2>
                    <p>List your key skills here...</p>
                </div>
                """,
                "category": "Professional"
            },
            {
                "name": "Meeting Minutes",
                "content": """
                <div style="max-width: 800px; margin: 0 auto;">
                    <h1 style="text-align: center; color: #2c3e50;">Meeting Minutes</h1>
                    <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
                        <p><strong>Date:</strong> [Meeting Date]</p>
                        <p><strong>Time:</strong> [Start Time] - [End Time]</p>
                        <p><strong>Location:</strong> [Meeting Location/Platform]</p>
                        <p><strong>Chair:</strong> [Meeting Chair]</p>
                        <p><strong>Attendees:</strong> [List of Attendees]</p>
                    </div>
                    
                    <h2>Agenda Items</h2>
                    <ol>
                        <li>Agenda item 1</li>
                        <li>Agenda item 2</li>
                        <li>Agenda item 3</li>
                    </ol>
                    
                    <h2>Discussion Points</h2>
                    <h3>1. [Topic]</h3>
                    <p>Discussion summary...</p>
                    
                    <h2>Action Items</h2>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr style="background: #f8f9fa;">
                            <th style="border: 1px solid #dee2e6; padding: 8px;">Action</th>
                            <th style="border: 1px solid #dee2e6; padding: 8px;">Responsible</th>
                            <th style="border: 1px solid #dee2e6; padding: 8px;">Due Date</th>
                        </tr>
                        <tr>
                            <td style="border: 1px solid #dee2e6; padding: 8px;">[Action item]</td>
                            <td style="border: 1px solid #dee2e6; padding: 8px;">[Person]</td>
                            <td style="border: 1px solid #dee2e6; padding: 8px;">[Date]</td>
                        </tr>
                    </table>
                    
                    <h2>Next Meeting</h2>
                    <p><strong>Date:</strong> [Next Meeting Date]</p>
                    <p><strong>Time:</strong> [Next Meeting Time]</p>
                </div>
                """,
                "category": "Business"
            }
        ]
    
    # Get theme CSS
    theme_css = ThemeManager.generate_css(theme)
    theme_switcher_html = ThemeManager.get_theme_switcher_html(theme)
    theme_switcher_js = ThemeManager.get_theme_switcher_js()
    
    # Convert templates to JSON
    templates_json = json.dumps(templates)
    
    component_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Enhanced Document Editor</title>
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
            
            .editor-container {{
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
            
            .mode-btn:hover:not(.active) {{
                background: var(--primary-bg);
                color: var(--text-primary);
            }}
            
            .toolbar {{
                background: var(--secondary-bg);
                border-bottom: 1px solid var(--border-color);
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
                border-right: 1px solid var(--border-color);
                padding-right: 12px;
            }}
            
            .toolbar-group:last-child {{
                border-right: none;
            }}
            
            .toolbar .theta-button {{
                min-width: 36px;
                height: 36px;
                font-size: 14px;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 4px;
            }}
            
            .toolbar .theta-button.active {{
                background: var(--accent-color);
                color: var(--primary-bg);
            }}
            
            .toolbar select {{
                background: var(--primary-bg);
                color: var(--text-primary);
                border: 1px solid var(--border-color);
                border-radius: 4px;
                padding: 6px 8px;
                font-size: 14px;
            }}
            
            .content-area {{
                flex: 1;
                display: flex;
                overflow: hidden;
            }}
            
            .editor-pane {{
                flex: 1;
                display: flex;
                flex-direction: column;
                border-right: 1px solid var(--border-color);
            }}
            
            .editor-pane.full {{
                border-right: none;
            }}
            
            .preview-pane {{
                flex: 1;
                display: flex;
                flex-direction: column;
            }}
            
            .editor-content {{
                flex: 1;
                padding: 20px;
                overflow-y: auto;
                background: var(--primary-bg);
                outline: none;
                font-family: inherit;
                font-size: 16px;
                line-height: 1.6;
                color: var(--text-primary);
            }}
            
            .preview-content {{
                flex: 1;
                padding: 20px;
                overflow-y: auto;
                background: var(--primary-bg);
                font-family: inherit;
                font-size: 16px;
                line-height: 1.6;
                color: var(--text-primary);
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
            
            .status-left {{
                display: flex;
                gap: 16px;
            }}
            
            .status-right {{
                display: flex;
                gap: 16px;
            }}
            
            .word-count {{
                font-weight: 500;
            }}
            
            .autosave-indicator {{
                color: var(--success-color);
            }}
            
            .autosave-indicator.saving {{
                color: var(--warning-color);
            }}
            
            .collaboration-indicator {{
                display: flex;
                align-items: center;
                gap: 4px;
                color: var(--info-color);
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
                grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
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
            }}
            
            .template-card:hover {{
                background: var(--tertiary-bg);
                border-color: var(--accent-color);
                transform: translateY(-2px);
            }}
            
            .template-name {{
                font-weight: 600;
                color: var(--text-primary);
                margin-bottom: 8px;
            }}
            
            .template-category {{
                font-size: 12px;
                color: var(--text-secondary);
                background: var(--tertiary-bg);
                padding: 2px 6px;
                border-radius: 3px;
                display: inline-block;
            }}
            
            .find-replace-panel {{
                position: absolute;
                top: 60px;
                right: 16px;
                background: var(--primary-bg);
                border: 1px solid var(--border-color);
                border-radius: 6px;
                padding: 16px;
                box-shadow: var(--shadow-hover);
                z-index: 500;
                min-width: 300px;
            }}
            
            .find-replace-row {{
                display: flex;
                gap: 8px;
                margin-bottom: 8px;
                align-items: center;
            }}
            
            .find-replace-row input {{
                flex: 1;
                padding: 6px 8px;
                border: 1px solid var(--border-color);
                border-radius: 4px;
                background: var(--primary-bg);
                color: var(--text-primary);
            }}
            
            .find-replace-row .theta-button {{
                padding: 6px 12px;
                font-size: 12px;
                height: auto;
                min-width: auto;
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
                
                .header-left, .header-right {{
                    justify-content: center;
                }}
                
                .toolbar {{
                    justify-content: center;
                }}
                
                .content-area {{
                    flex-direction: column;
                }}
                
                .editor-pane {{
                    border-right: none;
                    border-bottom: 1px solid var(--border-color);
                }}
                
                .templates-content {{
                    margin: 16px;
                    max-width: calc(100% - 32px);
                }}
                
                .templates-grid {{
                    grid-template-columns: 1fr;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="editor-container theta-editor" data-theme="{theme}">
            {theme_switcher_html}
            
            <div class="header">
                <div class="header-left">
                    <h3>📝 Enhanced Document Editor</h3>
                    <div class="mode-switcher">
                        <button class="mode-btn active" data-mode="edit">✏️ Edit</button>
                        <button class="mode-btn" data-mode="preview">👁️ Preview</button>
                        <button class="mode-btn" data-mode="split">↔️ Split</button>
                    </div>
                </div>
                <div class="header-right">
                    <button class="theta-button" onclick="showTemplates()">📋 Templates</button>
                    <button class="theta-button" onclick="toggleFindReplace()">🔍 Find & Replace</button>
                    <button class="theta-button success" onclick="saveDocument()">💾 Save</button>
                </div>
            </div>
            
            <div class="toolbar">
                <div class="toolbar-group">
                    <button class="theta-button" onclick="executeCommand('undo')" title="Undo">↶</button>
                    <button class="theta-button" onclick="executeCommand('redo')" title="Redo">↷</button>
                </div>
                <div class="toolbar-group">
                    <button class="theta-button" onclick="executeCommand('bold')" title="Bold"><strong>B</strong></button>
                    <button class="theta-button" onclick="executeCommand('italic')" title="Italic"><em>I</em></button>
                    <button class="theta-button" onclick="executeCommand('underline')" title="Underline"><u>U</u></button>
                    <button class="theta-button" onclick="executeCommand('strikethrough')" title="Strikethrough"><s>S</s></button>
                </div>
                <div class="toolbar-group">
                    <select onchange="executeCommand('formatBlock', this.value)">
                        <option value="p">Paragraph</option>
                        <option value="h1">Heading 1</option>
                        <option value="h2">Heading 2</option>
                        <option value="h3">Heading 3</option>
                        <option value="h4">Heading 4</option>
                        <option value="h5">Heading 5</option>
                        <option value="h6">Heading 6</option>
                    </select>
                </div>
                <div class="toolbar-group">
                    <button class="theta-button" onclick="executeCommand('justifyLeft')" title="Align Left">⬅️</button>
                    <button class="theta-button" onclick="executeCommand('justifyCenter')" title="Align Center">↔️</button>
                    <button class="theta-button" onclick="executeCommand('justifyRight')" title="Align Right">➡️</button>
                    <button class="theta-button" onclick="executeCommand('justifyFull')" title="Justify">↕️</button>
                </div>
                <div class="toolbar-group">
                    <button class="theta-button" onclick="executeCommand('insertUnorderedList')" title="Bullet List">• List</button>
                    <button class="theta-button" onclick="executeCommand('insertOrderedList')" title="Numbered List">1. List</button>
                    <button class="theta-button" onclick="executeCommand('indent')" title="Indent">→</button>
                    <button class="theta-button" onclick="executeCommand('outdent')" title="Outdent">←</button>
                </div>
                <div class="toolbar-group">
                    <button class="theta-button" onclick="insertTable()" title="Insert Table">📊 Table</button>
                    <button class="theta-button" onclick="insertImage()" title="Insert Image">🖼️ Image</button>
                    <button class="theta-button" onclick="insertLink()" title="Insert Link">🔗 Link</button>
                </div>
            </div>
            
            <div class="content-area">
                <div class="editor-pane full" id="editor-pane">
                    <div class="editor-content" id="editor-content" contenteditable="true">
                        {content}
                    </div>
                </div>
                <div class="preview-pane hidden" id="preview-pane">
                    <div class="preview-content" id="preview-content">
                        {content}
                    </div>
                </div>
            </div>
            
            <div class="find-replace-panel hidden" id="find-replace-panel">
                <div class="find-replace-row">
                    <input type="text" id="find-input" placeholder="Find...">
                    <button class="theta-button" onclick="findText()">Find</button>
                    <button class="theta-button" onclick="findNext()">Next</button>
                </div>
                <div class="find-replace-row">
                    <input type="text" id="replace-input" placeholder="Replace with...">
                    <button class="theta-button" onclick="replaceText()">Replace</button>
                    <button class="theta-button" onclick="replaceAll()">Replace All</button>
                </div>
                <div class="find-replace-row">
                    <button class="theta-button" onclick="toggleFindReplace()">Close</button>
                </div>
            </div>
            
            <div class="status-bar">
                <div class="status-left">
                    <span class="word-count">Words: <span id="word-count">0</span></span>
                    <span>Characters: <span id="char-count">0</span></span>
                    <span>Lines: <span id="line-count">0</span></span>
                </div>
                <div class="status-right">
                    <span class="autosave-indicator" id="autosave-indicator">
                        {"✅ Auto-save enabled" if enable_autosave else "⚠️ Auto-save disabled"}
                    </span>
                    {"<span class='collaboration-indicator'>👥 Collaboration mode</span>" if enable_collaboration else ""}
                </div>
            </div>
        </div>
        
        <div class="templates-panel hidden" id="templates-panel">
            <div class="templates-content">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                    <h2>📋 Document Templates</h2>
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
            let autosaveEnabled = {str(enable_autosave).lower()};
            let collaborationEnabled = {str(enable_collaboration).lower()};
            let templates = {templates_json};
            let autosaveTimeout;
            let findResults = [];
            let currentFindIndex = 0;
            
            // Initialize editor
            document.addEventListener('DOMContentLoaded', function() {{
                populateTemplates();
                updateWordCount();
                setupEventListeners();
                if (autosaveEnabled) {{
                    startAutosave();
                }}
            }});
            
            function setupEventListeners() {{
                const editorContent = document.getElementById('editor-content');
                const modeBtns = document.querySelectorAll('.mode-btn');
                
                // Mode switching
                modeBtns.forEach(btn => {{
                    btn.addEventListener('click', function() {{
                        switchMode(this.dataset.mode);
                    }});
                }});
                
                // Editor content changes
                editorContent.addEventListener('input', function() {{
                    updateWordCount();
                    updatePreview();
                    if (autosaveEnabled) {{
                        scheduleAutosave();
                    }}
                }});
                
                // Keyboard shortcuts
                document.addEventListener('keydown', function(e) {{
                    if (e.ctrlKey || e.metaKey) {{
                        switch(e.key) {{
                            case 's':
                                e.preventDefault();
                                saveDocument();
                                break;
                            case 'f':
                                e.preventDefault();
                                toggleFindReplace();
                                break;
                            case 'z':
                                if (e.shiftKey) {{
                                    executeCommand('redo');
                                }} else {{
                                    executeCommand('undo');
                                }}
                                break;
                            case 'b':
                                e.preventDefault();
                                executeCommand('bold');
                                break;
                            case 'i':
                                e.preventDefault();
                                executeCommand('italic');
                                break;
                            case 'u':
                                e.preventDefault();
                                executeCommand('underline');
                                break;
                        }}
                    }}
                }});
            }}
            
            function switchMode(mode) {{
                currentMode = mode;
                const modeBtns = document.querySelectorAll('.mode-btn');
                const editorPane = document.getElementById('editor-pane');
                const previewPane = document.getElementById('preview-pane');
                
                // Update button states
                modeBtns.forEach(btn => {{
                    btn.classList.toggle('active', btn.dataset.mode === mode);
                }});
                
                // Update pane visibility
                switch(mode) {{
                    case 'edit':
                        editorPane.classList.add('full');
                        editorPane.classList.remove('hidden');
                        previewPane.classList.add('hidden');
                        break;
                    case 'preview':
                        editorPane.classList.add('hidden');
                        previewPane.classList.remove('hidden');
                        previewPane.classList.add('full');
                        updatePreview();
                        break;
                    case 'split':
                        editorPane.classList.remove('full', 'hidden');
                        previewPane.classList.remove('full', 'hidden');
                        updatePreview();
                        break;
                }}
            }}
            
            function updatePreview() {{
                const editorContent = document.getElementById('editor-content');
                const previewContent = document.getElementById('preview-content');
                previewContent.innerHTML = editorContent.innerHTML;
            }}
            
            function updateWordCount() {{
                const editorContent = document.getElementById('editor-content');
                const text = editorContent.innerText || editorContent.textContent || '';
                const words = text.trim().split(/\\s+/).filter(word => word.length > 0);
                const lines = text.split('\n').length;
                
                document.getElementById('word-count').textContent = words.length;
                document.getElementById('char-count').textContent = text.length;
                document.getElementById('line-count').textContent = lines;
            }}
            
            function executeCommand(command, value = null) {{
                document.execCommand(command, false, value);
                const editorContent = document.getElementById('editor-content');
                editorContent.focus();
                updateWordCount();
                updatePreview();
            }}
            
            function insertTable() {{
                const rows = prompt('Number of rows:', '3');
                const cols = prompt('Number of columns:', '3');
                
                if (rows && cols) {{
                    let tableHTML = '<table style="border-collapse: collapse; width: 100%; border: 1px solid var(--border-color);">';
                    
                    for (let i = 0; i < parseInt(rows); i++) {{
                        tableHTML += '<tr>';
                        for (let j = 0; j < parseInt(cols); j++) {{
                            tableHTML += '<td style="border: 1px solid var(--border-color); padding: 8px;">Cell</td>';
                        }}
                        tableHTML += '</tr>';
                    }}
                    tableHTML += '</table>';
                    
                    executeCommand('insertHTML', tableHTML);
                }}
            }}
            
            function insertImage() {{
                const url = prompt('Image URL:', '');
                if (url) {{
                    executeCommand('insertImage', url);
                }}
            }}
            
            function insertLink() {{
                const url = prompt('Link URL:', '');
                if (url) {{
                    executeCommand('createLink', url);
                }}
            }}
            
            function populateTemplates() {{
                const grid = document.getElementById('templates-grid');
                grid.innerHTML = '';
                
                templates.forEach(template => {{
                    const card = document.createElement('div');
                    card.className = 'template-card';
                    card.innerHTML = `
                        <div class="template-name">${{template.name}}</div>
                        <div class="template-category">${{template.category}}</div>
                    `;
                    card.addEventListener('click', function() {{
                        loadTemplate(template);
                    }});
                    grid.appendChild(card);
                }});
            }}
            
            function loadTemplate(template) {{
                const editorContent = document.getElementById('editor-content');
                editorContent.innerHTML = template.content;
                updateWordCount();
                updatePreview();
                hideTemplates();
            }}
            
            function showTemplates() {{
                document.getElementById('templates-panel').classList.remove('hidden');
            }}
            
            function hideTemplates() {{
                document.getElementById('templates-panel').classList.add('hidden');
            }}
            
            function toggleFindReplace() {{
                const panel = document.getElementById('find-replace-panel');
                panel.classList.toggle('hidden');
                if (!panel.classList.contains('hidden')) {{
                    document.getElementById('find-input').focus();
                }}
            }}
            
            function findText() {{
                const findInput = document.getElementById('find-input');
                const searchTerm = findInput.value.toLowerCase();
                const editorContent = document.getElementById('editor-content');
                
                if (!searchTerm) return;
                
                // Clear previous highlights
                const highlighted = editorContent.querySelectorAll('.search-highlight');
                highlighted.forEach(el => {{
                    el.outerHTML = el.innerHTML;
                }});
                
                // Find and highlight all matches
                const walker = document.createTreeWalker(
                    editorContent,
                    NodeFilter.SHOW_TEXT,
                    null,
                    false
                );
                
                const textNodes = [];
                let node;
                while (node = walker.nextNode()) {{
                    textNodes.push(node);
                }}
                
                findResults = [];
                textNodes.forEach(textNode => {{
                    const text = textNode.textContent.toLowerCase();
                    let index = 0;
                    while ((index = text.indexOf(searchTerm, index)) !== -1) {{
                        findResults.push({{
                            node: textNode,
                            start: index,
                            end: index + searchTerm.length
                        }});
                        index++;
                    }}
                }});
                
                highlightResults();
            }}
            
            function highlightResults() {{
                findResults.forEach((result, index) => {{
                    const textNode = result.node;
                    const start = result.start;
                    const end = result.end;
                    
                    const beforeText = textNode.textContent.substring(0, start);
                    const highlightText = textNode.textContent.substring(start, end);
                    const afterText = textNode.textContent.substring(end);
                    
                    const span = document.createElement('span');
                    span.className = 'search-highlight';
                    span.style.backgroundColor = '#ffeb3b';
                    span.style.color = '#000';
                    span.textContent = highlightText;
                    
                    const parent = textNode.parentNode;
                    const beforeNode = document.createTextNode(beforeText);
                    const afterNode = document.createTextNode(afterText);
                    
                    parent.insertBefore(beforeNode, textNode);
                    parent.insertBefore(span, textNode);
                    parent.insertBefore(afterNode, textNode);
                    parent.removeChild(textNode);
                }});
            }}
            
            function findNext() {{
                if (findResults.length === 0) return;
                
                currentFindIndex = (currentFindIndex + 1) % findResults.length;
                const highlights = document.querySelectorAll('.search-highlight');
                if (highlights[currentFindIndex]) {{
                    highlights[currentFindIndex].scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                }}
            }}
            
            function replaceText() {{
                const replaceInput = document.getElementById('replace-input');
                const replaceValue = replaceInput.value;
                
                if (findResults.length === 0) return;
                
                const highlights = document.querySelectorAll('.search-highlight');
                if (highlights[currentFindIndex]) {{
                    highlights[currentFindIndex].outerHTML = replaceValue;
                    findResults.splice(currentFindIndex, 1);
                    if (currentFindIndex >= findResults.length) {{
                        currentFindIndex = 0;
                    }}
                }}
            }}
            
            function replaceAll() {{
                const replaceInput = document.getElementById('replace-input');
                const replaceValue = replaceInput.value;
                
                const highlights = document.querySelectorAll('.search-highlight');
                highlights.forEach(highlight => {{
                    highlight.outerHTML = replaceValue;
                }});
                
                findResults = [];
                currentFindIndex = 0;
            }}
            
            function scheduleAutosave() {{
                if (autosaveTimeout) {{
                    clearTimeout(autosaveTimeout);
                }}
                
                const indicator = document.getElementById('autosave-indicator');
                indicator.textContent = '💾 Saving...';
                indicator.className = 'autosave-indicator saving';
                
                autosaveTimeout = setTimeout(function() {{
                    autosave();
                }}, 2000);
            }}
            
            function startAutosave() {{
                if (!autosaveEnabled) return;
                
                setInterval(function() {{
                    autosave();
                }}, 30000); // Auto-save every 30 seconds
            }}
            
            function autosave() {{
                const editorContent = document.getElementById('editor-content');
                const content = editorContent.innerHTML;
                
                // Save to localStorage
                localStorage.setItem('theta-document-autosave', content);
                
                const indicator = document.getElementById('autosave-indicator');
                indicator.textContent = '✅ Auto-saved';
                indicator.className = 'autosave-indicator';
                
                // Hide indicator after 2 seconds
                setTimeout(function() {{
                    indicator.textContent = '✅ Auto-save enabled';
                }}, 2000);
            }}
            
            function saveDocument() {{
                const editorContent = document.getElementById('editor-content');
                const content = editorContent.innerHTML;
                
                // Get document stats
                const text = editorContent.innerText || editorContent.textContent || '';
                const words = text.trim().split(/\s+/).filter(word => word.length > 0).length;
                const chars = text.length;
                const lines = text.split('\n').length;
                
                // Create document data
                const documentData = {{
                    content: content,
                    mode: currentMode,
                    theme: document.documentElement.getAttribute('data-theme') || 'light',
                    stats: {{
                        words: words,
                        characters: chars,
                        lines: lines
                    }},
                    metadata: {{
                        lastModified: new Date().toISOString(),
                        version: '1.1.0'
                    }}
                }};
                
                // Send to Streamlit
                window.parent.postMessage({{
                    type: 'streamlit:setComponentValue',
                    value: documentData
                }}, '*');
                
                // Show success message
                const indicator = document.getElementById('autosave-indicator');
                indicator.textContent = '✅ Saved successfully';
                indicator.className = 'autosave-indicator';
                
                setTimeout(function() {{
                    indicator.textContent = autosaveEnabled ? '✅ Auto-save enabled' : '⚠️ Auto-save disabled';
                }}, 2000);
            }}
            
            // Load autosaved content on page load
            window.addEventListener('load', function() {{
                if (autosaveEnabled) {{
                    const savedContent = localStorage.getItem('theta-document-autosave');
                    if (savedContent && !'{content}'.trim()) {{
                        const editorContent = document.getElementById('editor-content');
                        editorContent.innerHTML = savedContent;
                        updateWordCount();
                        updatePreview();
                    }}
                }}
            }});
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