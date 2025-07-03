"""
Theta Newsletter/Email Editor - HTML email template designer
Provides a visual interface for creating email templates.
"""

import streamlit as st
import streamlit.components.v1 as components
import json
from typing import Dict, List, Any, Optional

def theta_newsletter_editor(
    template_data: Optional[Dict[str, Any]] = None,
    width: int = 900,
    height: int = 600,
    key: Optional[str] = None
) -> None:
    """
    Create a newsletter/email template editor.
    
    Parameters:
    -----------
    template_data : Dict[str, Any]
        Email template data with sections and content
    width : int
        Width of the editor in pixels
    height : int  
        Height of the editor in pixels
    key : str or None
        Unique key for the component
    
    Returns:
    --------
    Dict with email template data or None
    """
    
    # Default template data if none provided
    if template_data is None:
        template_data = {
            "subject": "Welcome to Our Newsletter",
            "preheader": "Stay updated with our latest news and updates",
            "settings": {
                "width": 600,
                "backgroundColor": "#f4f4f4",
                "fontFamily": "Arial, sans-serif",
                "textColor": "#333333"
            },
            "sections": [
                {
                    "id": "header",
                    "type": "header",
                    "content": {
                        "logo": "",
                        "title": "Company Newsletter",
                        "subtitle": "Monthly Updates & News",
                        "backgroundColor": "#007bff",
                        "textColor": "#ffffff"
                    }
                },
                {
                    "id": "content1",
                    "type": "text",
                    "content": {
                        "title": "Welcome Message",
                        "text": "Thank you for subscribing to our newsletter. We're excited to share our latest updates with you.",
                        "alignment": "left"
                    }
                },
                {
                    "id": "content2",
                    "type": "button",
                    "content": {
                        "text": "Read More",
                        "url": "https://example.com",
                        "backgroundColor": "#28a745",
                        "textColor": "#ffffff",
                        "alignment": "center"
                    }
                },
                {
                    "id": "footer",
                    "type": "footer",
                    "content": {
                        "text": "© 2024 Company Name. All rights reserved.",
                        "unsubscribeText": "Unsubscribe from this list",
                        "unsubscribeUrl": "#",
                        "backgroundColor": "#f8f9fa",
                        "textColor": "#6c757d"
                    }
                }
            ]
        }
    
    # Convert template data to JSON for JavaScript
    data_json = json.dumps(template_data).replace('"', '\\"')
    
    component_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Theta Newsletter Editor</title>
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
            
            .editor-header {{
                padding: 15px 20px;
                background: #f8f9fa;
                border-bottom: 1px solid #dee2e6;
                border-radius: 8px 8px 0 0;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}
            
            .editor-content {{
                flex: 1;
                display: flex;
            }}
            
            .email-preview {{
                flex: 1;
                padding: 20px;
                background: #f8f9fa;
                overflow-y: auto;
            }}
            
            .email-container {{
                max-width: 600px;
                margin: 0 auto;
                background: white;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                overflow: hidden;
            }}
            
            .components-panel {{
                width: 250px;
                background: white;
                border-right: 1px solid #dee2e6;
                padding: 20px;
                overflow-y: auto;
            }}
            
            .properties-panel {{
                width: 300px;
                background: white;
                border-left: 1px solid #dee2e6;
                padding: 20px;
                overflow-y: auto;
            }}
            
            .component-library h4 {{
                margin: 0 0 15px 0;
                font-size: 14px;
                color: #495057;
            }}
            
            .component-item {{
                display: flex;
                align-items: center;
                padding: 12px;
                margin-bottom: 8px;
                background: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                cursor: pointer;
                transition: all 0.2s;
            }}
            
            .component-item:hover {{
                border-color: #007bff;
                background: #e3f2fd;
            }}
            
            .component-icon {{
                width: 24px;
                text-align: center;
                margin-right: 12px;
                font-size: 16px;
            }}
            
            .email-section {{
                position: relative;
                border: 2px dashed transparent;
                transition: all 0.2s;
            }}
            
            .email-section:hover {{
                border-color: #007bff;
            }}
            
            .email-section.selected {{
                border-color: #007bff;
                background: rgba(0, 123, 255, 0.05);
            }}
            
            .section-controls {{
                position: absolute;
                top: 5px;
                right: 5px;
                display: none;
                gap: 5px;
            }}
            
            .email-section:hover .section-controls,
            .email-section.selected .section-controls {{
                display: flex;
            }}
            
            .control-btn {{
                width: 20px;
                height: 20px;
                border: none;
                border-radius: 3px;
                cursor: pointer;
                font-size: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 1px 3px rgba(0,0,0,0.2);
            }}
            
            .control-btn.edit {{ background: #007bff; color: white; }}
            .control-btn.delete {{ background: #dc3545; color: white; }}
            .control-btn.move {{ background: #6c757d; color: white; cursor: move; }}
            
            .property-group {{
                margin-bottom: 20px;
                padding: 15px;
                background: #f8f9fa;
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
            
            .btn.secondary {{
                background: #6c757d;
            }}
            
            .btn.secondary:hover {{
                background: #545b62;
            }}
            
            /* Email Section Styles */
            .email-header {{
                padding: 30px 20px;
                text-align: center;
            }}
            
            .email-title {{
                margin: 0 0 10px 0;
                font-size: 24px;
                font-weight: bold;
            }}
            
            .email-subtitle {{
                margin: 0;
                font-size: 16px;
                opacity: 0.8;
            }}
            
            .email-text {{
                padding: 20px;
            }}
            
            .email-text h3 {{
                margin: 0 0 15px 0;
                font-size: 18px;
                color: #333;
            }}
            
            .email-text p {{
                margin: 0;
                line-height: 1.6;
                color: #555;
            }}
            
            .email-button {{
                padding: 20px;
                text-align: center;
            }}
            
            .email-btn {{
                display: inline-block;
                padding: 12px 24px;
                text-decoration: none;
                border-radius: 6px;
                font-weight: bold;
                color: white;
            }}
            
            .email-image {{
                padding: 20px;
                text-align: center;
            }}
            
            .email-image img {{
                max-width: 100%;
                height: auto;
                border-radius: 6px;
            }}
            
            .email-spacer {{
                height: 20px;
                background: transparent;
            }}
            
            .email-footer {{
                padding: 20px;
                text-align: center;
                font-size: 12px;
                border-top: 1px solid #eee;
            }}
            
            .email-footer p {{
                margin: 5px 0;
            }}
            
            .email-footer a {{
                color: #007bff;
                text-decoration: none;
            }}
            
            .toolbar {{
                display: flex;
                gap: 10px;
                align-items: center;
            }}
            
            .toolbar button {{
                padding: 6px 12px;
                border: 1px solid #dee2e6;
                background: white;
                border-radius: 4px;
                cursor: pointer;
                font-size: 11px;
            }}
            
            .toolbar button:hover {{
                background: #f8f9fa;
            }}
            
            .drop-zone {{
                min-height: 60px;
                border: 2px dashed #dee2e6;
                border-radius: 6px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #6c757d;
                font-style: italic;
                margin: 10px;
                transition: all 0.2s;
            }}
            
            .drop-zone.dragover {{
                border-color: #007bff;
                background: #f8f9ff;
                color: #007bff;
            }}
            
            .preview-controls {{
                display: flex;
                gap: 10px;
                align-items: center;
                margin-bottom: 15px;
            }}
            
            .device-preview {{
                display: flex;
                gap: 5px;
            }}
            
            .device-btn {{
                padding: 5px 10px;
                border: 1px solid #dee2e6;
                background: white;
                border-radius: 4px;
                cursor: pointer;
                font-size: 11px;
            }}
            
            .device-btn.active {{
                background: #007bff;
                color: white;
                border-color: #007bff;
            }}
        </style>
    </head>
    <body>
        <div class="editor-container">
            <div class="editor-header">
                <h3 style="margin: 0;">📧 Newsletter Editor</h3>
                <div class="toolbar">
                    <button onclick="previewEmail()">👁️ Preview</button>
                    <button onclick="testEmail()">📤 Test Send</button>
                    <button onclick="exportEmail()">💾 Export</button>
                </div>
            </div>
            
            <div class="editor-content">
                <div class="components-panel">
                    <div class="component-library">
                        <h4>📚 Components</h4>
                        
                        <div class="component-item" onclick="addSection('header')">
                            <span class="component-icon">🏠</span>
                            <span>Header</span>
                        </div>
                        
                        <div class="component-item" onclick="addSection('text')">
                            <span class="component-icon">📝</span>
                            <span>Text Block</span>
                        </div>
                        
                        <div class="component-item" onclick="addSection('button')">
                            <span class="component-icon">🔘</span>
                            <span>Button</span>
                        </div>
                        
                        <div class="component-item" onclick="addSection('image')">
                            <span class="component-icon">🖼️</span>
                            <span>Image</span>
                        </div>
                        
                        <div class="component-item" onclick="addSection('columns')">
                            <span class="component-icon">📊</span>
                            <span>Columns</span>
                        </div>
                        
                        <div class="component-item" onclick="addSection('spacer')">
                            <span class="component-icon">📏</span>
                            <span>Spacer</span>
                        </div>
                        
                        <div class="component-item" onclick="addSection('divider')">
                            <span class="component-icon">➖</span>
                            <span>Divider</span>
                        </div>
                        
                        <div class="component-item" onclick="addSection('footer')">
                            <span class="component-icon">🔽</span>
                            <span>Footer</span>
                        </div>
                    </div>
                </div>
                
                <div class="email-preview">
                    <div class="preview-controls">
                        <div class="device-preview">
                            <button class="device-btn active" onclick="setPreviewMode('desktop')">🖥️ Desktop</button>
                            <button class="device-btn" onclick="setPreviewMode('mobile')">📱 Mobile</button>
                        </div>
                        <span style="color: #6c757d; font-size: 12px;">Preview Mode</span>
                    </div>
                    
                    <div class="email-container" id="email-container">
                        <!-- Email sections will be rendered here -->
                    </div>
                    
                    <div class="drop-zone" id="drop-zone">
                        Drop components here or click to add sections
                    </div>
                </div>
                
                <div class="properties-panel">
                    <div class="property-group">
                        <h4>📧 Email Settings</h4>
                        <div class="property-row">
                            <label>Subject Line:</label>
                            <input type="text" id="email-subject" value="Welcome to Our Newsletter" onchange="updateEmailSettings()">
                        </div>
                        <div class="property-row">
                            <label>Preheader Text:</label>
                            <textarea id="email-preheader" onchange="updateEmailSettings()">Stay updated with our latest news and updates</textarea>
                        </div>
                        <div class="property-row">
                            <label>Email Width:</label>
                            <select id="email-width" onchange="updateEmailSettings()">
                                <option value="600">600px (Standard)</option>
                                <option value="700">700px (Wide)</option>
                                <option value="100%">100% (Responsive)</option>
                            </select>
                        </div>
                        <div class="property-row">
                            <label>Background Color:</label>
                            <input type="color" id="email-bg" value="#f4f4f4" class="color-input" onchange="updateEmailSettings()">
                        </div>
                        <div class="property-row">
                            <label>Font Family:</label>
                            <select id="email-font" onchange="updateEmailSettings()">
                                <option value="Arial, sans-serif">Arial</option>
                                <option value="Georgia, serif">Georgia</option>
                                <option value="'Times New Roman', serif">Times New Roman</option>
                                <option value="Helvetica, sans-serif">Helvetica</option>
                            </select>
                        </div>
                    </div>
                    
                    <div class="property-group" id="section-properties" style="display: none;">
                        <h4>🔧 Section Properties</h4>
                        <div id="section-properties-content">
                            <!-- Section-specific properties will be shown here -->
                        </div>
                    </div>
                    
                    <div class="property-group">
                        <h4>💾 Export</h4>
                        <button onclick="exportEmail('html')" class="btn">🌐 Export HTML</button>
                        <button onclick="exportEmail('json')" class="btn">📄 Export JSON</button>
                        <button onclick="generatePreview()" class="btn secondary">👁️ Open Preview</button>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            let templateData = {data_json};
            let selectedSection = null;
            let sectionCounter = 4;
            let previewMode = 'desktop';
            
            function initNewsletterEditor() {{
                renderEmail();
                setupDragAndDrop();
                updateEmailSettings();
            }}
            
            function renderEmail() {{
                const container = document.getElementById('email-container');
                container.innerHTML = '';
                
                // Apply email-wide styles
                container.style.width = templateData.settings.width + 'px';
                container.style.backgroundColor = templateData.settings.backgroundColor;
                container.style.fontFamily = templateData.settings.fontFamily;
                container.style.color = templateData.settings.textColor;
                
                templateData.sections.forEach((section, index) => {{
                    const sectionElement = createSectionElement(section, index);
                    container.appendChild(sectionElement);
                }});
            }}
            
            function createSectionElement(section, index) {{
                const wrapper = document.createElement('div');
                wrapper.className = 'email-section';
                wrapper.setAttribute('data-section-index', index);
                wrapper.onclick = (e) => {{
                    e.stopPropagation();
                    selectSection(index);
                }};
                
                const controls = document.createElement('div');
                controls.className = 'section-controls';
                controls.innerHTML = `
                    <button class="control-btn edit" onclick="editSection(${{index}})" title="Edit">✏️</button>
                    <button class="control-btn move" title="Move">↕️</button>
                    <button class="control-btn delete" onclick="deleteSection(${{index}})" title="Delete">🗑️</button>
                `;
                
                let sectionHTML = '';
                
                switch (section.type) {{
                    case 'header':
                        sectionHTML = `
                            <div class="email-header" style="background-color: ${{section.content.backgroundColor}}; color: ${{section.content.textColor}};">
                                ${{section.content.logo ? `<img src="${{section.content.logo}}" alt="Logo" style="max-height: 50px; margin-bottom: 15px;">` : ''}}
                                <h1 class="email-title">${{section.content.title}}</h1>
                                <p class="email-subtitle">${{section.content.subtitle}}</p>
                            </div>
                        `;
                        break;
                    case 'text':
                        sectionHTML = `
                            <div class="email-text" style="text-align: ${{section.content.alignment}};">
                                <h3>${{section.content.title}}</h3>
                                <p>${{section.content.text}}</p>
                            </div>
                        `;
                        break;
                    case 'button':
                        sectionHTML = `
                            <div class="email-button" style="text-align: ${{section.content.alignment}};">
                                <a href="${{section.content.url}}" class="email-btn" 
                                   style="background-color: ${{section.content.backgroundColor}}; color: ${{section.content.textColor}};">
                                    ${{section.content.text}}
                                </a>
                            </div>
                        `;
                        break;
                    case 'image':
                        sectionHTML = `
                            <div class="email-image">
                                <img src="${{section.content.src || 'https://via.placeholder.com/400x200'}}" 
                                     alt="${{section.content.alt || 'Image'}}"
                                     style="width: ${{section.content.width || '100%'}};">
                                ${{section.content.caption ? `<p style="margin-top: 10px; font-size: 12px; color: #666;">${{section.content.caption}}</p>` : ''}}
                            </div>
                        `;
                        break;
                    case 'spacer':
                        sectionHTML = `
                            <div class="email-spacer" style="height: ${{section.content.height || '20'}}px;"></div>
                        `;
                        break;
                    case 'divider':
                        sectionHTML = `
                            <div style="padding: 10px 20px;">
                                <hr style="border: none; height: 1px; background-color: ${{section.content.color || '#eee'}};">
                            </div>
                        `;
                        break;
                    case 'footer':
                        sectionHTML = `
                            <div class="email-footer" style="background-color: ${{section.content.backgroundColor}}; color: ${{section.content.textColor}};">
                                <p>${{section.content.text}}</p>
                                <p><a href="${{section.content.unsubscribeUrl}}" style="color: ${{section.content.textColor}};">${{section.content.unsubscribeText}}</a></p>
                            </div>
                        `;
                        break;
                }}
                
                wrapper.innerHTML = sectionHTML;
                wrapper.appendChild(controls);
                
                return wrapper;
            }}
            
            function setupDragAndDrop() {{
                const dropZone = document.getElementById('drop-zone');
                
                dropZone.addEventListener('dragover', (e) => {{
                    e.preventDefault();
                    dropZone.classList.add('dragover');
                }});
                
                dropZone.addEventListener('dragleave', () => {{
                    dropZone.classList.remove('dragover');
                }});
                
                dropZone.addEventListener('drop', (e) => {{
                    e.preventDefault();
                    dropZone.classList.remove('dragover');
                    // Handle drop logic here
                }});
                
                dropZone.addEventListener('click', () => {{
                    addSection('text');
                }});
            }}
            
            function addSection(type) {{
                sectionCounter++;
                const newSection = {{
                    id: `section_${{sectionCounter}}`,
                    type: type,
                    content: getDefaultSectionContent(type)
                }};
                
                templateData.sections.push(newSection);
                renderEmail();
                selectSection(templateData.sections.length - 1);
            }}
            
            function getDefaultSectionContent(type) {{
                switch (type) {{
                    case 'header':
                        return {{
                            title: 'Newsletter Title',
                            subtitle: 'Subtitle text',
                            backgroundColor: '#007bff',
                            textColor: '#ffffff',
                            logo: ''
                        }};
                    case 'text':
                        return {{
                            title: 'Section Title',
                            text: 'Your content goes here...',
                            alignment: 'left'
                        }};
                    case 'button':
                        return {{
                            text: 'Click Here',
                            url: '#',
                            backgroundColor: '#28a745',
                            textColor: '#ffffff',
                            alignment: 'center'
                        }};
                    case 'image':
                        return {{
                            src: 'https://via.placeholder.com/400x200',
                            alt: 'Image',
                            width: '100%',
                            caption: ''
                        }};
                    case 'spacer':
                        return {{ height: 20 }};
                    case 'divider':
                        return {{ color: '#eee' }};
                    case 'footer':
                        return {{
                            text: '© 2024 Company Name. All rights reserved.',
                            unsubscribeText: 'Unsubscribe',
                            unsubscribeUrl: '#',
                            backgroundColor: '#f8f9fa',
                            textColor: '#6c757d'
                        }};
                    default:
                        return {{}};
                }}
            }}
            
            function selectSection(index) {{
                selectedSection = index;
                
                // Update visual selection
                document.querySelectorAll('.email-section').forEach(section => {{
                    section.classList.remove('selected');
                }});
                document.querySelector(`[data-section-index="${{index}}"]`).classList.add('selected');
                
                // Show section properties
                showSectionProperties(templateData.sections[index]);
            }}
            
            function showSectionProperties(section) {{
                const panel = document.getElementById('section-properties');
                const content = document.getElementById('section-properties-content');
                
                panel.style.display = 'block';
                
                let propertiesHTML = '';
                
                switch (section.type) {{
                    case 'header':
                        propertiesHTML = `
                            <div class="property-row">
                                <label>Title:</label>
                                <input type="text" id="header-title" value="${{section.content.title}}" onchange="updateSectionProperty('title', this.value)">
                            </div>
                            <div class="property-row">
                                <label>Subtitle:</label>
                                <input type="text" id="header-subtitle" value="${{section.content.subtitle}}" onchange="updateSectionProperty('subtitle', this.value)">
                            </div>
                            <div class="property-row">
                                <label>Background Color:</label>
                                <input type="color" id="header-bg" value="${{section.content.backgroundColor}}" class="color-input" onchange="updateSectionProperty('backgroundColor', this.value)">
                            </div>
                            <div class="property-row">
                                <label>Text Color:</label>
                                <input type="color" id="header-color" value="${{section.content.textColor}}" class="color-input" onchange="updateSectionProperty('textColor', this.value)">
                            </div>
                            <div class="property-row">
                                <label>Logo URL:</label>
                                <input type="url" id="header-logo" value="${{section.content.logo || ''}}" onchange="updateSectionProperty('logo', this.value)">
                            </div>
                        `;
                        break;
                    case 'text':
                        propertiesHTML = `
                            <div class="property-row">
                                <label>Title:</label>
                                <input type="text" id="text-title" value="${{section.content.title}}" onchange="updateSectionProperty('title', this.value)">
                            </div>
                            <div class="property-row">
                                <label>Content:</label>
                                <textarea id="text-content" onchange="updateSectionProperty('text', this.value)">${{section.content.text}}</textarea>
                            </div>
                            <div class="property-row">
                                <label>Alignment:</label>
                                <select id="text-align" onchange="updateSectionProperty('alignment', this.value)">
                                    <option value="left" ${{section.content.alignment === 'left' ? 'selected' : ''}}>Left</option>
                                    <option value="center" ${{section.content.alignment === 'center' ? 'selected' : ''}}>Center</option>
                                    <option value="right" ${{section.content.alignment === 'right' ? 'selected' : ''}}>Right</option>
                                </select>
                            </div>
                        `;
                        break;
                    case 'button':
                        propertiesHTML = `
                            <div class="property-row">
                                <label>Button Text:</label>
                                <input type="text" id="button-text" value="${{section.content.text}}" onchange="updateSectionProperty('text', this.value)">
                            </div>
                            <div class="property-row">
                                <label>Link URL:</label>
                                <input type="url" id="button-url" value="${{section.content.url}}" onchange="updateSectionProperty('url', this.value)">
                            </div>
                            <div class="property-row">
                                <label>Background Color:</label>
                                <input type="color" id="button-bg" value="${{section.content.backgroundColor}}" class="color-input" onchange="updateSectionProperty('backgroundColor', this.value)">
                            </div>
                            <div class="property-row">
                                <label>Text Color:</label>
                                <input type="color" id="button-color" value="${{section.content.textColor}}" class="color-input" onchange="updateSectionProperty('textColor', this.value)">
                            </div>
                            <div class="property-row">
                                <label>Alignment:</label>
                                <select id="button-align" onchange="updateSectionProperty('alignment', this.value)">
                                    <option value="left" ${{section.content.alignment === 'left' ? 'selected' : ''}}>Left</option>
                                    <option value="center" ${{section.content.alignment === 'center' ? 'selected' : ''}}>Center</option>
                                    <option value="right" ${{section.content.alignment === 'right' ? 'selected' : ''}}>Right</option>
                                </select>
                            </div>
                        `;
                        break;
                }}
                
                content.innerHTML = propertiesHTML;
            }}
            
            function updateSectionProperty(property, value) {{
                if (selectedSection !== null) {{
                    templateData.sections[selectedSection].content[property] = value;
                    renderEmail();
                    selectSection(selectedSection);
                }}
            }}
            
            function deleteSection(index) {{
                if (confirm('Delete this section?')) {{
                    templateData.sections.splice(index, 1);
                    renderEmail();
                    document.getElementById('section-properties').style.display = 'none';
                    selectedSection = null;
                }}
            }}
            
            function updateEmailSettings() {{
                templateData.subject = document.getElementById('email-subject').value;
                templateData.preheader = document.getElementById('email-preheader').value;
                templateData.settings.width = document.getElementById('email-width').value;
                templateData.settings.backgroundColor = document.getElementById('email-bg').value;
                templateData.settings.fontFamily = document.getElementById('email-font').value;
                
                renderEmail();
            }}
            
            function setPreviewMode(mode) {{
                previewMode = mode;
                document.querySelectorAll('.device-btn').forEach(btn => btn.classList.remove('active'));
                document.querySelector(`[onclick="setPreviewMode('${{mode}}')"]`).classList.add('active');
                
                const container = document.getElementById('email-container');
                if (mode === 'mobile') {{
                    container.style.width = '320px';
                }} else {{
                    container.style.width = templateData.settings.width + 'px';
                }}
            }}
            
            function exportEmail(format) {{
                if (format === 'html') {{
                    const htmlContent = generateEmailHTML();
                    const blob = new Blob([htmlContent], {{ type: 'text/html' }});
                    const link = document.createElement('a');
                    link.download = `newsletter-${{new Date().toISOString().slice(0, 19).replace(/:/g, '-')}}.html`;
                    link.href = URL.createObjectURL(blob);
                    link.click();
                }} else if (format === 'json') {{
                    const blob = new Blob([JSON.stringify(templateData, null, 2)], {{ type: 'application/json' }});
                    const link = document.createElement('a');
                    link.download = `newsletter-template-${{new Date().toISOString().slice(0, 19).replace(/:/g, '-')}}.json`;
                    link.href = URL.createObjectURL(blob);
                    link.click();
                }}
            }}
            
            function generateEmailHTML() {{
                let html = `<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${{templateData.subject}}</title>
    <style>
        body {{ margin: 0; padding: 0; font-family: ${{templateData.settings.fontFamily}}; background-color: ${{templateData.settings.backgroundColor}}; }}
        .email-container {{ max-width: ${{templateData.settings.width}}px; margin: 0 auto; background: white; }}
        .email-header {{ padding: 30px 20px; text-align: center; }}
        .email-text {{ padding: 20px; }}
        .email-button {{ padding: 20px; text-align: center; }}
        .email-btn {{ display: inline-block; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: bold; }}
        .email-footer {{ padding: 20px; text-align: center; font-size: 12px; border-top: 1px solid #eee; }}
    </style>
</head>
<body>
    <div class="email-container">`;
                
                templateData.sections.forEach(section => {{
                    switch (section.type) {{
                        case 'header':
                            html += `
                                <div class="email-header" style="background-color: ${{section.content.backgroundColor}}; color: ${{section.content.textColor}};">
                                    ${{section.content.logo ? `<img src="${{section.content.logo}}" alt="Logo" style="max-height: 50px; margin-bottom: 15px;">` : ''}}
                                    <h1 style="margin: 0 0 10px 0; font-size: 24px;">${{section.content.title}}</h1>
                                    <p style="margin: 0; font-size: 16px; opacity: 0.8;">${{section.content.subtitle}}</p>
                                </div>
                            `;
                            break;
                        case 'text':
                            html += `
                                <div class="email-text" style="text-align: ${{section.content.alignment}};">
                                    <h3 style="margin: 0 0 15px 0; font-size: 18px;">${{section.content.title}}</h3>
                                    <p style="margin: 0; line-height: 1.6;">${{section.content.text}}</p>
                                </div>
                            `;
                            break;
                        case 'button':
                            html += `
                                <div class="email-button" style="text-align: ${{section.content.alignment}};">
                                    <a href="${{section.content.url}}" class="email-btn" 
                                       style="background-color: ${{section.content.backgroundColor}}; color: ${{section.content.textColor}};">
                                        ${{section.content.text}}
                                    </a>
                                </div>
                            `;
                            break;
                        case 'footer':
                            html += `
                                <div class="email-footer" style="background-color: ${{section.content.backgroundColor}}; color: ${{section.content.textColor}};">
                                    <p style="margin: 5px 0;">${{section.content.text}}</p>
                                    <p style="margin: 5px 0;"><a href="${{section.content.unsubscribeUrl}}" style="color: ${{section.content.textColor}};">${{section.content.unsubscribeText}}</a></p>
                                </div>
                            `;
                            break;
                    }}
                }});
                
                html += `
    </div>
</body>
</html>`;
                
                return html;
            }}
            
            function previewEmail() {{
                const htmlContent = generateEmailHTML();
                const newWindow = window.open('', '_blank');
                newWindow.document.write(htmlContent);
                newWindow.document.close();
            }}
            
            function testEmail() {{
                alert('Test email functionality would integrate with your email service provider (SendGrid, Mailchimp, etc.)');
            }}
            
            function generatePreview() {{
                previewEmail();
            }}
            
            function editSection(index) {{
                selectSection(index);
            }}
            
            // Initialize the newsletter editor
            initNewsletterEditor();
        </script>
    </body>
    </html>
    """
    
    # Use Streamlit's HTML component
    components.html(component_html, width=width, height=height)
    
    # Return None due to Streamlit version compatibility
    return None
