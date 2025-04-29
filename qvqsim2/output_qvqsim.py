"""
output_qvqsim - Output plugin for formatting results in a standard format.

This module provides the 'output_results' function required by the main
qvqsim script to format and output the simulation results.
"""

import json
import sys

def output_results(results, output_path=None):
    """
    Outputs the simulation results.

    Currently prints the results dictionary to the console (if output_path is None)
    or writes it as a JSON string to the specified file.

    Args:
        results (dict): The dictionary containing simulation results (e.g., counts).
                        Example: {'00': 512, '11': 512}
        output_path (str, optional): The path to the file where results
                                     should be written. If None, prints to stdout.
    """
    try:
        # Format the results as a JSON string for consistent output
        results_str = json.dumps(results, indent=2)

        if output_path:
            # Write to file
            with open(output_path, 'w') as f:
                f.write(results_str)
                f.write('\n') # Add a newline for better file handling
            print(f"[output_qvqsim] Results written to {output_path}")
        else:
            # Print to console
            print("[output_qvqsim] Simulation Results:")
            print(results_str)

    except TypeError as e:
        print(f"[output_qvqsim] Error: Results object is not JSON serializable: {results}", file=sys.stderr)
        print(f"Error details: {e}", file=sys.stderr)
        # Fallback: try printing raw results
        if not output_path:
             print("\n[output_qvqsim] Raw Results (fallback):")
             print(results)
    except IOError as e:
        print(f"[output_qvqsim] Error writing results to file '{output_path}': {e}", file=sys.stderr)
    except Exception as e:
        print(f"[output_qvqsim] An unexpected error occurred during output: {e}", file=sys.stderr)


# Example usage (for testing the stub)
if __name__ == "__main__":
    dummy_results = {'00': 505, '11': 495, '01': 5, '10': 3}
    dummy_file = "dummy_output.json"

    print("--- Testing output_qvqsim stub ---")

    # Test printing to console
    print("\nTesting output to console:")
    output_results(dummy_results, None)

    # Test writing to file
    print(f"\nTesting output to file ({dummy_file}):")
    try:
        output_results(dummy_results, dummy_file)
        # Verify file content
        if os.path.exists(dummy_file):
            with open(dummy_file, 'r') as f:
                content = f.read()
                print(f"Content of {dummy_file}:\n{content}")
            os.remove(dummy_file) # Clean up
        else:
            print(f"Error: Output file {dummy_file} was not created.")
    except Exception as e:
        print(f"Test failed: {e}")

    print("--- End output_qvqsim test ---")
