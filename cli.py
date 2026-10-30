import click
import os
from pipeline import MotionGraphicsPipeline
from config import DEFAULT_DURATION_SECONDS, DEFAULT_FPS, DEFAULT_WIDTH, DEFAULT_HEIGHT

@click.group()
def cli():
    """
    🎬 Gemini + Blender 3D Motion Graphics Pipeline CLI
    Create -> Render -> Add Sound -> Export stunning 3D animations using AI and code.
    """
    pass

@cli.command()
@click.option("--prompt", "-p", required=True, help="Natural language description of the 3D motion graphic animation.")
@click.option("--output", "-o", default="motion_graphic", help="Output filename prefix.")
@click.option("--duration", "-d", default=DEFAULT_DURATION_SECONDS, type=int, help="Duration in seconds.")
@click.option("--fps", default=DEFAULT_FPS, type=int, help="Frames per second.")
@click.option("--width", default=DEFAULT_WIDTH, type=int, help="Video width in pixels.")
@click.option("--height", default=DEFAULT_HEIGHT, type=int, help="Video height in pixels.")
@click.option("--audio/--no-audio", default=True, help="Include AI generated ambient soundtrack.")
@click.option("--api-key", envvar="GEMINI_API_KEY", help="Gemini API Key.")
@click.option("--blender-path", envvar="BLENDER_PATH", help="Path to Blender executable.")
def generate(prompt, output, duration, fps, width, height, audio, api_key, blender_path):
    """
    Generate a 3D motion graphic animation from a natural language prompt.
    """
    if not api_key:
        click.echo("Error: Gemini API key not provided. Set GEMINI_API_KEY env var or pass --api-key.", err=True)
        raise click.Abort()

    try:
        pipeline = MotionGraphicsPipeline(api_key=api_key, blender_path=blender_path)
        pipeline.run(
            prompt=prompt,
            output_name=output,
            duration=duration,
            fps=fps,
            width=width,
            height=height,
            add_audio=audio
        )
    except Exception as e:
        click.echo(f"[-] Error: {e}", err=True)
        raise click.Abort()

if __name__ == "__main__":
    cli()
