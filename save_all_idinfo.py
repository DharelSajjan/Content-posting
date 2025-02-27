from get_all_video_ids import get_video_ids
from get_transcribe import process_video

def save_all_idinfo(channel_url):
    """Fetches all video IDs from a channel and saves them to the database."""
    video_ids = get_video_ids(channel_url)
    if not video_ids:
        print("No video IDs found.")
        return
    try:
        for video_id in video_ids:
            process_video(video_id)
        print("All video IDs saved successfully.")
    except Exception as e:
        print(f"Error saving video IDs: {e}")

if __name__ == "__main__":
    channel_url = 'https://www.youtube.com/@TheDiaryOfACEO/videos'
    save_all_idinfo(channel_url)
