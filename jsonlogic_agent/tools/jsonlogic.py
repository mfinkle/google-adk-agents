from typing import Dict, Any, List, Optional
import json

from google.adk.tools import ToolContext
from google.genai.types import Part
from google.genai import types

def create_jsonlogic_from_intent(parsed_intent: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert the parsed intent structure to a JSONLogic rule.
    
    Args:
        parsed_intent: The structured representation from the LLM
        
    Returns:
        A JSONLogic rule as a dictionary
        
    Example:
        >>> create_jsonlogic_from_intent({"operation": "AND", "conditions": [{"field": "age", "operator": "greaterThan", "value": 18}]})
        {"and": [{">": [{"var": "age"}, 18]}]}
    """
    # Map our standard intent operator names directly to JSONLogic operators
    operator_map = {
        # Logical operators (with both cases for flexibility)
        "AND": "and",
        "and": "and",
        "OR": "or", 
        "or": "or",
        "NOT": "!",
        "not": "!",
        
        # Comparison operators
        "equals": "==",
        "notEquals": "!=",
        "greaterThan": ">",
        "lessThan": "<",
        "greaterOrEqual": ">=",
        "lessOrEqual": "<=",
        
        # Range operators
        "between": "between",
        "betweenOrEqual": "betweenOrEqual",
        
        # Array operations
        "empty": "empty",
        "notEmpty": "notEmpty",
        "length": "length",
        "lengthEquals": "lengthEquals",
        "lengthGreaterThan": "lengthGreaterThan",
        "lengthLessThan": "lengthLessThan",
        "contains": "contains",
        
        # String operations
        "startsWith": "startsWith",
        "endsWith": "endsWith",
        
        # Item check operations (Array and String)
        "contains": "contains",
    }
    
    # Helper function to create array length logic
    def create_length_logic(field):
        return {"reduce": [
            {"var": field},
            {"+": [1, {"var": "accumulator"}]},
            0
        ]}
    
    # Process a single condition or a nested structure
    def process_node(node):
        # If this is a leaf condition
        if "field" in node and "operator" in node:
            field = node["field"]
            op = node["operator"]  # Use the operator exactly as provided
            value = node.get("value")
            
            # Map to JSONLogic operator - direct lookup with fallback
            jsonlogic_op = operator_map.get(op, op)
            
            # Create the appropriate JSONLogic structure
            if jsonlogic_op in ["==", "!=", ">", "<", ">=", "<="]:
                return {jsonlogic_op: [{"var": field}, value]}
            elif jsonlogic_op == "!":
                # Negation of a condition
                inner_condition = process_node({"field": field, "operator": node.get("negatedOperator", "=="), "value": value})
                return {"!": inner_condition}
            elif jsonlogic_op == "between":
                # Between operation requires lower and upper bounds
                if isinstance(value, list) and len(value) == 2:
                    return {"<": [value[0], {"var": field}, value[1]]}
                
                raise ValueError(f"Between operation requires lower and upper bounds: {node}")
            elif jsonlogic_op == "betweenOrEqual":
                # BetweenOrEqual operation requires lower and upper bounds
                if isinstance(value, list) and len(value) == 2:
                    return {"<=": [value[0], {"var": field}, value[1]]}
                
                raise ValueError(f"BetweenOrEqual operation requires lower and upper bounds: {node}")
            elif jsonlogic_op == "empty":
                return {"==": [{"var": field}, []]}
            elif jsonlogic_op == "notEmpty":
                return {"!=": [{"var": field}, []]}
            elif jsonlogic_op == "length":
                # Just calculate array length
                return create_length_logic(field)
            elif jsonlogic_op == "lengthEquals":
                # Compare array length with a value
                return {"==": [create_length_logic(field), value]}
            elif jsonlogic_op == "lengthGreaterThan":
                # Check if array length is greater than a value
                return {">": [create_length_logic(field), value]}
            elif jsonlogic_op == "lengthLessThan":
                # Check if array length is less than a value
                return {"<": [create_length_logic(field), value]}
            elif jsonlogic_op == "startsWith":
                # Check if a string starts with a prefix
                prefix = value
                return {"and": [
                    {"var": field},  # Ensure field exists
                    {"==": [
                        {"substr": [{"var": field}, 0, len(str(prefix))]},
                        prefix
                    ]}
                ]}
            elif jsonlogic_op == "endsWith":
                # Check if a string ends with a suffix
                suffix = value
                suffix_len = len(str(suffix))
                return {"and": [
                    {"var": field},  # Ensure field exists
                    {"==": [
                        {"substr": [
                            {"var": field}, 
                            {"-": [{"var": {"var": field, "default": ""}}, suffix_len]}, 
                            suffix_len
                        ]},
                        suffix
                    ]}
                ]}
            elif jsonlogic_op == "contains":
                # Check if an array contains specific value(s)
                if isinstance(value, list):
                    # For multiple values, use "some" for more control
                    # "some" checks if at least one array element satisfies the condition
                    items_to_check = []
                    for item in value:
                        items_to_check.append({"==": [{"var": ""}, item]})
                        
                    return {"some": [
                        {"var": field},
                        {"or": items_to_check}  # At least one of these must match
                    ]}
                else:
                    # For a single value, use the more concise "in"
                    return {"in": [value, {"var": field}]}
            else:
                # For any other operators
                return {jsonlogic_op: [{"var": field}, value]}
        
        # If this is a composite condition with nested logic
        elif "operation" in node and "conditions" in node:
            # Direct lookup of operation
            operation = node["operation"]
            jsonlogic_op = operator_map.get(operation, operation)
            
            # Process all child conditions
            conditions = [process_node(condition) for condition in node["conditions"]]
            
            # Special handling for NOT
            if jsonlogic_op == "!":
                # NOT should have only one child condition
                if len(conditions) == 1:
                    return {"!": conditions[0]}
                else:
                    # If multiple conditions, wrap them in AND first
                    return {"!": {"and": conditions}}
            else:
                # For AND, OR, etc.
                return {jsonlogic_op: conditions}
        
        # Handle unexpected node structure
        else:
            raise ValueError(f"Invalid node structure in parsed intent: {node}")
    
    # Rest of the function remains the same
    if "operation" in parsed_intent and "conditions" in parsed_intent:
        # This is already a structured intent
        return process_node(parsed_intent)
    elif "conditions" in parsed_intent:
        # Default to AND if no operation specified
        parsed_intent["operation"] = "AND"
        return process_node(parsed_intent)
    elif "field" in parsed_intent and "operator" in parsed_intent:
        # This is a single condition without the standard wrapper structure
        # Process it directly
        return process_node(parsed_intent)
    elif len(parsed_intent) == 1:
        # Single condition without explicit operation/conditions structure
        for key, value in parsed_intent.items():
            if isinstance(value, dict):
                return process_node(value)
        # If not found, treat the whole thing as a single condition
        return process_node(parsed_intent)
    else:
        # Try to interpret as a flat set of conditions with implicit AND
        conditions = []
        for key, value in parsed_intent.items():
            if isinstance(value, dict) and "field" in value:
                conditions.append(value)
        
        if conditions:
            return process_node({"operation": "AND", "conditions": conditions})
        else:
            raise ValueError(f"Could not interpret parsed intent as JSONLogic: {parsed_intent}")

def get_available_fields_from_schema(tool_context: ToolContext, filter_usable: bool = True) -> Dict[str, Any]:
    """
    Get all available fields from the data schema with their descriptions when available.
    
    Args:
        filter_usable: If True, returns only fields that can be used directly in JSONLogic operations
        
    Returns:
        Dictionary with status and a list of field information objects
        
    Example:
        >>> get_available_fields_from_schema()
        {
            "status": "success", 
            "fields": [
                {
                    "name": "questions.productUsage.usageDuration.response",
                    "description": "How long the user has been using the product", 
                    "type": "string",
                    "values": ["less than 1 month", "1-3 months", "3-6 months", "6-12 months", "more than 1 year"]
                },
                {
                    "name": "questions.satisfaction.overallSatisfaction.response",
                    "description": "User's overall satisfaction rating of the product",
                    "type": "number",
                    "range": [1, 5]
                }
            ]
        }
    """
    field_info = tool_context.state.get("field_info", [])
    if not field_info:
        schema_artifact = tool_context.load_artifact("schema.json")
        if schema_artifact and schema_artifact.text:
            field_info = _extract_field_info(schema_artifact.text)
            tool_context.state["field_info"] = field_info
    
    if filter_usable:
        # Filter the field list to include only those usable in JSONLogic operations
        usable_fields = []
        for field in field_info:
            # Skip fields that are objects without value-related properties
            if field.get("type") == "object" and not any(k in field for k in ["values", "range"]):
                continue
                
            # Skip fields with a wildcard in the name (these are usually container patterns)
            if ".*" in field.get("name", ""):
                continue
                
            # Skip parent object paths (e.g., "questions.productUsage" when "questions.productUsage.usageFrequency" exists)
            is_parent_path = False
            for other_field in field_info:
                if other_field["name"] != field["name"] and other_field["name"].startswith(field["name"] + "."):
                    is_parent_path = True
                    break
                    
            if not is_parent_path:
                # This appears to be a leaf field or terminal value
                usable_fields.append(field)
        
        return {
            "status": "success",
            "fields": usable_fields
        }
    
    # Return all fields if not filtering
    return {
        "status": "success",
        "fields": field_info
    }

def validate_fields_from_jsonlogic(fields: List[str], tool_context: ToolContext) -> Dict[str, Any]:
    """
    Validate that JSONLogic 'var' fields exist in the schema.
    
    Args:
        fields: List of fields to validate
        
    Returns:
        Dictionary with validation results
    """
    field_info = tool_context.state.get("field_info", [])
    if not field_info:
        schema_artifact = tool_context.load_artifact("schema.json")
        if schema_artifact and schema_artifact.text:
            field_info = _extract_field_info(schema_artifact.text)
            tool_context.state["field_info"] = field_info
    
    # Extract field names and their types for validation
    available_fields = {field["name"]: field.get("type", "") for field in field_info}

    invalid_fields = []
    for field in fields:
        # Handle array indexing with dot notation (e.g., object.array.0)
        if '.' in field:
            # Split by dots to handle nested paths
            parts = field.split('.')
            
            # Check if last part is a numeric index
            if parts[-1].isdigit():
                # Remove the index and check if the base path exists and is an array
                base_field = '.'.join(parts[:-1])
                if base_field in available_fields and available_fields[base_field] == "array":
                    continue
            
        # If it's not a valid array index reference, do a regular check
        if field not in available_fields:
            invalid_fields.append(field)
            
    return {
        "is_valid": len(invalid_fields) == 0,
        "invalid_fields": invalid_fields
    }

def _extract_field_info(schema: str) -> List[Dict[str, Any]]:
    """
    Extract field information including names, descriptions, and types from the schema.
    
    Args:
        schema: JSON schema as a string
        
    Returns:
        List of field information objects with name, description, and type
    """
    field_info = []  # List to store field information objects
    
    def extract_fields(schema, path=""):
        if not isinstance(schema, dict):
            return
        
        # Extract field description and other metadata
        field_data = {
            "name": path
        }
        
        # Add description if available
        if "description" in schema:
            field_data["description"] = schema["description"]
            
        # Add type information
        if "type" in schema:
            field_data["type"] = schema["type"]
            
        # Add enum values if available
        if "enum" in schema:
            field_data["values"] = schema["enum"]
            
        # Add range for numeric types
        if "minimum" in schema and "maximum" in schema:
            field_data["range"] = [schema["minimum"], schema["maximum"]]
            
        # Add the field info if we have a path (skip the root)
        if path:
            field_info.append(field_data)
        
        # Process properties
        if "properties" in schema:
            for prop_name, prop_schema in schema["properties"].items():
                field_path = f"{path}.{prop_name}" if path else prop_name
                extract_fields(prop_schema, field_path)
        
        # Handle object without properties
        if schema.get("type") == "object" and "properties" not in schema:
            field_info.append({
                "name": f"{path}.*",
                "description": "Dynamic object with arbitrary properties",
                "type": "object"
            })
        
        # Handle arrays
        if schema.get("type") == "array" and "items" in schema:
            # Add the array field itself
            field_data["type"] = "array"
            
            # If array items have properties, process them
            if isinstance(schema["items"], dict):
                if "properties" in schema["items"]:
                    extract_fields(schema["items"], f"{path}.*")

    schema_dict = json.loads(schema)
    extract_fields(schema_dict)
    
    return sorted(field_info, key=lambda x: x["name"])
