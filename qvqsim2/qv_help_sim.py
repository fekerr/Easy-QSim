"""
qv_help_sim - Helper functions for quantum circuit simulation.

This module contains helper functions used by the qv_simulate module
for constructing operators and performing measurements.
"""

import numpy as np
from . import qv_gates  # Import gate definitions

def _get_operator(gate_matrix, target_qubit, num_qubits):
    """
    Constructs the full operator matrix for a single-qubit gate.

    Applies the gate to the target_qubit and identity to others using
    Kronecker products.

    Args:
        gate_matrix (numpy.ndarray): The 2x2 matrix for the gate.
        target_qubit (int): The index of the qubit the gate acts on (0-based).
        num_qubits (int): The total number of qubits in the system.

    Returns:
        numpy.ndarray: The (2^num_qubits) x (2^num_qubits) operator matrix.
    """
    op_list = [qv_gates.I] * num_qubits  # Start with identity on all qubits
    op_list[target_qubit] = gate_matrix  # Place the gate on the target

    # Compute the full operator using Kronecker product
    full_op = op_list[0]
    for i in range(1, num_qubits):
        full_op = np.kron(full_op, op_list[i])

    return full_op

def _get_cnot_operator(control_qubit, target_qubit, num_qubits):
    """
    Constructs the CNOT (Controlled-NOT) operator matrix.

    Args:
        control_qubit (int): The index of the control qubit (0-based).
        target_qubit (int): The index of the target qubit (0-based).
        num_qubits (int): The total number of qubits in the system.

    Returns:
        numpy.ndarray: The (2^num_qubits) x (2^num_qubits) CNOT operator matrix.
    """
    size = 2**num_qubits
    cnot_matrix = np.zeros((size, size), dtype=complex)
    for i in range(size):
        binary_i = format(i, f'0{num_qubits}b')
        if binary_i[control_qubit] == '1':
            target_bit = int(binary_i[target_qubit]) ^ 1
            new_binary = list(binary_i)
            new_binary[target_qubit] = str(target_bit)
            j = int("".join(new_binary), 2)
            cnot_matrix[i, j] = 1.0
        else:
            cnot_matrix[i, i] = 1.0
    return cnot_matrix

def _measure(state_vector, shots):
    """
    Simulates measurement of the quantum state.

    Calculates probabilities based on the Born rule and samples outcomes.

    Args:
        state_vector (numpy.ndarray): The final state vector (size 2^num_qubits).
        shots (int): The number of times to simulate the measurement.

    Returns:
        dict: A dictionary mapping computational basis states (bitstrings)
              to their measured counts.
    """
    num_qubits = int(np.log2(len(state_vector)))
    probabilities = np.abs(state_vector)**2  # Born rule: Prob = |amplitude|^2

    # Ensure probabilities sum to 1 (within floating point tolerance)
    if not np.isclose(np.sum(probabilities), 1.0):
        print(f"Warning: Probabilities sum to {np.sum(probabilities)}, renormalizing.")
        probabilities /= np.sum(probabilities)  # Renormalize if needed

    # Generate basis states (e.g., '00', '01', '10', '11' for 2 qubits)
    basis_states = [format(i, f'0{num_qubits}b') for i in range(2**num_qubits)]

    # Sample outcomes based on probabilities
    measured_outcomes = np.random.choice(basis_states, size=shots, p=probabilities)

    # Count the occurrences of each outcome
    counts = dict(Counter(measured_outcomes))
    return counts
