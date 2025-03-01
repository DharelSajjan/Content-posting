import re
import json
import google.generativeai as genai
from string import Template as StringTemplate
from utils.settings import PROMPTS_PATH

from logger_config import get_logger

logger = get_logger(__name__)


def parse_twitter_content(text):
    # Regular expression to capture JSON-like list of dictionaries
    pattern = r"\[\s*\{.*?\}\s*\]"

    # Search for the pattern in the text
    match = re.search(pattern, text, re.DOTALL)

    if match:
        json_str = match.group(0)  # Extract matched JSON string
        try:
            json_data = json.loads(json_str)  # Convert to JSON object
            return json_data  # Return parsed JSON
        except json.JSONDecodeError as e:
            logger.exception("JSON Decode Error:", e)
            return None
    else:
        logger.info("No JSON-like data found.")
        return None


def parse_linkedin_content(text):
    """Parses LinkedIn posts from text using regular expressions and JSON."""

    try:
        # Use regex to extract the JSON-like data from the string
        pattern = r"\{.*\}"  # Match the outermost JSON object
        match = re.search(pattern, text, re.DOTALL)

        if not match:
            logger.info("No JSON-like data found in the text.")
            return {}

        # Extract the JSON-like string
        json_str = match.group(0)

        # Load the JSON string into a Python dictionary
        data = json.loads(json_str)

        # Extract the LinkedIn posts
        linkedin_posts = data.get("linkedin_posts", [])

        # Initialize the result dictionary
        parsed_posts = {}

        # Iterate over each post and structure it
        for i, post in enumerate(linkedin_posts, start=1):
            post_key = f"Post {i}"
            parsed_posts[post_key] = {
                "Title": post.get("Title", ""),
                "Content": post.get("Content", ""),
                "Bullet-points": post.get("Bullet-points", []),
                "Question": post.get("Question", ""),
                "Hashtags": post.get("Hashtags", []),
            }

        return parsed_posts

    except json.JSONDecodeError as e:
        logger.exception(f"Error decoding JSON: {e}")
        return {}
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
        return {}


def get_llm_response(platform, **placeholders):
    """
    Send transcript to Gemini API and get generated social media content.

    Args:
        transcript (str): The transcript to be used for generating social media content.

    Returns:
        str: API response containing generated content, or None if the request fails.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt_subpath = f"{platform}_prompt.txt"
    with open(PROMPTS_PATH / f"{prompt_subpath}.txt", "r") as file:
        prompt = StringTemplate(file.read()).substitute(**placeholders)

    generation_config = {
        "temperature": 0.7,  # Adjust for more or less randomness
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 2048,  # Limit the length of the output
    }

    try:
        logger.debug(f"Sending prompt: {prompt}")
        response = model.generate_content(prompt, generation_config=generation_config)
        logger.debug(f"API response: {response}")
        return response
    except Exception as e:
        logger.exception(f"API request failed: {e}")
        return None
