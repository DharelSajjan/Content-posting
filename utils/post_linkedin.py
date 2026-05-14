import requests
import json
from logger_config import get_logger

logger = get_logger(__name__)

def get_linkedin_user_urn(access_token):
    url = 'https://api.linkedin.com/v2/userinfo'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        logger.info(f"Error: {response.status_code}, {response.text}")
        return None

def actual_post(access_token, user_urn, content):
    """Posts content to LinkedIn using the UGC Posts API."""
    response = get_linkedin_user_urn(access_token)
    user_urn = response.get("sub")
    url = 'https://api.linkedin.com/v2/ugcPosts'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'X-Restli-Protocol-Version': '2.0.0'
    }
    payload = {
        "author": f"urn:li:person:{user_urn}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": content
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status() 
        if response.status_code == 201:
            logger.info("Post created successfully.")
        else:
            logger.info(f"Unexpected status code: {response.status_code}")
            logger.info(response.text)

    except requests.exceptions.RequestException as e:
        logger.exception(f"An error occurred: {e}")
    except json.JSONDecodeError:
        logger.error("Error decoding json response for Linkedin api posting.")

def post_linkedin(content):
    """Main function to orchestrate the LinkedIn posting process."""
    access_token=""
    user_urn = get_linkedin_user_urn(access_token)
    if user_urn:
        actual_post(access_token, user_urn, content)
    else:
        logger.error("Failed to retrieve user URN. Cannot post.")


