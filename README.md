# 🎬 3D Motion Graphics with Gemini + Blender

Stop spending hours manually animating every frame. This tool provides a complete, code-driven 3D animation workflow powered by:

- 🤖 **Gemini AI** (Natural language prompt to Blender Python script generation)
- 🧊 **Blender** (Headless 3D rendering engine)
- 🐍 **Python** (Automation pipeline orchestration)
- 🎵 **Sound & SFX** (Ambient soundtrack generation and synchronization)
- 🎬 **FFmpeg** (Production-ready MP4 video export)

---

## 🚀 Target Audience
- 📣 **Content Creators & Marketers**: Instantly generate eye-catching social media animations, product teasers, and promo videos.
- 🚀 **SaaS Founders & Startups**: Create sleek 3D logo reveals and feature callout animations without hiring a motion designer.
- 🎥 **Motion Designers**: Accelerate prototyping by generating base procedural scenes with AI and refining them in Blender.
- ⚙️ **AI & Automation Learners**: Learn how to orchestrate multimodal LLMs, local rendering tools, audio synthesis, and FFmpeg codecs.

---

## 🛠️ Installation & Prerequisites

1. **Python 3.10+** installed.
2. **Blender** installed and added to PATH (or set via `BLENDER_PATH`).
3. **FFmpeg** installed and added to PATH.
4. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Set your Gemini API key:
   ```bash
   export GEMINI_API_KEY="your-api-key-here"
   # On Windows PowerShell:
   # $env:GEMINI_API_KEY="your-api-key-here"
   ```

---

## 🎯 The Main Journey: Create → Render → Add Sound → Export

Run animations directly from the CLI:

```bash
python cli.py generate --prompt "A futuristic SaaS logo reveal with glowing neon rings rotating around a sleek metallic cube with dramatic studio lighting." --output saas_logo_reveal --duration 5
```

### Options:
- `--prompt`, `-p`: Natural language description of your animation.
- `--output`, `-o`: Output filename prefix.
- `--duration`, `-d`: Duration in seconds (default: 5).
- `--fps`: Frames per second (default: 30).
- `--width`: Resolution width (default: 1920).
- `--height`: Resolution height (default: 1080).
- `--audio / --no-audio`: Include or exclude synthesized ambient soundtrack.

---

## 💡 Example Prompt Ideas

1. **SaaS Product Feature Callout**:
   > *"A sleek floating 3D smartphone mockup rotating 360 degrees against a dark gradient background with floating particle effects and glowing cyan accents."*
2. **Kinetic Typography Intro**:
   > *"Bold 3D metallic text spelling 'AI REVOLUTION' zooming forward from deep space with lens flare and camera shake."*
3. **Abstract Geometric Background**:
   > *"An endless grid of glossy black cubes pulsing up and down in wave patterns with warm golden rim lighting."*
