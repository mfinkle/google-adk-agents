import json
import re
import logging
from typing import Callable, Awaitable, TypeVar, Optional, Dict, Any
from google.adk.runners import Runner
from google.genai import types

T = TypeVar('T')  # Return type for the final response processor

async def extract_json_from_response(response: str) -> dict:
    """
    Extract JSON from LLM response with improved error handling
    
    Args:
        response: The raw text response from the agent
        
    Returns:
        Parsed JSON dictionary
        
    Raises:
        ValueError: If no valid JSON could be extracted
    """
    try:
        # First try parsing as full JSON if possible
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # Look for code block with JSON content
            json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', response)
            if json_match:
                return json.loads(json_match.group(1))
            
            # Look for JSON wrapped in FINAL_ANSWER markers
            final_answer_match = re.search(r'/\*FINAL_ANSWER\*/\s*([\s\S]*?)\s*(?:/\*END\*/|$)', response)
            if final_answer_match:
                return json.loads(final_answer_match.group(1))
            
            # Try to extract any JSON-like structure
            json_match = re.search(r'({[\s\S]*?})', response)
            if json_match:
                return json.loads(json_match.group(1))
            
            raise ValueError("No valid JSON found in response")
    except Exception as e:
        logging.error(f"Failed to parse response: {response}")
        raise ValueError(f"Failed to parse JSON from agent response: {e}\nResponse: {response}")


async def process_agent_response(
    runner: Runner,
    user_id: str,
    session_id: str,
    content: types.Content,
    on_final_response: Callable[[str], Awaitable[T]],
    verbose: bool = True
) -> Optional[T]:
    """
    Process agent responses with a callback for the final response
    
    Args:
        runner: The ADK Runner instance
        user_id: User ID for the session
        session_id: Session ID
        content: Content to send to the agent
        on_final_response: Callback for processing the final text response
        verbose: Whether to print event processing information
        
    Returns:
        The result from on_final_response callback
    """
    try:
        async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
            # Handle planning thoughts (if verbose)
            if verbose and event.content and event.content.parts:
                response_thought_raw = "".join([
                    part.text for part in event.content.parts 
                    if hasattr(part, 'text') and part.text and part.text.strip() 
                    and hasattr(part, 'thought') and part.thought
                ])
                planning_match = re.search(r'/\*(RE)?PLANNING\*/(.+?)/\*ACTION\*/', response_thought_raw, re.DOTALL)
                if planning_match:
                    planning_thought = planning_match.group(2).strip()
                    print(f"  Planning:\n{planning_thought}\n")
            
                reasoning_match = re.search(r'/\*REASONING\*/(.+?)/\*ACTION\*/', response_thought_raw, re.DOTALL)
                if reasoning_match:
                    reasoning_thought = reasoning_match.group(1).strip()
                    print(f"  Reasoning:\n{reasoning_thought}\n")

            # Handle tool calls (if verbose)
            if verbose and event.get_function_calls():
                func_calls = event.get_function_calls()
                print(f"  Tool Call: {func_calls[0].name}({func_calls[0].args})\n")
            elif verbose and event.get_function_responses():
                func_responses = event.get_function_responses()
                print(f"  Tool Result: {func_responses[0].name} -> {func_responses[0].response})\n")
                
            # Process final response
            if event.is_final_response() and event.content and event.content.parts:
                response_text = "".join([
                    part.text for part in event.content.parts 
                    if hasattr(part, 'text') and part.text and part.text.strip()
                ])
                
                return await on_final_response(response_text.strip())
        
        # If we get here, no final response was received
        if verbose:
            print("Warning: No final response received from agent")
        return None
        
    except Exception as e:
        logging.error(f"Error during agent response processing: {e}")
        if verbose:
            print(f"❌ ERROR: {e}")
        return None