#!/usr/bin/env python3

from http.server import HTTPServer, BaseHTTPRequestHandler

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tentacle Control</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 500px;
            margin: 50px auto;
            padding: 20px;
            background: #1a1a1a;
            color: #fff;
        }
        .control-group {
            margin: 20px 0;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
        }
        select, input[type="range"] {
            width: 100%;
            padding: 8px;
            font-size: 16px;
        }
        select {
            background: #2a2a2a;
            color: #fff;
            border: 1px solid #444;
            border-radius: 4px;
        }
        input[type="range"] {
            height: 40px;
            cursor: pointer;
        }
        .value-display {
            text-align: center;
            font-size: 24px;
            color: #4CAF50;
            margin: 10px 0;
        }
        .status {
            padding: 10px;
            margin-top: 20px;
            border-radius: 4px;
            text-align: center;
        }
        .status.success {
            background: #2d5016;
            color: #8bc34a;
        }
        .status.error {
            background: #5d1a1a;
            color: #f44336;
        }
    </style>
</head>
<body>
    <h1>🐙 Tentacle Control</h1>

    <div class="control-group">
        <label for="tentacle">Select Tentacle:</label>
        <select id="tentacle">
            <option value="0">Tentacle 0</option>
            <option value="1">Tentacle 1</option>
            <option value="2">Tentacle 2</option>
            <option value="3">Tentacle 3</option>
            <option value="4">Tentacle 4</option>
            <option value="5">Tentacle 5</option>
            <option value="6">Tentacle 6</option>
            <option value="7">Tentacle 7</option>
        </select>
    </div>

    <div class="control-group">
        <label for="height">Height:</label>
        <input type="range" id="height" min="0" max="1" step="0.01" value="0.5">
        <div class="value-display" id="heightValue">0.50</div>
    </div>

    <div id="status"></div>

    <script>
        const tentacleSelect = document.getElementById('tentacle');
        const heightSlider = document.getElementById('height');
        const heightValue = document.getElementById('heightValue');
        const statusDiv = document.getElementById('status');

        function updateHeightDisplay() {
            heightValue.textContent = parseFloat(heightSlider.value).toFixed(2);
        }

        async function sendControl() {
            const data = {
                tentacle: parseInt(tentacleSelect.value),
                height: parseFloat(heightSlider.value)
            };

            try {
                const response = await fetch('http://10.100.2.218:5000/arm', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });

                const result = await response.json();

                if (response.ok) {
                    statusDiv.className = 'status success';
                    statusDiv.textContent = `✓ Sent: Tentacle ${data.tentacle} → ${data.height.toFixed(2)}`;
                } else {
                    statusDiv.className = 'status error';
                    statusDiv.textContent = `✗ Error: ${result.message || 'Unknown error'}`;
                }
            } catch (error) {
                statusDiv.className = 'status error';
                statusDiv.textContent = `✗ Connection error: ${error.message}`;
            }
        }

        // Update display and send on slider change
        heightSlider.addEventListener('input', () => {
            updateHeightDisplay();
            sendControl();
        });

        // Initial display
        updateHeightDisplay();
    </script>
</body>
</html>
"""

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(HTML_PAGE.encode())

    def log_message(self, format, *args):
        # Custom log format
        print(f"[Web Server] {args[0]}")

if __name__ == '__main__':
    PORT = 8080
    server = HTTPServer(('0.0.0.0', PORT), RequestHandler)
    print("=" * 60)
    print("🐙 Tentacle Control Interface")
    print("=" * 60)
    print(f"Server running at: http://localhost:{PORT}")
    print("Make sure direct_control_main.py is running on port 5000")
    print("=" * 60)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\nShutting down server...")
        server.shutdown()
