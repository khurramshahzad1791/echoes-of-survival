import google.generativeai as genai
import json
import os
from datetime import datetime

# Initialize Gemini
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# 50 Historical Survival Scenarios
SCENARIOS = [
    ("Celtic Warrior", "Lost in ancient oak forest, 500 BC"),
    ("Viking", "Shipwreck survivor on hostile coast, 850 AD"),
    ("Samurai", "Lost in Japanese Alps winter, 1200 AD"),
    ("Roman Legionnaire", "Separated from unit in German forest, 100 AD"),
    ("Stone Age Hunter", "Lost in tundra after storm, 10,000 BC"),
    ("Egyptian Scribe", "Lost in desert after sandstorm, 1500 BC"),
    ("Mongol Scout", "Alone on empty steppe, 1200 AD"),
    ("Aztec Warrior", "Lost in jungle, 1400 AD"),
    ("Knight", "Stranded after battle, 1300 AD"),
    ("Samurai Ronin", "Wandering post-war Japan, 1600 AD"),
    ("Inca Messenger", "Lost in Andes mountains, 1450 AD"),
    ("Zulu Scout", "Alone on African savannah, 1700 AD"),
    ("Greek Hoplite", "Lost on mountainous island, 400 BC"),
    ("Persian Messenger", "Crossing salt desert, 500 BC"),
    ("Native American", "Lost in canyon, 1500 AD"),
]

def generate_scene(scenario, warrior_type, scene_num):
    prompt = f"""Create a detailed scene description for a historical survival video.
Warrior: {warrior_type}
Scenario: {scenario}
Scene number: {scene_num} of 6

The video has NO narration, NO dialogue. Just visual action and ambient sounds.
Each scene should be 30-40 seconds long.

Format your response exactly as:
SCENE {scene_num} ACTION: [describe what the warrior does in 2-3 sentences]
SOUNDS: [list 3-5 ambient sounds, comma separated]"""

    response = model.generate_content(prompt)
    return response.text

def generate_video_script(warrior_type, scenario, video_num):
    scenes = []
    for i in range(1, 7):
        scene_text = generate_scene(scenario, warrior_type, i)
        scenes.append(scene_text)
    
    script = {
        "video_id": f"vid_{video_num:03d}",
        "warrior": warrior_type,
        "scenario": scenario,
        "date": datetime.now().isoformat(),
        "scenes": scenes
    }
    return script

def main():
    print("🔄 Generating 15 video scripts...")
    scripts = []
    
    for i, (warrior, scenario) in enumerate(SCARIOS[:15]):
        script = generate_video_script(warrior, scenario, i+1)
        scripts.append(script)
        print(f"✅ Generated script {i+1}/15: {warrior} - {scenario}")
    
    # Save all scripts
    with open('scripts.json', 'w') as f:
        json.dump(scripts, f, indent=2)
    
    print(f"🎉 Saved 15 scripts to scripts.json")

if __name__ == "__main__":
    main()
