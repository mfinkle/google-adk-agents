# JSONLogic Generator Agent

The JSONLogic Generator Agent creates logical rules from natural language descriptions using a two-step process:

1. **Intent Parsing**: First, the agent parses natural language into a structured intent representation that captures the logical conditions in a standardized format
2. **JSONLogic Generation**: Then, it transforms this intent structure into valid JSONLogic expressions that can be executed against data

This two-step approach provides several advantages:
- More reliable translation from natural language to logical rules
- Consistent structure that's easier for the LLM to generate correctly
- Better validation and error handling at each step
- Clearer separation between understanding intent and creating executable logic

The agent uses LLM reasoning capabilities to handle this translation process across various data domains.

## Features

- **Natural Language to JSONLogic**: Convert plain English descriptions into structured rule expressions
- **Schema-Aware**: Validate fields against a provided data schema with rich field metadata
- **Interactive Mode**: Test and refine rules through a command-line interface
- **Multiple Data Types**: Support different domains (user data, survey responses) through structured JSON files
- **Validation**: Test rules against sample data and compare against expected outcomes
- **Semantic Understanding**: Interpret the meaning and purpose of fields through descriptive metadata

## Tools

The JSONLogic Generator Agent uses specialized tools for creating and validating rules:

### JSONLogic Tools (`tools/jsonlogic.py`)
- `get_available_fields_from_schema`: Extract field information with descriptions and valid values
- `create_jsonlogic_from_intent`: Convert the LLM's structured intent into valid JSONLogic rules
- `validate_fields_from_jsonlogic`: Verify that field references exist in the schema

### Utility Modules
- `utils/event_processing.py`: Process agent responses and extract JSON content
- `utils/logging.py`: Configure standardized logging
- `utils/data_loader.py`: Load schema and sample data from JSON files
- `utils/jsonlogic_utils.py`: Test generated rules against sample data

## Data Sources

The project includes a few data sets to explore:

- **userdata.json**: User profiles with demographic data, subscriptions, and activity metrics
- **survey.json**: Product satisfaction survey responses with detailed question and answer structures

Each data file contains:
- `schema`: Detailed data structure with field types, descriptions, and valid values
- `sample_data`: Test instances for validating rules
- `descriptions`: Example rule descriptions
- `expected_results`: Expected outcomes for validation

## Running the Agent

```bash
# Basic usage with user data
python jsonlogic_agent/cli.py

# Specify a different data domain
python jsonlogic_agent/cli.py --data survey
```

## Architecture

The JSONLogic Generator is built on a simple, but modular structure:

- **Google ADK Framework**: Provides the foundation for agent capabilities
- **Gemini 2.0 Flash Model**: Powers the natural language understanding
- **PlanReActPlanner**: Enables multi-step reasoning for complex rule creation
- **Function Tools**: Execute specialized JSONLogic operations
- **Event Processing**: Manage agent communication flow with callback support
- **Schema Enhancement**: Provide rich field metadata for better semantic understanding

## High-Level Rule Intent Features

The agent primarily works by creating a structured intent representation that captures the logical conditions of the natural language rule description. Several high-level concepts and operations are made available to the agent when creating this intermediate structure. These operations are then converted into JSONLogic patterns in a deterministic manner by the tools. Here are some examples:

- **Between Checks**: Check if a value is between a lower and upper bound. Both exclusive and inclusive checks are available
- **Empty Checks**: Use `empty` and `notEmpty` to validate array presence
- **Length Checks**: Verify array `length` with operators like `lengthEquals`, `lengthGreaterThan`, and `lengthLessThan`
- **Contains**: Check if an array `contains` a specific value or any of multiple values

### Length Operation

The `length` operator (and variants) is actually implemented using the JSONLogic `reduce` operator. Using `length` as a high-level operator means the LLM can use a simple, consistent format without needing to work directly with JSONLogic.

### Contains Operation

The `contains` operator has been optimized for different use cases:

- For single values: Uses JSONLogic's efficient `in` operator
- For multiple values: Leverages JSONLogic's `some` with an `or` condition for better performance

## Testing Framework

The codebase includes a comprehensive testing setup:

- **Test Data Files**: Sample schemas and data in `/data/` for validating agent behavior
- **Test Cases**: Structured test cases that verify each operation works correctly
- **Runtime Validation**: Comparison of generated rule results against expected outcomes

## Example Rule Descriptions

Try these sample descriptions with the agent:

### User Data Examples
```
Find active users over 30 years old
Find users from the US with an active premium subscription
Find users who logged in more than 5 times and have the tag 'developer'
```

### Survey Data Examples
```
Find highly satisfied customers (overall satisfaction of 4 or 5) who use the product daily
Find responses from mobile devices where the user reported pain points related to mobile experience
Find customers who would recommend the product but rated value for money as 3 or lower
```

## Development

### Adding New Data Domains

1. Create a JSON file in the data directory with `schema`, `sample_data`, `descriptions`, and `expected_results` sections
2. Register the new data type in `TEST_DATA_MODULES` in cli.py

### Enhancing Schema Understanding

The agent uses rich metadata to understand field semantics:

```json
{
  "name": "questions.productUsage.usageDuration.response",
  "description": "How long the user has been using the product", 
  "type": "string",
  "values": ["less than 1 month", "1-3 months", "3-6 months", "6-12 months", "more than 1 year"]
}
```

### Extending JSONLogic Capabilities

To add support for new JSONLogic operations:
1. Update the operator map in `create_jsonlogic_from_intent`
2. Add processing logic for the new operation
3. Update the system prompt to explain the new capability

## Interactive Mode

The CLI includes an interactive mode for testing and refining rules:

1. Run the agent with your chosen data type
2. After processing sample descriptions, the interactive prompt appears
3. Enter natural language descriptions of rules
4. See the generated JSONLogic rule and test results immediately
5. Type `exit` or `quit` to end the session

## Code Organization

- `agent.py`: Core agent definition with tool registration
- `cli.py`: Command-line interface for batch and interactive modes
- `prompt.py`: System prompt guiding the agent's behavior
- `tools/jsonlogic.py`: JSONLogic generation and validation tools
- `utils/`: Shared utility functions for processing, logging, and testing
- `data/`: JSON schema and sample data files
