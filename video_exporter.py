import subprocess
from pathlib import Path

class VideoExporter:
    """
    Handles FFmpeg-based assembly of rendered frame sequences into final production MP4 files.
    """
    def __init__(self):
        pass

    def assemble_frames_to_video(
        self,
        frames_dir: Path,
        output_video_path: Path,
        fps: int = 30,
        pattern: str = "frame_%04d.png"
    ) -> Path:
        """
        Assembles a sequence of rendered PNG frames into an H.264 MP4 video using FFmpeg.
        """
        input_pattern = str(frames_dir / pattern)
        print(f"[*] Assembling frames from {input_pattern} at {fps} fps into {output_video_path}...")

        cmd = [
            "ffmpeg",
            "-y",
            "-framerate", str(fps),
            "-i", input_pattern,
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-crf", "18",
            "-preset", "slow",
            str(output_video_path)
        ]

        try:
            subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace"
            )
            print(f"[+] Video assembled successfully: {output_video_path}")
            return output_video_path
        except subprocess.CalledProcessError as e:
            print("[-] FFmpeg execution failed:")
            print(e.stdout)
            raise RuntimeError(f"FFmpeg failed with exit code {e.returncode}")
        except FileNotFoundError:
            raise FileNotFoundError(
                "FFmpeg executable not found in PATH. Please install FFmpeg to export final MP4 videos."
            )
