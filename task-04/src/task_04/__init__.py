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


def summarize_task(task_description):
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


def main():
    """Main function to demonstrate task summarization"""
    
    # Sample paragraph-length task descriptions
    task_descriptions = [
        """I need to prepare a comprehensive presentation for the upcoming quarterly 
        business review meeting. This involves gathering all the sales data from the 
        past three months, creating visualizations and charts to show trends, writing 
        up analysis of what worked well and what didn't, and putting together a 
        PowerPoint deck with at least 20 slides. I also need to practice my delivery 
        and make sure I can present everything within the 30-minute time limit that 
        was allocated to me.""",
        
        """For my garden project, I need to completely renovate the backyard space. 
        This means first removing all the old, dead plants and weeds, then tilling 
        the soil and adding fresh compost and fertilizer. After that, I'll need to 
        map out where different plants should go based on sunlight requirements, 
        purchase all the seeds and seedlings from the nursery, plant everything 
        according to the plan, set up a drip irrigation system, and finally add 
        mulch around all the plants to help retain moisture. The whole project will 
        probably take several weekends to complete.""",
        
        """I'm planning to organize a surprise birthday party for my best friend next 
        month. I need to coordinate with all our mutual friends to pick a date that 
        works for everyone, find and book a suitable venue that can accommodate about 
        30 people, arrange for catering or food options, create and send out 
        invitations without my friend finding out, plan some games and activities for 
        entertainment, order a custom cake from the bakery, set up decorations on the 
        day of the party, and make sure someone can keep my friend busy while we all 
        get set up. I also need to collect money from everyone who's contributing."""
    ]
    
    print("Task Summarizer using OpenAI API")
    print("=" * 50)
    print()
    
    # Summarize each task description
    for i, description in enumerate(task_descriptions, 1):
        print(f"Task {i}:")
        print(f"Original: {description[:100]}...")  # Show first 100 chars
        print(f"Summarizing...")
        
        summary = summarize_task(description)
        print(f"Summary: {summary}")
        print("-" * 50)
        print()


if __name__ == "__main__":
    main()