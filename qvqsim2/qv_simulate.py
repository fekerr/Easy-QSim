"""
qv_simulate - Core Quantum Circuit Simulation Logic

This module implements the state vector simulation for quantum circuits.
It defines quantum gates as matrices and simulates the evolution of the
quantum state vector.
"""

import numpy as np
from collections import Counter

# --- Gate Definitions ---
# Define standard quantum gates as NumPy matrices.
# These matrices operate on the state vector representation of qubits.
# |0> = ^T, |1> = ^T

# Identity gate (does nothing)
I = np.array([[1, 0], [0, 1]], dtype=complex)

# Pauli-X gate (NOT gate, bit-flip) [1, 2, 3]
X = np.array([[0, 1], [1, 0]], dtype=complex)

# Pauli-Y gate [1, 2, 3]
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)

# Pauli-Z gate (phase-flip) [1, 2, 3]
Z = np.array([[1, 0], [0, -1]], dtype=complex)

# Hadamard gate (creates superposition) [1, 2, 3]
H = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)

# Phase gate (S gate)
S = np.array([[1, 0], [0, 1j]], dtype=complex)
# S dagger gate (conjugate transpose of S)
Sdg = S.conj().T # Using .conj().T for conjugate transpose [4, 5]

# T gate (pi/8 gate)
T = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]], dtype=complex)
# T dagger gate
Tdg = T.conj().T

# Square root of X gate
sX = (1/2)*np.array([[1+1j, 1-1j],[1-1j, 1+1j]], dtype=complex)

def Rx(theta):
    """
    Returns the Rx rotation gate matrix.

    Args:
        theta (float): Rotation angle in radians.

    Returns:
        numpy.ndarray: The 2x2 unitary matrix for Rx(theta). [2, 6]
    """
    return np.array([np.cos(theta / 2), -1j * np.sin(theta / 2)],
        [-1j * np.sin(theta / 2), np.cos(theta / 2)], dtype=complex)

def Ry(theta):
    """
    Returns the Ry rotation gate matrix.

    Args:
        theta (float): Rotation angle in radians.

    Returns:
        numpy.ndarray: The 2x2 unitary matrix for Ry(theta). [2, 6]
    """
    return np.array([np.cos(theta / 2), -np.sin(theta / 2)],
        [np.sin(theta / 2), np.cos(theta / 2)], dtype=complex)

def Rz(theta):
    """
    Returns the Rz rotation gate matrix (phase shift).

    Args:
        theta (float): Rotation angle in radians.

    Returns:
        numpy.ndarray: The 2x2 unitary matrix for Rz(theta). [2, 6]
    """
    return np.array([np.exp(-1j * theta / 2), 0],
        [0, np.exp(1j * theta / 2)], dtype=complex)

# --- Helper Functions ---

def _get_operator(gate_matrix, target_qubit, num_qubits):
    """
    Constructs the full operator matrix for a single-qubit gate.

    Applies the gate to the target_qubit and identity to others using
    Kronecker products. [7, 8, 9, 10]

    Args:
        gate_matrix (numpy.ndarray): The 2x2 matrix for the gate.
        target_qubit (int): The index of the qubit the gate acts on (0-based).
        num_qubits (int): The total number of qubits in the system.

    Returns:
        numpy.ndarray: The (2^num_qubits) x (2^num_qubits) operator matrix.
    """
    op_list = [I] * num_qubits # Start with identity on all qubits
    op_list[target_qubit] = gate_matrix # Place the gate on the target

    # Compute the full operator using Kronecker product [11, 12, 13]
    full_op = op_list
    for i in range(1, num_qubits):
        full_op = np.kron(full_op, op_list[i]) # np.kron computes Kronecker product

    return full_op

def _measure(state_vector, shots):
    """
    Simulates measurement of the quantum state.

    Calculates probabilities based on the Born rule and samples outcomes.
    [14, 15, 16, 17]

    Args:
        state_vector (numpy.ndarray): The final state vector (size 2^num_qubits).
        shots (int): The number of times to simulate the measurement.

    Returns:
        dict: A dictionary mapping computational basis states (bitstrings)
              to their measured counts.
    """
    num_qubits = int(np.log2(len(state_vector)))
    probabilities = np.abs(state_vector)**2 # Born rule: Prob = |amplitude|^2
    
    # Ensure probabilities sum to 1 (within floating point tolerance)
    # This is a crucial check for valid quantum states [15, 18]
    if not np.isclose(np.sum(probabilities), 1.0):
        print(f"Warning: Probabilities sum to {np.sum(probabilities)}, renormalizing.")
        probabilities /= np.sum(probabilities) # Renormalize if needed

    # Generate basis states (e.g., '00', '01', '10', '11' for 2 qubits)
    basis_states = [format(i, f'0{num_qubits}b') for i in range(2**num_qubits)]

    # Sample outcomes based on probabilities
    measured_outcomes = np.random.choice(basis_states, size=shots, p=probabilities)

    # Count the occurrences of each outcome
    counts = dict(Counter(measured_outcomes))
    return counts

# --- Simulation Function ---

def simulate(num_qubits, shots, circuit=None):
    """
    Simulates a quantum circuit using state vector evolution.

    Args:
        num_qubits (int): The number of qubits in the circuit.
        shots (int): The number of times to measure the final state.
        circuit (list, optional): A description of the quantum circuit.
            The format needs to be defined (e.g., list of tuples:
            [('H', 0), ('CX', 0, 1), ('Measure', )]).
            If None or empty, simulates the initial |0...0> state.

    Returns:
        dict: A dictionary containing the measurement results (counts).
              Example: {'00': 512, '11': 512}
    """
    # Initialize state vector to |0...0>
    # State vector size is 2^num_qubits [7, 9, 10]
    state_vector = np.zeros(2**num_qubits, dtype=complex)
    state_vector[0] = 1.0 # |0...0> state has amplitude 1 at index 0

    print(f"Starting simulation: {num_qubits} qubits, {shots} shots.")
    print(f"Initial state |{'0'*num_qubits}>: {state_vector}")

    # --- Circuit Execution Placeholder ---
    # TODO: Implement actual circuit processing based on the 'circuit' description.
    # This will involve iterating through the circuit steps, constructing
    # the appropriate operator matrices (using _get_operator for single-qubit
    # gates and defining multi-qubit gates like CNOT), and applying them
    # to the state_vector via matrix multiplication (np.dot).
    if circuit:
        print(f"Processing circuit description (placeholder): {circuit}")
        # Example pseudo-code:
        # for gate_info in circuit:
        #     gate_name = gate_info
        #     qubit_indices = gate_info[1:]
        #     if gate_name == 'H':
        #         op = _get_operator(H, qubit_indices, num_qubits)
        #     elif gate_name == 'CX':
        #         # op = _get_cnot_operator(qubit_indices, qubit_indices[1], num_qubits) # Needs implementation
        #         pass # Placeholder for CNOT
        #     elif gate_name == 'Rx':
        #         theta = gate_info[2] # Assuming format ('Rx', qubit, angle)
        #         op = _get_operator(Rx(theta), qubit_indices, num_qubits)
        #     #... other gates...
        #     else:
        #         print(f"Warning: Unknown gate '{gate_name}'")
        #         continue
        #
        #     # Apply the gate: state_vector = np.dot(op, state_vector)
        #     # print(f"Applied {gate_name}{qubit_indices}, new state: {state_vector}") # Debugging
        pass # Remove this pass when implementing circuit logic
    else:
        print("No circuit provided, simulating initial state.")

    # --- Measurement ---
    print(f"Final state vector before measurement: {state_vector}")
    results = _measure(state_vector, shots)

    return results

# --- Example Usage (can be removed or kept for basic testing) ---
if __name__ == "__main__":
    # Example: Simulate a simple 2-qubit Bell state |Φ+> = (|00> + |11>)/sqrt(2)
    # This replaces the previous hardcoded CHSH logic with a defined circuit.
    example_num_qubits = 2
    example_shots = 1000

    print("\n--- Running Example Simulation ---")
    # Manually create Bell state for now, as CNOT isn't implemented in the loop yet
    bell_state_vector = np.zeros(2**example_num_qubits, dtype=complex)
    bell_state_vector = 1/np.sqrt(2) # Amplitude for |00>
    bell_state_vector[3] = 1/np.sqrt(2) # Amplitude for |11>

    print(f"Manually setting state to Bell state |Φ+>: {bell_state_vector}")
    example_results = _measure(bell_state_vector, example_shots)

    # results = simulate(example_num_qubits, example_shots, example_circuit) # Use this line once circuit execution is implemented
    print("\nExample Simulation Results:")
    print(json.dumps(example_results, indent=2))
    print("--- End Example Simulation ---")
