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
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is not set")
            
        self.model = AnthropicModel(
            model_name="claude-3-5-sonnet-latest",
            api_key=api_key
        )
        self.agent = Agent(
            model=self.model,
            system_prompt="""You are an expert at analyzing transcripts and identifying potential LinkedIn post ideas.

For each idea you find, output a valid JSON object with exactly this structure:
{
    "idea": "Brief title of the idea",
    "category": "Category of the post (e.g., AI, Business, Technology)",
    "engagement": <number between 1 and 5>,
    "mentioned_by": "Name of person who mentioned it, or null if not specified",
    "summary": "Detailed summary of the idea"
}

After each complete JSON object, add three dashes (---) as a separator.

Rate engagement on a scale of 1 to 5 (never higher) based on:
- Relevance to professional audience
- Uniqueness of insight
- Potential for discussion
- Practical value

Example output format:
{
    "idea": "AI Implementation Guide",
    "category": "Technology",
    "engagement": 4,
    "mentioned_by": "Sarah",
    "summary": "Step-by-step guide for small businesses to start their AI journey"
}
---
{
    "idea": "Next idea title",
    "category": "Next category",
    "engagement": 3,
    "mentioned_by": null,
    "summary": "Next summary"
}""",
            result_type=str  # Expect a single string output
        )
    
    def process_transcript(self, transcript: Transcript) -> List[IdeaItem]:
        """Process a transcript and extract LinkedIn post ideas."""
        try:
            # Get RunResult from agent
            result = self.agent.run_sync(transcript.text)
            # Access the output text using .data
            raw_output = result.data
            ideas = []
            
            # Split the output into individual idea strings
            idea_strings = [s.strip() for s in raw_output.split("---") if s.strip()]
            print(f"Raw output: {raw_output}")  # Debug print
            print(f"Found {len(idea_strings)} potential ideas")  # Debug print
            
            for idea_string in idea_strings:
                try:
                    # Parse JSON and create IdeaItem
                    print(f"Processing idea string: {idea_string}")  # Debug print
                    idea_data = json.loads(idea_string)
                    idea_item = IdeaItem(**idea_data)
                    ideas.append(idea_item)
                except json.JSONDecodeError as e:
                    print(f"Failed to parse idea JSON: {e}")
                    print(f"Problematic string: {idea_string}")  # Debug print
                    continue
                except ValueError as e:
                    print(f"Failed to create IdeaItem: {e}")
                    print(f"Problematic data: {idea_data}")  # Debug print
                    continue
            
            return ideas
        except Exception as e:
            print(f"Error processing transcript: {e}")
            return []