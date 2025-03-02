import json
import sqlite3
from logger_config import get_logger

logger = get_logger(__name__)

def save_posts(video_id, twitter_posts, linkedin_posts):
    """Parses the response and saves the tweets and LinkedIn posts to the database."""
    try:
        with sqlite3.connect('content.db') as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS posts (
                video_id TEXT PRIMARY KEY,
                tweets TEXT,
                linkedin TEXT
            )''')

            tweets_json = json.dumps(twitter_posts)
            linkedin_json = json.dumps(linkedin_posts)

            c.execute('INSERT OR REPLACE INTO posts (video_id, tweets, linkedin) VALUES (?, ?, ?)',
                      (video_id, tweets_json, linkedin_json))
            conn.commit()
            logger.info(f"Response saved successfully for video ID: {video_id}")

    except (sqlite3.Error, json.JSONDecodeError, Exception) as e:  # Catch general exceptions
        logger.error(f"Error saving response: {e}")
        raise 

def fetch_posts(video_id):
    """Fetches the tweets and LinkedIn posts from the database and returns them."""
    try:
        with sqlite3.connect('content.db') as conn:
            c = conn.cursor()
            c.execute('SELECT tweets, linkedin FROM posts WHERE video_id = ?', (video_id,))
            row = c.fetchone()

            if row:
                tweets = json.loads(row[0])
                linkedin_posts = json.loads(row[1])
                return tweets, linkedin_posts
            else:
                logger.debug(f"No response found for video ID: {video_id}")
                return {}, []  
    except (sqlite3.Error, json.JSONDecodeError) as e:
        logger.exception(f"Error fetching response: {e}")
        return {}, []
