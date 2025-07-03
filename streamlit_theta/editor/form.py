"""
Theta Form Builder - Visual form designer with validation
Provides a drag-and-drop interface for creating forms.
"""

import streamlit as st
import streamlit.components.v1 as components
import json
from typing import Dict, List, Any, Optional

def theta_form_builder(
    form_config: Optional[Dict[str, Any]] = None,
    width: int = 900,
    height: int = 600,
    key: Optional[str] = None
) -> None:
    """
    Create a visual form builder.
    
    Parameters:
    -----------
    form_config : Dict[str, Any]
        Form configuration with fields and settings
    width : int
        Width of the editor in pixels
    height : int  
        Height of the editor in pixels
    key : str or None
        Unique key for the component
    
    Returns:
    --------
    Dict with form configuration or None
    """
    
    # Default form configuration if none provided
    if form_config is None:
        form_config = {
            "title": "Sample Form",
            "description": "Fill out this form to get started",
            "fields": [
                {
                    "id": "name",
                    "type": "text",
                    "label": "Full Name",
                    "placeholder": "Enter your full name",
                    "required": True,
                    "validation": {"minLength": 2, "maxLength": 50}
                },
                {
                    "id": "email",
                    "type": "email",
                    "label": "Email Address",
                    "placeholder": "Enter your email",
                    "required": True,
                    "validation": {"pattern": "email"}
                }
            ],
            "settings": {
                "submitText": "Submit Form",
                "theme": "light",
                "layout": "vertical"
            }
        }
    
    # Convert form config to JSON for JavaScript
    config_json = json.dumps(form_config).replace('"', '\\"')
    
    component_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Theta Form Builder</title>
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
            
            .form-builder {{
                flex: 1;
                display: flex;
                flex-direction: column;
            }}
            
            .builder-header {{
                padding: 15px 20px;
                background: #f8f9fa;
                border-bottom: 1px solid #dee2e6;
                border-radius: 8px 8px 0 0;
            }}
            
            .builder-content {{
                flex: 1;
                display: flex;
            }}
            
            .form-preview {{
                flex: 1;
                padding: 20px;
                background: #fff;
                overflow-y: auto;
            }}
            
            .field-library {{
                width: 250px;
                background: #f8f9fa;
                border-left: 1px solid #dee2e6;
                padding: 20px;
                overflow-y: auto;
            }}
            
            .properties-panel {{
                width: 300px;
                background: #f8f9fa;
                border-left: 1px solid #dee2e6;
                padding: 20px;
                overflow-y: auto;
            }}
            
            .form-container {{
                max-width: 600px;
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            
            .form-field {{
                margin-bottom: 20px;
                padding: 15px;
                border: 2px dashed transparent;
                border-radius: 6px;
                position: relative;
                transition: all 0.2s;
            }}
            
            .form-field:hover {{
                border-color: #007bff;
                background: #f8f9ff;
            }}
            
            .form-field.selected {{
                border-color: #007bff;
                background: #e3f2fd;
            }}
            
            .field-controls {{
                position: absolute;
                top: -5px;
                right: -5px;
                display: none;
                gap: 5px;
            }}
            
            .form-field:hover .field-controls,
            .form-field.selected .field-controls {{
                display: flex;
            }}
            
            .field-control-btn {{
                width: 20px;
                height: 20px;
                border: none;
                border-radius: 3px;
                cursor: pointer;
                font-size: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            
            .field-control-btn.edit {{ background: #007bff; color: white; }}
            .field-control-btn.delete {{ background: #dc3545; color: white; }}
            .field-control-btn.move {{ background: #6c757d; color: white; cursor: move; }}
            
            .field-library h4 {{
                margin: 0 0 15px 0;
                font-size: 14px;
                color: #495057;
            }}
            
            .field-type {{
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
            
            .field-type:hover {{
                border-color: #007bff;
                background: #f8f9ff;
            }}
            
            .field-type-icon {{
                width: 20px;
                text-align: center;
                margin-right: 10px;
            }}
            
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
            
            .form-field label {{
                display: block;
                margin-bottom: 5px;
                font-weight: 500;
                color: #495057;
            }}
            
            .form-field input, .form-field select, .form-field textarea {{
                width: 100%;
                padding: 10px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                font-size: 14px;
                font-family: inherit;
            }}
            
            .form-field input:focus, .form-field select:focus, .form-field textarea:focus {{
                outline: none;
                border-color: #007bff;
                box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
            }}
            
            .required-indicator {{
                color: #dc3545;
                margin-left: 3px;
            }}
            
            .field-help {{
                font-size: 12px;
                color: #6c757d;
                margin-top: 5px;
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
            
            .submit-btn {{
                background: #28a745;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                cursor: pointer;
                font-size: 16px;
                margin-top: 20px;
            }}
            
            .submit-btn:hover {{
                background: #218838;
            }}
            
            .drop-zone {{
                min-height: 100px;
                border: 2px dashed #dee2e6;
                border-radius: 6px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #6c757d;
                font-style: italic;
                margin: 20px 0;
            }}
            
            .drop-zone.dragover {{
                border-color: #007bff;
                background: #f8f9ff;
                color: #007bff;
            }}
            
            .checkbox-group, .radio-group {{
                display: flex;
                flex-direction: column;
                gap: 8px;
            }}
            
            .checkbox-option, .radio-option {{
                display: flex;
                align-items: center;
                gap: 8px;
            }}
            
            .form-title {{
                margin: 0 0 10px 0;
                font-size: 24px;
                font-weight: 600;
                color: #212529;
            }}
            
            .form-description {{
                margin: 0 0 30px 0;
                color: #6c757d;
                line-height: 1.5;
            }}
        </style>
    </head>
    <body>
        <div class="editor-container">
            <div class="form-builder">
                <div class="builder-header">
                    <h3 style="margin: 0;">📋 Form Builder</h3>
                    <p style="margin: 5px 0 0 0; color: #6c757d;">Drag fields from the library to build your form</p>
                </div>
                
                <div class="builder-content">
                    <div class="form-preview">
                        <div class="form-container" id="form-container">
                            <h1 class="form-title" id="form-title">Sample Form</h1>
                            <p class="form-description" id="form-description">Fill out this form to get started</p>
                            
                            <div id="form-fields">
                                <!-- Form fields will be rendered here -->
                            </div>
                            
                            <div class="drop-zone" id="drop-zone">
                                Drop form fields here or click to add
                            </div>
                            
                            <button class="submit-btn" id="submit-btn">Submit Form</button>
                        </div>
                    </div>
                    
                    <div class="field-library">
                        <h4>📚 Field Library</h4>
                        
                        <div class="field-type" draggable="true" data-type="text">
                            <span class="field-type-icon">📝</span>
                            <span>Text Input</span>
                        </div>
                        
                        <div class="field-type" draggable="true" data-type="email">
                            <span class="field-type-icon">📧</span>
                            <span>Email</span>
                        </div>
                        
                        <div class="field-type" draggable="true" data-type="password">
                            <span class="field-type-icon">🔒</span>
                            <span>Password</span>
                        </div>
                        
                        <div class="field-type" draggable="true" data-type="number">
                            <span class="field-type-icon">🔢</span>
                            <span>Number</span>
                        </div>
                        
                        <div class="field-type" draggable="true" data-type="tel">
                            <span class="field-type-icon">📱</span>
                            <span>Phone</span>
                        </div>
                        
                        <div class="field-type" draggable="true" data-type="textarea">
                            <span class="field-type-icon">📄</span>
                            <span>Textarea</span>
                        </div>
                        
                        <div class="field-type" draggable="true" data-type="select">
                            <span class="field-type-icon">📋</span>
                            <span>Dropdown</span>
                        </div>
                        
                        <div class="field-type" draggable="true" data-type="radio">
                            <span class="field-type-icon">🔘</span>
                            <span>Radio Buttons</span>
                        </div>
                        
                        <div class="field-type" draggable="true" data-type="checkbox">
                            <span class="field-type-icon">☑️</span>
                            <span>Checkboxes</span>
                        </div>
                        
                        <div class="field-type" draggable="true" data-type="date">
                            <span class="field-type-icon">📅</span>
                            <span>Date</span>
                        </div>
                        
                        <div class="field-type" draggable="true" data-type="time">
                            <span class="field-type-icon">🕐</span>
                            <span>Time</span>
                        </div>
                        
                        <div class="field-type" draggable="true" data-type="file">
                            <span class="field-type-icon">📎</span>
                            <span>File Upload</span>
                        </div>
                    </div>
                    
                    <div class="properties-panel">
                        <div class="property-group">
                            <h4>🎨 Form Settings</h4>
                            <div class="property-row">
                                <label>Form Title:</label>
                                <input type="text" id="form-title-input" value="Sample Form" onchange="updateFormSettings()">
                            </div>
                            <div class="property-row">
                                <label>Description:</label>
                                <textarea id="form-description-input" onchange="updateFormSettings()">Fill out this form to get started</textarea>
                            </div>
                            <div class="property-row">
                                <label>Submit Button Text:</label>
                                <input type="text" id="submit-text-input" value="Submit Form" onchange="updateFormSettings()">
                            </div>
                            <div class="property-row">
                                <label>Theme:</label>
                                <select id="theme-select" onchange="updateFormSettings()">
                                    <option value="light">Light</option>
                                    <option value="dark">Dark</option>
                                    <option value="blue">Blue</option>
                                </select>
                            </div>
                        </div>
                        
                        <div class="property-group" id="field-properties" style="display: none;">
                            <h4>🔧 Field Properties</h4>
                            <div id="field-properties-content">
                                <!-- Field-specific properties will be shown here -->
                            </div>
                        </div>
                        
                        <div class="property-group">
                            <h4>💾 Export</h4>
                            <button onclick="exportForm('json')" class="btn">📄 Export JSON</button>
                            <button onclick="exportForm('html')" class="btn">🌐 Export HTML</button>
                            <button onclick="previewForm()" class="btn secondary">👁️ Preview Form</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            let formConfig = {config_json};
            let selectedField = null;
            let fieldCounter = 0;
            
            function initFormBuilder() {{
                renderForm();
                setupDragAndDrop();
                updateFormSettings();
            }}
            
            function renderForm() {{
                const fieldsContainer = document.getElementById('form-fields');
                fieldsContainer.innerHTML = '';
                
                formConfig.fields.forEach((field, index) => {{
                    const fieldElement = createFieldElement(field, index);
                    fieldsContainer.appendChild(fieldElement);
                }});
            }}
            
            function createFieldElement(field, index) {{
                const wrapper = document.createElement('div');
                wrapper.className = 'form-field';
                wrapper.setAttribute('data-field-index', index);
                wrapper.onclick = () => selectField(index);
                
                const controls = document.createElement('div');
                controls.className = 'field-controls';
                controls.innerHTML = `
                    <button class="field-control-btn edit" onclick="editField(${{index}})" title="Edit">✏️</button>
                    <button class="field-control-btn move" title="Move">↕️</button>
                    <button class="field-control-btn delete" onclick="deleteField(${{index}})" title="Delete">🗑️</button>
                `;
                
                let fieldHTML = '';
                const required = field.required ? '<span class="required-indicator">*</span>' : '';
                
                switch (field.type) {{
                    case 'text':
                    case 'email':
                    case 'password':
                    case 'number':
                    case 'tel':
                    case 'date':
                    case 'time':
                        fieldHTML = `
                            <label>${{field.label}}${{required}}</label>
                            <input type="${{field.type}}" placeholder="${{field.placeholder || ''}}" ${{field.required ? 'required' : ''}}>
                        `;
                        break;
                    case 'textarea':
                        fieldHTML = `
                            <label>${{field.label}}${{required}}</label>
                            <textarea placeholder="${{field.placeholder || ''}}" ${{field.required ? 'required' : ''}} rows="4"></textarea>
                        `;
                        break;
                    case 'select':
                        const options = field.options || ['Option 1', 'Option 2', 'Option 3'];
                        fieldHTML = `
                            <label>${{field.label}}${{required}}</label>
                            <select ${{field.required ? 'required' : ''}}>
                                <option value="">Choose an option</option>
                                ${{options.map(opt => `<option value="${{opt}}">${{opt}}</option>`).join('')}}
                            </select>
                        `;
                        break;
                    case 'radio':
                        const radioOptions = field.options || ['Option 1', 'Option 2'];
                        fieldHTML = `
                            <label>${{field.label}}${{required}}</label>
                            <div class="radio-group">
                                ${{radioOptions.map((opt, i) => `
                                    <div class="radio-option">
                                        <input type="radio" name="${{field.id}}" value="${{opt}}" id="${{field.id}}_${{i}}">
                                        <label for="${{field.id}}_${{i}}">${{opt}}</label>
                                    </div>
                                `).join('')}}
                            </div>
                        `;
                        break;
                    case 'checkbox':
                        const checkboxOptions = field.options || ['Option 1', 'Option 2'];
                        fieldHTML = `
                            <label>${{field.label}}${{required}}</label>
                            <div class="checkbox-group">
                                ${{checkboxOptions.map((opt, i) => `
                                    <div class="checkbox-option">
                                        <input type="checkbox" name="${{field.id}}" value="${{opt}}" id="${{field.id}}_${{i}}">
                                        <label for="${{field.id}}_${{i}}">${{opt}}</label>
                                    </div>
                                `).join('')}}
                            </div>
                        `;
                        break;
                    case 'file':
                        fieldHTML = `
                            <label>${{field.label}}${{required}}</label>
                            <input type="file" ${{field.required ? 'required' : ''}}>
                        `;
                        break;
                }}
                
                if (field.helpText) {{
                    fieldHTML += `<div class="field-help">${{field.helpText}}</div>`;
                }}
                
                wrapper.innerHTML = fieldHTML;
                wrapper.appendChild(controls);
                
                return wrapper;
            }}
            
            function setupDragAndDrop() {{
                const fieldTypes = document.querySelectorAll('.field-type');
                const dropZone = document.getElementById('drop-zone');
                
                fieldTypes.forEach(fieldType => {{
                    fieldType.addEventListener('dragstart', (e) => {{
                        e.dataTransfer.setData('text/plain', fieldType.dataset.type);
                    }});
                }});
                
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
                    const fieldType = e.dataTransfer.getData('text/plain');
                    addField(fieldType);
                }});
                
                dropZone.addEventListener('click', () => {{
                    // Show field type selector
                    addField('text');
                }});
            }}
            
            function addField(type) {{
                fieldCounter++;
                const newField = {{
                    id: `field_${{fieldCounter}}`,
                    type: type,
                    label: `New ${{type.charAt(0).toUpperCase() + type.slice(1)}} Field`,
                    placeholder: '',
                    required: false,
                    validation: {{}},
                    helpText: ''
                }};
                
                if (type === 'select' || type === 'radio' || type === 'checkbox') {{
                    newField.options = ['Option 1', 'Option 2', 'Option 3'];
                }}
                
                formConfig.fields.push(newField);
                renderForm();
                selectField(formConfig.fields.length - 1);
            }}
            
            function selectField(index) {{
                selectedField = index;
                document.querySelectorAll('.form-field').forEach(field => {{
                    field.classList.remove('selected');
                }});
                document.querySelector(`[data-field-index="${{index}}"]`).classList.add('selected');
                showFieldProperties(formConfig.fields[index]);
            }}
            
            function showFieldProperties(field) {{
                const panel = document.getElementById('field-properties');
                const content = document.getElementById('field-properties-content');
                
                panel.style.display = 'block';
                
                let propertiesHTML = `
                    <div class="property-row">
                        <label>Label:</label>
                        <input type="text" id="field-label" value="${{field.label}}" onchange="updateFieldProperty('label', this.value)">
                    </div>
                    <div class="property-row">
                        <label>Placeholder:</label>
                        <input type="text" id="field-placeholder" value="${{field.placeholder || ''}}" onchange="updateFieldProperty('placeholder', this.value)">
                    </div>
                    <div class="property-row">
                        <label>
                            <input type="checkbox" id="field-required" ${{field.required ? 'checked' : ''}} onchange="updateFieldProperty('required', this.checked)">
                            Required Field
                        </label>
                    </div>
                    <div class="property-row">
                        <label>Help Text:</label>
                        <textarea id="field-help" onchange="updateFieldProperty('helpText', this.value)">${{field.helpText || ''}}</textarea>
                    </div>
                `;
                
                if (field.type === 'select' || field.type === 'radio' || field.type === 'checkbox') {{
                    const options = field.options || [];
                    propertiesHTML += `
                        <div class="property-row">
                            <label>Options (one per line):</label>
                            <textarea id="field-options" onchange="updateFieldOptions(this.value)">${{options.join('\\n')}}</textarea>
                        </div>
                    `;
                }}
                
                content.innerHTML = propertiesHTML;
            }}
            
            function updateFieldProperty(property, value) {{
                if (selectedField !== null) {{
                    formConfig.fields[selectedField][property] = value;
                    renderForm();
                    selectField(selectedField);
                }}
            }}
            
            function updateFieldOptions(value) {{
                if (selectedField !== null) {{
                    formConfig.fields[selectedField].options = value.split('\\n').filter(opt => opt.trim());
                    renderForm();
                    selectField(selectedField);
                }}
            }}
            
            function deleteField(index) {{
                if (confirm('Delete this field?')) {{
                    formConfig.fields.splice(index, 1);
                    renderForm();
                    document.getElementById('field-properties').style.display = 'none';
                    selectedField = null;
                }}
            }}
            
            function updateFormSettings() {{
                const title = document.getElementById('form-title-input').value;
                const description = document.getElementById('form-description-input').value;
                const submitText = document.getElementById('submit-text-input').value;
                const theme = document.getElementById('theme-select').value;
                
                document.getElementById('form-title').textContent = title;
                document.getElementById('form-description').textContent = description;
                document.getElementById('submit-btn').textContent = submitText;
                
                formConfig.title = title;
                formConfig.description = description;
                formConfig.settings = formConfig.settings || {{}};
                formConfig.settings.submitText = submitText;
                formConfig.settings.theme = theme;
            }}
            
            function exportForm(format) {{
                if (format === 'json') {{
                    const blob = new Blob([JSON.stringify(formConfig, null, 2)], {{ type: 'application/json' }});
                    const link = document.createElement('a');
                    link.download = `form-config-${{new Date().toISOString().slice(0, 19).replace(/:/g, '-')}}.json`;
                    link.href = URL.createObjectURL(blob);
                    link.click();
                }} else if (format === 'html') {{
                    const formHTML = generateFormHTML();
                    const blob = new Blob([formHTML], {{ type: 'text/html' }});
                    const link = document.createElement('a');
                    link.download = `form-${{new Date().toISOString().slice(0, 19).replace(/:/g, '-')}}.html`;
                    link.href = URL.createObjectURL(blob);
                    link.click();
                }}
            }}
            
            function generateFormHTML() {{
                let html = `<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>${{formConfig.title}}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 40px; }}
        .form-container {{ max-width: 600px; margin: 0 auto; }}
        .form-field {{ margin-bottom: 20px; }}
        label {{ display: block; margin-bottom: 5px; font-weight: 500; }}
        input, select, textarea {{ width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; }}
        .submit-btn {{ background: #007bff; color: white; padding: 12px 24px; border: none; border-radius: 4px; cursor: pointer; }}
        .required {{ color: red; }}
    </style>
</head>
<body>
    <div class="form-container">
        <h1>${{formConfig.title}}</h1>
        <p>${{formConfig.description}}</p>
        <form>`;
                
                formConfig.fields.forEach(field => {{
                    html += generateFieldHTML(field);
                }});
                
                html += `
            <button type="submit" class="submit-btn">${{formConfig.settings?.submitText || 'Submit'}}</button>
        </form>
    </div>
</body>
</html>`;
                
                return html;
            }}
            
            function generateFieldHTML(field) {{
                const required = field.required ? '<span class="required">*</span>' : '';
                let html = `<div class="form-field">`;
                
                switch (field.type) {{
                    case 'text':
                    case 'email':
                    case 'password':
                    case 'number':
                    case 'tel':
                    case 'date':
                    case 'time':
                        html += `
                            <label>${{field.label}}${{required}}</label>
                            <input type="${{field.type}}" name="${{field.id}}" placeholder="${{field.placeholder || ''}}" ${{field.required ? 'required' : ''}}>
                        `;
                        break;
                    case 'textarea':
                        html += `
                            <label>${{field.label}}${{required}}</label>
                            <textarea name="${{field.id}}" placeholder="${{field.placeholder || ''}}" ${{field.required ? 'required' : ''}} rows="4"></textarea>
                        `;
                        break;
                    case 'select':
                        const options = field.options || [];
                        html += `
                            <label>${{field.label}}${{required}}</label>
                            <select name="${{field.id}}" ${{field.required ? 'required' : ''}}>
                                <option value="">Choose an option</option>
                                ${{options.map(opt => `<option value="${{opt}}">${{opt}}</option>`).join('')}}
                            </select>
                        `;
                        break;
                }}
                
                if (field.helpText) {{
                    html += `<small style="color: #666;">${{field.helpText}}</small>`;
                }}
                
                html += `</div>`;
                return html;
            }}
            
            function previewForm() {{
                const formHTML = generateFormHTML();
                const newWindow = window.open('', '_blank');
                newWindow.document.write(formHTML);
                newWindow.document.close();
            }}
            
            // Initialize the form builder
            initFormBuilder();
        </script>
    </body>
    </html>
    """
    
    # Use Streamlit's HTML component
    components.html(component_html, width=width, height=height)
    
    # Return None due to Streamlit version compatibility
    return None
