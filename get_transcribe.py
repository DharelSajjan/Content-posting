import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
import re
import sqlite3
from datetime import datetime

# Function to extract metadata from a YouTube video
def get_metadata(video_url):
    ydl_opts = {"quiet": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        
        # Format the date (YYYY-MM-DD) if available
        upload_date = info.get("upload_date", "N/A")
        if upload_date != "N/A" and len(upload_date) == 8:
            upload_date = datetime.strptime(upload_date, "%Y%m%d").date()

        metadata = {
            "id": info.get("id", "N/A"),
            "title": info.get("title", "N/A"),
            "upload_date": upload_date
        }
    return metadata

# Function to clean transcript text
def clean_transcript(text):
    text = re.sub(r"[♪…]", "", text)                     # Remove music notes and ellipses
    text = re.sub(r"[^\w\s.,!?'\-+*/=%<>]", "", text)    # Keep English and math symbols, remove others
    text = re.sub(r"\s+", " ", text).strip()             # Remove extra spaces
    return text

# Function to fetch and clean transcript
def get_transcript(video_id):    
    try:
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([entry["text"] for entry in transcript_data])
        return clean_transcript(transcript_text)
    except TranscriptsDisabled:
        return "No transcript available for this video."
    except Exception as e:
        return f"Error fetching transcript: {str(e)}"

# Function to initialize the SQLite database
def initialize_database():
    conn = sqlite3.connect("content.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS youtube_data (
            video_id TEXT PRIMARY KEY,
            title TEXT,
            upload_date DATE)
    """)
    conn.commit()
    conn.close()

# Function to save data to the database
def save_to_database(metadata):
    conn = sqlite3.connect("content.db", timeout=10)  # Adding timeout to avoid lock issues
    c = conn.cursor()

    try:
        c.execute("""
            INSERT INTO youtube_data (video_id, title, upload_date)
            VALUES (?, ?, ?)
        """, (metadata["id"], metadata["title"], metadata["upload_date"]))
        
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Video {metadata['id']} already exists in the database. Skipping...")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

# Main function to process the video URL
def process_video(video_id):
    initialize_database()  # Ensure the database is set up
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    metadata = get_metadata(video_url)

    # Display extracted information
    print("\nMetadata:")
    print(f"Video ID: {metadata['id']}")
    print(f"Title: {metadata['title']}")
    print(f"Upload Date: {metadata['upload_date']}")    
    save_to_database(metadata)
