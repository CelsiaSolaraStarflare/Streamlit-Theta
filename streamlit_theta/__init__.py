# Streamlit Theta - Open Source Visual Editors Suite for Streamlit
# Provides editors for presentations, documents, spreadsheets, tables, audio, video, charts, images, forms, mind maps, diagrams, and newsletters.
# Enhanced with new modes, themes, and automation features.

# Standard editors
from .editor.document import theta_document_editor
from .editor.spreadsheet import theta_spreadsheet_editor
from .editor.csv import theta_csv_editor
from .editor.audio import theta_audio_editor
from .editor.video import theta_video_editor
from .editor.chart import theta_chart_editor
from .editor.image import theta_image_editor
from .editor.form import theta_form_builder
from .editor.mindmap import theta_mindmap_editor
from .editor.diagram import theta_diagram_editor
from .editor.newsletter import theta_newsletter_editor
from .editor.powerpoint import powerpoint_editor as theta_slide_editor

# Enhanced editors with new features
from .editor.document_enhanced import theta_document_editor_enhanced
from .editor.chart_enhanced import theta_chart_editor_enhanced

# Theme manager
from .theme_manager import ThemeManager

# Convenience imports
slide_editor = theta_slide_editor
document_editor = theta_document_editor
spreadsheet_editor = theta_spreadsheet_editor
csv_editor = theta_csv_editor
audio_editor = theta_audio_editor
video_editor = theta_video_editor
chart_editor = theta_chart_editor
image_editor = theta_image_editor
form_builder = theta_form_builder
mindmap_editor = theta_mindmap_editor
diagram_editor = theta_diagram_editor
newsletter_editor = theta_newsletter_editor

# Enhanced convenience imports
document_editor_enhanced = theta_document_editor_enhanced
chart_editor_enhanced = theta_chart_editor_enhanced

__version__ = "1.1.0"
__author__ = "Arcana Team"
__description__ = "Enhanced visual editors suite for Streamlit with advanced modes, themes, and automation features"

__all__ = [
    # Standard editors
    'theta_slide_editor',
    'theta_document_editor',
    'theta_spreadsheet_editor', 
    'theta_csv_editor',
    'theta_audio_editor',
    'theta_video_editor',
    'theta_chart_editor',
    'theta_image_editor',
    'theta_form_builder',
    'theta_mindmap_editor',
    'theta_diagram_editor',
    'theta_newsletter_editor',
    
    # Enhanced editors
    'theta_document_editor_enhanced',
    'theta_chart_editor_enhanced',
    
    # Theme manager
    'ThemeManager',
    
    # Convenience imports
    'slide_editor',
    'document_editor',
    'spreadsheet_editor',
    'csv_editor',
    'audio_editor',
    'video_editor',
    'chart_editor',
    'image_editor',
    'form_builder',
    'mindmap_editor',
    'diagram_editor',
    'newsletter_editor',
    'document_editor_enhanced',
    'chart_editor_enhanced'
]