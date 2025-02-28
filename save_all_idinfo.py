from get_all_video_ids import get_video_ids
from get_transcribe import process_video
from logger_config import get_logger

logger = get_logger(__name__)

def save_all_idinfo(channel_url):
    """Fetches all video IDs from a channel and saves them to the database."""
    video_ids = get_video_ids(channel_url)
    if not video_ids:
        logger.info("No video IDs found.")
        return
    try:
        for video_id in video_ids:
            process_video(video_id)
        logger.info("All video IDs saved successfully.")
    except Exception as e:
        logger.exception(f"Error saving video IDs: {e}")