import sqlite3
from get_random_video_id import get_random_video_id_from_db
from get_transcribe import get_transcript
from  generate_posts_from_ai import generate_twitter_content, generate_linkedin_content
from save_posts import save_posts


def is_video_id_in_other_db(video_id):
    """Checks if a given video_id exists in 'posts.db'. Creates table if not exists."""
    
    conn = sqlite3.connect("content.db")
    c = conn.cursor()

    # ✅ Ensure the table exists
    c.execute('''CREATE TABLE IF NOT EXISTS posts (
                video_id TEXT PRIMARY KEY,
                tweets TEXT,
                linkedin TEXT
            )''')
    conn.commit()  

    # ✅ Check if the video_id exists
    c.execute("SELECT 1 FROM posts WHERE video_id = ?", (video_id,))
    result = c.fetchone()

    conn.close()
    
    return result is not None


def get_unique_random_video_id():
    """Fetches a random video_id from database that is NOT in post tbale'."""
    while True:
        video_id = get_random_video_id_from_db()  
        if video_id is None:
            return None  

        if not is_video_id_in_other_db(video_id):
            return video_id  # Found a unique video ID


# Main function to process the video URL
def create_contents_for_id():
    video_id = get_unique_random_video_id()
    if video_id is None:
        return "No videos available."
    else:
        transcript = get_transcript(video_id)
        if "Error" in transcript:
            return transcript
        else:
            video_id, twitter_posts = generate_twitter_content(video_id, transcript)
            _, linkedin_posts = generate_linkedin_content(video_id, transcript)
            save_posts(video_id, twitter_posts, linkedin_posts)
            print(f"Content created and saved successfully for video ID: {video_id}")
            return  video_id
