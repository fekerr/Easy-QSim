"""
input_yaml - Input plugin for loading circuits from YAML files.

This module provides the 'load_input' function required by the main
qvqsim script to parse circuit descriptions from YAML files.

NOTE: This is currently a stub implementation. It requires the 'PyYAML'
      library to be installed (`pip install pyyaml`). It needs to be
      developed to actually parse a defined YAML schema for quantum circuits.
"""

import os
try:
    import yaml
except ImportError:
    print("Error: PyYAML library not found. Please install it: pip install pyyaml")
    yaml = None # Set to None to handle import error gracefully

def load_input(file_path):
    """
    Loads quantum circuit description from a YAML file.

    Args:
        file_path (str): The path to the YAML input file.

    Returns:
        dict: A dictionary representing the circuit data.
              Expected format (example):
              num_qubits: 2
              shots: 1024
              circuit:
                - ["H", 0]
                - ["CX", 0, 1]
                - ["Measure", ]
              Returns an empty dict if the file doesn't exist, is invalid,
              or PyYAML is not installed.

    Raises:
        FileNotFoundError: If the file_path does not exist.
        yaml.YAMLError: If the file is not valid YAML.
        Exception: For other potential file reading errors.
    """
    if not yaml:
        print("[input_yaml] Error: PyYAML library is required but not installed.")
        return {} # Cannot function without yaml library

    print(f"[input_yaml] Attempting to load: {file_path}")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Input file not found: {file_path}")

    try:
        with open(file_path, 'r') as f:
            # Use safe_load to prevent arbitrary code execution
            data = yaml.safe_load(f)
            print(f"[input_yaml] Successfully loaded data.")
            # TODO: Add validation against a defined circuit YAML schema.
            # Handle case where YAML is empty or just comments
            return data if data else {}
    except yaml.YAMLError as e:
        print(f"[input_yaml] Error: Invalid YAML format in {file_path}: {e}")
        raise # Re-raise the specific error
    except Exception as e:
        print(f"[input_yaml] Error reading file {file_path}: {e}")
        raise # Re-raise other exceptions

# Example usage (for testing the stub)
if __name__ == "__main__":
    if not yaml:
        print("Skipping input_yaml test because PyYAML is not installed.")
    else:
        # Create a dummy YAML file for testing
        dummy_file = "dummy_circuit.yaml"
        dummy_yaml_content = """
num_qubits: 3
shots: 2000
circuit:
  - ["H", 0]
  - ["CX", 0, 1]
  - # Example Rx gate
"""
        with open(dummy_file, 'w') as f:
            f.write(dummy_yaml_content)

        print(f"--- Testing input_yaml stub with {dummy_file} ---")
        try:
            loaded_data = load_input(dummy_file)
            print("Loaded data:")
            # Print using yaml dump for consistent formatting
            print(yaml.dump(loaded_data, default_flow_style=False))
        except Exception as e:
            print(f"Test failed: {e}")
        finally:
            # Clean up the dummy file
            if os.path.exists(dummy_file):
                os.remove(dummy_file)
        print("--- End input_yaml test ---")
