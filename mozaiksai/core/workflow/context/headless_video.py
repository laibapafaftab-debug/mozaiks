import asyncio 
import os
import edge_tts
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, AudioFileClip, CompositeVideoClip

# Configuration
TEXT_SCRIPT = "Welcome to Mozaiks! The AI App Factory that builds, iterates, and automates your workflows seamlessly."
VOICE = "en-US-ChristopherNeural"
AUDIO_FILE = "voiceover.mp3"
FRAME_FILE = "frame.png"
OUTPUT_VIDEO = "headless_marketing_poc.mp4"


async def generate_audio():
    """Step 1: Text-to-Speech via Edge-TTS (No API key needed)"""
    print("🎙️ Generating AI Voiceover...")
    communicate = edge_tts.Communicate(TEXT_SCRIPT, VOICE)
    await communicate.save(AUDIO_FILE)
    print("✓ Voiceover generated!")


def create_text_frame():
    """Step 2: Generate background frame with caption overlay using Pillow"""
    print("🖼️ Rendering Frame...")
    width, height = 1080, 1920  # 9:16 Vertical Video format
    bg_color = (15, 23, 42)     # Slate Dark Theme
    text_color = (255, 255, 255)

    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Simple centered text rendering
    words = TEXT_SCRIPT.split()
    lines = []
    current_line = []
    
    for word in words:
        current_line.append(word)
        if len(" ".join(current_line)) > 25:
            lines.append(" ".join(current_line[:-1]))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))

    text_to_draw = "\n".join(lines)
    
    # Draw simple text block in the center
    draw.multiline_text((100, height // 3), text_to_draw, fill=text_color, spacing=20)
    img.save(FRAME_FILE)
    print("✓ Frame rendered!")


def render_headless_video():
    """Step 3: Combine Audio + Image Frame into MP4 Video (MoviePy v2.x compatible)"""
    print("🎬 Rendering Headless Video...")
    
    audio_clip = AudioFileClip(AUDIO_FILE)
    duration = audio_clip.duration

    # MoviePy v2.x syntax updates
    video_clip = ImageClip(FRAME_FILE).with_duration(duration)
    final_clip = video_clip.with_audio(audio_clip)

    final_clip.write_videofile(
        OUTPUT_VIDEO,
        fps=24,
        codec="libx264",
        audio_codec="aac"
    )

    # Cleanup temporary files
    if os.path.exists(AUDIO_FILE): os.remove(AUDIO_FILE)
    if os.path.exists(FRAME_FILE): os.remove(FRAME_FILE)
    
    print(f"\n✅ SUCCESS! Video saved as: {OUTPUT_VIDEO}")


if __name__ == "__main__":
    asyncio.run(generate_audio())
    create_text_frame()
    render_headless_video()
