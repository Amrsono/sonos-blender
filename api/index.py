from http.server import BaseHTTPRequestHandler
import json
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        response = {
            "status": "online",
            "service": "Gemini + Blender 3D Motion Graphics Pipeline",
            "version": "1.0.0",
            "endpoints": {
                "GET /": "API status and info",
                "POST /api/generate": "Trigger animation generation request"
            },
            "note": "Full 3D rendering (Blender + FFmpeg) runs locally via python cli.py generate."
        }
        self.wfile.write(json.dumps(response).encode('utf-8'))
        return

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rhi.read(content_length) if hasattr(self, 'rhi') else self.rfile.read(content_length)

        try:
            data = json.loads(body.decode('utf-8')) if body else {}
        except Exception:
            data = {}

        prompt = data.get("prompt", "Default 3D motion graphic")
        api_key = os.environ.get("GEMINI_API_KEY")

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        response = {
            "status": "success",
            "message": "Animation request received.",
            "prompt": prompt,
            "api_key_configured": bool(api_key),
            "note": "Blender rendering runs locally."
        }
        self.wfile.write(json.dumps(response).encode('utf-8'))
        return
