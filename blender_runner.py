import subprocess
import os
from pathlib import Path
from config import BLENDER_EXECUTABLE, OUTPUT_DIR, SCRIPTS_DIR

class BlenderRunner:
    """
    Executes Blender in headless background mode to run Python animation scripts and render output.
    """
    def __init__(self, blender_path: str = None):
        self.blender_path = blender_path or BLENDER_EXECUTABLE

    def run_script(self, script_content: str, script_name: str = "anim_script.py") -> Path:
        """
        Saves the python script to the scripts directory and executes it via Blender headless.
        """
        script_path = SCRIPTS_DIR / script_name
        script_path.write_text(script_content, encoding="utf-8")

        print(f"[*] Running Blender script: {script_path}")
        print(f"[*] Using Blender executable: {self.blender_path}")

        # Blender command line for background execution with python script
        # Format: blender --background --python script.py
        cmd = [
            str(self.blender_path),
            "--background",
            "--python",
            str(script_path)
        ]

        try:
            result = subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace"
            )
            print("[+] Blender execution completed successfully.")
            return script_path
        except subprocess.CalledProcessError as e:
            print("[-] Error executing Blender:")
            print(e.stdout)
            raise RuntimeError(f"Blender process failed with exit code {e.returncode}")
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Blender executable not found at '{self.blender_path}'. "
                "Please install Blender or set the BLENDER_PATH environment variable."
            )
