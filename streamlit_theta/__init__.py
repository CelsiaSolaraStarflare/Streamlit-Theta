# Streamlit Theta - Open Source Visual Editors Suite for Streamlit
# Provides editors for presentations, documents, spreadsheets, tables, audio, video, charts, images, forms, mind maps, diagrams, and newsletters.

# from .editor.slide import theta_slide_editor  # Disabled to avoid missing frontend/build error
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



__version__ = "1.0.4"
__author__ = "Arcana Team"
__description__ = "Comprehensive visual editors suite for Streamlit: presentations, documents, spreadsheets, charts, images, forms, mind maps, diagrams, newsletters, and more"

__all__ = [
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
    'newsletter_editor'
]