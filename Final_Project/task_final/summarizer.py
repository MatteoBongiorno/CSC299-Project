"""
Task summarizer using OpenAI Chat Completions API
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def summarize_task(task_description: str) -> str:
    """
    Use OpenAI's ChatGPT to summarize a paragraph-length task description
    into a short phrase.
    
    Args:
        task_description (str): Long task description
        
    Returns:
        str: Short summarized task phrase
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Using GPT-4o-mini (ChatGPT-4o-mini)
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes task descriptions into short, concise phrases of 3-7 words. Only return the summary, nothing else."
                },
                {
                    "role": "user",
                    "content": f"Summarize this task into a short phrase: {task_description}"
                }
            ],
            temperature=0.7,
            max_tokens=50
        )
        
        summary = response.choices[0].message.content.strip()
        return summary
        
    except Exception as e:
        return f"Error: {str(e)}"
