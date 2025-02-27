import sqlite3

def get_random_video_id_from_db():
    conn = sqlite3.connect("content.db")
    c = conn.cursor()
    
    c.execute("SELECT video_id FROM youtube_data ORDER BY RANDOM() LIMIT 1")
    result = c.fetchone()
    
    conn.close()

    if result is not None:
        return result[0]  
    return None  
