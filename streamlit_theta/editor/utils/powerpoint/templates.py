"""
PowerPoint Editor Templates and Layouts
Pre-designed slide templates and layout options
"""

def get_slide_templates():
    return {
        "title_slide": {
            "name": "Title Slide",
            "elements": [
                {
                    "type": "text",
                    "id": "title",
                    "content": "Presentation Title",
                    "x": 100, "y": 150, "width": 760, "height": 100,
                    "fontSize": 48, "fontFamily": "Arial", "color": "#1f2937",
                    "bold": True, "italic": False, "underline": False,
                    "align": "center"
                },
                {
                    "type": "text",
                    "id": "subtitle",
                    "content": "Subtitle or Author Name",
                    "x": 100, "y": 280, "width": 760, "height": 60,
                    "fontSize": 24, "fontFamily": "Arial", "color": "#6b7280",
                    "bold": False, "italic": False, "underline": False,
                    "align": "center"
                }
            ],
            "background": "#ffffff"
        },
        
        "content_slide": {
            "name": "Content Slide",
            "elements": [
                {
                    "type": "text",
                    "id": "title",
                    "content": "Slide Title",
                    "x": 80, "y": 60, "width": 800, "height": 80,
                    "fontSize": 36, "fontFamily": "Arial", "color": "#1f2937",
                    "bold": True, "italic": False, "underline": False,
                    "align": "left"
                },
                {
                    "type": "text",
                    "id": "content",
                    "content": "• Bullet point 1\\n• Bullet point 2\\n• Bullet point 3",
                    "x": 80, "y": 160, "width": 800, "height": 300,
                    "fontSize": 24, "fontFamily": "Arial", "color": "#374151",
                    "bold": False, "italic": False, "underline": False,
                    "align": "left"
                }
            ],
            "background": "#ffffff"
        },
        
        "two_column": {
            "name": "Two Column",
            "elements": [
                {
                    "type": "text",
                    "id": "title",
                    "content": "Two Column Layout",
                    "x": 80, "y": 60, "width": 800, "height": 80,
                    "fontSize": 36, "fontFamily": "Arial", "color": "#1f2937",
                    "bold": True, "italic": False, "underline": False,
                    "align": "left"
                },
                {
                    "type": "text",
                    "id": "left_content",
                    "content": "Left Column Content\\n\\n• Point 1\\n• Point 2\\n• Point 3",
                    "x": 80, "y": 160, "width": 380, "height": 300,
                    "fontSize": 20, "fontFamily": "Arial", "color": "#374151",
                    "bold": False, "italic": False, "underline": False,
                    "align": "left"
                },
                {
                    "type": "text",
                    "id": "right_content",
                    "content": "Right Column Content\\n\\n• Point A\\n• Point B\\n• Point C",
                    "x": 480, "y": 160, "width": 380, "height": 300,
                    "fontSize": 20, "fontFamily": "Arial", "color": "#374151",
                    "bold": False, "italic": False, "underline": False,
                    "align": "left"
                }
            ],
            "background": "#ffffff"
        },
        
        "image_content": {
            "name": "Image with Content",
            "elements": [
                {
                    "type": "text",
                    "id": "title",
                    "content": "Image and Content",
                    "x": 80, "y": 60, "width": 800, "height": 80,
                    "fontSize": 36, "fontFamily": "Arial", "color": "#1f2937",
                    "bold": True, "italic": False, "underline": False,
                    "align": "left"
                },
                {
                    "type": "image",
                    "id": "main_image",
                    "src": "https://via.placeholder.com/400x250/3b82f6/ffffff?text=Image",
                    "x": 80, "y": 160, "width": 400, "height": 250,
                    "fit": "cover"
                },
                {
                    "type": "text",
                    "id": "content",
                    "content": "Content describing the image or additional information that complements the visual.",
                    "x": 500, "y": 160, "width": 360, "height": 250,
                    "fontSize": 20, "fontFamily": "Arial", "color": "#374151",
                    "bold": False, "italic": False, "underline": False,
                    "align": "left"
                }
            ],
            "background": "#ffffff"
        },
        
        "comparison": {
            "name": "Comparison",
            "elements": [
                {
                    "type": "text",
                    "id": "title",
                    "content": "Comparison",
                    "x": 80, "y": 60, "width": 800, "height": 80,
                    "fontSize": 36, "fontFamily": "Arial", "color": "#1f2937",
                    "bold": True, "italic": False, "underline": False,
                    "align": "center"
                },
                {
                    "type": "shape",
                    "id": "left_box",
                    "shape": "rectangle",
                    "x": 80, "y": 160, "width": 360, "height": 280,
                    "color": "#dbeafe", "borderRadius": "8px"
                },
                {
                    "type": "text",
                    "id": "left_title",
                    "content": "Option A",
                    "x": 100, "y": 180, "width": 320, "height": 40,
                    "fontSize": 24, "fontFamily": "Arial", "color": "#1e40af",
                    "bold": True, "italic": False, "underline": False,
                    "align": "center"
                },
                {
                    "type": "text",
                    "id": "left_content",
                    "content": "• Advantage 1\\n• Advantage 2\\n• Advantage 3",
                    "x": 100, "y": 230, "width": 320, "height": 180,
                    "fontSize": 18, "fontFamily": "Arial", "color": "#374151",
                    "bold": False, "italic": False, "underline": False,
                    "align": "left"
                },
                {
                    "type": "shape",
                    "id": "right_box",
                    "shape": "rectangle",
                    "x": 520, "y": 160, "width": 360, "height": 280,
                    "color": "#fef3c7", "borderRadius": "8px"
                },
                {
                    "type": "text",
                    "id": "right_title",
                    "content": "Option B",
                    "x": 540, "y": 180, "width": 320, "height": 40,
                    "fontSize": 24, "fontFamily": "Arial", "color": "#d97706",
                    "bold": True, "italic": False, "underline": False,
                    "align": "center"
                },
                {
                    "type": "text",
                    "id": "right_content",
                    "content": "• Benefit 1\\n• Benefit 2\\n• Benefit 3",
                    "x": 540, "y": 230, "width": 320, "height": 180,
                    "fontSize": 18, "fontFamily": "Arial", "color": "#374151",
                    "bold": False, "italic": False, "underline": False,
                    "align": "left"
                }
            ],
            "background": "#ffffff"
        },
        
        "section_header": {
            "name": "Section Header",
            "elements": [
                {
                    "type": "shape",
                    "id": "background_shape",
                    "shape": "rectangle",
                    "x": 0, "y": 0, "width": 960, "height": 540,
                    "color": "#1f2937"
                },
                {
                    "type": "text",
                    "id": "section_title",
                    "content": "Section Title",
                    "x": 80, "y": 200, "width": 800, "height": 100,
                    "fontSize": 60, "fontFamily": "Arial", "color": "#ffffff",
                    "bold": True, "italic": False, "underline": False,
                    "align": "center"
                },
                {
                    "type": "text",
                    "id": "section_subtitle",
                    "content": "Section description or overview",
                    "x": 80, "y": 320, "width": 800, "height": 60,
                    "fontSize": 24, "fontFamily": "Arial", "color": "#d1d5db",
                    "bold": False, "italic": False, "underline": False,
                    "align": "center"
                }
            ],
            "background": "#1f2937"
        },
        
        "thank_you": {
            "name": "Thank You",
            "elements": [
                {
                    "type": "text",
                    "id": "thank_you_text",
                    "content": "Thank You",
                    "x": 80, "y": 180, "width": 800, "height": 120,
                    "fontSize": 72, "fontFamily": "Arial", "color": "#1f2937",
                    "bold": True, "italic": False, "underline": False,
                    "align": "center"
                },
                {
                    "type": "text",
                    "id": "contact_info",
                    "content": "Questions?\\nyour.email@example.com",
                    "x": 80, "y": 320, "width": 800, "height": 100,
                    "fontSize": 20, "fontFamily": "Arial", "color": "#6b7280",
                    "bold": False, "italic": False, "underline": False,
                    "align": "center"
                }
            ],
            "background": "#ffffff"
        }
    }

def get_color_themes():
    return {
        "professional": {
            "name": "Professional",
            "primary": "#1f2937",
            "secondary": "#3b82f6",
            "accent": "#10b981",
            "background": "#ffffff",
            "text": "#374151"
        },
        "modern": {
            "name": "Modern",
            "primary": "#6366f1",
            "secondary": "#8b5cf6",
            "accent": "#ec4899",
            "background": "#f8fafc",
            "text": "#1e293b"
        },
        "warm": {
            "name": "Warm",
            "primary": "#dc2626",
            "secondary": "#ea580c",
            "accent": "#d97706",
            "background": "#fefefe",
            "text": "#292524"
        },
        "cool": {
            "name": "Cool",
            "primary": "#0891b2",
            "secondary": "#0284c7",
            "accent": "#2563eb",
            "background": "#f0f9ff",
            "text": "#0c4a6e"
        },
        "nature": {
            "name": "Nature",
            "primary": "#059669",
            "secondary": "#16a34a",
            "accent": "#65a30d",
            "background": "#f0fdf4",
            "text": "#14532d"
        },
        "dark": {
            "name": "Dark",
            "primary": "#f3f4f6",
            "secondary": "#e5e7eb",
            "accent": "#60a5fa",
            "background": "#111827",
            "text": "#f9fafb"
        }
    }

def get_layout_templates():
    return """
        function applyTemplate(templateName) {
            const templates = getSlideTemplates();
            const template = templates[templateName];
            
            if (!template) return;
            
            const slide = editorInstance.slides[editorInstance.currentSlide];
            slide.elements = JSON.parse(JSON.stringify(template.elements));
            slide.background = template.background;
            
            // Generate new IDs for elements
            slide.elements.forEach(el => {
                el.id = el.type + '_' + editorInstance.generateId();
            });
            
            editorInstance.renderCanvas();
            editorInstance.saveState();
        }
        
        function applyColorTheme(themeName) {
            const themes = getColorThemes();
            const theme = themes[themeName];
            
            if (!theme) return;
            
            // Apply theme to current slide
            const slide = editorInstance.slides[editorInstance.currentSlide];
            slide.background = theme.background;
            
            slide.elements.forEach(el => {
                if (el.type === 'text') {
                    if (el.id.includes('title')) {
                        el.color = theme.primary;
                    } else {
                        el.color = theme.text;
                    }
                } else if (el.type === 'shape') {
                    el.color = theme.secondary;
                }
            });
            
            editorInstance.renderCanvas();
            editorInstance.saveState();
        }
        
        function getSlideTemplates() {
            return ${get_slide_templates()};
        }
        
        function getColorThemes() {
            return ${get_color_themes()};
        }
    """
