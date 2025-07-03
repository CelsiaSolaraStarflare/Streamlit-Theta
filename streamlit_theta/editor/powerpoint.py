"""
PowerPoint Editor - Streamlit Component
A comprehensive PowerPoint-style editor for creating, editing, and exporting presentations.
"""

import streamlit as st
import streamlit.components.v1 as components
import json
from typing import List, Dict, Any, Optional

def powerpoint_editor(
    slides: Optional[List[Dict[str, Any]]] = None,
    width: int = 1000,
    height: int = 700,
    key: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    PowerPoint-style editor for Streamlit.
    Supports text, images, shapes, backgrounds, slide management, and export.
    """
    if slides is None:
        slides = [
            {
                "id": "slide_1",
                "title": "Title Slide",
                "elements": [
                    {
                        "type": "text",
                        "id": "text_1",
                        "content": "Double-click to edit title",
                        "x": 100,
                        "y": 100,
                        "width": 600,
                        "height": 80,
                        "fontSize": 36,
                        "fontFamily": "Arial",
                        "color": "#222222",
                        "bold": True,
                        "italic": False,
                        "underline": False
                    }
                ],
                "background": "#f8fafc"
            }
        ]

    # Responsive: fit editor to parent container, not fixed px
    editor_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset='utf-8'>
        <title>PowerPoint Editor</title>
        <style>
            html, body {{ height: 100%; margin: 0; padding: 0; }}
            body {{ background: #f0f0f0; width: 100vw; height: 100vh; }}
            .ppt-editor {{ width: 100%; height: 100vh; max-width: 100vw; max-height: 100vh; background: #fff; border-radius: 10px; box-shadow: 0 2px 16px #0002; margin: 0 auto; display: flex; flex-direction: column; }}
            .ppt-toolbar {{ height: 56px; background: #2d3748; color: #fff; display: flex; align-items: center; padding: 0 20px; gap: 10px; border-radius: 10px 10px 0 0; }}
            .ppt-toolbar button {{ background: #4a5568; color: #fff; border: none; border-radius: 4px; padding: 8px 14px; cursor: pointer; font-size: 14px; }}
            .ppt-toolbar button:hover {{ background: #3182ce; }}
            .ppt-main {{ flex: 1; display: flex; min-height: 0; }}
            .ppt-slides {{ width: 160px; background: #e2e8f0; border-right: 1px solid #cbd5e0; overflow-y: auto; padding: 10px; }}
            .ppt-slide-thumb {{ width: 130px; height: 90px; background: #fff; border: 2px solid #cbd5e0; border-radius: 4px; margin-bottom: 10px; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 12px; color: #666; }}
            .ppt-slide-thumb.active {{ border-color: #3182ce; }}
            .ppt-canvas-wrap {{ flex: 1; display: flex; align-items: center; justify-content: center; background: #f7fafc; position: relative; min-width: 0; min-height: 0; }}
            .ppt-canvas {{ width: 90vw; max-width: 900px; height: 54vw; max-height: 540px; background: #fff; border: 2px solid #e2e8f0; border-radius: 8px; position: relative; overflow: visible; box-shadow: 0 8px 25px #0001; transition: transform 0.2s; }}
            .ppt-element {{ position: absolute; border: 2px solid transparent; min-width: 40px; min-height: 20px; }}
            .ppt-element.selected {{ border-color: #3182ce; }}
            .ppt-element.text {{ padding: 8px 12px; background: #fff9; border-radius: 4px; font-size: 18px; line-height: 1.4; }}
            .ppt-element.image {{ background-size: cover; background-position: center; border-radius: 4px; }}
            .zoom-controls {{ margin-left: 20px; display: flex; align-items: center; gap: 6px; }}
            .zoom-btn {{ background: #4a5568; color: #fff; border: none; border-radius: 4px; padding: 4px 10px; font-size: 16px; cursor: pointer; }}
            .zoom-btn:hover {{ background: #3182ce; }}
            .zoom-display {{ color: #fff; font-size: 14px; min-width: 48px; text-align: center; }}
        </style>
    </head>
    <body>
        <div class='ppt-editor'>
            <div class='ppt-toolbar'>
                <button id='ppt-add-text'>Text</button>
                <button id='ppt-add-image'>Image</button>
                <button id='ppt-add-shape'>Shape</button>
                <button id='ppt-delete-element'>Delete</button>
                <button id='ppt-add-slide' style='margin-left:20px;'>+ Slide</button>
                <button id='ppt-remove-slide'>- Slide</button>
                <div class='zoom-controls'>
                    <button class='zoom-btn' id='zoom-out'>-</button>
                    <span class='zoom-display' id='zoom-display'>100%</span>
                    <button class='zoom-btn' id='zoom-in'>+</button>
                    <button class='zoom-btn' id='zoom-fit' title='Fit to window'>⛶</button>
                </div>
                <button id='ppt-export-json' style='margin-left:auto;'>Export JSON</button>
            </div>
            <div class='ppt-main'>
                <div class='ppt-slides' id='ppt-slide-list'></div>
                <div class='ppt-canvas-wrap'>
                    <div class='ppt-canvas' id='ppt-canvas'></div>
                </div>
            </div>
        </div>
        <script>
            let slides = {json.dumps(slides)};
            let currentSlide = 0;
            let selectedElement = null;
            let zoomLevel = 1.0;
            function renderSlides() {{
                let list = document.getElementById('ppt-slide-list');
                list.innerHTML = '';
                slides.forEach((slide, idx) => {{
                    let div = document.createElement('div');
                    div.className = 'ppt-slide-thumb' + (idx === currentSlide ? ' active' : '');
                    div.textContent = slide.title || `Slide ${{idx+1}}`;
                    div.onclick = () => {{ currentSlide = idx; renderSlides(); renderCanvas(); }};
                    list.appendChild(div);
                }});
            }}
            function renderCanvas() {{
                let canvas = document.getElementById('ppt-canvas');
                let slide = slides[currentSlide];
                canvas.innerHTML = '';
                canvas.style.background = slide.background || '#fff';
                slide.elements.forEach(el => {{
                    let div = document.createElement('div');
                    div.className = 'ppt-element ' + el.type + (selectedElement === el.id ? ' selected' : '');
                    div.style.left = el.x + 'px';
                    div.style.top = el.y + 'px';
                    div.style.width = el.width + 'px';
                    div.style.height = el.height + 'px';
                    div.dataset.id = el.id;
                    if (el.type === 'text') {{
                        div.contentEditable = true;
                        div.textContent = el.content;
                        div.style.fontSize = (el.fontSize||18) + 'px';
                        div.style.fontFamily = el.fontFamily||'Arial';
                        div.style.color = el.color||'#222';
                        div.style.fontWeight = el.bold ? 'bold' : 'normal';
                        div.style.fontStyle = el.italic ? 'italic' : 'normal';
                        div.style.textDecoration = el.underline ? 'underline' : 'none';
                        div.oninput = (e) => {{ el.content = div.textContent; }};
                    }}
                    if (el.type === 'image' && el.src) {{
                        div.style.backgroundImage = `url(${{el.src}})`;
                    }}
                    div.onclick = (e) => {{
                        e.stopPropagation();
                        selectedElement = el.id;
                        renderCanvas();
                    }};
                    canvas.appendChild(div);
                }});
                // Apply zoom
                canvas.style.transform = `scale(${{zoomLevel}})`;
                canvas.style.transformOrigin = 'center center';
                document.getElementById('zoom-display').textContent = Math.round(zoomLevel*100) + '%';
            }}
            function setZoom(level) {{
                zoomLevel = Math.max(0.2, Math.min(level, 3));
                renderCanvas();
            }}
            document.getElementById('zoom-in').onclick = () => setZoom(zoomLevel * 1.2);
            document.getElementById('zoom-out').onclick = () => setZoom(zoomLevel / 1.2);
            document.getElementById('zoom-fit').onclick = () => {{
                // Fit canvas to parent
                let wrap = document.querySelector('.ppt-canvas-wrap');
                let canvas = document.getElementById('ppt-canvas');
                let scaleW = wrap.clientWidth / canvas.offsetWidth;
                let scaleH = wrap.clientHeight / canvas.offsetHeight;
                setZoom(Math.min(scaleW, scaleH, 1));
            }};
            document.getElementById('ppt-add-text').onclick = () => {{
                let el = {{
                    type: 'text',
                    id: 'text_' + Math.random().toString(36).slice(2,8),
                    content: 'New Text',
                    x: 120, y: 120, width: 200, height: 50,
                    fontSize: 24, fontFamily: 'Arial', color: '#222', bold: false, italic: false, underline: false
                }};
                slides[currentSlide].elements.push(el);
                renderCanvas();
            }};
            document.getElementById('ppt-add-image').onclick = () => {{
                let url = prompt('Image URL:');
                if (!url) return;
                let el = {{ type: 'image', id: 'img_' + Math.random().toString(36).slice(2,8), src: url, x: 150, y: 150, width: 200, height: 120 }};
                slides[currentSlide].elements.push(el);
                renderCanvas();
            }};
            document.getElementById('ppt-add-shape').onclick = () => {{
                let el = {{ type: 'shape', id: 'shape_' + Math.random().toString(36).slice(2,8), shape: 'rect', x: 200, y: 200, width: 120, height: 80, color: '#3182ce' }};
                slides[currentSlide].elements.push(el);
                renderCanvas();
            }};
            document.getElementById('ppt-delete-element').onclick = () => {{
                if (!selectedElement) return;
                let slide = slides[currentSlide];
                slide.elements = slide.elements.filter(e => e.id !== selectedElement);
                selectedElement = null;
                renderCanvas();
            }};
            document.getElementById('ppt-add-slide').onclick = () => {{
                slides.push({{ id: 'slide_' + (slides.length+1), title: 'New Slide', elements: [], background: '#fff' }});
                currentSlide = slides.length-1;
                renderSlides();
                renderCanvas();
            }};
            document.getElementById('ppt-remove-slide').onclick = () => {{
                if (slides.length <= 1) return;
                slides.splice(currentSlide, 1);
                currentSlide = Math.max(0, currentSlide-1);
                renderSlides();
                renderCanvas();
            }};
            document.getElementById('ppt-export-json').onclick = () => {{
                let data = JSON.stringify(slides, null, 2);
                let blob = new Blob([data], {{type:'application/json'}});
                let url = URL.createObjectURL(blob);
                let a = document.createElement('a');
                a.href = url;
                a.download = 'presentation.json';
                a.click();
                URL.revokeObjectURL(url);
            }};
            document.body.onclick = () => {{ selectedElement = null; renderCanvas(); }};
            window.addEventListener('resize', () => renderCanvas());
            renderSlides();
            renderCanvas();
        </script>
    </body>
    </html>
    """
    # Use 'key' only if supported by Streamlit version
    try:
        components.html(editor_html, width=width+40, height=height+40, key=key)
    except TypeError:
        components.html(editor_html, width=width+40, height=height+40)
    return slides
