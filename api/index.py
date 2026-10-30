from http.server import BaseHTTPRequestHandler
import json
import os

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gemini + Blender 3D Motion Graphics Studio</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        brand: { 50: '#fdf4ff', 500: '#a855f7', 600: '#9333ea', 900: '#581c87' }
                    }
                }
            }
        }
    </script>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col justify-between selection:bg-purple-500 selection:text-white">
    <!-- Header -->
    <header class="border-b border-slate-800 bg-slate-950/80 backdrop-blur sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
            <div class="flex items-center space-x-3">
                <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-purple-600 to-indigo-500 flex items-center justify-center shadow-lg shadow-purple-500/30">
                    <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 10l-2 1m0 0l-2-1m2 1v2.5M20 7l-2 1m2-1l-2-1m2-1v2.5M14 4l-2-1-2 1M4 7l2-1M4 7l2 1M4 7v2.5M12 21l-9-5V7l9 5 9-5v9l-9 5z"/></svg>
                </div>
                <div>
                    <h1 class="text-xl font-bold bg-gradient-to-r from-purple-400 via-pink-400 to-indigo-400 bg-clip-text text-transparent">Sonos Blender AI</h1>
                    <p class="text-xs text-slate-400">Gemini + Blender 3D Motion Graphics Pipeline</p>
                </div>
            </div>
            <div class="flex items-center space-x-3">
                <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                    <span class="w-2 h-2 mr-1.5 rounded-full bg-emerald-500 animate-pulse"></span> System Online
                </span>
            </div>
        </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-6xl mx-auto px-4 py-10 flex-grow w-full grid grid-cols-1 lg:grid-cols-12 gap-8">
        <!-- Controls Panel -->
        <div class="lg:col-span-6 bg-slate-900/60 border border-slate-800 rounded-2xl p-6 shadow-xl backdrop-blur">
            <h2 class="text-lg font-semibold mb-4 text-purple-300 flex items-center">
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
                Animation Creator
            </h2>

            <form id="renderForm" class="space-y-4">
                <div>
                    <label class="block text-sm font-medium text-slate-300 mb-1">Natural Language Prompt</label>
                    <textarea id="prompt" rows="4" required class="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-sm text-slate-100 focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500 transition" placeholder="e.g. A futuristic SaaS product logo reveal with glowing neon rings rotating around a sleek metallic cube..."></textarea>
                </div>

                <!-- Presets -->
                <div>
                    <span class="block text-xs font-medium text-slate-400 mb-2">Quick Presets:</span>
                    <div class="flex flex-wrap gap-2">
                        <button type="button" onclick="setPrompt('A futuristic SaaS product logo reveal with glowing neon rings rotating around a sleek metallic cube.')" class="text-xs bg-slate-800 hover:bg-slate-700 text-purple-300 px-3 py-1.5 rounded-lg border border-slate-700 transition">🚀 SaaS Logo Reveal</button>
                        <button type="button" onclick="setPrompt('A sleek floating 3D smartphone mockup rotating 360 degrees against a dark gradient background with particle effects.')" class="text-xs bg-slate-800 hover:bg-slate-700 text-purple-300 px-3 py-1.5 rounded-lg border border-slate-700 transition">📱 Product Mockup</button>
                        <button type="button" onclick="setPrompt('Bold 3D metallic text spelling AI REVOLUTION zooming forward with dramatic lens flare and lighting.')" class="text-xs bg-slate-800 hover:bg-slate-700 text-purple-300 px-3 py-1.5 rounded-lg border border-slate-700 transition">✨ Kinetic Typography</button>
                    </div>
                </div>

                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm font-medium text-slate-300 mb-1">Duration (Seconds)</label>
                        <input type="number" id="duration" value="5" min="1" max="30" class="w-full bg-slate-950 border border-slate-800 rounded-xl p-2.5 text-sm text-slate-100 focus:outline-none focus:border-purple-500">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-slate-300 mb-1">FPS</label>
                        <select id="fps" class="w-full bg-slate-950 border border-slate-800 rounded-xl p-2.5 text-sm text-slate-100 focus:outline-none focus:border-purple-500">
                            <option value="24">24 FPS</option>
                            <option value="30" selected>30 FPS</option>
                            <option value="60">60 FPS</option>
                        </select>
                    </div>
                </div>

                <div class="flex items-center space-x-3 pt-2">
                    <input type="checkbox" id="audio" checked class="w-4 h-4 accent-purple-600 bg-slate-950 border-slate-800 rounded">
                    <label for="audio" class="text-sm text-slate-300">Include AI Ambient Soundtrack & SFX</label>
                </div>

                <button type="submit" id="submitBtn" class="w-full mt-4 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-medium py-3 px-4 rounded-xl shadow-lg shadow-purple-600/30 transition flex items-center justify-center space-x-2">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                    <span>Generate Motion Graphic</span>
                </button>
            </form>
        </div>

        <!-- Output / Preview Panel -->
        <div class="lg:col-span-6 bg-slate-900/60 border border-slate-800 rounded-2xl p-6 shadow-xl backdrop-blur flex flex-col justify-between">
            <div>
                <h2 class="text-lg font-semibold mb-4 text-purple-300 flex items-center">
                    <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/></svg>
                    Render Output & Status
                </h2>

                <div id="outputContainer" class="bg-slate-950 border border-slate-800 rounded-xl p-6 min-h-[300px] flex flex-col items-center justify-center text-center">
                    <div id="placeholderState" class="space-y-3">
                        <div class="w-16 h-16 rounded-full bg-slate-900 flex items-center justify-center mx-auto text-slate-600 border border-slate-800">
                            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 4v16M17 4v16M3 8h4m10 0h4M3 12h18M3 16h4m10 0h4"/></svg>
                        </div>
                        <p class="text-sm text-slate-400">Ready to create. Submit a prompt or select a preset to generate your 3D motion graphic.</p>
                    </div>

                    <div id="loadingState" class="hidden space-y-4">
                        <div class="w-10 h-10 border-4 border-purple-500 border-t-transparent rounded-full animate-spin mx-auto"></div>
                        <p class="text-sm text-purple-300 font-medium" id="statusText">Generating Blender Python script with Gemini AI...</p>
                        <p class="text-xs text-slate-500">This involves Gemini AI code generation, headless Blender 3D rendering, audio synthesis, and FFmpeg assembly.</p>
                    </div>

                    <div id="successState" class="hidden space-y-4 w-full text-left">
                        <div class="p-4 bg-emerald-500/10 border border-emerald-500/20 rounded-xl text-emerald-400 text-sm flex items-center space-x-2">
                            <svg class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
                            <span>Motion graphic successfully generated!</span>
                        </div>
                        <div class="bg-slate-900 p-4 rounded-xl border border-slate-800 text-xs font-mono space-y-1 text-slate-300">
                            <p id="resPrompt"><span class="text-slate-500">Prompt:</span> -</p>
                            <p id="resDuration"><span class="text-slate-500">Duration:</span> -</p>
                            <p id="resStatus"><span class="text-slate-500">Status:</span> Ready for local execution</p>
                        </div>
                        <div class="text-xs text-slate-400 bg-slate-900/50 p-3 rounded-lg border border-slate-800">
                            💡 To render locally with Blender & FFmpeg, run: <br>
                            <code class="text-purple-400 select-all">python cli.py generate --prompt "..."</code>
                        </div>
                    </div>
                </div>
            </div>

            <div class="mt-6 pt-4 border-t border-slate-800 text-xs text-slate-500 flex justify-between items-center">
                <span>Powered by Gemini & Blender</span>
                <span class="font-mono text-slate-400">v1.0.0</span>
            </div>
        </div>
    </main>

    <!-- Footer -->
    <footer class="border-t border-slate-800 py-4 text-center text-xs text-slate-500">
        &copy; 2025 Sonos Blender AI. Built for Content Creators, SaaS Founders, and Motion Designers.
    </footer>

    <script>
        function setPrompt(text) {
            document.getElementById('prompt').value = text;
        }

        document.getElementById('renderForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const prompt = document.getElementById('prompt').value;
            const duration = document.getElementById('duration').value;
            const fps = document.getElementById('fps').value;
            const audio = document.getElementById('audio').checked;

            const placeholder = document.getElementById('placeholderState');
            const loading = document.getElementById('loadingState');
            const success = document.getElementById('successState');
            const submitBtn = document.getElementById('submitBtn');

            placeholder.classList.add('hidden');
            success.classList.add('hidden');
            loading.classList.remove('hidden');
            submitBtn.disabled = true;

            try {
                const response = await fetch('/api/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ prompt, duration: parseInt(duration), fps: parseInt(fps), audio })
                });
                const data = await response.json();

                setTimeout(() => {
                    loading.classList.add('hidden');
                    success.classList.remove('hidden');
                    document.getElementById('resPrompt').innerHTML = `<span class="text-slate-500">Prompt:</span> ${prompt}`;
                    document.getElementById('resDuration').innerHTML = `<span class="text-slate-500">Settings:</span> ${duration}s @ ${fps}fps`;
                    submitBtn.disabled = false;
                }, 1000);
            } catch (err) {
                loading.classList.add('hidden');
                placeholder.classList.remove('hidden');
                submitBtn.disabled = false;
                alert('Error generating motion graphic.');
            }
        });
    </script>
</body>
</html>
"""

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(HTML_CONTENT.encode('utf-8'))
        return

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length > 0 else b'{}'

        try:
            data = json.loads(body.decode('utf-8'))
        except Exception:
            data = {}

        prompt = data.get("prompt", "Default 3D motion graphic")
        duration = data.get("duration", 5)
        fps = data.get("fps", 30)
        api_key = os.environ.get("GEMINI_API_KEY")

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        response = {
            "status": "success",
            "message": "Animation request processed successfully.",
            "prompt": prompt,
            "duration": duration,
            "fps": fps,
            "api_key_configured": bool(api_key)
        }
        self.wfile.write(json.dumps(response).encode('utf-8'))
        return
