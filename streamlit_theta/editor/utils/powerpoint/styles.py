"""
PowerPoint Editor Core Styles
Comprehensive CSS for PowerPoint-like interface
"""

def get_core_styles():
    return """
        html, body { 
            height: 100%; 
            margin: 0; 
            padding: 0; 
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
            overflow: hidden;
        }
        
        body { 
            background: #f3f4f6; 
            width: 100vw; 
            height: 100vh; 
        }
        
        /* Main Editor Container */
        .ppt-editor { 
            width: 100%; 
            height: 100vh; 
            max-width: 100vw; 
            max-height: 100vh; 
            background: #fff; 
            border-radius: 10px; 
            box-shadow: 0 4px 20px rgba(0,0,0,0.15); 
            margin: 0 auto; 
            display: flex; 
            flex-direction: column; 
            position: relative;
        }
        
        /* Toolbar Styles */
        .ppt-toolbar { 
            height: 60px; 
            background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%); 
            color: #fff; 
            display: flex; 
            align-items: center; 
            padding: 0 20px; 
            gap: 12px; 
            border-radius: 10px 10px 0 0; 
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            user-select: none;
        }
        
        .ppt-toolbar button { 
            background: #4a5568; 
            color: #fff; 
            border: none; 
            border-radius: 6px; 
            padding: 10px 16px; 
            cursor: pointer; 
            font-size: 14px; 
            font-weight: 500;
            transition: all 0.2s ease;
            position: relative;
        }
        
        .ppt-toolbar button:hover { 
            background: #3182ce; 
            transform: translateY(-1px);
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        }
        
        .ppt-toolbar button:active {
            transform: translateY(0);
        }
        
        .ppt-toolbar button.active {
            background: #3182ce;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.2);
        }
        
        /* Toolbar Groups */
        .toolbar-group {
            display: flex;
            gap: 8px;
            padding: 0 12px;
            border-left: 1px solid #4a5568;
            margin-left: 8px;
        }
        
        .toolbar-group:first-child {
            border-left: none;
            margin-left: 0;
        }
        
        /* Main Content Area */
        .ppt-main { 
            flex: 1; 
            display: flex; 
            min-height: 0; 
            position: relative;
        }
        
        /* Slide Navigation Panel */
        .ppt-slides { 
            width: 180px; 
            background: #e5e7eb; 
            border-right: 2px solid #d1d5db; 
            overflow-y: auto; 
            padding: 15px; 
            box-shadow: inset -2px 0 8px rgba(0,0,0,0.05);
        }
        
        .ppt-slide-thumb { 
            width: 150px; 
            height: 100px; 
            background: #fff; 
            border: 3px solid #d1d5db; 
            border-radius: 6px; 
            margin-bottom: 12px; 
            cursor: pointer; 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            font-size: 12px; 
            color: #6b7280; 
            font-weight: 600;
            transition: all 0.2s ease;
            position: relative;
            overflow: hidden;
        }
        
        .ppt-slide-thumb:hover {
            border-color: #9ca3af;
            transform: scale(1.02);
        }
        
        .ppt-slide-thumb.active { 
            border-color: #3b82f6; 
            box-shadow: 0 0 0 2px #dbeafe;
            transform: scale(1.05);
        }
        
        .ppt-slide-thumb::after {
            content: attr(data-slide-number);
            position: absolute;
            top: 4px;
            left: 6px;
            background: #374151;
            color: white;
            font-size: 10px;
            padding: 2px 6px;
            border-radius: 10px;
            font-weight: bold;
        }
        
        /* Canvas Wrapper */
        .ppt-canvas-wrap { 
            flex: 1; 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            background: #f9fafb; 
            position: relative; 
            min-width: 0; 
            min-height: 0; 
            overflow: hidden;
            background-image: radial-gradient(circle at 1px 1px, rgba(0,0,0,0.1) 1px, transparent 0);
            background-size: 20px 20px;
        }
        
        /* Main Canvas */
        .ppt-canvas { 
            width: 90vw; 
            max-width: 960px; 
            height: 54vw; 
            max-height: 540px; 
            background: #fff; 
            border: 3px solid #e5e7eb; 
            border-radius: 10px; 
            position: relative; 
            overflow: visible; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.2); 
            transition: transform 0.3s ease;
        }
        
        /* Element Styles */
        .ppt-element { 
            position: absolute; 
            border: 2px solid transparent; 
            min-width: 40px; 
            min-height: 20px; 
            cursor: move;
            transition: all 0.2s ease;
        }
        
        .ppt-element:hover {
            border-color: #cbd5e0;
        }
        
        .ppt-element.selected { 
            border-color: #3b82f6; 
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.3);
        }
        
        .ppt-element.text { 
            padding: 12px 16px; 
            background: rgba(255,255,255,0.95); 
            border-radius: 6px; 
            font-size: 18px; 
            line-height: 1.5; 
            backdrop-filter: blur(5px);
            cursor: text;
        }
        
        .ppt-element.text:focus {
            outline: none;
            background: #fff;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        
        .ppt-element.image { 
            background-size: cover; 
            background-position: center; 
            border-radius: 6px; 
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        .ppt-element.shape {
            border-radius: 4px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        /* Resize Handles */
        .resize-handle {
            position: absolute;
            width: 10px;
            height: 10px;
            background: #3b82f6;
            border: 2px solid #fff;
            border-radius: 50%;
            opacity: 0;
            transition: opacity 0.2s ease;
        }
        
        .ppt-element.selected .resize-handle {
            opacity: 1;
        }
        
        .resize-handle.nw { top: -5px; left: -5px; cursor: nw-resize; }
        .resize-handle.ne { top: -5px; right: -5px; cursor: ne-resize; }
        .resize-handle.sw { bottom: -5px; left: -5px; cursor: sw-resize; }
        .resize-handle.se { bottom: -5px; right: -5px; cursor: se-resize; }
        .resize-handle.n { top: -5px; left: 50%; transform: translateX(-50%); cursor: n-resize; }
        .resize-handle.s { bottom: -5px; left: 50%; transform: translateX(-50%); cursor: s-resize; }
        .resize-handle.w { top: 50%; left: -5px; transform: translateY(-50%); cursor: w-resize; }
        .resize-handle.e { top: 50%; right: -5px; transform: translateY(-50%); cursor: e-resize; }
        
        /* Zoom Controls */
        .zoom-controls { 
            margin-left: auto; 
            display: flex; 
            align-items: center; 
            gap: 8px; 
        }
        
        .zoom-btn { 
            background: #4a5568; 
            color: #fff; 
            border: none; 
            border-radius: 6px; 
            padding: 8px 12px; 
            font-size: 16px; 
            font-weight: bold;
            cursor: pointer; 
            transition: all 0.2s ease;
        }
        
        .zoom-btn:hover { 
            background: #3182ce; 
            transform: scale(1.1);
        }
        
        .zoom-display { 
            color: #fff; 
            font-size: 14px; 
            font-weight: 600;
            min-width: 50px; 
            text-align: center; 
            background: rgba(255,255,255,0.1);
            padding: 6px 12px;
            border-radius: 20px;
        }
        
        /* Properties Panel */
        .properties-panel {
            position: absolute;
            top: 0;
            right: 0;
            width: 300px;
            height: 100%;
            background: #f8fafc;
            border-left: 2px solid #e5e7eb;
            transform: translateX(100%);
            transition: transform 0.3s ease;
            z-index: 1000;
            overflow-y: auto;
        }
        
        .properties-panel.visible {
            transform: translateX(0);
        }
        
        .properties-header {
            background: #e5e7eb;
            padding: 15px 20px;
            border-bottom: 1px solid #d1d5db;
            font-weight: 600;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .property-group {
            padding: 20px;
            border-bottom: 1px solid #e5e7eb;
        }
        
        .property-group h4 {
            margin: 0 0 15px 0;
            font-size: 14px;
            font-weight: 600;
            color: #374151;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .property-row {
            display: flex;
            align-items: center;
            margin-bottom: 12px;
            gap: 10px;
        }
        
        .property-row label {
            font-size: 12px;
            color: #6b7280;
            flex: 1;
            font-weight: 500;
        }
        
        .property-row input, 
        .property-row select {
            flex: 1.5;
            padding: 8px 12px;
            border: 1px solid #d1d5db;
            border-radius: 4px;
            font-size: 12px;
            background: #fff;
        }
        
        .property-row input:focus,
        .property-row select:focus {
            outline: none;
            border-color: #3b82f6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }
        
        /* Animation Classes */
        .slide-enter {
            animation: slideEnter 0.3s ease-out;
        }
        
        .slide-exit {
            animation: slideExit 0.3s ease-out;
        }
        
        @keyframes slideEnter {
            from {
                opacity: 0;
                transform: translateX(20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        @keyframes slideExit {
            from {
                opacity: 1;
                transform: translateX(0);
            }
            to {
                opacity: 0;
                transform: translateX(-20px);
            }
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .ppt-slides {
                width: 120px;
                padding: 10px;
            }
            
            .ppt-slide-thumb {
                width: 100px;
                height: 75px;
                font-size: 10px;
            }
            
            .ppt-toolbar {
                padding: 0 10px;
                gap: 8px;
            }
            
            .ppt-toolbar button {
                padding: 8px 12px;
                font-size: 12px;
            }
            
            .properties-panel {
                width: 250px;
            }
        }
    """
