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
        self.arm_positions = { i: 0.5 for i in range(8)}
        self.lock = threading.Lock()

        # Start the web server in a background thread
        self.server_thread = threading.Thread(target=self._run_server, daemon=True)
        self.server_thread.start()

        # Give server time to start
        time.sleep(0.5)

        # Open browser
        print(f"Opening visualization at http://localhost:{self._PORT}")

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = WebVisualizationServer()
        return cls._instance

    def _run_server(self):
        """Run the HTTP server."""
        handler = self._make_handler()

        # Allow reusing the address immediately after shutdown
        socketserver.TCPServer.allow_reuse_address = True

        try:
            with socketserver.TCPServer(("", self._PORT), handler) as httpd:
                httpd.allow_reuse_address = True
                self.httpd = httpd
                print(f"Web server running on http://localhost:{self._PORT}")
                httpd.serve_forever()
        except OSError as e:
            if "Address already in use" in str(e):
                print(f"Port {self._PORT} is already in use. The server may still be running from a previous session.")
                print(f"You can access the visualization at http://localhost:{self._PORT}")
            else:
                raise

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
                        # Swap left/right for stage perspective (stage left = audience right)
                        state = {
                            "left_eye": server_instance.left_eye_data,
                            "right_eye": server_instance.right_eye_data,
                        } | {
                            f"arm_{i}": pos for i, pos in server_instance.arm_positions.items()
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

    def update_arm(self, index, position):
        """Update arm position."""
        with self.lock:
            self.arm_positions[index] = position

    def shutdown(self):
        """Shutdown the server cleanly."""
        if hasattr(self, 'httpd'):
            print("Shutting down web server...")
            self.httpd.shutdown()
            self.httpd.server_close()

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
        .arm-value {
            font-size: 11px;
            margin-top: 5px;
            color: #64c8ff;
        }
        .arms-octagon {
            margin-top: 40px;
            position: relative;
            width: 600px;
            height: 600px;
        }
        .arm-canvas-wrapper {
            position: absolute;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .arm-canvas-wrapper canvas {
            border: 1px solid #646464;
        }
    </style>
</head>
<body>
    <h1>Abbott the Octopus - Test Mode</h1>
    <div class="container">
        <div class="eye-section">
            <div class="eye-label">(House) Left Eye</div>
            <div class="eye-display">
                <img id="left-eye" src="" alt="Left eye">
            </div>
        </div>

        <div class="eye-section">
            <div class="eye-label">(House) Right Eye</div>
            <div class="eye-display">
                <img id="right-eye" src="" alt="Right eye">
            </div>
        </div>
    </div>

    <div class="arms-octagon" id="arms-container">
        <!-- Arms arranged in octagon with point at bottom (Arm 7), going clockwise from Arm 0 -->
        <!-- Arm 0: Bottom-left diagonal -->
        <div class="arm-canvas-wrapper" style="left: 66px; top: 384px;">
            <div class="arm-label">Arm 0</div>
            <canvas id="arm-canvas-0" width="150" height="150"></canvas>
            <div class="arm-value" id="arm-value-0">0.50</div>
        </div>
        <!-- Arm 1: Left side -->
        <div class="arm-canvas-wrapper" style="left: 0px; top: 225px;">
            <div class="arm-label">Arm 1</div>
            <canvas id="arm-canvas-1" width="150" height="150"></canvas>
            <div class="arm-value" id="arm-value-1">0.50</div>
        </div>
        <!-- Arm 2: Top-left diagonal -->
        <div class="arm-canvas-wrapper" style="left: 66px; top: 66px;">
            <div class="arm-label">Arm 2</div>
            <canvas id="arm-canvas-2" width="150" height="150"></canvas>
            <div class="arm-value" id="arm-value-2">0.50</div>
        </div>
        <!-- Arm 3: Top center -->
        <div class="arm-canvas-wrapper" style="left: 225px; top: 0px;">
            <div class="arm-label">Arm 3</div>
            <canvas id="arm-canvas-3" width="150" height="150"></canvas>
            <div class="arm-value" id="arm-value-3">0.50</div>
        </div>
        <!-- Arm 4: Top-right diagonal -->
        <div class="arm-canvas-wrapper" style="left: 384px; top: 66px;">
            <div class="arm-label">Arm 4</div>
            <canvas id="arm-canvas-4" width="150" height="150"></canvas>
            <div class="arm-value" id="arm-value-4">0.50</div>
        </div>
        <!-- Arm 5: Right side -->
        <div class="arm-canvas-wrapper" style="left: 450px; top: 225px;">
            <div class="arm-label">Arm 5</div>
            <canvas id="arm-canvas-5" width="150" height="150"></canvas>
            <div class="arm-value" id="arm-value-5">0.50</div>
        </div>
        <!-- Arm 6: Bottom-right diagonal -->
        <div class="arm-canvas-wrapper" style="left: 384px; top: 384px;">
            <div class="arm-label">Arm 6</div>
            <canvas id="arm-canvas-6" width="150" height="150"></canvas>
            <div class="arm-value" id="arm-value-6">0.50</div>
        </div>
        <!-- Arm 7: Bottom point -->
        <div class="arm-canvas-wrapper" style="left: 225px; top: 450px;">
            <div class="arm-label">Arm 7</div>
            <canvas id="arm-canvas-7" width="150" height="150"></canvas>
            <div class="arm-value" id="arm-value-7">0.50</div>
        </div>
    </div>


    <script>
        const leftEye = document.getElementById('left-eye');
        const rightEye = document.getElementById('right-eye');

        function drawArm(canvas, isLeft, value) {
            const ctx = canvas.getContext("2d");
            // angle in radians * radius = arm length = constant
            const ARM_LENGTH = 60;

            // Arc has zero at X axis, increasing clockwise

            // Lets go a little under 2*pi
            const MAX_ARM_RADS = 5;
            const ARM_OFF_X = 75;
            const ARM_OFF_Y = 75;

            // signed value
            const rads = MAX_ARM_RADS * 2 * (value - 0.5) * (isLeft ? 1 : -1);


            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.strokeStyle = 'white';
            ctx.lineWidth = 4;

            if (Math.abs(rads) < 0.1) {
                ctx.beginPath()
                ctx.moveTo(ARM_OFF_X, ARM_OFF_Y);
                ctx.lineTo(ARM_OFF_X - ARM_LENGTH * (isLeft ? 1 : -1), ARM_OFF_Y);
                ctx.stroke();
            } else {
                // This is signed
                // yes this flips the flip
                const radius = ARM_LENGTH / rads * (isLeft ? 1 : -1);

                ctx.beginPath();
                const middle = radius > 0 ? Math.PI / 2 : -Math.PI / 2;
                const clockwise = rads < 0
                ctx.arc(ARM_OFF_X, ARM_OFF_Y - radius, Math.abs(radius), middle, middle + rads, clockwise);
                ctx.stroke();
            }
        }

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

                    // Update all 8 arms
                    // First 4 arms (0-3) are considered "left" for drawing purposes
                    for (let i = 0; i < 8; i++) {
                        const armData = data[`arm_${i}`];
                        if (armData !== undefined) {
                            const canvas = document.getElementById(`arm-canvas-${i}`);
                            const valueElement = document.getElementById(`arm-value-${i}`);
                            const isLeft = i < 4; // First 4 arms are "left"

                            if (canvas && valueElement) {
                                drawArm(canvas, isLeft, armData);
                                valueElement.textContent = armData.toFixed(2);
                            }
                        }
                    }
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

    def __init__(self, index):
        self.index = index
        self.server = WebVisualizationServer.get_instance()
        self.current_pos = 0.5

    def set_pos(self, pos: float):
        """Set arm position (0.0 to 1.0)."""
        self.current_pos = pos
        self.server.update_arm(self.index, pos)


def make_graphical_displays():
    """Create graphical stub displays for testing."""
    return GraphicalStubDisplay(True), GraphicalStubDisplay(False)


def make_graphical_arm_controllers():
    """Create graphical stub arm controllers for testing."""
    return [GraphicalStubArmController(i) for i in range(8)]
