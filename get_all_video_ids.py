import yt_dlp
from logger_config import get_logger

logger = get_logger(__name__)

def get_video_ids(channel_url):
    """
    Extracts all video URLs from a given YouTube channel using yt_dlp.

    Args:
        channel_url (str): The URL of the YouTube channel.

    Returns:
        list: A list of video URLs found on the channel.
    """
    ydl_opts = {
        'quiet': True,          
        'extract_flat': True,   
        'skip_download': True  
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(channel_url, download=False)

            # Ensure entries exist in the extracted info
            if 'entries' in info:
                video_ids = [
                    entry['id']  
                    for entry in info['entries']
                    if entry.get('id')  
                ]
                logger.info(f"{len(video_ids)} videos found.")
                return video_ids
            else:
                logger.info("No videos found in the channel.")
                return []

    except Exception as e:
        logger.exception(f"Error occurred: {e}")
        return []