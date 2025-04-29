"""
input_json - Input plugin for loading circuits from JSON files.

This module provides the 'load_input' function required by the main
qvqsim script to parse circuit descriptions from JSON files.

NOTE: This is currently a stub implementation. It needs to be developed
      to actually parse a defined JSON schema for quantum circuits.
"""

import json
import os

def load_input(file_path):
    """
    Loads quantum circuit description from a JSON file.

    Args:
        file_path (str): The path to the JSON input file.

    Returns:
        dict: A dictionary representing the circuit data.
              Expected format (example):
              {
                  "num_qubits": 2,
                  "shots": 1024,
                  "circuit": ["H", 0],
                      ["CX", 0, 1],
                      ["Measure", ]
              }
              Returns an empty dict if the file doesn't exist or is invalid.

    Raises:
        FileNotFoundError: If the file_path does not exist.
        json.JSONDecodeError: If the file is not valid JSON.
        Exception: For other potential file reading errors.
    """
    print(f"[input_json] Attempting to load: {file_path}")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Input file not found: {file_path}")

    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            print(f"[input_json] Successfully loaded data.")
            # TODO: Add validation against a defined circuit JSON schema.
            return data
    except json.JSONDecodeError as e:
        print(f"[input_json] Error: Invalid JSON format in {file_path}: {e}")
        raise # Re-raise the specific error
    except Exception as e:
        print(f"[input_json] Error reading file {file_path}: {e}")
        raise # Re-raise other exceptions

# Example usage (for testing the stub)
if __name__ == "__main__":
    # Create a dummy JSON file for testing
    dummy_file = "dummy_circuit.json"
    dummy_data = {
        "num_qubits": 2,
        "shots": 500,
        "circuit": ["H", 0],
            ["CX", 0, 1]
    }
    with open(dummy_file, 'w') as f:
        json.dump(dummy_data, f, indent=2)

    print(f"--- Testing input_json stub with {dummy_file} ---")
    try:
        loaded_data = load_input(dummy_file)
        print("Loaded data:")
        print(json.dumps(loaded_data, indent=2))
    except Exception as e:
        print(f"Test failed: {e}")
    finally:
        # Clean up the dummy file
        if os.path.exists(dummy_file):
            os.remove(dummy_file)
    print("--- End input_json test ---")
