# Multi-Tool Agent

The Multi-Tool Agent demonstrates how to create an agent with access to multiple tools for handling user requests. This agent can help with common tasks like checking weather, managing appointments, performing calculations, and providing date/time information.

## Features

- **Weather Information**: Get current weather conditions for a location
- **Appointment Management**: View, book, and cancel appointments for various specialties
- **Date and Time**: Get the current date and time
- **Location Services**: Get current location or find zip codes
- **Calculations**: Perform basic mathematical calculations

## Tools

The Multi-Tool Agent uses several tools organized into modules:

### Utility Tools (`utils.py`)
- `get_weather`: Get weather conditions for a zip code
- `get_zipcode`: Find the zip code for a location
- `get_current_location`: Get the user's current location
- `get_datetime`: Get the current date and time
- `calculate`: Perform mathematical calculations

### Appointment Tools (`appointments.py`)
- `get_appointment_specialties`: List available appointment specialties
- `get_available_appointments`: Find open appointments by specialty
- `get_appointment_details`: Get details for a specific appointment
- `book_appointment`: Reserve an appointment
- `cancel_appointment`: Cancel a booked appointment
- `get_my_appointments`: View all booked appointments

## Running the Agent

To run the Multi-Tool Agent:

```bash
# From the project root folder
adk run multi_tool_agent
```

## Architecture
The Multi-Tool Agent is built using:

* Google's ADK framework
* Gemini 2.0 Flash model for natural language understanding
* `PlanReActPlanner` for orchestrating multi-step interactions
* Python functions for executing specific actions using `FunctionTool`

## Example Interactions
Try these sample queries with the agent:

* "What's the weather today?"
* "I need to book a dentist appointment"
* "What's 234 * 15.7?"
* "What's the current date and time?"
* "Cancel my upcoming appointment"
* "What's the zip code for Beverly Hills?"

## Development
### Adding New Tools
To add new tools to the agent:

1. Create functions in the appropriate module
2. Ensure each function has proper docstrings with examples
3. Register the function as a tool in `agent.py`

### Testing
Currently, the agent uses mock data for tools like weather and appointments. In a production environment, these would be connected to real APIs.
