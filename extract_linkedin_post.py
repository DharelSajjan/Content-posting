from colorama import Fore, Style
from post_linkedin import post_linkedin

def bold_text(text):
    """Returns the input text formatted in bold."""
    return ''.join(chr(0x1D400 + ord(c) - ord('A')) if 'A' <= c <= 'Z' else 
                   chr(0x1D41A + ord(c) - ord('a')) if 'a' <= c <= 'z' else c 
                   for c in text)
def extract_linkedin_post(post_data, index):
    """
    Extracts and formats a LinkedIn post from the given structured data.

    Args:
        post_data (dict): A dictionary containing LinkedIn post details.
        index (int): The index of the post to extract.

    Returns:
        str: A formatted LinkedIn post.
    """
    # Get all post keys (Post 1, Post 2, etc.)
    post_keys = list(post_data.keys())  
    if index >= len(post_keys):  
        index = 0  

    post_key = post_keys[index]  
    # Extract the actual post content
    post = post_data[post_key]  

    # Format the LinkedIn post
    title = post.get("Title", "")
    question = post.get("Question", "")
    content = post.get("Content", "")
    bullet_points = "\n".join(post.get("Bullet-points", []))  
    hashtags = " ".join(post.get("Hashtags", []))  
    formatted_bullet_points = "\n".join(f" {point.strip()}" for point in bullet_points.split("\n") if point.strip())
    
    bold_title = bold_text(title) 
    linkedin_post  = f"{bold_title}" if title else ""
    linkedin_post += f"\n\n{content}\n\n"
    linkedin_post += f"{formatted_bullet_points}\n\n" if bullet_points else ""
    linkedin_post += f"{question}\n\n" if question else "" 

    linkedin_post += f"{hashtags}\n"


    return linkedin_post.strip(), index + 1  

