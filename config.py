import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Project Directories
ROOT_DIR = Path(__file__).parent.absolute()
OUTPUT_DIR = ROOT_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

SCRIPTS_DIR = ROOT_DIR / "generated_scripts"
SCRIPTS_DIR.mkdir(exist_ok=True, parents=True)

# Blender Configuration
def find_blender():
    env_path = os.environ.get("BLENDER_PATH")
    if env_path and Path(env_path).exists():
        return env_path

    common_paths = [
        r"C:\Program Files\Blender Foundation\Blender 4.3\blender.exe",
        r"C:\Program Files\Blender Foundation\Blender 4.2\blender.exe",
        r"C:\Program Files\Blender Foundation\Blender 4.1\blender.exe",
        r"C:\Program Files\Blender Foundation\Blender 4.0\blender.exe",
        r"C:\Program Files\Blender Foundation\Blender 3.6\blender.exe",
        "/Applications/Blender.app/Contents/MacOS/Blender",
        "/usr/bin/blender",
        "/usr/local/bin/blender"
    ]
    for p in common_paths:
        if Path(p).exists():
            return p
    return "blender"

BLENDER_EXECUTABLE = find_blender()

# Gemini AI Configuration
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")

# Render Defaults
DEFAULT_WIDTH = 1920
DEFAULT_HEIGHT = 1080
DEFAULT_FPS = 30
DEFAULT_DURATION_SECONDS = 5
