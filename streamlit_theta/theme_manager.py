"""
Theme Manager for Streamlit-Theta Editors

Provides centralized theme management for all editors including:
- Dark/Light mode switching
- Custom color schemes
- Consistent styling across editors
- Accessibility support
"""

from typing import Dict, Any, Optional
import json

class ThemeManager:
    """Central theme management for all editors"""
    
    THEMES = {
        "light": {
            "name": "Light",
            "primary_bg": "#ffffff",
            "secondary_bg": "#f8f9fa",
            "tertiary_bg": "#e9ecef",
            "text_primary": "#212529",
            "text_secondary": "#6c757d",
            "text_muted": "#adb5bd",
            "border_color": "#dee2e6",
            "accent_color": "#0066cc",
            "accent_hover": "#0052a3",
            "success_color": "#28a745",
            "warning_color": "#ffc107",
            "danger_color": "#dc3545",
            "info_color": "#17a2b8",
            "shadow": "0 2px 4px rgba(0,0,0,0.1)",
            "shadow_hover": "0 4px 8px rgba(0,0,0,0.15)"
        },
        "dark": {
            "name": "Dark",
            "primary_bg": "#1a1a1a",
            "secondary_bg": "#2d2d2d",
            "tertiary_bg": "#3a3a3a",
            "text_primary": "#ffffff",
            "text_secondary": "#b0b0b0",
            "text_muted": "#808080",
            "border_color": "#444444",
            "accent_color": "#4da6ff",
            "accent_hover": "#3399ff",
            "success_color": "#4caf50",
            "warning_color": "#ff9800",
            "danger_color": "#f44336",
            "info_color": "#2196f3",
            "shadow": "0 2px 4px rgba(0,0,0,0.3)",
            "shadow_hover": "0 4px 8px rgba(0,0,0,0.4)"
        },
        "blue": {
            "name": "Blue Professional",
            "primary_bg": "#f0f4f8",
            "secondary_bg": "#e2e8f0",
            "tertiary_bg": "#cbd5e0",
            "text_primary": "#1a202c",
            "text_secondary": "#4a5568",
            "text_muted": "#718096",
            "border_color": "#e2e8f0",
            "accent_color": "#3182ce",
            "accent_hover": "#2c5aa0",
            "success_color": "#38a169",
            "warning_color": "#d69e2e",
            "danger_color": "#e53e3e",
            "info_color": "#3182ce",
            "shadow": "0 2px 4px rgba(0,0,0,0.1)",
            "shadow_hover": "0 4px 8px rgba(0,0,0,0.15)"
        },
        "green": {
            "name": "Green Nature",
            "primary_bg": "#f0fff4",
            "secondary_bg": "#e6fffa",
            "tertiary_bg": "#c6f6d5",
            "text_primary": "#1a202c",
            "text_secondary": "#2d3748",
            "text_muted": "#718096",
            "border_color": "#c6f6d5",
            "accent_color": "#38a169",
            "accent_hover": "#2f855a",
            "success_color": "#38a169",
            "warning_color": "#d69e2e",
            "danger_color": "#e53e3e",
            "info_color": "#3182ce",
            "shadow": "0 2px 4px rgba(0,0,0,0.1)",
            "shadow_hover": "0 4px 8px rgba(0,0,0,0.15)"
        },
        "purple": {
            "name": "Purple Modern",
            "primary_bg": "#faf5ff",
            "secondary_bg": "#e9d8fd",
            "tertiary_bg": "#d6bcfa",
            "text_primary": "#1a202c",
            "text_secondary": "#4a5568",
            "text_muted": "#718096",
            "border_color": "#e9d8fd",
            "accent_color": "#805ad5",
            "accent_hover": "#6b46c1",
            "success_color": "#38a169",
            "warning_color": "#d69e2e",
            "danger_color": "#e53e3e",
            "info_color": "#805ad5",
            "shadow": "0 2px 4px rgba(0,0,0,0.1)",
            "shadow_hover": "0 4px 8px rgba(0,0,0,0.15)"
        }
    }
    
    @classmethod
    def get_theme(cls, theme_name: str = "light") -> Dict[str, Any]:
        """Get theme configuration"""
        return cls.THEMES.get(theme_name, cls.THEMES["light"])
    
    @classmethod
    def get_theme_names(cls) -> list:
        """Get list of available theme names"""
        return list(cls.THEMES.keys())
    
    @classmethod
    def generate_css(cls, theme_name: str = "light") -> str:
        """Generate CSS for a theme"""
        theme = cls.get_theme(theme_name)
        
        return f"""
        :root {{
            --primary-bg: {theme['primary_bg']};
            --secondary-bg: {theme['secondary_bg']};
            --tertiary-bg: {theme['tertiary_bg']};
            --text-primary: {theme['text_primary']};
            --text-secondary: {theme['text_secondary']};
            --text-muted: {theme['text_muted']};
            --border-color: {theme['border_color']};
            --accent-color: {theme['accent_color']};
            --accent-hover: {theme['accent_hover']};
            --success-color: {theme['success_color']};
            --warning-color: {theme['warning_color']};
            --danger-color: {theme['danger_color']};
            --info-color: {theme['info_color']};
            --shadow: {theme['shadow']};
            --shadow-hover: {theme['shadow_hover']};
        }}
        
        .theta-editor {{
            background-color: var(--primary-bg);
            color: var(--text-primary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            box-shadow: var(--shadow);
            transition: all 0.3s ease;
        }}
        
        .theta-editor:hover {{
            box-shadow: var(--shadow-hover);
        }}
        
        .theta-toolbar {{
            background-color: var(--secondary-bg);
            border-bottom: 1px solid var(--border-color);
            padding: 10px;
        }}
        
        .theta-button {{
            background-color: var(--accent-color);
            color: var(--primary-bg);
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        
        .theta-button:hover {{
            background-color: var(--accent-hover);
            transform: translateY(-1px);
        }}
        
        .theta-button.success {{
            background-color: var(--success-color);
        }}
        
        .theta-button.warning {{
            background-color: var(--warning-color);
        }}
        
        .theta-button.danger {{
            background-color: var(--danger-color);
        }}
        
        .theta-input {{
            background-color: var(--primary-bg);
            color: var(--text-primary);
            border: 1px solid var(--border-color);
            border-radius: 4px;
            padding: 8px;
            transition: border-color 0.2s ease;
        }}
        
        .theta-input:focus {{
            outline: none;
            border-color: var(--accent-color);
            box-shadow: 0 0 0 2px rgba(var(--accent-color), 0.2);
        }}
        
        .theta-panel {{
            background-color: var(--secondary-bg);
            border: 1px solid var(--border-color);
            border-radius: 4px;
            padding: 16px;
            margin: 8px 0;
        }}
        
        .theta-text-secondary {{
            color: var(--text-secondary);
        }}
        
        .theta-text-muted {{
            color: var(--text-muted);
        }}
        
        .theta-theme-switcher {{
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
            background-color: var(--secondary-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 8px;
            box-shadow: var(--shadow);
        }}
        
        .theta-theme-switcher select {{
            background-color: var(--primary-bg);
            color: var(--text-primary);
            border: 1px solid var(--border-color);
            border-radius: 4px;
            padding: 4px 8px;
            cursor: pointer;
        }}
        
        /* Accessibility improvements */
        .theta-editor:focus-within {{
            outline: 2px solid var(--accent-color);
            outline-offset: 2px;
        }}
        
        /* Dark mode specific adjustments */
        .theta-editor[data-theme="dark"] {{
            --scrollbar-bg: #2d2d2d;
            --scrollbar-thumb: #4a4a4a;
        }}
        
        .theta-editor[data-theme="dark"] ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        
        .theta-editor[data-theme="dark"] ::-webkit-scrollbar-track {{
            background: var(--scrollbar-bg);
        }}
        
        .theta-editor[data-theme="dark"] ::-webkit-scrollbar-thumb {{
            background: var(--scrollbar-thumb);
            border-radius: 4px;
        }}
        
        .theta-editor[data-theme="dark"] ::-webkit-scrollbar-thumb:hover {{
            background: #606060;
        }}
        
        /* Animation classes */
        .theta-fade-in {{
            animation: thetaFadeIn 0.3s ease-in;
        }}
        
        .theta-slide-in {{
            animation: thetaSlideIn 0.3s ease-out;
        }}
        
        @keyframes thetaFadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        
        @keyframes thetaSlideIn {{
            from {{ transform: translateY(-10px); opacity: 0; }}
            to {{ transform: translateY(0); opacity: 1; }}
        }}
        
        /* Responsive design */
        @media (max-width: 768px) {{
            .theta-toolbar {{
                flex-direction: column;
                gap: 8px;
            }}
            
            .theta-button {{
                width: 100%;
                margin-bottom: 4px;
            }}
            
            .theta-theme-switcher {{
                position: relative;
                top: auto;
                right: auto;
                margin-bottom: 16px;
            }}
        }}
        """
    
    @classmethod
    def get_theme_switcher_html(cls, current_theme: str = "light") -> str:
        """Generate theme switcher HTML"""
        options = ""
        for theme_name, theme_data in cls.THEMES.items():
            selected = "selected" if theme_name == current_theme else ""
            options += f'<option value="{theme_name}" {selected}>{theme_data["name"]}</option>'
        
        return f"""
        <div class="theta-theme-switcher">
            <label for="theme-selector">🎨 Theme:</label>
            <select id="theme-selector" onchange="changeTheme(this.value)">
                {options}
            </select>
        </div>
        """
    
    @classmethod
    def get_theme_switcher_js(cls) -> str:
        """Generate theme switcher JavaScript"""
        return """
        function changeTheme(themeName) {
            // Update CSS variables
            const theme = """ + json.dumps(cls.THEMES) + """;
            const selectedTheme = theme[themeName];
            
            if (selectedTheme) {
                const root = document.documentElement;
                Object.entries(selectedTheme).forEach(([key, value]) => {
                    if (key !== 'name') {
                        const cssVar = '--' + key.replace(/_/g, '-');
                        root.style.setProperty(cssVar, value);
                    }
                });
                
                // Update editor data attribute
                const editors = document.querySelectorAll('.theta-editor');
                editors.forEach(editor => {
                    editor.setAttribute('data-theme', themeName);
                });
                
                // Store preference
                localStorage.setItem('theta-theme', themeName);
                
                // Trigger custom event
                window.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme: themeName } }));
            }
        }
        
        // Load saved theme on page load
        document.addEventListener('DOMContentLoaded', function() {
            const savedTheme = localStorage.getItem('theta-theme') || 'light';
            const selector = document.getElementById('theme-selector');
            if (selector) {
                selector.value = savedTheme;
                changeTheme(savedTheme);
            }
        });
        
        // Listen for system theme changes
        if (window.matchMedia) {
            const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
            mediaQuery.addListener(function(e) {
                if (!localStorage.getItem('theta-theme')) {
                    changeTheme(e.matches ? 'dark' : 'light');
                }
            });
        }
        """