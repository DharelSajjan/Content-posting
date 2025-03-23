import sqlite3
import json
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
                print(f"No response found for video ID: {video_id}")
                return {}, []  
    except (sqlite3.Error, json.JSONDecodeError) as e:
        print(f"Error fetching response: {e}")
        return {}, []


x, y = fetch_posts("qeEwAKeB4Ow")
print(x)
print(y)
