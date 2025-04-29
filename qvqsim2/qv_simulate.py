"""
qv_simulate - Core Quantum Circuit Simulation Logic

This module implements the state vector simulation for quantum circuits.
It defines quantum gates as matrices and simulates the evolution of the
quantum state vector.
"""

import numpy as np
from . import qv_gates  # Import gate definitions
from . import qv_help_sim  # Import helper functions

# --- Simulation Function ---

def simulate(num_qubits, shots, circuit=None):
    """
    Simulates a quantum circuit using state vector evolution.

    Args:
        num_qubits (int): The number of qubits in the circuit.
        shots (int): The number of times to measure the final state.
        circuit (list, optional): A description of the quantum circuit.
            The format should be a list of lists or tuples, where each
            inner element represents an operation:
            - Single-qubit gates: ['GateName', target_qubit] (e.g., ['H', 0])
            - Rotation gates: ['GateName', target_qubit, angle] (e.g., ['Rx', 1, np.pi/2])
            - CNOT: ['CX', control_qubit, target_qubit]
            - Measure: ['Measure', [qubit_to_measure, ...]] (optional: specify qubits, all if omitted)

        If None or empty, simulates the initial |0...0> state.

    Returns:
        dict: A dictionary containing the measurement results (counts).
              Example: {'00': 512, '11': 512}
    """
    # Initialize state vector to |0...0>
    state_vector = np.zeros(2**num_qubits, dtype=complex)
    state_vector[0] = 1.0  # |0...0> state has amplitude 1 at index 0

    print(f"Starting simulation: {num_qubits} qubits, {shots} shots.")
    print(f"Initial state |{'0'*num_qubits}>: {state_vector}")

    if circuit:
        print(f"Processing circuit description: {circuit}")
        for operation in circuit:
            gate_name = operation[0]
            qubits = operation[1:]

            if gate_name in ['I', 'X', 'Y', 'Z', 'H', 'S', 'T', 'Sdg', 'Tdg', 'sX']:
                if len(qubits) == 1:
                    target_qubit = qubits[0]
                    gate = getattr(qv_gates, gate_name)
                    operator = qv_help_sim._get_operator(gate, target_qubit, num_qubits)
                    state_vector = np.dot(operator, state_vector)
                    print(f"Applied {gate_name} on qubit {target_qubit}")
                else:
                    print(f"Warning: {gate_name} requires 1 qubit, but got {len(qubits)}")

            elif gate_name in ['Rx', 'Ry', 'Rz']:
                if len(qubits) == 2:
                    target_qubit = qubits[0]
                    angle = qubits[1]
                    gate_func = getattr(qv_gates, gate_name)
                    gate = gate_func(angle)
                    operator = qv_help_sim._get_operator(gate, target_qubit, num_qubits)
                    state_vector = np.dot(operator, state_vector)
                    print(f"Applied {gate_name}({angle}) on qubit {target_qubit}")
                else:
                    print(f"Warning: {gate_name} requires 1 qubit and an angle, but got {len(qubits)}")

            elif gate_name == 'CX':
                if len(qubits) == 2:
                    control_qubit = qubits[0]
                    target_qubit = qubits[1]
                    operator = qv_help_sim._get_cnot_operator(control_qubit, target_qubit, num_qubits)
                    state_vector = np.dot(operator, state_vector)
                    print(f"Applied CNOT (control={control_qubit}, target={target_qubit})")
                else:
                    print(f"Warning: CX requires 2 qubits (control, target), but got {len(qubits)}")

            elif gate_name == 'Measure':
                print("Warning: Measurement operation is currently a placeholder and doesn't modify the state vector.")
                # In a full implementation, this would trigger a measurement on the specified qubits.

            else:
                print(f"Warning: Unknown gate '{gate_name}' in circuit.")

            print(f"State vector after operation: {state_vector}")

    else:
        print("No circuit provided, simulating initial state.")

    # --- Measurement ---
    print(f"Final state vector before measurement: {state_vector}")
    results = qv_help_sim._measure(state_vector, shots)

    return results

# --- Example Usage (can be removed or kept for basic testing) ---
if __name__ == "__main__":
    # Example: Simulate a simple 2-qubit Bell state |Φ+> = (|00> + |11>)/sqrt(2)
    example_num_qubits = 2
    example_shots = 1000
    # Define the Bell state preparation circuit
    example_circuit = [('H', 0), ('CX', 0, 1)]

    print("\n--- Running Example Simulation ---")
    results = simulate(example_num_qubits, example_shots, example_circuit)
    print("\nExample Simulation Results:")
    import json
    print(json.dumps(results, indent=2))
    print("--- End Example Simulation ---")
