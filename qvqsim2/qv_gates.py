"""
qv_gates - Definitions of quantum gates as NumPy matrices.

This module defines standard quantum gates as NumPy arrays (matrices)
for use in quantum circuit simulation.
"""

import numpy as np

# --- Single-Qubit Gates ---

# Identity gate (does nothing)
I = np.array([[1, 0], [0, 1]], dtype=complex)

# Pauli-X gate (NOT gate, bit-flip)
X = np.array([[0, 1], [1, 0]], dtype=complex)

# Pauli-Y gate
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)

# Pauli-Z gate (phase-flip)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

# Hadamard gate (creates superposition)
H = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)

# Phase gate (S gate)
S = np.array([[1, 0], [0, 1j]], dtype=complex)
# S dagger gate (conjugate transpose of S)
Sdg = S.conj().T

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
        numpy.ndarray: The 2x2 unitary matrix for Rx(theta).
    """
    return np.array([[np.cos(theta / 2), -1j * np.sin(theta / 2)],
                     [-1j * np.sin(theta / 2), np.cos(theta / 2)]], dtype=complex)

def Ry(theta):
    """
    Returns the Ry rotation gate matrix.

    Args:
        theta (float): Rotation angle in radians.

    Returns:
        numpy.ndarray: The 2x2 unitary matrix for Ry(theta).
    """
    return np.array([[np.cos(theta / 2), -np.sin(theta / 2)],
                     [np.sin(theta / 2), np.cos(theta / 2)]], dtype=complex)

def Rz(theta):
    """
    Returns the Rz rotation gate matrix (phase shift).

    Args:
        theta (float): Rotation angle in radians.

    Returns:
        numpy.ndarray: The 2x2 unitary matrix for Rz(theta).
    """
    return np.array([[np.exp(-1j * theta / 2), 0],
                     [0, np.exp(1j * theta / 2)]], dtype=complex)

# --- Multi-Qubit Gates (To be implemented as needed) ---
# Example: CNOT (Controlled-NOT)
# def CNOT(control_qubit, target_qubit, num_qubits):
#     """
#     Returns the CNOT gate matrix for the given control and target qubits.
#     """
#     size = 2**num_qubits
#     cnot_matrix = np.zeros((size, size), dtype=complex)
#     for i in range(size):
#         binary_i = format(i, f'0{num_qubits}b')
#         if binary_i[control_qubit] == '1':
#             target_bit = int(binary_i[target_qubit]) ^ 1
#             new_binary = list(binary_i)
#             new_binary[target_qubit] = str(target_bit)
#             j = int("".join(new_binary), 2)
#             cnot_matrix[i, j] = 1.0
#         else:
#             cnot_matrix[i, i] = 1.0
#     return cnot_matrix

# Add other multi-qubit gates here (e.g., CZ, SWAP) as you need them.
