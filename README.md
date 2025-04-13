# Google ADK Agents

This repository contains sample agents built with Google's Agent Development Kit (ADK). These agents showcase various capabilities of the ADK framework for building intelligent, task-oriented conversational agents.

## Setup
### Using a Virtual Environment

It is a good practice to use a Python virtual environment to manage dependencies and avoid conflicts with other projects. To create and activate a virtual environment, run the following commands:

On macOS and Linux:
```
python3 -m venv venv
source venv/bin/activate
```

On Windows:
```
python -m venv venv
.\venv\Scripts\activate
```

Once the virtual environment is activated, you can install the necessary dependencies.

## Dependencies
The agent scripts use Google's `Agent Development Kit` to create different types of Agents. More information on setting up and using `google-adk` can be found in its [documentation](https://google.github.io/adk-docs/).

To install the necessary dependencies, run:

```bash
pip install -r requirements.txt
```

## Multi-Tool Agent

The [Multi-Tool Agent](multi_tool_agent/README.md) demonstrates how to create an agent with access to multiple tools for handling user requests. This agent can help with common tasks like checking weather, managing appointments, performing calculations, and providing date/time information.

The code exposes Python methods to the agent using `FunctionTool` and uses ReAct planning via `PlanReActPlanner`.

### Running the Agent

To run the Multi-Tool Agent:

```bash
# From the project root folder
adk run multi_tool_agent
```
