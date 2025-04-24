#!/usr/bin/env python3
import argparse
import sys
import os
import tomllib
import importlib

# Import simulation and input/output functions
from qv_simulate import simulate
import input_qvqsim
import output_qvqsim

def load_config(config_path="config.toml"):
    try:
        with open(config_path, "rb") as f:
            config = tomllib.load(f)
        return config
    except Exception as e:
        print(f"Error loading configuration: {e}")
        sys.exit(1)

def parse_args():
    parser = argparse.ArgumentParser(
        description="Quantum Village Simulator (qvqsim) - A quantum simulation tool"
    )
    parser.add_argument("input_file", help="Path to the quantum circuit input file")
    parser.add_argument("-c", "--config", default="config.toml", help="Path to config file (default: config.toml)")
    return parser.parse_args()

def main():
    args = parse_args()
    config = load_config(args.config)

    input_file = args.input_file
    ext = os.path.splitext(input_file)[1].lower()

    # Select proper input module based on the file extension
    if ext == ".json":
        input_module = importlib.import_module("input_json")
        circuit = input_module.load_input(input_file)
    elif ext in [".yaml", ".yml"]:
        input_module = importlib.import_module("input_yaml")
        circuit = input_module.load_input(input_file)
    else:
        # Default to the qvqsim input if no known extension is found
        circuit = input_qvqsim.load_input(input_file)

    # Execute the simulation (stub)
    results = simulate(circuit, config)

    # Process the output
    output_qvqsim.output_results(results)

if __name__ == "__main__":
    main()
