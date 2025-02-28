import google.generativeai as genai
from logger_config import get_logger

logger = get_logger(__name__)

def twitter_response_fromai(transcript):
    """
    Send transcript to Gemini API and get generated social media content.

    Args:
        transcript (str): The transcript to be used for generating social media content.

    Returns:
        str: API response containing generated content, or None if the request fails.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""
            You are a highly skilled social media strategist known for crafting **engaging, informative, and shareable** Twitter posts. Your goal is to generate **10 high-quality tweets** based on the transcript below.

            **Instructions for Twitter Posts:**
            - Each tweet should be **punchy, engaging**, and **under 280 characters**.
            - Start strong**: Use a hook (question, bold statement, or surprising fact).
            - Donot include unnecessary fillers like yep, crazy, right or claims about the speaker.
            - Include **key data, statistics**, or **facts** from the transcript to make tweets **informative** and **engaging**.
            - Use simple, natural language** that sounds real—not forced or robotic.
            - Make it insightful**: Focus on lessons, takeaways, or thought-provoking angles.
            - Use **relevant emojis** to make the tweets visually appealing.
            - Avoid mentioning the **source, speaker**, or **platform** in the tweet.
            - Add **2-3 relevant hashtags** per tweet to increase discoverability.
            - Do **not reference subscription percentages** or channel-related details.

            **Format for Each Tweet**:
            ---

            [{{"tweet 1":"Insert tweet content here."}},
            {{"tweet 2":"Insert tweet content here."}},
            ...
            {{"tweet 10":"Insert tweet content here."}}]

            ---
            Transcript:
            {transcript}
            """


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
        
def linkedin_response_fromai(transcript):
    """
    Send transcript to Gemini API and get generated liknedin content.

    Args:
        transcript (str): The tryanscript to be used for generating liknedin content.

    Returns:
        str: API response containing generated content, or None if the request fails.
    """

    # Configure the API key from the environment variable
    client = genai.configure(api_key="AIzaSyBrhhs8Wjcoj4ECDvCkwH69mUJHcuCP098")

    # For text-only input, use the gemini-1.5-flash model
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""
        You are a highly skilled social media strategist known for crafting **engaging, informative, and shareable** LinkedIn posts. Your goal is to generate **4 high-quality posts** based on the transcript below.

        Generate the content in **JSON format**:

        {{
        "linkedin_posts":[
            {{
                "Title":"[Insert the title here]",
                "Content":"[Insert introductory paragraph here with more words and content. You can include data, statistics and examples. Then add a connecting point to the bullet points.]",
                "Bullet-points":[
                    "- [Insert bullet point 1]",
                    "- [Insert bullet point 2]",
                    "- [Insert bullet point 3]"
                    ],
                "Question":"[Insert a thought-provoking question here.]",
                "Hashtags":["#Hashtag1", "#Hashtag2", "#Hashtag3"]
            }},
            {{
                "Title":"[Insert the title here]",
                "Content":"[Insert introductory paragraph here with more words and content. You can include data, statistics and examples. Then add a connecting point to the bullet points.]",
                "Bullet-points":[
                    "- [Insert bullet point 1]",
                    "- [Insert bullet point 2]",
                    "- [Insert bullet point 3]"
                    ],
                "Question":"[Insert a thought-provoking question here.]",
                "Hashtags":["#Hashtag1", "#Hashtag2", "#Hashtag3"]
            }},
            {{
                "Title":"[Insert the title here]",
                "Content":"[Insert introductory paragraph here with more words and content. You can include data, statistics and examples. Then add a connecting point to the bullet points.]",
                Bullet-points":[
                    "- [Insert bullet point 1]",
                    "- [Insert bullet point 2]",
                    "- [Insert bullet point 3]"
                    ],
                "Question":"[Insert a thought-provoking question here.]",
                "Hashtags":["#Hashtag1", "#Hashtag2", "#Hashtag3"]
            }},
            {{
                "Title":"[Insert the title here]",
                "Content":"[Insert introductory paragraph here with more words and content. You can include data, statistics and examples. Then add a connecting point to the bullet points.]",
                Bullet-points":[
                    "- [Insert bullet point 1]",
                    "- [Insert bullet point 2]",
                    "- [Insert bullet point 3]"
                    ],
                "Question":"[Insert a thought-provoking question here.]",
                "Hashtags":["#Hashtag1", "#Hashtag2", "#Hashtag3"]
            }}
            ]
        }}

        ---
        Transcript:
        {transcript}

        **Instructions for LinkedIn Posts:**
        - Each LinkedIn post should be **professional, insightful, and informative**.
        - The brief introductory paragraph, followed by **actionable insights or tips** in bullet points or numbered lists.
        - Include **key data, statistics**, or **facts** from the transcript to make posts **informative** and **engaging**.
        - Use **emojis sparingly** for visual engagement.
        - Avoid mentioning the **source, speaker**, or **platform** in the post.
        - Add **3-5 relevant hashtags** per post to increase discoverability.
        - Do **not reference subscription percentages**, **ads information**, or channel-related details.
        - Each post must strictly follow its respective format: **Title**, **Content**, **Question**, and **Hashtags**.
        """  # Added instructions for LinkedIn posts


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
        logger.exception(f"API request failed: {e}")  # Log the exception with traceback
        return None