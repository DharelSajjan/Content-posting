import re
import json
import logging
logging.basicConfig(level=logging.INFO)


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
            print("JSON Decode Error:", e)
            return None
    else:
        print("No JSON-like data found.")
        return None
    
def parse_linkedin_content(text):
    """Parses LinkedIn posts from text using regular expressions and JSON."""

    try:
        # Use regex to extract the JSON-like data from the string
        pattern = r"\{.*\}"  # Match the outermost JSON object
        match = re.search(pattern, text, re.DOTALL)

        if not match:
            print("No JSON-like data found in the text.")
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
                "Hashtags": post.get("Hashtags", [])

            }

        return parsed_posts

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {}

