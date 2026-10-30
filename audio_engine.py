from pathlib import Path
from pydub import AudioSegment
from pydub.generators import Sine, WhiteNoise

class AudioEngine:
    """
    Manages background audio generation, sound effects, and timing synchronization for 3D animations.
    """
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir

    def create_ambient_soundtrack(self, duration_seconds: int = 5, output_filename: str = "soundtrack.wav") -> Path:
        """
        Generates a sleek, cinematic ambient synth sound/drone or rhythm for the motion graphic.
        """
        duration_ms = duration_seconds * 1000

        # Generate a pleasant chord or drone using Sine waves (e.g., C major / ambient synth)
        # Root note (C3 = 130.81 Hz), fifth (G3 = 196.00 Hz), octave (C4 = 261.63 Hz)
        tone1 = Sine(130.81).to_audio_segment(duration=duration_ms, volume=-15)
        tone2 = Sine(196.00).to_audio_segment(duration=duration_ms, volume=-18)
        tone3 = Sine(261.63).to_audio_segment(duration=duration_ms, volume=-20)

        soundtrack = tone1.overlay(tone2).overlay(tone3)

        # Add a subtle swoosh / rise at the beginning if duration allows
        if duration_seconds >= 2:
            swoosh = WhiteNoise().to_audio_segment(duration=min(1000, duration_ms), volume=-25)
            # Fade in/out the swoosh
            swoosh = swoosh.fade_in(500).fade_out(500)
            soundtrack = soundtrack.overlay(swoosh, position=0)

        # Apply fade in and fade out
        soundtrack = soundtrack.fade_in(200).fade_out(300)

        output_path = self.output_dir / output_filename
        soundtrack.export(str(output_path), format="wav")
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

        # Ensure audio matches video duration
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
