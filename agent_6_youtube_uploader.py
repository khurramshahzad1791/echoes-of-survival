import os
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_to_youtube(video_path, title, description, tags, category='24'):
    """
    Upload video to YouTube
    Category 24 = Entertainment
    """
    # Load credentials (set up once)
    SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
    
    try:
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    except:
        print("⚠️ YouTube API not authenticated. Run oauth setup first.")
        return None
    
    youtube = build('youtube', 'v3', credentials=creds)
    
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': category
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False,
            'madeForKids': False
        }
    }
    
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    
    request = youtube.videos().insert(
        part='snippet,status',
        body=body,
        media_body=media
    )
    
    response = request.execute()
    print(f"✅ Uploaded: {title} - https://youtu.be/{response['id']}")
    return response

def generate_title_and_desc(warrior, scenario):
    """Generate SEO-optimized title and description"""
    
    # Clean title (short, visual, global-friendly)
    title = f"{warrior} - {scenario.split(',')[0]}"
    
    # Description with keywords
    description = f"""{warrior} survival journey through ancient times.

Experience the struggle, solitude, and determination of a {warrior} facing nature's challenges. No words. Pure atmosphere.

🌍 Perfect for:
• Studying & focus
• Relaxation & sleep
• Background ambiance
• History enthusiasts

🎬 New video daily. Subscribe for more historical survival stories.

#historicalsurvival #{warrior.replace(' ', '')} #ancientsurvival #ambientcinema #silentcinema #history"
"""
    
    tags = [warrior, scenario.split(',')[0], "historical survival", "ancient survival", "silent cinema", "ambient", "history", "survival", "nature"]
    
    return title, description, tags

def main():
    print("🔄 Loading final videos...")
    
    # Get list of videos to upload
    # This assumes videos are stored in 'final_videos/' directory
    
    video_files = [f for f in os.listdir('final_videos') if f.endswith('.mp4')]
    
    for video_file in video_files:
        # Extract warrior name from filename
        warrior = video_file.replace('.mp4', '').replace('_', ' ')
        
        title, desc, tags = generate_title_and_desc(warrior, "Survival Journey")
        
        print(f"📤 Uploading: {title}")
        upload_to_youtube(
            f'final_videos/{video_file}',
            title,
            desc,
            tags
        )
    
    print("✅ All videos uploaded to YouTube")

if __name__ == "__main__":
    main()
