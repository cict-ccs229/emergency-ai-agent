from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.google_search_tool import google_search

search_agent = Agent (
    name="Search_Agent_Grounding",
    model="gemini-2.5-flash-preview-05-20",
    description=(
        "Agent to provide grounding for google search results for admiral agent"
    ),
    instruction=("""
    Answer the user's question by providing a concise and accurate response based on the search results.
    Use the search results to supplement your answer, especially if the user asks for specific details, or a ship or battle is obscure, but do not simply repeat the search results.
    If the search results do not provide a clear answer, state that you could not find relevant information.
    Use the search results to provide a source at the end of your response.
    If the user asks for an image, provide a direct link to the image if available in the search results.
    If the user asks for a video on the topic, provide a youtube link to the video
    IMPORTANT:
    - Ensure that the youtube video matches the user's query
    - Ensure that the video is still related to World War 2 Naval History
    - Ensure that the video is factual and is not related to a game or series.
    """
    ),
    tools=[google_search],
)

Search_Agent_Grounding = AgentTool(agent=search_agent)
    