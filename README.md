# Google ADK Agents

This repository contains sample agents built with Google's Agent Development Kit (ADK). These agents showcase various capabilities of the ADK framework for building intelligent, task-oriented conversational agents.

## Multi-Tool Agent

The [Multi-Tool Agent](multi_tool_agent/README.md) demonstrates how to create an agent with access to multiple tools for handling user requests. This agent can help with common tasks like checking weather, managing appointments, performing calculations, and providing date/time information.

The code exposes Python methods to the agent using `FunctionTool` and uses ReAct planning via `PlanReActPlanner`.

### Running the Agent

To run the Multi-Tool Agent:

```bash
# From the project root folder
adk run multi_tool_agent
```

# Requirements
* Google ADK
* Python 3.9+
* Additional dependencies specified in `requirements.txt`