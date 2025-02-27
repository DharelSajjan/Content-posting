from responses_fromai import twitter_response_fromai, linkedin_response_fromai
from parse_response import parse_twitter_content, parse_linkedin_content
import time

def generate_twitter_content(id, transcript):
    """ Generate content by fetching transcript and calling the API """
    max_retries = 3
    for attempt in range(max_retries):
        response = twitter_response_fromai(transcript)

        if response is None:
            print(f"❌ API call failed: Response is None (Attempt {attempt+1}/{max_retries})")
        elif not response.candidates or not response.candidates[0].content.parts:
            print(f"❌ API response has no valid content. (Attempt {attempt+1}/{max_retries})")
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
        response = linkedin_response_fromai(transcript)

        # ✅ Check if API response is None
        if response is None or response is {}:
            print(f"❌ API call failed: Response is None (Attempt {attempt+1}/{max_retries})")
        elif not response.candidates or not response.candidates[0].content.parts:
            print(f"❌ API response has no valid content. (Attempt {attempt+1}/{max_retries})")
        else:
            generated_text = response.candidates[0].content.parts[0].text
            linkedin_post = parse_linkedin_content(generated_text)  
            return id, linkedin_post

        time.sleep(2 ** attempt)

    return id, "No content generated after multiple attempts."

