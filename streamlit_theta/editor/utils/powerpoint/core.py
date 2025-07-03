"""
PowerPoint Editor Core JavaScript Functionality
Handles all interactive features and state management
"""

def get_core_javascript():
    return """
        // PowerPoint Editor Core JavaScript
        class PowerPointEditor {
            constructor(initialSlides) {
                this.slides = initialSlides || this.getDefaultSlides();
                this.currentSlide = 0;
                this.selectedElement = null;
                this.zoomLevel = 1.0;
                this.isDragging = false;
                this.isResizing = false;
                this.dragStart = {x: 0, y: 0};
                this.elementStart = {x: 0, y: 0};
                this.history = [];
                this.historyIndex = -1;
                this.clipboard = null;
                
                this.init();
            }
            
            getDefaultSlides() {
                return [{
                    id: 'slide_1',
                    title: 'Title Slide',
                    elements: [{
                        type: 'text',
                        id: 'text_1',
                        content: 'Click to edit title',
                        x: 100, y: 100, width: 600, height: 80,
                        fontSize: 36, fontFamily: 'Arial', color: '#222222',
                        bold: true, italic: false, underline: false
                    }],
                    background: '#ffffff',
                    transition: 'fade'
                }];
            }
            
            init() {
                this.setupEventListeners();
                this.renderSlides();
                this.renderCanvas();
                this.saveState();
            }
            
            setupEventListeners() {
                // Toolbar buttons
                document.getElementById('ppt-add-text').onclick = () => this.addTextElement();
                document.getElementById('ppt-add-image').onclick = () => this.addImageElement();
                document.getElementById('ppt-add-shape').onclick = () => this.addShapeElement();
                document.getElementById('ppt-delete-element').onclick = () => this.deleteSelectedElement();
                document.getElementById('ppt-add-slide').onclick = () => this.addSlide();
                document.getElementById('ppt-remove-slide').onclick = () => this.removeSlide();
                document.getElementById('ppt-duplicate-slide').onclick = () => this.duplicateSlide();
                document.getElementById('ppt-export-json').onclick = () => this.exportJSON();
                document.getElementById('ppt-export-html').onclick = () => this.exportHTML();
                document.getElementById('ppt-import-json').onclick = () => this.importJSON();
                
                // Zoom controls
                document.getElementById('zoom-in').onclick = () => this.zoomIn();
                document.getElementById('zoom-out').onclick = () => this.zoomOut();
                document.getElementById('zoom-fit').onclick = () => this.zoomFit();
                document.getElementById('zoom-100').onclick = () => this.setZoom(1.0);
                
                // Properties panel
                document.getElementById('toggle-properties').onclick = () => this.togglePropertiesPanel();
                document.getElementById('close-properties').onclick = () => this.togglePropertiesPanel();
                
                // Keyboard shortcuts
                document.addEventListener('keydown', (e) => this.handleKeyboardShortcuts(e));
                
                // Canvas interactions
                document.body.onclick = (e) => {
                    if (!e.target.closest('.ppt-element') && !e.target.closest('.properties-panel')) {
                        this.clearSelection();
                    }
                };
                
                // Window resize
                window.addEventListener('resize', () => this.renderCanvas());
                
                // Drag and drop for file import
                const canvas = document.getElementById('ppt-canvas');
                canvas.addEventListener('dragover', (e) => e.preventDefault());
                canvas.addEventListener('drop', (e) => this.handleFileDrop(e));
            }
            
            renderSlides() {
                const list = document.getElementById('ppt-slide-list');
                list.innerHTML = '';
                
                this.slides.forEach((slide, idx) => {
                    const div = document.createElement('div');
                    div.className = 'ppt-slide-thumb' + (idx === this.currentSlide ? ' active' : '');
                    div.textContent = slide.title || `Slide ${idx + 1}`;
                    div.setAttribute('data-slide-number', idx + 1);
                    div.onclick = () => this.selectSlide(idx);
                    
                    // Add context menu
                    div.oncontextmenu = (e) => {
                        e.preventDefault();
                        this.showSlideContextMenu(e, idx);
                    };
                    
                    list.appendChild(div);
                });
                
                // Add slide button
                const addBtn = document.createElement('button');
                addBtn.className = 'add-slide-btn';
                addBtn.innerHTML = '+ Add Slide';
                addBtn.onclick = () => this.addSlide();
                list.appendChild(addBtn);
            }
            
            renderCanvas() {
                const canvas = document.getElementById('ppt-canvas');
                const slide = this.slides[this.currentSlide];
                
                canvas.innerHTML = '';
                canvas.style.background = slide.background || '#ffffff';
                canvas.style.transform = `scale(${this.zoomLevel})`;
                canvas.style.transformOrigin = 'center center';
                
                slide.elements.forEach(el => {
                    const elementDiv = this.createElementDiv(el);
                    canvas.appendChild(elementDiv);
                });
                
                this.updateZoomDisplay();
            }
            
            createElementDiv(element) {
                const div = document.createElement('div');
                div.className = `ppt-element ${element.type}` + 
                              (this.selectedElement === element.id ? ' selected' : '');
                div.dataset.id = element.id;
                div.style.left = element.x + 'px';
                div.style.top = element.y + 'px';
                div.style.width = element.width + 'px';
                div.style.height = element.height + 'px';
                
                if (element.type === 'text') {
                    this.setupTextElement(div, element);
                } else if (element.type === 'image') {
                    this.setupImageElement(div, element);
                } else if (element.type === 'shape') {
                    this.setupShapeElement(div, element);
                }
                
                // Add interaction handlers
                div.onclick = (e) => {
                    e.stopPropagation();
                    this.selectElement(element.id);
                };
                
                div.ondblclick = (e) => {
                    e.stopPropagation();
                    if (element.type === 'text') {
                        this.enterTextEditMode(div);
                    }
                };
                
                this.setupDragAndResize(div, element);
                
                return div;
            }
            
            setupTextElement(div, element) {
                div.contentEditable = false;
                div.textContent = element.content;
                div.style.fontSize = (element.fontSize || 18) + 'px';
                div.style.fontFamily = element.fontFamily || 'Arial';
                div.style.color = element.color || '#222';
                div.style.fontWeight = element.bold ? 'bold' : 'normal';
                div.style.fontStyle = element.italic ? 'italic' : 'normal';
                div.style.textDecoration = element.underline ? 'underline' : 'none';
                div.style.textAlign = element.align || 'left';
                div.style.lineHeight = element.lineHeight || '1.5';
            }
            
            setupImageElement(div, element) {
                if (element.src) {
                    div.style.backgroundImage = `url(${element.src})`;
                } else {
                    div.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;height:100%;color:#666;">Image</div>';
                }
                div.style.backgroundSize = element.fit || 'cover';
                div.style.backgroundPosition = 'center';
                div.style.backgroundRepeat = 'no-repeat';
            }
            
            setupShapeElement(div, element) {
                div.style.backgroundColor = element.color || '#3182ce';
                div.style.borderRadius = element.borderRadius || '0px';
                div.style.border = element.border || 'none';
                
                if (element.shape === 'circle') {
                    div.style.borderRadius = '50%';
                } else if (element.shape === 'triangle') {
                    div.style.clipPath = 'polygon(50% 0%, 0% 100%, 100% 100%)';
                }
            }
            
            setupDragAndResize(div, element) {
                div.onmousedown = (e) => {
                    if (e.target === div || e.target.classList.contains('ppt-element')) {
                        this.startDrag(e, div, element);
                    }
                };
                
                // Add resize handles when selected
                if (this.selectedElement === element.id) {
                    this.addResizeHandles(div, element);
                }
            }
            
            addResizeHandles(div, element) {
                const handles = ['nw', 'ne', 'sw', 'se', 'n', 's', 'w', 'e'];
                handles.forEach(position => {
                    const handle = document.createElement('div');
                    handle.className = `resize-handle ${position}`;
                    handle.onmousedown = (e) => {
                        e.stopPropagation();
                        this.startResize(e, div, element, position);
                    };
                    div.appendChild(handle);
                });
            }
            
            startDrag(e, div, element) {
                this.isDragging = true;
                div.style.cursor = 'grabbing';
                
                this.dragStart = { x: e.clientX, y: e.clientY };
                this.elementStart = { x: element.x, y: element.y };
                
                const onMouseMove = (e) => {
                    if (this.isDragging) {
                        const deltaX = (e.clientX - this.dragStart.x) / this.zoomLevel;
                        const deltaY = (e.clientY - this.dragStart.y) / this.zoomLevel;
                        
                        element.x = Math.max(0, this.elementStart.x + deltaX);
                        element.y = Math.max(0, this.elementStart.y + deltaY);
                        
                        div.style.left = element.x + 'px';
                        div.style.top = element.y + 'px';
                        
                        this.updatePropertiesPanel();
                    }
                };
                
                const onMouseUp = () => {
                    this.isDragging = false;
                    div.style.cursor = 'move';
                    document.removeEventListener('mousemove', onMouseMove);
                    document.removeEventListener('mouseup', onMouseUp);
                    this.saveState();
                };
                
                document.addEventListener('mousemove', onMouseMove);
                document.addEventListener('mouseup', onMouseUp);
                e.preventDefault();
            }
            
            startResize(e, div, element, direction) {
                this.isResizing = true;
                
                const startX = e.clientX;
                const startY = e.clientY;
                const startWidth = element.width;
                const startHeight = element.height;
                const startLeft = element.x;
                const startTop = element.y;
                
                const onMouseMove = (e) => {
                    if (this.isResizing) {
                        const deltaX = (e.clientX - startX) / this.zoomLevel;
                        const deltaY = (e.clientY - startY) / this.zoomLevel;
                        
                        this.handleResize(element, div, direction, deltaX, deltaY, 
                                        startWidth, startHeight, startLeft, startTop);
                    }
                };
                
                const onMouseUp = () => {
                    this.isResizing = false;
                    document.removeEventListener('mousemove', onMouseMove);
                    document.removeEventListener('mouseup', onMouseUp);
                    this.saveState();
                };
                
                document.addEventListener('mousemove', onMouseMove);
                document.addEventListener('mouseup', onMouseUp);
                e.preventDefault();
            }
            
            handleResize(element, div, direction, deltaX, deltaY, startWidth, startHeight, startLeft, startTop) {
                let newWidth = startWidth;
                let newHeight = startHeight;
                let newLeft = startLeft;
                let newTop = startTop;
                
                if (direction.includes('e')) {
                    newWidth = Math.max(20, startWidth + deltaX);
                }
                if (direction.includes('w')) {
                    newWidth = Math.max(20, startWidth - deltaX);
                    newLeft = startLeft + deltaX;
                }
                if (direction.includes('s')) {
                    newHeight = Math.max(20, startHeight + deltaY);
                }
                if (direction.includes('n')) {
                    newHeight = Math.max(20, startHeight - deltaY);
                    newTop = startTop + deltaY;
                }
                
                element.width = newWidth;
                element.height = newHeight;
                element.x = Math.max(0, newLeft);
                element.y = Math.max(0, newTop);
                
                div.style.width = element.width + 'px';
                div.style.height = element.height + 'px';
                div.style.left = element.x + 'px';
                div.style.top = element.y + 'px';
                
                this.updatePropertiesPanel();
            }
            
            selectElement(elementId) {
                this.selectedElement = elementId;
                this.renderCanvas();
                this.updatePropertiesPanel();
            }
            
            clearSelection() {
                this.selectedElement = null;
                this.renderCanvas();
                this.updatePropertiesPanel();
            }
            
            selectSlide(index) {
                this.currentSlide = index;
                this.clearSelection();
                this.renderSlides();
                this.renderCanvas();
            }
            
            addTextElement() {
                const element = {
                    type: 'text',
                    id: 'text_' + this.generateId(),
                    content: 'New Text',
                    x: 100, y: 100, width: 200, height: 50,
                    fontSize: 24, fontFamily: 'Arial', color: '#222',
                    bold: false, italic: false, underline: false,
                    align: 'left', lineHeight: '1.5'
                };
                
                this.slides[this.currentSlide].elements.push(element);
                this.selectElement(element.id);
                this.renderCanvas();
                this.saveState();
            }
            
            addImageElement() {
                const url = prompt('Enter image URL:');
                if (!url) return;
                
                const element = {
                    type: 'image',
                    id: 'img_' + this.generateId(),
                    src: url,
                    x: 150, y: 150, width: 200, height: 150,
                    fit: 'cover'
                };
                
                this.slides[this.currentSlide].elements.push(element);
                this.selectElement(element.id);
                this.renderCanvas();
                this.saveState();
            }
            
            addShapeElement() {
                const shapes = ['rectangle', 'circle', 'triangle'];
                const shape = prompt(`Enter shape type (${shapes.join(', ')}):`) || 'rectangle';
                
                const element = {
                    type: 'shape',
                    id: 'shape_' + this.generateId(),
                    shape: shape,
                    x: 200, y: 200, width: 120, height: 80,
                    color: '#3182ce',
                    borderRadius: shape === 'rectangle' ? '8px' : '0px'
                };
                
                this.slides[this.currentSlide].elements.push(element);
                this.selectElement(element.id);
                this.renderCanvas();
                this.saveState();
            }
            
            deleteSelectedElement() {
                if (!this.selectedElement) return;
                
                const slide = this.slides[this.currentSlide];
                slide.elements = slide.elements.filter(el => el.id !== this.selectedElement);
                this.clearSelection();
                this.renderCanvas();
                this.saveState();
            }
            
            addSlide() {
                const newSlide = {
                    id: 'slide_' + this.generateId(),
                    title: `Slide ${this.slides.length + 1}`,
                    elements: [],
                    background: '#ffffff',
                    transition: 'fade'
                };
                
                this.slides.push(newSlide);
                this.selectSlide(this.slides.length - 1);
                this.renderSlides();
                this.saveState();
            }
            
            removeSlide() {
                if (this.slides.length <= 1) return;
                
                this.slides.splice(this.currentSlide, 1);
                this.currentSlide = Math.max(0, this.currentSlide - 1);
                this.renderSlides();
                this.renderCanvas();
                this.saveState();
            }
            
            duplicateSlide() {
                const currentSlideData = JSON.parse(JSON.stringify(this.slides[this.currentSlide]));
                currentSlideData.id = 'slide_' + this.generateId();
                currentSlideData.title += ' (Copy)';
                
                // Generate new IDs for all elements
                currentSlideData.elements.forEach(el => {
                    el.id = el.type + '_' + this.generateId();
                });
                
                this.slides.splice(this.currentSlide + 1, 0, currentSlideData);
                this.selectSlide(this.currentSlide + 1);
                this.renderSlides();
                this.saveState();
            }
            
            setZoom(level) {
                this.zoomLevel = Math.max(0.1, Math.min(level, 5));
                this.renderCanvas();
            }
            
            zoomIn() {
                this.setZoom(this.zoomLevel * 1.25);
            }
            
            zoomOut() {
                this.setZoom(this.zoomLevel / 1.25);
            }
            
            zoomFit() {
                const wrap = document.querySelector('.ppt-canvas-wrap');
                const canvas = document.getElementById('ppt-canvas');
                const scaleW = (wrap.clientWidth - 40) / canvas.offsetWidth;
                const scaleH = (wrap.clientHeight - 40) / canvas.offsetHeight;
                this.setZoom(Math.min(scaleW, scaleH, 1));
            }
            
            updateZoomDisplay() {
                document.getElementById('zoom-display').textContent = Math.round(this.zoomLevel * 100) + '%';
            }
            
            togglePropertiesPanel() {
                const panel = document.querySelector('.properties-panel');
                panel.classList.toggle('visible');
            }
            
            updatePropertiesPanel() {
                // Implementation for updating properties panel based on selected element
                // This would be expanded based on the element type
            }
            
            handleKeyboardShortcuts(e) {
                if (e.ctrlKey || e.metaKey) {
                    switch(e.key) {
                        case 'z':
                            e.preventDefault();
                            this.undo();
                            break;
                        case 'y':
                            e.preventDefault();
                            this.redo();
                            break;
                        case 'c':
                            e.preventDefault();
                            this.copy();
                            break;
                        case 'v':
                            e.preventDefault();
                            this.paste();
                            break;
                        case 's':
                            e.preventDefault();
                            this.exportJSON();
                            break;
                    }
                }
                
                if (e.key === 'Delete' && this.selectedElement) {
                    this.deleteSelectedElement();
                }
            }
            
            saveState() {
                this.history = this.history.slice(0, this.historyIndex + 1);
                this.history.push(JSON.parse(JSON.stringify(this.slides)));
                this.historyIndex++;
                
                if (this.history.length > 50) {
                    this.history.shift();
                    this.historyIndex--;
                }
            }
            
            undo() {
                if (this.historyIndex > 0) {
                    this.historyIndex--;
                    this.slides = JSON.parse(JSON.stringify(this.history[this.historyIndex]));
                    this.renderSlides();
                    this.renderCanvas();
                }
            }
            
            redo() {
                if (this.historyIndex < this.history.length - 1) {
                    this.historyIndex++;
                    this.slides = JSON.parse(JSON.stringify(this.history[this.historyIndex]));
                    this.renderSlides();
                    this.renderCanvas();
                }
            }
            
            copy() {
                if (this.selectedElement) {
                    const element = this.slides[this.currentSlide].elements.find(el => el.id === this.selectedElement);
                    this.clipboard = JSON.parse(JSON.stringify(element));
                }
            }
            
            paste() {
                if (this.clipboard) {
                    const newElement = JSON.parse(JSON.stringify(this.clipboard));
                    newElement.id = newElement.type + '_' + this.generateId();
                    newElement.x += 20;
                    newElement.y += 20;
                    
                    this.slides[this.currentSlide].elements.push(newElement);
                    this.selectElement(newElement.id);
                    this.renderCanvas();
                    this.saveState();
                }
            }
            
            exportJSON() {
                const data = JSON.stringify(this.slides, null, 2);
                const blob = new Blob([data], {type: 'application/json'});
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'presentation.json';
                a.click();
                URL.revokeObjectURL(url);
            }
            
            exportHTML() {
                // Implementation for HTML export
                const html = this.generateHTMLPresentation();
                const blob = new Blob([html], {type: 'text/html'});
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'presentation.html';
                a.click();
                URL.revokeObjectURL(url);
            }
            
            generateHTMLPresentation() {
                // Generate a standalone HTML presentation
                return `<!DOCTYPE html>
                <html>
                <head>
                    <title>Presentation</title>
                    <style>
                        body { margin: 0; font-family: Arial, sans-serif; }
                        .slide { width: 100vw; height: 100vh; display: none; position: relative; }
                        .slide.active { display: block; }
                        .element { position: absolute; }
                        .navigation { position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); }
                        .nav-btn { padding: 10px 20px; margin: 0 5px; background: #3182ce; color: white; border: none; border-radius: 5px; cursor: pointer; }
                    </style>
                </head>
                <body>
                    ${this.slides.map((slide, index) => this.generateSlideHTML(slide, index)).join('')}
                    <div class="navigation">
                        <button class="nav-btn" onclick="previousSlide()">Previous</button>
                        <button class="nav-btn" onclick="nextSlide()">Next</button>
                    </div>
                    <script>
                        let currentSlide = 0;
                        const slides = document.querySelectorAll('.slide');
                        
                        function showSlide(n) {
                            slides.forEach(s => s.classList.remove('active'));
                            slides[n].classList.add('active');
                        }
                        
                        function nextSlide() {
                            currentSlide = (currentSlide + 1) % slides.length;
                            showSlide(currentSlide);
                        }
                        
                        function previousSlide() {
                            currentSlide = currentSlide === 0 ? slides.length - 1 : currentSlide - 1;
                            showSlide(currentSlide);
                        }
                        
                        showSlide(0);
                        
                        document.addEventListener('keydown', (e) => {
                            if (e.key === 'ArrowRight') nextSlide();
                            if (e.key === 'ArrowLeft') previousSlide();
                        });
                    </script>
                </body>
                </html>`;
            }
            
            generateSlideHTML(slide, index) {
                const elementsHTML = slide.elements.map(el => {
                    let elementHTML = `<div class="element" style="left: ${el.x}px; top: ${el.y}px; width: ${el.width}px; height: ${el.height}px;`;
                    
                    if (el.type === 'text') {
                        elementHTML += `font-size: ${el.fontSize}px; color: ${el.color}; font-family: ${el.fontFamily};`;
                        elementHTML += `font-weight: ${el.bold ? 'bold' : 'normal'}; font-style: ${el.italic ? 'italic' : 'normal'};`;
                        elementHTML += `text-decoration: ${el.underline ? 'underline' : 'none'};">${el.content}</div>`;
                    } else if (el.type === 'image') {
                        elementHTML += `background-image: url(${el.src}); background-size: cover; background-position: center;"></div>`;
                    } else if (el.type === 'shape') {
                        elementHTML += `background-color: ${el.color};"></div>`;
                    }
                    
                    return elementHTML;
                }).join('');
                
                return `<div class="slide${index === 0 ? ' active' : ''}" style="background: ${slide.background};">${elementsHTML}</div>`;
            }
            
            generateId() {
                return Math.random().toString(36).substr(2, 9);
            }
        }
        
        // Initialize editor when DOM is loaded
        let editorInstance;
        document.addEventListener('DOMContentLoaded', () => {
            editorInstance = new PowerPointEditor(window.initialSlides);
        });
    """
