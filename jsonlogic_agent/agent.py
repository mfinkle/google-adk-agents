from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from google.adk.planners import PlanReActPlanner
from google.genai import types

from tools.jsonlogic import create_jsonlogic_from_intent, validate_fields_from_jsonlogic, get_available_fields_from_schema
from prompt import SYSTEM_PROMPT

root_agent = Agent(
    name="jsonlogic_agent",
    model="gemini-2.0-flash",
    instruction=SYSTEM_PROMPT,
    generate_content_config=types.GenerateContentConfig(
        temperature=0 # More deterministic output
    ),
    planner=PlanReActPlanner(),
    tools=[
        FunctionTool(func=create_jsonlogic_from_intent),
        FunctionTool(func=validate_fields_from_jsonlogic),
        FunctionTool(func=get_available_fields_from_schema),
    ],
)