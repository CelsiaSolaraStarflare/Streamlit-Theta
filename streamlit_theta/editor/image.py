"""
Theta Image Editor - Basic image editing with filters, crop, and resize
Provides a visual interface for editing images.
"""

import streamlit as st
import streamlit.components.v1 as components
import base64
from typing import Optional, Dict, Any

def theta_image_editor(
    image_file: Optional[str] = None,
    width: int = 900,
    height: int = 600,
    key: Optional[str] = None
) -> None:
    """
    Create an image editor with basic editing features.
    
    Parameters:
    -----------
    image_file : str or None
        Path to image file or base64 encoded image
    width : int
        Width of the editor in pixels
    height : int  
        Height of the editor in pixels
    key : str or None
        Unique key for the component
    
    Returns:
    --------
    Dict with image data and edits or None
    """
    
    component_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Theta Image Editor</title>
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
            
            .image-panel {{
                flex: 1;
                padding: 20px;
                display: flex;
                flex-direction: column;
                background: #f8f9fa;
            }}
            
            .controls-panel {{
                width: 300px;
                background: white;
                border-left: 1px solid #dee2e6;
                padding: 20px;
                overflow-y: auto;
            }}
            
            .image-container {{
                flex: 1;
                display: flex;
                align-items: center;
                justify-content: center;
                background: #fff;
                border: 2px dashed #dee2e6;
                border-radius: 8px;
                position: relative;
                overflow: hidden;
            }}
            
            .image-canvas {{
                max-width: 100%;
                max-height: 100%;
                border-radius: 4px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }}
            
            .upload-area {{
                text-align: center;
                color: #6c757d;
                cursor: pointer;
                padding: 40px;
            }}
            
            .upload-area:hover {{
                background: #f8f9fa;
                border-color: #007bff;
                color: #007bff;
            }}
            
            .toolbar {{
                display: flex;
                gap: 10px;
                margin-bottom: 15px;
                padding: 10px;
                background: white;
                border-radius: 6px;
                border: 1px solid #dee2e6;
            }}
            
            .toolbar button {{
                padding: 8px 12px;
                border: 1px solid #dee2e6;
                background: white;
                border-radius: 4px;
                cursor: pointer;
                font-size: 12px;
                transition: all 0.2s;
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
            
            .control-group {{
                margin-bottom: 20px;
                padding: 15px;
                background: #f8f9fa;
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
                align-items: center;
                margin-bottom: 10px;
                gap: 10px;
            }}
            
            .control-row label {{
                min-width: 80px;
                font-size: 12px;
                color: #6c757d;
            }}
            
            .control-row input[type="range"] {{
                flex: 1;
                height: 4px;
                background: #dee2e6;
                border-radius: 2px;
                outline: none;
                -webkit-appearance: none;
            }}
            
            .control-row input[type="range"]::-webkit-slider-thumb {{
                -webkit-appearance: none;
                appearance: none;
                width: 16px;
                height: 16px;
                background: #007bff;
                border-radius: 50%;
                cursor: pointer;
            }}
            
            .control-row span {{
                min-width: 40px;
                font-size: 11px;
                text-align: right;
                color: #6c757d;
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
            
            .hidden {{
                display: none;
            }}
            
            .crop-overlay {{
                position: absolute;
                border: 2px dashed #007bff;
                background: rgba(0, 123, 255, 0.1);
                cursor: move;
                display: none;
            }}
            
            .resize-handle {{
                position: absolute;
                width: 8px;
                height: 8px;
                background: #007bff;
                border: 1px solid white;
                cursor: nw-resize;
            }}
            
            .resize-handle.top-left {{ top: -4px; left: -4px; }}
            .resize-handle.top-right {{ top: -4px; right: -4px; cursor: ne-resize; }}
            .resize-handle.bottom-left {{ bottom: -4px; left: -4px; cursor: sw-resize; }}
            .resize-handle.bottom-right {{ bottom: -4px; right: -4px; cursor: se-resize; }}
        </style>
    </head>
    <body>
        <div class="editor-container">
            <div class="image-panel">
                <div class="toolbar">
                    <button onclick="resetImage()" title="Reset">🔄 Reset</button>
                    <button onclick="undoLast()" title="Undo">↶ Undo</button>
                    <button onclick="toggleCropMode()" id="crop-btn" title="Crop">✂️ Crop</button>
                    <button onclick="rotateImage(90)" title="Rotate Right">↻ Rotate</button>
                    <button onclick="flipImage('horizontal')" title="Flip Horizontal">↔️ Flip H</button>
                    <button onclick="flipImage('vertical')" title="Flip Vertical">↕️ Flip V</button>
                </div>
                
                <div class="image-container" id="image-container">
                    <div class="upload-area" id="upload-area" onclick="document.getElementById('file-input').click()">
                        <h3>📸 Click to Upload Image</h3>
                        <p>Supports: JPG, PNG, GIF, WebP</p>
                        <p>Max size: 10MB</p>
                    </div>
                    <canvas id="image-canvas" class="image-canvas hidden"></canvas>
                    <div class="crop-overlay" id="crop-overlay">
                        <div class="resize-handle top-left"></div>
                        <div class="resize-handle top-right"></div>
                        <div class="resize-handle bottom-left"></div>
                        <div class="resize-handle bottom-right"></div>
                    </div>
                    <input type="file" id="file-input" class="hidden" accept="image/*">
                </div>
            </div>
            
            <div class="controls-panel">
                <div class="control-group">
                    <h4>🎨 Filters</h4>
                    <div class="control-row">
                        <label>Brightness:</label>
                        <input type="range" id="brightness" min="0" max="200" value="100" onchange="applyFilters()">
                        <span id="brightness-val">100%</span>
                    </div>
                    <div class="control-row">
                        <label>Contrast:</label>
                        <input type="range" id="contrast" min="0" max="200" value="100" onchange="applyFilters()">
                        <span id="contrast-val">100%</span>
                    </div>
                    <div class="control-row">
                        <label>Saturation:</label>
                        <input type="range" id="saturation" min="0" max="200" value="100" onchange="applyFilters()">
                        <span id="saturation-val">100%</span>
                    </div>
                    <div class="control-row">
                        <label>Hue:</label>
                        <input type="range" id="hue" min="0" max="360" value="0" onchange="applyFilters()">
                        <span id="hue-val">0°</span>
                    </div>
                    <div class="control-row">
                        <label>Blur:</label>
                        <input type="range" id="blur" min="0" max="10" value="0" onchange="applyFilters()">
                        <span id="blur-val">0px</span>
                    </div>
                </div>
                
                <div class="control-group">
                    <h4>🎭 Effects</h4>
                    <button onclick="applyEffect('grayscale')" class="btn">⚫ Grayscale</button>
                    <button onclick="applyEffect('sepia')" class="btn">🟤 Sepia</button>
                    <button onclick="applyEffect('invert')" class="btn">🔄 Invert</button>
                    <button onclick="applyEffect('vintage')" class="btn">📷 Vintage</button>
                    <button onclick="resetFilters()" class="btn danger">🔄 Reset Filters</button>
                </div>
                
                <div class="control-group">
                    <h4>📏 Resize</h4>
                    <div class="control-row">
                        <label>Width:</label>
                        <input type="number" id="resize-width" value="800" min="1" max="2000">
                        <span>px</span>
                    </div>
                    <div class="control-row">
                        <label>Height:</label>
                        <input type="number" id="resize-height" value="600" min="1" max="2000">
                        <span>px</span>
                    </div>
                    <div class="control-row">
                        <label>
                            <input type="checkbox" id="maintain-aspect" checked> Maintain Aspect
                        </label>
                    </div>
                    <button onclick="resizeImage()" class="btn">📏 Apply Resize</button>
                </div>
                
                <div class="control-group">
                    <h4>💾 Export</h4>
                    <div class="control-row">
                        <label>Format:</label>
                        <select id="export-format">
                            <option value="png">PNG</option>
                            <option value="jpeg">JPEG</option>
                            <option value="webp">WebP</option>
                        </select>
                    </div>
                    <div class="control-row">
                        <label>Quality:</label>
                        <input type="range" id="export-quality" min="10" max="100" value="90">
                        <span id="quality-val">90%</span>
                    </div>
                    <button onclick="exportImage()" class="btn">💾 Download Image</button>
                </div>
                
                <div class="control-group">
                    <h4>ℹ️ Info</h4>
                    <div id="image-info">
                        <p>No image loaded</p>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            let canvas = document.getElementById('image-canvas');
            let ctx = canvas.getContext('2d');
            let originalImage = null;
            let currentImage = null;
            let imageHistory = [];
            let cropMode = false;
            let currentFilters = {{
                brightness: 100,
                contrast: 100,
                saturation: 100,
                hue: 0,
                blur: 0
            }};
            
            // File input handler
            document.getElementById('file-input').addEventListener('change', function(e) {{
                const file = e.target.files[0];
                if (file && file.type.startsWith('image/')) {{
                    const reader = new FileReader();
                    reader.onload = function(event) {{
                        loadImage(event.target.result);
                    }};
                    reader.readAsDataURL(file);
                }}
            }});
            
            function loadImage(src) {{
                const img = new Image();
                img.onload = function() {{
                    originalImage = img;
                    currentImage = img;
                    canvas.width = img.width;
                    canvas.height = img.height;
                    
                    document.getElementById('upload-area').classList.add('hidden');
                    canvas.classList.remove('hidden');
                    
                    drawImage();
                    updateImageInfo();
                    saveToHistory();
                    
                    // Update resize inputs
                    document.getElementById('resize-width').value = img.width;
                    document.getElementById('resize-height').value = img.height;
                }};
                img.src = src;
            }}
            
            function drawImage() {{
                if (!currentImage) return;
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.filter = buildFilterString();
                ctx.drawImage(currentImage, 0, 0, canvas.width, canvas.height);
                ctx.filter = 'none';
            }}
            
            function buildFilterString() {{
                return `brightness(${{currentFilters.brightness}}%) ` +
                       `contrast(${{currentFilters.contrast}}%) ` +
                       `saturate(${{currentFilters.saturation}}%) ` +
                       `hue-rotate(${{currentFilters.hue}}deg) ` +
                       `blur(${{currentFilters.blur}}px)`;
            }}
            
            function applyFilters() {{
                currentFilters.brightness = document.getElementById('brightness').value;
                currentFilters.contrast = document.getElementById('contrast').value;
                currentFilters.saturation = document.getElementById('saturation').value;
                currentFilters.hue = document.getElementById('hue').value;
                currentFilters.blur = document.getElementById('blur').value;
                
                document.getElementById('brightness-val').textContent = currentFilters.brightness + '%';
                document.getElementById('contrast-val').textContent = currentFilters.contrast + '%';
                document.getElementById('saturation-val').textContent = currentFilters.saturation + '%';
                document.getElementById('hue-val').textContent = currentFilters.hue + '°';
                document.getElementById('blur-val').textContent = currentFilters.blur + 'px';
                
                drawImage();
            }}
            
            function applyEffect(effect) {{
                switch(effect) {{
                    case 'grayscale':
                        currentFilters.saturation = 0;
                        document.getElementById('saturation').value = 0;
                        break;
                    case 'sepia':
                        currentFilters.hue = 35;
                        currentFilters.saturation = 70;
                        currentFilters.brightness = 110;
                        document.getElementById('hue').value = 35;
                        document.getElementById('saturation').value = 70;
                        document.getElementById('brightness').value = 110;
                        break;
                    case 'invert':
                        currentFilters.hue = 180;
                        document.getElementById('hue').value = 180;
                        break;
                    case 'vintage':
                        currentFilters.contrast = 120;
                        currentFilters.saturation = 80;
                        currentFilters.brightness = 110;
                        document.getElementById('contrast').value = 120;
                        document.getElementById('saturation').value = 80;
                        document.getElementById('brightness').value = 110;
                        break;
                }}
                applyFilters();
            }}
            
            function resetFilters() {{
                currentFilters = {{ brightness: 100, contrast: 100, saturation: 100, hue: 0, blur: 0 }};
                document.getElementById('brightness').value = 100;
                document.getElementById('contrast').value = 100;
                document.getElementById('saturation').value = 100;
                document.getElementById('hue').value = 0;
                document.getElementById('blur').value = 0;
                applyFilters();
            }}
            
            function rotateImage(angle) {{
                if (!currentImage) return;
                
                const tempCanvas = document.createElement('canvas');
                const tempCtx = tempCanvas.getContext('2d');
                
                if (angle === 90 || angle === 270) {{
                    tempCanvas.width = canvas.height;
                    tempCanvas.height = canvas.width;
                }} else {{
                    tempCanvas.width = canvas.width;
                    tempCanvas.height = canvas.height;
                }}
                
                tempCtx.translate(tempCanvas.width / 2, tempCanvas.height / 2);
                tempCtx.rotate((angle * Math.PI) / 180);
                tempCtx.drawImage(canvas, -canvas.width / 2, -canvas.height / 2);
                
                canvas.width = tempCanvas.width;
                canvas.height = tempCanvas.height;
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.drawImage(tempCanvas, 0, 0);
                
                updateImageInfo();
                saveToHistory();
            }}
            
            function flipImage(direction) {{
                if (!currentImage) return;
                
                const tempCanvas = document.createElement('canvas');
                const tempCtx = tempCanvas.getContext('2d');
                tempCanvas.width = canvas.width;
                tempCanvas.height = canvas.height;
                
                if (direction === 'horizontal') {{
                    tempCtx.scale(-1, 1);
                    tempCtx.drawImage(canvas, -canvas.width, 0);
                }} else {{
                    tempCtx.scale(1, -1);
                    tempCtx.drawImage(canvas, 0, -canvas.height);
                }}
                
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.drawImage(tempCanvas, 0, 0);
                
                saveToHistory();
            }}
            
            function resizeImage() {{
                if (!currentImage) return;
                
                const newWidth = parseInt(document.getElementById('resize-width').value);
                const newHeight = parseInt(document.getElementById('resize-height').value);
                
                canvas.width = newWidth;
                canvas.height = newHeight;
                
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.filter = buildFilterString();
                ctx.drawImage(currentImage, 0, 0, newWidth, newHeight);
                ctx.filter = 'none';
                
                updateImageInfo();
                saveToHistory();
            }}
            
            function saveToHistory() {{
                const imageData = canvas.toDataURL();
                imageHistory.push(imageData);
                if (imageHistory.length > 10) {{
                    imageHistory.shift();
                }}
            }}
            
            function undoLast() {{
                if (imageHistory.length > 1) {{
                    imageHistory.pop();
                    const previousState = imageHistory[imageHistory.length - 1];
                    const img = new Image();
                    img.onload = function() {{
                        canvas.width = img.width;
                        canvas.height = img.height;
                        ctx.clearRect(0, 0, canvas.width, canvas.height);
                        ctx.drawImage(img, 0, 0);
                        updateImageInfo();
                    }};
                    img.src = previousState;
                }}
            }}
            
            function resetImage() {{
                if (originalImage) {{
                    canvas.width = originalImage.width;
                    canvas.height = originalImage.height;
                    currentImage = originalImage;
                    resetFilters();
                    drawImage();
                    updateImageInfo();
                    saveToHistory();
                }}
            }}
            
            function updateImageInfo() {{
                const info = document.getElementById('image-info');
                if (currentImage) {{
                    const size = (canvas.toDataURL().length * 0.75 / 1024).toFixed(1);
                    info.innerHTML = `
                        <p><strong>Dimensions:</strong> ${{canvas.width}} × ${{canvas.height}}</p>
                        <p><strong>Size:</strong> ~${{size}} KB</p>
                        <p><strong>Format:</strong> Canvas</p>
                    `;
                }}
            }}
            
            function toggleCropMode() {{
                cropMode = !cropMode;
                const btn = document.getElementById('crop-btn');
                if (cropMode) {{
                    btn.classList.add('active');
                    btn.textContent = '✂️ Apply Crop';
                }} else {{
                    btn.classList.remove('active');
                    btn.textContent = '✂️ Crop';
                }}
            }}
            
            function exportImage() {{
                if (!canvas.width || !canvas.height) return;
                
                const format = document.getElementById('export-format').value;
                const quality = document.getElementById('export-quality').value / 100;
                
                let mimeType = 'image/png';
                if (format === 'jpeg') mimeType = 'image/jpeg';
                if (format === 'webp') mimeType = 'image/webp';
                
                const link = document.createElement('a');
                link.download = `edited-image-${{new Date().toISOString().slice(0, 19).replace(/:/g, '-')}}.${{format}}`;
                
                if (format === 'png') {{
                    link.href = canvas.toDataURL(mimeType);
                }} else {{
                    link.href = canvas.toDataURL(mimeType, quality);
                }}
                
                link.click();
            }}
            
            // Quality slider update
            document.getElementById('export-quality').addEventListener('input', function() {{
                document.getElementById('quality-val').textContent = this.value + '%';
            }});
            
            // Maintain aspect ratio for resize
            document.getElementById('resize-width').addEventListener('input', function() {{
                if (document.getElementById('maintain-aspect').checked && originalImage) {{
                    const ratio = originalImage.height / originalImage.width;
                    document.getElementById('resize-height').value = Math.round(this.value * ratio);
                }}
            }});
            
            document.getElementById('resize-height').addEventListener('input', function() {{
                if (document.getElementById('maintain-aspect').checked && originalImage) {{
                    const ratio = originalImage.width / originalImage.height;
                    document.getElementById('resize-width').value = Math.round(this.value * ratio);
                }}
            }});
        </script>
    </body>
    </html>
    """
    
    # Use Streamlit's HTML component
    components.html(component_html, width=width, height=height)
    
    # Return None due to Streamlit version compatibility
    return None
