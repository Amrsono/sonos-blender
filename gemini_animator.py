import os
import re
from google import genai
from google.genai import types
from config import GEMINI_MODEL

class GeminiAnimator:
    """
    Generates Blender Python (bpy) scripts from natural language prompts using Gemini.
    """
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key not found. Please set GEMINI_API_KEY environment variable.")

        self.client = genai.Client(api_key=self.api_key)

    def generate_animation_script(self, prompt: str, duration_seconds: int = 5, fps: int = 30) -> str:
        """
        Sends a prompt to Gemini requesting a complete Blender Python script (`bpy`).
        """
        system_instruction = (
            "You are an expert Blender Python (bpy) automation engineer and 3D motion designer. "
            "Your task is to generate complete, executable Python code for Blender that creates a stunning 3D motion graphic animation. "
            "Rules:\n"
            "1. Output ONLY valid Python code inside a ```python markdown code block, with no other conversational text.\n"
            "2. Use the `bpy` library.\n"
            "3. Clean the scene at the start (remove default cube/light/camera if needed or configure them).\n"
            "4. Create objects (cubes, spheres, text, curves, etc.), materials with Principled BSDF shaders, lighting, and a camera.\n"
            "5. Set up keyframe animation over the specified frame range (e.g., frame 1 to total_frames).\n"
            "6. Configure render settings (resolution 1920x1080, output file path to absolute path or temporary path, Eevee engine).\n"
            "7. Ensure smooth easing, rotation, and scaling keyframes."
        )

        total_frames = duration_seconds * fps
        user_prompt = (
            f"Create a Blender Python script for the following 3D motion graphic animation:\n"
            f"Concept: {prompt}\n"
            f"Duration: {duration_seconds} seconds at {fps} fps ({total_frames} total frames).\n"
            f"Resolution: 1920x1080.\n"
            f"Ensure the script sets up keyframes from frame 1 to {total_frames}."
        )

        response = self.client.models.generate_content(
            model=GEMINI_MODEL,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.4,
            ),
        )

        code_text = response.text
        return self._extract_code(code_text)

    def _extract_code(self, response_text: str) -> str:
        """
        Extracts Python code from markdown code blocks in the response.
        """
        # Match ```python ... ``` or ``` ... ```
        pattern = r"```(?:python)?\s*(.*?)\s*```"
        matches = re.findall(pattern, response_text, re.DOTALL)
        if matches:
            return matches[0]

        # Fallback: return raw text if no code block found
        return response_text
