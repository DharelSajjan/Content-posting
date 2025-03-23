import time
import sqlite3
from datetime import datetime
from extract_linkedin_post import extract_linkedin_post
from utils.page_post_selenium import LinkedInAutomation
from logger_config import get_logger
from utils.settings import STAGE

logger = get_logger(__name__)

LINKEDIN_POST_TIMES = ["10:00", "22:00"]


def fetch_linkedin_posts(index):
    """Fetches LinkedIn posts from the database."""
    # Connect to the SQLite database
    conn = sqlite3.connect("content.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT video_id, linkedin FROM posts ORDER BY rowid ASC LIMIT 1 OFFSET ?",
        (index,),
    )
    row = cursor.fetchone()
    conn.close()
    return row


def get_current_time():
    """Returns the current time in HH:MM format.
    In test mode (STAGE=test), always returns the first scheduled time.
    """
    if STAGE == "test":
        return LINKEDIN_POST_TIMES[0]
    return datetime.now().strftime("%H:%M")


def post_to_linkedin(post):
    """Posts content to LinkedIn."""
    bot = LinkedInAutomation()
    bot.post_content(post)
    logger.info("✅ Content posted to LinkedIn")


def scheduler_linkedin_post():
    """Continuously posts LinkedIn content for each video ID in sequence."""
    linkedin_index = 0
    table_index = 0
    posts_done = 0
    while True:
        row = fetch_linkedin_posts(table_index)

        if not row:
            logger.info("No more posts to schedule.")
            break
        video_id, linkedin_contents = row
        print(video_id)
        while posts_done < 4:
            current_time = get_current_time()
            if current_time in LINKEDIN_POST_TIMES:
                post, new_index = extract_linkedin_post(
                    linkedin_contents, linkedin_index
                )
                if post:
                    post_to_linkedin(post)
                    linkedin_index = new_index
                    posts_done += 1
                    time.sleep(60)
                else:
                    logger.warning(
                        f"No post found at index {posts_done} for the {video_id}. Skipping."
                    )
                    break
            else:
                logger.info("No posts scheduled for this time.")
                time.sleep(60)
        table_index += 1
        posts_done = 0


if __name__ == "__main__":
    scheduler_linkedin_post()
