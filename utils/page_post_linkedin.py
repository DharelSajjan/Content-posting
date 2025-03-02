import requests
import json

# def get_linkedin_organization_urn(access_token, organization_vanity_name):
#     """Retrieves the organization URN using the organization's vanity name."""
#     url = f"https://api.linkedin.com/v2/organizations?q=vanityName&vanityName={organization_vanity_name}"
#     headers = {
#         'Authorization': f'Bearer {access_token}'
#     }
#     try:
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()  # Raise an exception for bad status codes
#         data = response.json()
#         if 'elements' in data and data['elements']:
#             return data['elements'][0]['id']  # Returns the numeric ID, which is needed for constructing the URN
#         else:
#             print(f"Organization '{organization_vanity_name}' not found.")
#             return None
#     except requests.exceptions.RequestException as e:
#         print(f"An error occurred: {e}")
#         return None
#     except json.JSONDecodeError:
#         print("Error decoding json response")
#         return None






def actual_post_organization(access_token, organization_urn, content):
    """Posts content to a LinkedIn organization page using the UGC Posts API."""
    url = 'https://api.linkedin.com/v2/ugcPosts'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'X-Restli-Protocol-Version': '2.0.0'
    }
    payload = {
        "author": f"urn:li:organization:{organization_urn}",
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
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        if response.status_code == 201:
            print("Post created successfully on the organization page.")
        else:
            print(f"Unexpected status code: {response.status_code}")
            print(response.text)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    except json.JSONDecodeError:
        print("Error decoding json response")

def post_linkedin_organization(content, organization_vanity_name):
    """Main function to orchestrate the LinkedIn organization page posting process."""
    access_token = "AQVkD94xfeCBnY_ALiYfGDK4yzCe7q9M4i_CHKcCfJflZkbZQGixVjjWO_9NHZdjr3aeemsY7TZ7WNkX78DAdORmtpTMR_f4yOARmTQ6j8vlC2Gj4F8fRFrteQS0JxBc8NOm3BcBG5HooLV0RX3loeWOFAHdzDcOyJpvKktQpD04gPqveuoNksA9cbhunRcH-En6IGBcgTmcNZRDtO1JL-U_1TkJXmZcS7WMO0WWZTe_eLkWIGIiWYL2oNpJE75P5Vo1sunm6XbWWyrCS0DlYOO5RPOsqmRzyS6WdW6okYyc63CkDBADRpPTT3YEOJuZNBICzyvXSw_yVM8_kv-_ljaPX0LuSw!" # Replace with your actual access token
    organization_urn = get_linkedin_organization_urn(access_token, organization_vanity_name)

    if organization_urn:
        actual_post_organization(access_token, organization_urn, content)
    else:
        print("Failed to retrieve organization URN. Cannot post.")

# Example usage:
content = "This is the first post"
organization_vanity_name = "106607818" # Replace with your organization's vanity name



post_linkedin_organization(content, organization_vanity_name)