from google.adk.agents import Agent
from google.adk.tools import google_search

from . import prompt

web_searcher_agent = Agent(
  name='google_search_tool',
  model='gemini-2.0-flash',
  instruction= prompt.WEB_SEARCHER_PROMPT,
  description='To search for nearby hospitals within the user\'s given location and return detailed information.',
  tools=[
    google_search
  ]
)
