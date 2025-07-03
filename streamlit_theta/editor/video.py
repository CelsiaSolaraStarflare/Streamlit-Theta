"""
Theta Video Editor - Video player with basic editing features
"""

import streamlit as st
import streamlit.components.v1 as components
from typing import Optional, Dict, Any

def theta_video_editor(
    video_file: Optional[str] = None,
    width: int = 900,
    height: int = 600
) -> None:
    """
    Create a video editor with playback and basic editing features.
    
    Parameters:
    -----------
    video_file : str or None
        Path to video file
    width : int
        Width of the editor in pixels
    height : int  
        Height of the editor in pixels
        
    Returns:
    --------
    Dict with video data and edits or None
    """
    
    component_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Theta Video Editor</title>
        <style>
            body {{
                margin: 0;
                padding: 10px;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: #1a1a1a;
                color: white;
            }}
            
            .editor-container {{
                width: {width}px;
                height: {height}px;
                background: #2d2d2d;
                border-radius: 8px;
                box-shadow: 0 2px 20px rgba(0,0,0,0.3);
                display: flex;
                flex-direction: column;
                overflow: hidden;
            }}
            
            .header {{
                height: 50px;
                background: #1e1e1e;
                border-bottom: 1px solid #404040;
                display: flex;
                align-items: center;
                padding: 0 20px;
                font-size: 16px;
                font-weight: 600;
            }}
            
            .video-area {{
                flex: 1;
                display: flex;
                background: #1a1a1a;
            }}
            
            .video-container {{
                flex: 1;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }}
            
            .video-player {{
                width: 100%;
                max-width: 640px;
                height: auto;
                background: black;
                border-radius: 8px;
                border: 2px solid #404040;
            }}
            
            .video-placeholder {{
                width: 100%;
                max-width: 640px;
                height: 360px;
                background: #404040;
                border-radius: 8px;
                border: 2px dashed #666;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                color: #ccc;
                font-size: 18px;
            }}
            
            .controls-panel {{
                width: 280px;
                background: #2d2d2d;
                border-left: 1px solid #404040;
                display: flex;
                flex-direction: column;
            }}
            
            .control-group {{
                padding: 20px;
                border-bottom: 1px solid #404040;
            }}
            
            .control-group h3 {{
                margin: 0 0 15px 0;
                font-size: 14px;
                font-weight: 600;
                color: #fff;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            
            .file-upload {{
                margin-bottom: 20px;
            }}
            
            .file-input {{
                display: none;
            }}
            
            .file-label {{
                display: block;
                background: #007acc;
                color: white;
                padding: 12px 20px;
                border-radius: 6px;
                cursor: pointer;
                text-align: center;
                font-size: 14px;
                transition: background 0.3s;
            }}
            
            .file-label:hover {{
                background: #005fa3;
            }}
            
            .control-row {{
                display: flex;
                align-items: center;
                margin-bottom: 12px;
                gap: 10px;
            }}
            
            .control-row label {{
                min-width: 80px;
                font-size: 12px;
                color: #ccc;
            }}
            
            .control-row input[type="range"] {{
                flex: 1;
                height: 4px;
                background: #404040;
                border-radius: 2px;
                outline: none;
                -webkit-appearance: none;
            }}
            
            .control-row input[type="range"]::-webkit-slider-thumb {{
                -webkit-appearance: none;
                width: 16px;
                height: 16px;
                background: #007acc;
                border-radius: 50%;
                cursor: pointer;
            }}
            
            .control-row span {{
                min-width: 40px;
                font-size: 12px;
                color: #ccc;
                text-align: right;
            }}
            
            .playback-controls {{
                height: 80px;
                background: #1e1e1e;
                border-top: 1px solid #404040;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 15px;
                padding: 0 20px;
            }}
            
            .control-btn {{
                background: #007acc;
                border: none;
                color: white;
                padding: 12px 20px;
                border-radius: 25px;
                cursor: pointer;
                font-size: 14px;
                font-weight: 600;
                transition: all 0.3s;
                min-width: 90px;
            }}
            
            .control-btn:hover {{
                background: #005fa3;
                transform: translateY(-2px);
            }}
            
            .control-btn:disabled {{
                background: #555;
                cursor: not-allowed;
                transform: none;
            }}
            
            .timeline {{
                flex: 1;
                max-width: 400px;
                margin: 0 20px;
            }}
            
            .timeline-track {{
                height: 6px;
                background: #404040;
                border-radius: 3px;
                position: relative;
                cursor: pointer;
            }}
            
            .timeline-progress {{
                height: 100%;
                background: #007acc;
                border-radius: 3px;
                width: 0%;
                transition: width 0.1s;
            }}
            
            .time-display {{
                display: flex;
                justify-content: space-between;
                margin-top: 5px;
                font-size: 11px;
                color: #999;
                font-family: monospace;
            }}
            
            .effects-btn {{
                background: #28a745;
                border: none;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 12px;
                margin-bottom: 8px;
                width: 100%;
                transition: background 0.3s;
            }}
            
            .effects-btn:hover {{
                background: #218838;
            }}
        </style>
    </head>
    <body>
        <div class="editor-container">
            <!-- Header -->
            <div class="header">
                🎬 Theta Video Editor
            </div>
            
            <!-- Main Video Area -->
            <div class="video-area">
                <!-- Video Container -->
                <div class="video-container">
                    <div id="video-placeholder" class="video-placeholder">
                        📹<br>
                        Load a video file to start editing
                    </div>
                    <video id="video-player" class="video-player" style="display: none;" controls>
                        Your browser does not support the video tag.
                    </video>
                </div>
                
                <!-- Controls Panel -->
                <div class="controls-panel">
                    <!-- File Upload -->
                    <div class="control-group">
                        <h3>File</h3>
                        <div class="file-upload">
                            <label for="video-file" class="file-label">📁 Load Video File</label>
                            <input type="file" id="video-file" class="file-input" accept="video/*" onchange="loadVideoFile(event)">
                        </div>
                        <div id="file-info" style="font-size: 12px; color: #999;"></div>
                    </div>
                    
                    <!-- Video Properties -->
                    <div class="control-group">
                        <h3>Properties</h3>
                        
                        <div class="control-row">
                            <label>Volume:</label>
                            <input type="range" id="volume" min="0" max="100" value="50" onchange="adjustVolume(this.value)">
                            <span id="volume-val">50%</span>
                        </div>
                        
                        <div class="control-row">
                            <label>Speed:</label>
                            <input type="range" id="speed" min="25" max="300" value="100" onchange="adjustSpeed(this.value)">
                            <span id="speed-val">1.0x</span>
                        </div>
                        
                        <div class="control-row">
                            <label>Brightness:</label>
                            <input type="range" id="brightness" min="0" max="200" value="100" onchange="adjustBrightness(this.value)">
                            <span id="brightness-val">100%</span>
                        </div>
                        
                        <div class="control-row">
                            <label>Contrast:</label>
                            <input type="range" id="contrast" min="0" max="200" value="100" onchange="adjustContrast(this.value)">
                            <span id="contrast-val">100%</span>
                        </div>
                        
                        <div class="control-row">
                            <label>Saturation:</label>
                            <input type="range" id="saturation" min="0" max="200" value="100" onchange="adjustSaturation(this.value)">
                            <span id="saturation-val">100%</span>
                        </div>
                    </div>
                    
                    <!-- Effects -->
                    <div class="control-group">
                        <h3>Effects</h3>
                        <button class="effects-btn" onclick="applyEffect('grayscale')">Grayscale</button>
                        <button class="effects-btn" onclick="applyEffect('sepia')">Sepia</button>
                        <button class="effects-btn" onclick="applyEffect('blur')">Blur</button>
                        <button class="effects-btn" onclick="resetEffects()">Reset All</button>
                    </div>
                    
                    <!-- Save -->
                    <div class="control-group">
                        <h3>Export</h3>
                        <button class="effects-btn" onclick="saveChanges()" style="background: #dc3545;">💾 Save Changes</button>
                    </div>
                </div>
            </div>
            
            <!-- Playback Controls -->
            <div class="playback-controls">
                <button class="control-btn" id="play-btn" onclick="togglePlay()" disabled>▶ Play</button>
                <button class="control-btn" onclick="stopVideo()" disabled>⏹ Stop</button>
                <button class="control-btn" onclick="rewind()" disabled>⏪ -10s</button>
                <button class="control-btn" onclick="fastForward()" disabled>⏩ +10s</button>
                
                <!-- Timeline -->
                <div class="timeline">
                    <div class="timeline-track" onclick="seekTo(event)">
                        <div class="timeline-progress" id="timeline-progress"></div>
                    </div>
                    <div class="time-display">
                        <span id="current-time">0:00</span>
                        <span id="total-time">0:00</span>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            let videoPlayer = document.getElementById('video-player');
            let isPlaying = false;
            let videoFile = null;
            let currentEffects = {{}};
            
            function loadVideoFile(event) {{
                const file = event.target.files[0];
                if (!file) return;
                
                videoFile = file;
                
                const url = URL.createObjectURL(file);
                videoPlayer.src = url;
                
                // Show video player, hide placeholder
                document.getElementById('video-placeholder').style.display = 'none';
                videoPlayer.style.display = 'block';
                
                // Enable controls
                document.querySelectorAll('.control-btn').forEach(btn => btn.disabled = false);
                
                // Update file info
                const fileInfo = document.getElementById('file-info');
                fileInfo.textContent = file.name + ' (' + (file.size / 1024 / 1024).toFixed(1) + ' MB)';
                
                // Setup event listeners
                videoPlayer.addEventListener('loadedmetadata', updateTimeDisplay);
                videoPlayer.addEventListener('timeupdate', updateProgress);
            }}
            
            function togglePlay() {{
                const playBtn = document.getElementById('play-btn');
                
                if (isPlaying) {{
                    videoPlayer.pause();
                    playBtn.textContent = '▶ Play';
                    isPlaying = false;
                }} else {{
                    videoPlayer.play();
                    playBtn.textContent = '⏸ Pause';
                    isPlaying = true;
                }}
            }}
            
            function stopVideo() {{
                videoPlayer.pause();
                videoPlayer.currentTime = 0;
                document.getElementById('play-btn').textContent = '▶ Play';
                isPlaying = false;
                updateProgress();
            }}
            
            function rewind() {{
                videoPlayer.currentTime = Math.max(0, videoPlayer.currentTime - 10);
            }}
            
            function fastForward() {{
                videoPlayer.currentTime = Math.min(videoPlayer.duration, videoPlayer.currentTime + 10);
            }}
            
            function seekTo(event) {{
                if (videoPlayer.duration) {{
                    const rect = event.target.getBoundingClientRect();
                    const percent = (event.clientX - rect.left) / rect.width;
                    videoPlayer.currentTime = percent * videoPlayer.duration;
                }}
            }}
            
            function adjustVolume(value) {{
                videoPlayer.volume = value / 100;
                document.getElementById('volume-val').textContent = value + '%';
            }}
            
            function adjustSpeed(value) {{
                videoPlayer.playbackRate = value / 100;
                document.getElementById('speed-val').textContent = (value / 100).toFixed(1) + 'x';
            }}
            
            function adjustBrightness(value) {{
                document.getElementById('brightness-val').textContent = value + '%';
                updateVideoFilters();
            }}
            
            function adjustContrast(value) {{
                document.getElementById('contrast-val').textContent = value + '%';
                updateVideoFilters();
            }}
            
            function adjustSaturation(value) {{
                document.getElementById('saturation-val').textContent = value + '%';
                updateVideoFilters();
            }}
            
            function updateVideoFilters() {{
                const brightness = document.getElementById('brightness').value;
                const contrast = document.getElementById('contrast').value;
                const saturation = document.getElementById('saturation').value;
                
                let filters = 'brightness(' + brightness + '%) contrast(' + contrast + '%) saturate(' + saturation + '%)';
                
                // Add effects
                Object.keys(currentEffects).forEach(effect => {{
                    if (currentEffects[effect]) {{
                        switch(effect) {{
                            case 'grayscale':
                                filters += ' grayscale(100%)';
                                break;
                            case 'sepia':
                                filters += ' sepia(100%)';
                                break;
                            case 'blur':
                                filters += ' blur(2px)';
                                break;
                        }}
                    }}
                }});
                
                videoPlayer.style.filter = filters;
            }}
            
            function applyEffect(effect) {{
                currentEffects[effect] = !currentEffects[effect];
                updateVideoFilters();
            }}
            
            function resetEffects() {{
                currentEffects = {{}};
                document.getElementById('brightness').value = 100;
                document.getElementById('contrast').value = 100;
                document.getElementById('saturation').value = 100;
                document.getElementById('brightness-val').textContent = '100%';
                document.getElementById('contrast-val').textContent = '100%';
                document.getElementById('saturation-val').textContent = '100%';
                updateVideoFilters();
            }}
            
            function updateProgress() {{
                if (videoPlayer.duration) {{
                    const percent = (videoPlayer.currentTime / videoPlayer.duration) * 100;
                    document.getElementById('timeline-progress').style.width = percent + '%';
                    
                    document.getElementById('current-time').textContent = formatTime(videoPlayer.currentTime);
                    document.getElementById('total-time').textContent = formatTime(videoPlayer.duration);
                }}
            }}
            
            function updateTimeDisplay() {{
                if (videoPlayer.duration) {{
                    document.getElementById('total-time').textContent = formatTime(videoPlayer.duration);
                }}
            }}
            
            function formatTime(seconds) {{
                const mins = Math.floor(seconds / 60);
                const secs = Math.floor(seconds % 60);
                return mins + ':' + (secs < 10 ? '0' : '') + secs;
            }}
            
            function saveChanges() {{
                const settings = {{
                    title: "Theta Video Settings",
                    video: {{
                        filename: videoFile ? videoFile.name : "No file loaded",
                        volume: document.getElementById('volume').value,
                        speed: document.getElementById('speed').value,
                        brightness: document.getElementById('brightness').value,
                        contrast: document.getElementById('contrast').value,
                        saturation: document.getElementById('saturation').value,
                        effects: currentEffects
                    }},
                    saved: new Date().toISOString(),
                    version: "1.0.0"
                }};
                
                const jsonContent = JSON.stringify(settings, null, 2);
                const blob = new Blob([jsonContent], {{ type: 'application/json' }});
                
                // Create download link
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `video-settings_${{new Date().toISOString().slice(0,19).replace(/:/g,'-')}}.json`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
                
                alert('Video settings downloaded successfully!');
            }}
            
            // Video ended event
            videoPlayer.addEventListener('ended', () => {{
                document.getElementById('play-btn').textContent = '▶ Play';
                isPlaying = false;
            }});
        </script>
    </body>
    </html>
    """
    
    component_value = components.html(
        component_html,
        width=width + 50,
        height=height + 50
    )
    
    # Component doesn't return data due to Streamlit version compatibility
    return None 