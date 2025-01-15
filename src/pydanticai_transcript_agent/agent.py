from pydantic_ai import Agent
from pydantic_ai.models.anthropic import AnthropicModel
from typing import List
import json
import os
from dotenv import load_dotenv
from .models import Transcript, IdeaItem

# Load environment variables
load_dotenv()

class TranscriptAgent:
    """Agent for analyzing transcripts and extracting LinkedIn post ideas."""
    
    def __init__(self):
        if not os.getenv("ANTHROPIC_API_KEY"):
            raise ValueError("ANTHROPIC_API_KEY environment variable is not set")
            
        self.model = AnthropicModel(
            model_name="claude-3-5-sonnet-latest",
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )
        self.agent = Agent(
            model=self.model,
            system_prompt="""You are an expert at analyzing transcripts and identifying potential LinkedIn post ideas.
            For each idea you find, you should output a JSON object in the format: 
            {'idea': '...', 'category': '...', 'engagement': ..., 'mentioned_by': '...', 'summary': '...'}.
            Separate each idea JSON object by '---'.

            Focus on explicitly mentioned ideas that would make good LinkedIn posts.
            Rate engagement based on:
            - Relevance to professional audience
            - Uniqueness of insight
            - Potential for discussion
            - Practical value
            """,
            result_type=str  # Expect a single string output
        )
    
    def process_transcript(self, transcript: Transcript) -> List[IdeaItem]:
        """Process a transcript and extract LinkedIn post ideas."""
        try:
            raw_output = self.agent.run_sync(transcript)
            ideas = []
            
            # Split the output into individual idea strings
            idea_strings = [s.strip() for s in raw_output.split("---") if s.strip()]
            
            for idea_string in idea_strings:
                try:
                    # Parse JSON and create IdeaItem
                    idea_data = json.loads(idea_string)
                    idea_item = IdeaItem(**idea_data)
                    ideas.append(idea_item)
                except json.JSONDecodeError as e:
                    print(f"Failed to parse idea JSON: {e}")
                    continue
                except ValueError as e:
                    print(f"Failed to create IdeaItem: {e}")
                    continue
            
            return ideas
        except Exception as e:
            print(f"Error processing transcript: {e}")
            return []