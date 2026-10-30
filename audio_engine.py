import wave
import struct
import math
from pathlib import Path

class AudioEngine:
    """
    Manages background audio generation, sound effects, and timing synchronization for 3D animations
    using pure Python (wave, struct, math) to ensure full compatibility across Python 3.10 to 3.14+.
    """
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir

    def create_ambient_soundtrack(self, duration_seconds: int = 5, output_filename: str = "soundtrack.wav", sample_rate: int = 44100) -> Path:
        """
        Generates a cinematic ambient synth chord (.wav) using pure Python wave generation.
        """
        output_path = self.output_dir / output_filename
        num_samples = duration_seconds * sample_rate

        # Frequencies for a pleasant ambient synth chord (C3 = 130.81 Hz, G3 = 196.00 Hz, C4 = 261.63 Hz)
        freqs = [130.81, 196.00, 261.63]

        with wave.open(str(output_path), 'w') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit PCM
            wav_file.setframerate(sample_rate)

            for i in range(num_samples):
                t = i / sample_rate
                # Envelope: smooth fade in (0.2s) and fade out (0.3s)
                envelope = 1.0
                if t < 0.2:
                    envelope = t / 0.2
                elif t > duration_seconds - 0.3:
                    envelope = max(0.0, (duration_seconds - t) / 0.3)

                # Combine sine waves
                val = 0.0
                for idx, f in enumerate(freqs):
                    amp = 9000.0 / (idx + 1)
                    val += amp * math.sin(2.0 * math.pi * f * t)

                val = int(val * envelope)
                val = max(-32768, min(32767, val))

                wav_file.writeframes(struct.pack('<h', val))

        print(f"[+] Ambient soundtrack generated: {output_path}")
        return output_path

    def mix_audio(self, video_path: Path, audio_path: Path, output_path: Path) -> Path:
        """
        Mixes audio track into video using moviepy.
        """
        from moviepy.editor import VideoFileClip, AudioFileClip

        print(f"[*] Mixing audio {audio_path} with video {video_path}...")
        video_clip = VideoFileClip(str(video_path))
        audio_clip = AudioFileClip(str(audio_path))

        if audio_clip.duration > video_clip.duration:
            audio_clip = audio_clip.subclip(0, video_clip.duration)

        final_clip = video_clip.set_audio(audio_clip)
        final_clip.write_videofile(
            str(output_path),
            codec="libx264",
            audio_codec="aac",
            fps=video_clip.fps,
            preset="medium",
            logger=None
        )

        video_clip.close()
        audio_clip.close()
        final_clip.close()

        print(f"[+] Mixed video saved to: {output_path}")
        return output_path
