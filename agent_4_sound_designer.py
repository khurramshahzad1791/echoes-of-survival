import requests
import json
import os
from moviepy.editor import *
import random

# Pixabay API (free)
PIXABAY_API_KEY = os.environ["PIXABAY_API_KEY"]

# Sound mapping for different actions
SOUND_MAP = {
    "wind": "wind",
    "footsteps": "footstep",
    "fire crackling": "fire",
    "water flowing": "water",
    "birds": "birds",
    "leaves rustling": "leaves",
    "thunder": "thunder",
    "rain": "rain",
    "wolf howl": "wolf",
    "eagle": "eagle",
    "river": "river",
    "snow crunch": "snow",
    "wood chop": "wood",
    "stone strike": "stone"
}

def download_sound(sound_type):
    """Download sound from Pixabay (free)"""
    url = "https://pixabay.com/api/"
    params = {
        "key": PIXABAY_API_KEY,
        "q": sound_type,
        "category": "sounds",
        "per_page": 1
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['hits']:
            return data['hits'][0]['preview_url']
    return None

def extract_sounds_from_scene(scene_text):
    """Extract sound keywords from scene description"""
    sounds = []
    sound_keywords = ["wind", "footsteps", "fire", "water", "birds", "leaves", 
                     "thunder", "rain", "wolf", "eagle", "river", "snow", "wood", "stone"]
    
    text_lower = scene_text.lower()
    for keyword in sound_keywords:
        if keyword in text_lower:
            sounds.append(keyword)
    
    return sounds[:5]  # Max 5 sounds per scene

def add_sounds_to_video(video_path, script, output_path):
    """Add ambient sounds to video"""
    video = VideoFileClip(video_path)
    audio_clips = []
    
    for scene in script['scenes']:
        sounds = extract_sounds_from_scene(scene)
        for sound_type in sounds:
            sound_url = download_sound(sound_type)
            if sound_url:
                temp_sound = requests.get(sound_url)
                with open('temp_sound.mp3', 'wb') as f:
                    f.write(temp_sound.content)
                audio_clip = AudioFileClip('temp_sound.mp3')
                audio_clips.append(audio_clip)
    
    # Combine all sounds
    if audio_clips:
        final_audio = CompositeAudioClip(audio_clips)
        video = video.set_audio(final_audio)
    
    video.write_videofile(output_path, fps=24)
    print(f"✅ Sounds added: {output_path}")
    return output_path

def main():
    print("🔄 Loading scripts with images...")
    with open('scripts_with_images.json', 'r') as f:
        scripts = json.load(f)
    
    for script in scripts:
        print(f"🎵 Adding sounds to {script['warrior']}...")
        # Add sounds to each animated scene
        pass  # Implementation depends on your file structure

if __name__ == "__main__":
    main()
