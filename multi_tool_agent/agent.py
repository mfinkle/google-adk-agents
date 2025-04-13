from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from google.adk.planners import PlanReActPlanner
from google.genai import types

from .tools.utils import get_weather, get_current_location, get_datetime, get_zipcode, calculate
from .tools.appointments import get_appointment_specialties, get_available_appointments, get_appointment_details, book_appointment, cancel_appointment 
from .prompt import SYSTEM_PROMPT


root_agent = Agent(
    name="multi_tool_agent",
    model="gemini-2.0-flash", #"gemini-2.0-flash-exp",
    instruction=SYSTEM_PROMPT,
    generate_content_config=types.GenerateContentConfig(
        temperature=0 # More deterministic output
    ),
    planner=PlanReActPlanner(),
    tools=[
        FunctionTool(func=get_weather),
        FunctionTool(func=get_datetime),
        FunctionTool(func=get_current_location),
        FunctionTool(func=get_zipcode),
        FunctionTool(func=calculate),
        FunctionTool(func=get_appointment_specialties),
        FunctionTool(func=get_available_appointments),
        FunctionTool(func=get_appointment_details),
        FunctionTool(func=book_appointment),
        FunctionTool(func=cancel_appointment),
    ],
)