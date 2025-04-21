"""
Utilities for working with JSONLogic rules.
This module provides functions to validate and test JSONLogic rules.
"""

import json
from typing import Dict, Any, List, Optional
import json_logic

class JSONLogicUtils:
    @staticmethod
    def validate_syntax(rule: Dict[str, Any]) -> bool:
        """
        Validate the syntax of a JSONLogic rule.
        Returns True if valid, raises an exception if invalid.
        
        Note: This is a simplified implementation and would need a proper
        JSONLogic validator for production use.
        """
        # Check if the rule is a dictionary
        if not isinstance(rule, dict):
            raise ValueError("JSONLogic rule must be a dictionary")
            
        # Check if the rule has at least one key (operator)
        if len(rule) == 0:
            raise ValueError("JSONLogic rule must have at least one operator")
            
        # Basic recursive validation
        def validate_object(obj):
            if isinstance(obj, dict):
                # Each key should be a valid JSONLogic operator
                for key in obj.keys():
                    if key not in JSONLogicUtils.valid_operators() and key != "var":
                        print(f"Warning: '{key}' is not a standard JSONLogic operator")
                
                # Each value should be valid
                for value in obj.values():
                    validate_object(value)
            elif isinstance(obj, list):
                for item in obj:
                    validate_object(item)
        
        validate_object(rule)
        return True
    
    @staticmethod
    def valid_operators() -> List[str]:
        """Return a list of standard JSONLogic operators."""
        return [
            # Logic
            "and", "or", "!",
            # Comparison
            "==", "===", "!=", "!==", ">", ">=", "<", "<=",
            # Numeric
            "+", "-", "*", "/", "%",
            # Array operations
            "in", "cat", "substr", "merge",
            # Misc
            "if", "missing", "missing_some", "var"
        ]
    
    @staticmethod
    def test_rule(rule: Dict[str, Any], data: Dict[str, Any]) -> Any:
        """
        Test a JSONLogic rule against data.
        """
        return json_logic.jsonLogic(rule, data)
