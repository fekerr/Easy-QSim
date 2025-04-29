"""
test_qvqsim - Unit tests for the qvqsim simulator components.

This module contains unit tests for the core simulation logic, gate definitions,
and potentially input/output handlers in the future.
"""

import unittest
import numpy as np
import os
import sys

# Ensure the simulator modules can be imported
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

# Import modules to be tested
import qv_simulate
# import input_json # Example: if testing input modules
# import output_qvqsim # Example: if testing output modules

class TestQvSimulateGates(unittest.TestCase):
    """Tests for the gate definitions in qv_simulate."""

    def test_identity_gate(self):
        """Verify the Identity gate matrix."""
        expected = np.array([, ], dtype=complex)
        np.testing.assert_array_almost_equal(qv_simulate.I, expected)

    def test_pauli_x_gate(self):
        """Verify the Pauli-X gate matrix."""
        expected = np.array([, ], dtype=complex)
        np.testing.assert_array_almost_equal(qv_simulate.X, expected)

    def test_pauli_y_gate(self):
        """Verify the Pauli-Y gate matrix."""
        expected = np.array([[0, -1j], [1j, 0]], dtype=complex)
        np.testing.assert_array_almost_equal(qv_simulate.Y, expected)

    def test_pauli_z_gate(self):
        """Verify the Pauli-Z gate matrix."""
        expected = np.array([, [0, -1]], dtype=complex)
        np.testing.assert_array_almost_equal(qv_simulate.Z, expected)

    def test_hadamard_gate(self):
        """Verify the Hadamard gate matrix."""
        expected = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)
        np.testing.assert_array_almost_equal(qv_simulate.H, expected)

    def test_rx_gate(self):
        """Verify the Rx gate matrix for a specific angle (e.g., pi/2)."""
        theta = np.pi / 2
        expected = np.array([np.cos(theta / 2), -1j * np.sin(theta / 2)],
            [-1j * np.sin(theta / 2), np.cos(theta / 2)], dtype=complex)
        np.testing.assert_array_almost_equal(qv_simulate.Rx(theta), expected)
        # TODO: Add tests for other angles (0, pi)

    def test_ry_gate(self):
        """Verify the Ry gate matrix for a specific angle (e.g., pi)."""
        theta = np.pi
        expected = np.array([np.cos(theta / 2), -np.sin(theta / 2)],
            [np.sin(theta / 2), np.cos(theta / 2)], dtype=complex) # Should be [[0, -1], ] = iY
        np.testing.assert_array_almost_equal(qv_simulate.Ry(theta), expected)
         # TODO: Add tests for other angles (0, pi/2)

    def test_rz_gate(self):
        """Verify the Rz gate matrix for a specific angle (e.g., pi/2)."""
        theta = np.pi / 2
        expected = np.array([np.exp(-1j * theta / 2), 0],
            [0, np.exp(1j * theta / 2)], dtype=complex) # Should be [[exp(-ipi/4), 0], [0, exp(ipi/4)]] = Sdg * exp(-ipi/4)? Check phase.
        # Rz(pi/2) = [[(1-i)/sqrt(2), 0], [0, (1+i)/sqrt(2)]]
        np.testing.assert_array_almost_equal(qv_simulate.Rz(theta), expected)
        # TODO: Add tests for other angles (0, pi)

    # TODO: Add tests for S, T, Sdg, Tdg, sX gates.

    def test_gate_unitarity(self):
        """Check if defined gates are unitary (U*U.H = I)."""
        gates_to_test = {
            "I": qv_simulate.I,
            "X": qv_simulate.X,
            "Y": qv_simulate.Y,
            "Z": qv_simulate.Z,
            "H": qv_simulate.H,
            "S": qv_simulate.S,
            "T": qv_simulate.T,
            "Rx(pi/3)": qv_simulate.Rx(np.pi/3),
            "Ry(pi/4)": qv_simulate.Ry(np.pi/4),
            "Rz(pi/5)": qv_simulate.Rz(np.pi/5),
        }
        identity = np.identity(2, dtype=complex)
        for name, gate in gates_to_test.items():
            with self.subTest(gate_name=name):
                # U_dagger = gate.conj().T #.H property requires numpy.matrix
                U_dagger = np.conjugate(gate).T
                product = np.dot(gate, U_dagger)
                np.testing.assert_array_almost_equal(product, identity,
                                                     err_msg=f"Gate {name} is not unitary")


class TestQvSimulateExecution(unittest.TestCase):
    """Tests for the simulation execution logic in qv_simulate."""

    def test_initial_state(self):
        """Verify the initial state is |0...0>."""
        for n in range(1, 5): # Test for 1 to 4 qubits
            with self.subTest(num_qubits=n):
                # Simulate with no circuit
                results = qv_simulate.simulate(num_qubits=n, shots=10, circuit=None)
                expected_state_str = '0' * n
                # Expect only the |0...0> state to be measured
                self.assertEqual(list(results.keys()), [expected_state_str])
                self.assertEqual(results[expected_state_str], 10) # All shots in |0...0>

    def test_single_qubit_hadamard(self):
        """Test applying H gate to |0>."""
        num_qubits = 1
        shots = 1000
        circuit = [('H', 0)]
        # Expected outcome: 50% |0>, 50% |1>
        results = qv_simulate.simulate(num_qubits=num_qubits, shots=shots, circuit=circuit)

        # Check if both outcomes are present
        self.assertIn('0', results)
        self.assertIn('1', results)
        # Check if counts are roughly equal (statistical test)
        # Allow for some statistical noise, e.g., within 15% of expected 500
        tolerance = shots * 0.15
        self.assertAlmostEqual(results['0'], shots / 2, delta=tolerance)
        self.assertAlmostEqual(results['1'], shots / 2, delta=tolerance)
        self.assertEqual(results['0'] + results['1'], shots) # Total shots must match

    def test_single_qubit_x_gate(self):
        """Test applying X gate to |0>."""
        num_qubits = 1
        shots = 100
        circuit = [('X', 0)]
        # Expected outcome: 100% |1>
        results = qv_simulate.simulate(num_qubits=num_qubits, shots=shots, circuit=circuit)
        self.assertEqual(list(results.keys()), ['1'])
        self.assertEqual(results['1'], shots)

    # --- TODO: Add More Sophisticated Tests ---
    # - Test multi-qubit gate application (requires implementing CNOT etc. first)
    #   - e.g., Bell state preparation H(0), CX(0, 1) -> |00> + |11>
    # - Test sequences of gates (e.g., HZH = X) by checking final state vector
    #   (requires modifying simulate or _measure to optionally return state vector)
    # - Test measurement on specific qubits (requires enhancing _measure)
    # - Test state vector normalization after multiple gate applications
    # - Test handling of invalid circuit descriptions or parameters


class TestHelperFunctions(unittest.TestCase):
    """Tests for helper functions in qv_simulate."""

    def test_get_operator_single_qubit(self):
        """Test _get_operator for a single qubit."""
        op = qv_simulate._get_operator(qv_simulate.X, 0, 1)
        np.testing.assert_array_almost_equal(op, qv_simulate.X)

    def test_get_operator_two_qubits_target0(self):
        """Test _get_operator for H on qubit 0 in a 2-qubit system (H ⊗ I)."""
        op = qv_simulate._get_operator(qv_simulate.H, 0, 2)
        expected = np.kron(qv_simulate.H, qv_simulate.I)
        np.testing.assert_array_almost_equal(op, expected)

    def test_get_operator_two_qubits_target1(self):
        """Test _get_operator for X on qubit 1 in a 2-qubit system (I ⊗ X)."""
        op = qv_simulate._get_operator(qv_simulate.X, 1, 2)
        expected = np.kron(qv_simulate.I, qv_simulate.X)
        np.testing.assert_array_almost_equal(op, expected)

    # TODO: Add tests for _measure function
    # - Test probability calculation for known states (e.g., |+>, |->)
    # - Test that counts sum to the number of shots
    # - Test handling of zero-amplitude states

if __name__ == '__main__':
    unittest.main()
