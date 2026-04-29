from moviepy.editor import *
import json
import os

def create_final_video(video_data, output_path):
    """
    video_data: list of (video_clip_path, duration, sound_clips)
    """
    clips = []
    
    for scene_data in video_data:
        clip_path, duration, scene_sounds = scene_data
        
        # Load video clip
        clip = VideoFileClip(clip_path).subclip(0, duration)
        
        # Add fade in/out for smooth transitions
        clip = clip.crossfadein(1).crossfadeout(1)
        
        clips.append(clip)
    
    # Concatenate all clips
    final_video = concatenate_videoclips(clips, method="compose")
    
    # Add gentle background music at very low volume
    try:
        bg_music = AudioFileClip("background_music.mp3").volumex(0.15)
        final_audio = CompositeAudioClip([final_video.audio, bg_music])
        final_video = final_video.set_audio(final_audio)
    except:
        pass
    
    # Export
    final_video.write_videofile(
        output_path,
        fps=24,
        codec='libx264',
        audio_codec='aac',
        threads=4
    )
    
    print(f"✅ Video saved: {output_path}")
    return output_path

def main():
    print("✂️ Loading animated scenes...")
    
    # This is simplified - your actual implementation will:
    # 1. Load all animated clips from previous step
    # 2. Collect them in order per video
    # 3. Create final MP4
    
    print("🎬 Creating final videos...")
    
    # Process each video
    video_count = 0
    # ... implementation based on your file structure
    
    print(f"✅ Created {video_count} videos")

if __name__ == "__main__":
    main()
