# This script runs on Google Colab (free GPU)
# Copy this into a Colab notebook and run

"""
# Silent Historical Survival - Animation Agent
# Run this on Google Colab with GPU runtime

!pip install diffusers transformers accelerate torch torchvision xformers

import torch
from diffusers import AnimateDiffPipeline, MotionAdapter
from diffusers.utils import export_to_video
import json
import requests
from PIL import Image
import io

# Load AnimateDiff
adapter = MotionAdapter.from_pretrained("guoyww/animatediff-motion-adapter-v1-5-2")
pipe = AnimateDiffPipeline.from_pretrained(
    "stable-diffusion-v1-5/stable-diffusion-v1-5",
    motion_adapter=adapter
).to("cuda")

# Enable memory optimization
pipe.enable_vae_slicing()
pipe.enable_model_cpu_offload()

def download_image(url):
    response = requests.get(url)
    return Image.open(io.BytesIO(response.content)).convert("RGB")

def animate_scene(image, prompt, output_path):
    # Generate 24 frames (4 seconds at 6fps)
    frames = pipe(
        prompt=prompt,
        image=image,
        num_frames=24,
        guidance_scale=7.5,
        num_inference_steps=25,
    ).frames[0]
    
    export_to_video(frames, output_path, fps=6)
    return output_path

# Load scripts with images
with open('scripts_with_images.json', 'r') as f:
    scripts = json.load(f)

# Animate each image
for video in scripts:
    for scene_num, image_url in enumerate(video.get('image_urls', [])):
        print(f"Animating {video['warrior']} - Scene {scene_num+1}...")
        
        # Download image
        image = download_image(image_url)
        
        # Create prompt from scene
        prompt = f"{video['warrior']}, {video['scenario']}, subtle natural movements, cinematic"
        
        # Animate
        output_path = f"output/{video['warrior']}_scene_{scene_num}.mp4"
        animate_scene(image, prompt, output_path)
        
print("✅ All scenes animated!")
"""
