import time
from pathlib import Path
from config import OUTPUT_DIR, DEFAULT_WIDTH, DEFAULT_HEIGHT, DEFAULT_FPS, DEFAULT_DURATION_SECONDS
from gemini_animator import GeminiAnimator
from blender_runner import BlenderRunner
from audio_engine import AudioEngine
from video_exporter import VideoExporter

class MotionGraphicsPipeline:
    """
    Orchestrates the full Create -> Render -> Add Sound -> Export journey.
    """
    def __init__(self, api_key: str = None, blender_path: str = None):
        self.animator = GeminiAnimator(api_key=api_key)
        self.blender_runner = BlenderRunner(blender_path=blender_path)
        self.audio_engine = AudioEngine(OUTPUT_DIR)
        self.video_exporter = VideoExporter()

    def run(
        self,
        prompt: str,
        output_name: str = "motion_graphic",
        duration: int = DEFAULT_DURATION_SECONDS,
        fps: int = DEFAULT_FPS,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
        add_audio: bool = True
    ) -> Path:
        print("==================================================")
        print("🚀 STARTING GEMINI + BLENDER 3D MOTION GRAPHICS")
        print("==================================================")
        print(f"[*] Prompt: {prompt}")
        print(f"[*] Duration: {duration}s | FPS: {fps} | Resolution: {width}x{height}")

        timestamp = int(time.time())
        frames_dir = OUTPUT_DIR / f"{output_name}_{timestamp}_frames"
        frames_dir.mkdir(exist_ok=True, parents=True)

        raw_video_path = OUTPUT_DIR / f"{output_name}_{timestamp}_raw.mp4"
        soundtrack_path = OUTPUT_DIR / f"{output_name}_{timestamp}_audio.wav"
        final_output_path = OUTPUT_DIR / f"{output_name}_{timestamp}.mp4"

        # Step 1: CREATE (Gemini generates Blender bpy script)
        print("\n--- STEP 1: CREATE (Gemini AI Script Generation) ---")
        # Enhance prompt to instruct outputting frame render settings
        enhanced_prompt = (
            f"{prompt}\n"
            f"Render settings: Set scene render resolution_x = {width}, resolution_y = {height}, "
            f"render.fps = {fps}, frame_start = 1, frame_end = {duration * fps}, "
            f"render.filepath = r'{frames_dir.absolute()}/frame_'."
        )
        script_code = self.animator.generate_animation_script(
            prompt=enhanced_prompt,
            duration_seconds=duration,
            fps=fps
        )
        print("[+] Gemini script generated successfully.")

        # Step 2: RENDER (Blender Headless Execution)
        print("\n--- STEP 2: RENDER (Blender Headless Execution) ---")
        script_filename = f"{output_name}_{timestamp}.py"
        self.blender_runner.run_script(script_code, script_name=script_filename)

        # Check if frames were rendered
        rendered_frames = list(frames_dir.glob("*.png"))
        if not rendered_frames:
            # If the script rendered a video directly or didn't output PNG sequence, check for video output or raise error
            raise RuntimeError(f"No frames rendered in {frames_dir}. Ensure the Blender script configured render output correctly.")

        print(f"[+] Rendered {len(rendered_frames)} frames.")

        # Step 3: ADD SOUND (Audio Generation & Mixing)
        print("\n--- STEP 3: ADD SOUND (Audio Engine) ---")
        if add_audio:
            self.audio_engine.create_ambient_soundtrack(
                duration_seconds=duration,
                output_filename=soundtrack_path.name
            )

        # Assemble raw video from frames first
        temp_video_path = OUTPUT_DIR / f"{output_name}_{timestamp}_temp.mp4"
        self.video_exporter.assemble_frames_to_video(
            frames_dir=frames_dir,
            output_video_path=temp_video_path,
            fps=fps,
            pattern="*.png" # or frame_*.png depending on blender output naming
        )

        # Mix audio if enabled
        if add_audio and soundtrack_path.exists():
            self.audio_engine.mix_video_with_audio = self.audio_engine.mix_audio(
                video_path=temp_video_path,
                audio_path=soundtrack_path,
                output_path=final_output_path
            )
            # Cleanup temp raw video
            if temp_video_path.exists():
                temp_video_path.unlink()
        else:
            temp_video_path.rename(final_output_path)

        print("\n==================================================")
        print(f"✨ SUCCESS! Final MP4 Exported to: {final_output_path}")
        print("==================================================")
        return final_output_path
