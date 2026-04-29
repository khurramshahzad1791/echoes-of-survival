import requests
import json
import base64
import time
import os

# Leonardo.ai API (free tier)
LEONARDO_API_KEY = os.environ["LEONARDO_API_KEY"]
LEONARDO_URL = "https://cloud.leonardo.ai/api/rest/v1/generations"

def generate_image(prompt, warrior_type, scene_id):
    payload = {
        "modelId": "6bef9f1b-29cb-40c7-b9df-32b51c1f67d3",  # Leonardo Photo Real
        "prompt": f"{prompt}, cinematic lighting, photorealistic, 4K, natural colors, historical accuracy, no text, no watermark, shot on film camera, documentary style",
        "negative_prompt": "text, watermark, signature, blurry, cartoon, anime, drawing, painting, modern objects, anachronism",
        "width": 1024,
        "height": 576,  # 16:9 aspect ratio
        "num_images": 1,
        "contrastRatio": 1.0,
        "public": False
    }
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {LEONARDO_API_KEY}"
    }
    
    response = requests.post(LEONARDO_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        generation_id = response.json()["sdGenerationJob"]["generationId"]
        return generation_id
    else:
        print(f"Error: {response.status_code}")
        return None

def check_generation_status(generation_id):
    url = f"https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id}"
    headers = {"authorization": f"Bearer {LEONARDO_API_KEY}"}
    
    for _ in range(30):  # Wait up to 60 seconds
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data["generations_by_pk"]["status"] == "COMPLETE":
                return data["generations_by_pk"]["generated_images"][0]["url"]
        time.sleep(2)
    return None

def main():
    print("🔄 Loading scripts...")
    with open('scripts.json', 'r') as f:
        scripts = json.load(f)
    
    print("🎨 Generating images for all videos...")
    print(f"⚠️ Leonardo free tier: 150 credits/day. Using 6 images/video = {len(scripts)*6} images max.")
    
    for video_idx, script in enumerate(scripts[:5]):  # Start with 5 videos per day
        print(f"\n📹 Processing Video {video_idx+1}: {script['warrior']}")
        
        for scene_num, scene_text in enumerate(script['scenes'][:6]):
            print(f"  Scene {scene_num+1}/6...")
            
            # Extract action from scene text
            action_start = scene_text.find("ACTION:")
            action_end = scene_text.find("SOUNDS:")
            action = scene_text[action_start+7:action_end].strip()
            
            prompt = f"{script['warrior']}, {script['scenario']}, {action}"
            
            print(f"    Prompt: {prompt[:100]}...")
            
            generation_id = generate_image(prompt, script['warrior'], scene_num)
            if generation_id:
                image_url = check_generation_status(generation_id)
                if image_url:
                    print(f"    ✅ Image generated: {image_url[:50]}...")
                    # Store URL for later
                    if 'image_urls' not in script:
                        script['image_urls'] = []
                    script['image_urls'].append(image_url)
    
    # Save updated scripts with image URLs
    with open('scripts_with_images.json', 'w') as f:
        json.dump(scripts, f, indent=2)
    
    print(f"\n🎉 Completed! Generated images for {min(len(scripts),5)} videos")
    print("Note: Leonardo free tier gives 150 credits/day. Run this daily for 15 videos.")

if __name__ == "__main__":
    main()
