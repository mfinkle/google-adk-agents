"""Utilities for loading test data from JSON files"""
import json
import os
from typing import Dict, Any, Optional

def load_test_data(data_type: str) -> Dict[str, Any]:
    """
    Load test data from a JSON file
    
    Args:
        data_type: The type of data to load (e.g., "userdata", "survey")
        
    Returns:
        A dictionary containing the test data
    """
    # Determine path to JSON file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(os.path.dirname(current_dir), "data")
    json_path = os.path.join(data_dir, f"{data_type}.json")
    
    # Check if file exists
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Test data file not found: {json_path}")
    
    # Load and return the data
    with open(json_path, 'r') as f:
        return json.load(f)

def get_schema(data_type: str) -> Dict[str, Any]:
    """Get schema from test data"""
    return load_test_data(data_type)["schema"]

def get_sample_data(data_type: str, named_set="primary") -> Dict[str, Any]:
    """Get sample data from test data"""
    return load_test_data(data_type)["sample_data"][named_set]

def get_descriptions(data_type: str) -> list:
    """Get descriptions from test data"""
    return load_test_data(data_type)["descriptions"]

def get_expected_results(data_type: str, named_set="primary") -> Optional[Dict[str, Any]]:
    """Get expected results from test data if available"""
    data = load_test_data(data_type)
    return data.get("expected_results", {}).get(named_set, {})