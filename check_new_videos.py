import yt_dlp
import sqlite3
from logger_config import get_logger

logger = get_logger(__name__)

# Function to get the latest video ID from the database based on the latest upload date
def get_latest_video_id_from_db():
    conn = sqlite3.connect("content.db")
    c = conn.cursor()
    c.execute("SELECT video_id FROM youtube_data ORDER BY upload_date DESC LIMIT 1")
    result = c.fetchone()
    conn.close()

    if result is not None:
        video_id = result[0]
        return video_id
    return None  # No videos in the database yet

# Function to fetch the last 10 video entries from the YouTube channel
def get_latest_videos_from_channel(channel_url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'skip_download': True,
        'playlistend': 5  # Limit to the latest 10 videos
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel_url, download=False)
        return info.get('entries', [])

# Function to check for new videos by comparing video IDs
def check_for_new_videos(channel_url):
    latest_db_video_id = get_latest_video_id_from_db()
    logger.info(f"Latest video ID in the database: {latest_db_video_id}")

    latest_videos = get_latest_videos_from_channel(channel_url)
    new_video_ids = []

    for video in latest_videos:
        video_id = video.get('id')
        # Stop checking once we find a video that matches the latest one in the database
        if video_id == latest_db_video_id:
            break

        # If the video is new, add it to the list
        new_video_ids.append(video_id)

    if new_video_ids:
        logger.info(f"New videos found: {len(new_video_ids)}")
        return new_video_ids[::-1]  # Return in chronological order (oldest to newest)
    else:
        logger.info("No new videos available.")
        return None
