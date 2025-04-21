import json
import asyncio
import argparse
import importlib
from agent import root_agent
from utils.jsonlogic_utils import JSONLogicUtils
from utils.event_processing import process_agent_response, extract_json_from_response
from utils.logging import setup_logging
from utils.data_loader import get_schema, get_sample_data, get_descriptions, get_expected_results

from google.adk.artifacts import InMemoryArtifactService
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

from dotenv import load_dotenv

# Available test data modules
TEST_DATA_MODULES = {
    "userdata": "test_data_userdata",
    "survey": "test_data_survey"
}

async def process_descriptions(agent, session, session_service, artifact_service, descriptions, sample_data, expected_results=None):
    """Process a list of descriptions and generate JSONLogic rules for each."""
    success_count = 0
    total_count = 0
    
    runner = Runner(agent=agent, app_name=session.app_name, session_service=session_service, artifact_service=artifact_service)

    for description in descriptions:
        total_count += 1
        print(f"\n{'='*50}\nDescription: {description}\n{'='*50}")
        
        content = types.Content(role='user', parts=[types.Part(text=description)])

        async def handle_final_response(response_text):
            nonlocal success_count
            
            try:
                rule = await extract_json_from_response(response_text)
                print(f"\nGenerated JSONLogic rule:")
                print(json.dumps(rule, indent=2))
                
                # Test the rule against sample data
                result = JSONLogicUtils.test_rule(rule, sample_data)
                print(f"\nTest result against sample data: {result}")
                
                # Validate against expected results if available
                if expected_results and description in expected_results:
                    expected = expected_results[description]
                    if result == expected:
                        print(f"✅ PASS - Result matches expected outcome: {expected}")
                        success_count += 1
                    else:
                        print(f"❌ FAIL - Result {result} doesn't match expected outcome: {expected}")
                
                return rule, result
            except ValueError as e:
                print(f"Error processing response: {e}")
                return None, None
            
        await process_agent_response(runner, session.user_id, session.id, content, on_final_response=handle_final_response)

    # Print summary
    if expected_results:
        print(f"\n\nValidation summary: {success_count}/{total_count} rules matched expected results")
        return success_count, total_count
    
    return None


async def interactive_mode(agent, session, session_service, artifact_service, sample_data):
    """Run an interactive session allowing users to input descriptions."""
    runner = Runner(agent=agent, app_name=session.app_name, session_service=session_service, artifact_service=artifact_service)

    print(f"\n\n{'='*50}\nInteractive Mode\n{'='*50}\nType your rule description (or 'exit' to quit):")
    
    while True:
        user_input = input("> ")
        if user_input.lower() in ['exit', 'quit']:
            break

        content = types.Content(role='user', parts=[types.Part(text=user_input)])

        async def handle_final_response(response_text):
            try:
                rule = await extract_json_from_response(response_text)
                print(f"\nGenerated JSONLogic rule:")
                print(json.dumps(rule, indent=2))
                
                # Test the rule against sample data
                result = JSONLogicUtils.test_rule(rule, sample_data)
                print(f"\nTest result against sample data: {result}")
                
                return rule, result
            except Exception as e:
                print(f"Error processing response: {e}")
                return None, None

        await process_agent_response(runner, session.user_id, session.id, content, on_final_response=handle_final_response)


def load_test_data_module(module_name):
    """Dynamically import the specified test data module."""
    try:
        # Prepend the 'data.' prefix to look in the data subfolder
        module = importlib.import_module(f"data.{module_name}")
        return module
    except ImportError:
        available = ", ".join(TEST_DATA_MODULES.keys())
        raise ImportError(f"Test data module '{module_name}' not found. Available options: {available}")


async def main_async(data_type):
    """Main async function that orchestrates the example."""
    # Set up logging
    setup_logging()

    APP_NAME = "jsonlogic_generator"
    USER_ID = "user_1"
    SESSION_ID = "session_001"

    artifact_service = InMemoryArtifactService()
    session_service = InMemorySessionService()
    session = session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    
    # Load data from JSON files
    schema = get_schema(data_type)
    sample_data = get_sample_data(data_type)
    descriptions = get_descriptions(data_type)
    expected_results = get_expected_results(data_type)
    
    print(f"Using test data from {data_type}.json")
    
    artifact_service.save_artifact(
        app_name=session.app_name, 
        user_id=session.user_id, 
        session_id=session.id,
        filename="schema.json", 
        artifact=types.Part(text=json.dumps(schema))
    )
    
    # Process all descriptions with expected results
    await process_descriptions(root_agent, session, session_service, artifact_service, descriptions, sample_data, expected_results)
    
    # Run interactive mode
    await interactive_mode(root_agent, session, session_service, artifact_service, sample_data)


def main():    
    """Entry point that runs the async code with asyncio."""
    load_dotenv()
    
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="JSONLogic Generator Agent")
    parser.add_argument(
        '--data', 
        choices=TEST_DATA_MODULES.keys(), 
        default='userdata',
        help='Test data type to use'
    )
    args = parser.parse_args()

    asyncio.run(main_async(args.data))

if __name__ == "__main__":
    main()