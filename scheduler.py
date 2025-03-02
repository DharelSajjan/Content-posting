import time
from datetime import datetime
from utils.tweet_helpers import post_tweet
from save_posts import fetch_posts
from extract_linkedin_post import extract_linkedin_post
from utils.post_linkedin import post_linkedin
from create_content import create_contents_for_id
from check_new_videos import check_for_new_videos
from utils.youtube_helpers import process_video
from logger_config import get_logger
    
logger = get_logger(__name__)


# Define posting times
TWITTER_POST_TIMES = ["08:00", "12:00", "16:00", "18:22", "02:00"]
LINKEDIN_POST_TIMES = ["9:00", "21:00"]


def get_current_time():
    """Returns the current time in HH:MM format."""
    return datetime.now().strftime("%H:%M")


def extract_post(post_dict):
    """Extracts the actual post content from a dictionary."""
    return list(post_dict.values())[0]


def post_to_twitter(post):
    """Posts content to Twitter."""
    post_tweet(post)
    print(f"✅ Content posted to Twitter")


def post_to_linkedin(post):
    """Posts content to LinkedIn."""
    # post_linkedin(post)
    logger.info(f"✅ Content posted to LinkedIn")


def process_new_video(channel_url):
    """Checks for new videos and processes them."""
    new_video_ids = check_for_new_videos(channel_url)
    if new_video_ids:
        for video_id in new_video_ids:
            process_video(video_id)
            logger.info(f"🔄 Processing video ID: {video_id}")
    else:
        print("No new videos posted on the channel.")


def fetch_new_content():
    """Fetches new content by creating a video ID and retrieving posts."""
    video_id = create_contents_for_id()
    TWITTER_POSTS, LINKEDIN_POSTS = fetch_posts(video_id)
    return TWITTER_POSTS, LINKEDIN_POSTS


def post_content(TWITTER_POSTS, LINKEDIN_POSTS):
    """Posts content to Twitter and LinkedIn over 2 days."""
    twitter_post_done = 0
    linkedin_post_done = 0
    posted_today = set()
    linkedin_index = 0
    twitter_daily_limit = 5
    linkedin_daily_limit = 2

    while twitter_post_done < len(TWITTER_POSTS) or linkedin_post_done < len(
        LINKEDIN_POSTS):
        current_time = get_current_time()
        logger.info(f"Checking time: {current_time}")

        posted = False

        if current_time in TWITTER_POST_TIMES and current_time not in posted_today:
            if (
                twitter_post_done < len(TWITTER_POSTS)
                and twitter_post_done < twitter_daily_limit
            ):
                post_to_twitter(
                    extract_post(TWITTER_POSTS[twitter_post_done])
                )  # post with the current done index
                twitter_post_done += 1
                posted = True

        if current_time in LINKEDIN_POST_TIMES and current_time not in posted_today:
            if (
                linkedin_post_done < len(LINKEDIN_POSTS)
                and linkedin_post_done < linkedin_daily_limit
            ):
                post, new_index = extract_linkedin_post(LINKEDIN_POSTS, linkedin_index)

                if post:
                    post_to_linkedin(post)
                    linkedin_post_done += 1
                    posted = True
                    linkedin_index = new_index
                else:
                    logger.error(
                        f"Error: Could not extract post at index {linkedin_index}"
                    )

        if posted:
            posted_today.add(current_time)
            logger.info(
                f"✅ Posts so far → Twitter: {twitter_post_done}, LinkedIn: {linkedin_post_done}"
            )

        # Check if daily limits are reached
        if (
            twitter_post_done >= twitter_daily_limit
            and linkedin_post_done >= linkedin_daily_limit
        ):
            logger.info("🎯 Daily posting limits reached.")
            break  # stop the loop for the day.

        # Check if all posts are done.
        if twitter_post_done >= len(TWITTER_POSTS) and linkedin_post_done >= len(
            LINKEDIN_POSTS
        ):
            logger.info("🎯 All posts done for the current video.")
            break
        time.sleep(60)


def main():
    """Main function to continuously fetch and post content."""
    channel_url = "https://www.youtube.com/@TheDiaryOfACEO/videos"

    while True:
        process_new_video(channel_url)
        TWITTER_POSTS, LINKEDIN_POSTS = fetch_new_content()
        post_content(TWITTER_POSTS, LINKEDIN_POSTS)
        logger.info("🔄 Restarting next 2-day cycle...")
        time.sleep(120)  # to avoid too many quick checks.


if __name__ == "__main__":
    main()
