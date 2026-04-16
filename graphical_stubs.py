"""
Graphical stub controllers for testing the octopus reactions without hardware.
Uses a local web server to visualize the eyes and arms in a browser.
"""

import threading
import http.server
import socketserver
import json
import base64
from io import BytesIO
from PIL import Image
import webbrowser
import time


class WebVisualizationServer:
    """Singleton web server for graphical test mode."""

    _instance = None
    _PORT = 8765

    def __init__(self):
        if WebVisualizationServer._instance is not None:
            raise RuntimeError("Use get_instance() instead")

        # Shared state for visualization
        self.left_eye_data = None
        self.right_eye_data = None
        self.left_arm_pos = 0.5
        self.right_arm_pos = 0.5
        self.lock = threading.Lock()

        # Start the web server in a background thread
        self.server_thread = threading.Thread(target=self._run_server, daemon=True)
        self.server_thread.start()

        # Give server time to start
        time.sleep(0.5)

        # Open browser
        print(f"Opening visualization at http://localhost:{self._PORT}")
        webbrowser.open(f"http://localhost:{self._PORT}")

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = WebVisualizationServer()
        return cls._instance

    def _run_server(self):
        """Run the HTTP server."""
        handler = self._make_handler()
        with socketserver.TCPServer(("", self._PORT), handler) as httpd:
            print(f"Web server running on http://localhost:{self._PORT}")
            httpd.serve_forever()

    def _make_handler(self):
        """Create a request handler with access to this instance."""
        server_instance = self

        class VisualizationHandler(http.server.SimpleHTTPRequestHandler):
            def log_message(self, format, *args):
                """Suppress server logs."""
                pass

            def do_GET(self):
                if self.path == "/" or self.path == "/index.html":
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(server_instance._get_html().encode())

                elif self.path == "/state":
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.send_header("Cache-Control", "no-cache")
                    self.end_headers()

                    with server_instance.lock:
                        state = {
                            "left_eye": server_instance.left_eye_data,
                            "right_eye": server_instance.right_eye_data,
                            "left_arm": server_instance.left_arm_pos,
                            "right_arm": server_instance.right_arm_pos,
                        }
                    self.wfile.write(json.dumps(state).encode())

                else:
                    self.send_error(404)

        return VisualizationHandler

    def update_eye(self, is_left, pil_image):
        """Update eye image."""
        # Convert PIL image to base64 data URL
        if pil_image.mode != 'RGB':
            pil_image = pil_image.convert('RGB')

        # Resize if needed
        if pil_image.size != (240, 240):
            pil_image = pil_image.resize((240, 240), Image.LANCZOS)

        # Convert to base64
        buffer = BytesIO()
        pil_image.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        data_url = f"data:image/png;base64,{img_str}"

        with self.lock:
            if is_left:
                self.left_eye_data = data_url
            else:
                self.right_eye_data = data_url

    def update_arm(self, is_left, position):
        """Update arm position."""
        with self.lock:
            if is_left:
                self.left_arm_pos = position
            else:
                self.right_arm_pos = position

    def _get_html(self):
        """Generate the HTML page."""
        return """<!DOCTYPE html>
<html>
<head>
    <title>Abbott the Octopus - Test Mode</title>
    <style>
        body {
            margin: 0;
            padding: 20px;
            background: #1e1e1e;
            color: #c8c8c8;
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        h1 {
            margin-bottom: 30px;
        }
        .container {
            display: flex;
            gap: 100px;
            align-items: flex-start;
        }
        .eye-section {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .eye-label {
            margin-bottom: 10px;
            font-size: 14px;
        }
        .eye-display {
            width: 240px;
            height: 240px;
            border: 3px solid #646464;
            background: black;
            position: relative;
        }
        .eye-display img {
            width: 100%;
            height: 100%;
            object-fit: contain;
        }
        .arm-display {
            margin-top: 20px;
            text-align: center;
        }
        .arm-label {
            font-size: 12px;
            margin-bottom: 5px;
        }
        .arm-bar {
            width: 240px;
            height: 30px;
            background: #3c3c3c;
            border-radius: 15px;
            position: relative;
            overflow: hidden;
        }
        .arm-fill {
            height: 100%;
            background: linear-gradient(90deg, #64c8ff, #4dabeb);
            transition: width 0.1s ease-out;
            border-radius: 15px;
        }
        .arm-value {
            font-size: 11px;
            margin-top: 5px;
            color: #64c8ff;
        }
        canvas {
            position: absolute;
            top: 0;
            left: 0;
        }
    </style>
</head>
<body>
    <h1>Abbott the Octopus - Test Mode</h1>
    <div class="container">
        <div class="eye-section">
            <div class="eye-label">Left Eye</div>
            <div class="eye-display">
                <img id="left-eye" src="" alt="Left eye">
            </div>
            <div class="arm-display">
                <div class="arm-label">Left Arm</div>
                <div class="arm-bar">
                    <div class="arm-fill" id="left-arm-fill"></div>
                </div>
                <div class="arm-value" id="left-arm-value">0.50</div>
            </div>
        </div>

        <div class="eye-section">
            <div class="eye-label">Right Eye</div>
            <div class="eye-display">
                <img id="right-eye" src="" alt="Right eye">
            </div>
            <div class="arm-display">
                <div class="arm-label">Right Arm</div>
                <div class="arm-bar">
                    <div class="arm-fill" id="right-arm-fill"></div>
                </div>
                <div class="arm-value" id="right-arm-value">0.50</div>
            </div>
        </div>
    </div>

    <script>
        const leftEye = document.getElementById('left-eye');
        const rightEye = document.getElementById('right-eye');
        const leftArmFill = document.getElementById('left-arm-fill');
        const rightArmFill = document.getElementById('right-arm-fill');
        const leftArmValue = document.getElementById('left-arm-value');
        const rightArmValue = document.getElementById('right-arm-value');

        function updateVisualization() {
            fetch('/state')
                .then(response => response.json())
                .then(data => {
                    // Update eyes
                    if (data.left_eye) {
                        leftEye.src = data.left_eye;
                    }
                    if (data.right_eye) {
                        rightEye.src = data.right_eye;
                    }

                    // Update arms
                    const leftArmPercent = (data.left_arm * 100).toFixed(0);
                    const rightArmPercent = (data.right_arm * 100).toFixed(0);

                    leftArmFill.style.width = leftArmPercent + '%';
                    rightArmFill.style.width = rightArmPercent + '%';

                    leftArmValue.textContent = data.left_arm.toFixed(2);
                    rightArmValue.textContent = data.right_arm.toFixed(2);
                })
                .catch(err => console.error('Update failed:', err));
        }

        // Poll for updates every 50ms
        setInterval(updateVisualization, 50);

        // Initial update
        updateVisualization();
    </script>
</body>
</html>"""


class GraphicalStubDisplay:
    """Stub display that updates the web visualization."""

    def __init__(self, is_left):
        self.is_left = is_left
        self.server = WebVisualizationServer.get_instance()

    def image(self, img, offset_x=0, offset_y=0):
        """Display a PIL Image in the web visualization."""
        self.server.update_eye(self.is_left, img)

    def fill(self, color=0):
        """Fill the display with a color."""
        if isinstance(color, tuple):
            r, g, b = color
        else:
            # Convert RGB565 to RGB
            r = (color >> 11) & 0x1F
            g = (color >> 5) & 0x3F
            b = color & 0x1F
            r = (r << 3) | (r >> 2)
            g = (g << 2) | (g >> 4)
            b = (b << 3) | (b >> 2)

        # Create a solid color image
        img = Image.new('RGB', (240, 240), (r, g, b))
        self.server.update_eye(self.is_left, img)

    def close(self):
        """Clean up resources."""
        pass


class GraphicalStubArmController:
    """Stub arm controller that updates the web visualization."""

    def __init__(self, is_left):
        self.is_left = is_left
        self.server = WebVisualizationServer.get_instance()
        self.current_pos = 0.5

    def set_pos(self, pos: float):
        """Set arm position (0.0 to 1.0)."""
        self.current_pos = pos
        self.server.update_arm(self.is_left, pos)


def make_graphical_displays():
    """Create graphical stub displays for testing."""
    return GraphicalStubDisplay(True), GraphicalStubDisplay(False)


def make_graphical_arm_controllers():
    """Create graphical stub arm controllers for testing."""
    return [GraphicalStubArmController(True), GraphicalStubArmController(False)]
