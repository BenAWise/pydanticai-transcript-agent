from src.pydanticai_transcript_agent.agent import TranscriptAgent
from src.pydanticai_transcript_agent.models import Transcript

def main():
    # Sample transcript text
    sample_transcript = """
    In today's podcast, we discussed several interesting topics about AI and business:

    Sarah mentioned that companies are struggling with AI implementation. She suggested 
    creating a step-by-step guide for small businesses to start their AI journey, 
    focusing on practical, low-cost solutions.

    John brought up an interesting point about AI ethics in healthcare. He proposed 
    writing about the balance between innovation and patient privacy, especially 
    for startups in the medical tech space.

    Later, we talked about AI productivity tools, and Mike shared his experience 
    using them in his consulting practice. He recommended creating content about 
    how consultants can use AI to automate routine tasks while maintaining quality.
    """

    # Create transcript object
    transcript = Transcript(text=sample_transcript)

    # Initialize agent
    agent = TranscriptAgent()

    try:
        # Process transcript
        ideas = agent.process_transcript(transcript)

        # Display results
        print("\nFound LinkedIn post ideas:\n")
        for i, idea in enumerate(ideas, 1):
            print(f"Idea {i}:")
            print(f"Title: {idea.idea}")
            print(f"Category: {idea.category}")
            print(f"Engagement Score: {idea.engagement}/5")
            print(f"Mentioned by: {idea.mentioned_by or 'Not specified'}")
            print(f"Summary: {idea.summary}")
            print("-" * 50)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()