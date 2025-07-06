from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from emergency.tools.dispatch import dispatch_ambulance


ambulance_dispatch_tool = FunctionTool(
    func=dispatch_ambulance
)

ambulance_dispatch_agent = Agent(
    model="gemini-2.0-flash-exp",
    name="ambulance_dispatch_agent",
    description="Handles emergency dispatch based on location queries.",
    instruction="""
        When the user provides a location:
        - First use google_search_agent to find nearby hospitals.
        - For each hospital, try dispatching an ambulance.
        - If dispatch succeeds, confirm with ETA.
        - If all fail, return a failure message.
    """,
    tools=[ambulance_dispatch_tool],
)
