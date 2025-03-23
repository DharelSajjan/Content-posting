import time
from utils.llm_helpers import get_llm_response,parse_twitter_content,parse_linkedin_content
from logger_config import get_logger

logger = get_logger(__name__)

def generate_twitter_content(id, transcript):
    """ Generate content by fetching transcript and calling the API """
    max_retries = 3
    for attempt in range(max_retries):
        response = get_llm_response("twitter",transcript=transcript)

        if response is None:
            logger.error(f"❌ API call failed: Response is None (Attempt {attempt+1}/{max_retries})")
        elif not response.candidates or not response.candidates[0].content.parts:
            logger.error(f"❌ API response has no valid content. (Attempt {attempt+1}/{max_retries})")
        else:
            generated_text = response.candidates[0].content.parts[0].text

            twitter_posts = parse_twitter_content(generated_text)
            return id, twitter_posts
        
        time.sleep(2 ** attempt)

    return id, "No content generated after multiple attempts."

def generate_linkedin_content(id, transcript):
    """ Generate content by fetching transcript and calling the API with retries """
    max_retries=3
    for attempt in range(max_retries):
        response = get_llm_response("linkedin",transcript=transcript)

        # ✅ Check if API response is None
        if response is None or response is {}:
            logger.error(f"❌ API call failed: Response is None (Attempt {attempt+1}/{max_retries})")
        elif not response.candidates or not response.candidates[0].content.parts:
            logger.info(f"❌ API response has no valid content. (Attempt {attempt+1}/{max_retries})")
        else:
            generated_text = response.candidates[0].content.parts[0].text
            linkedin_post = parse_linkedin_content(generated_text)  
            return id, linkedin_post

        time.sleep(2 ** attempt)

    return id, "No content generated after multiple attempts."
