"""
Quantum Circuit Simulation for HTCondor Parameter Sweep

This script simulates a simple quantum circuit using PennyLane and saves
the results for post-processing. It's designed to be executed as part of
a parameter sweep on the PIC HTCondor cluster.

Author: QML-CVC Research Group
Institution: Computer Vision Center, UAB
"""

import pennylane as qml
from pennylane import numpy as np 
import os
import sys
import argparse

# Add current directory to path for local imports
sys.path.insert(0, os.getcwd())


# Define quantum device: 1 qubit, 1000 measurement shots
dev = qml.device("default.qubit", wires=1, shots=1000)


@qml.qnode(dev)
def circuit(params):
    """
    Quantum circuit with two rotation gates.
    
    Args:
        params: Array of two rotation angles [p1, p2]
        
    Returns:
        Samples from measuring Pauli-Z operator
    """
    qml.RX(params[0], wires=0)  # Rotation around X-axis
    qml.RZ(params[1], wires=0)  # Rotation around Z-axis
    return qml.sample(qml.PauliZ(0))


if __name__ == "__main__":
    # Parse command-line arguments
    # These are passed from the HTCondor submission script
    parser = argparse.ArgumentParser(
        description="Quantum circuit simulation for parameter sweep",
        add_help=False
    )
    parser.add_argument("--p1", type=float, default=0,
                       help="First rotation parameter (RX gate)")
    parser.add_argument("--p2", type=float, default=0,
                       help="Second rotation parameter (RZ gate)")
    parser.add_argument("--seed", type=int, default=42,
                       help="Random seed for reproducibility")
    
    args = parser.parse_args()

    # Extract parameters
    p1 = args.p1
    p2 = args.p2
    seed = args.seed
    
    # Set random seed for reproducibility
    np.random.seed(seed)
    
    # Create parameter array and run circuit
    params = np.array([p1, p2])
    data = circuit(params)
    
    # Save results to disk
    # Note: Update this path to match your PIC directory structure
    # Example: /data/cvcqml/common/username/tutorial_pic/cost_reconstruction/
    save_dir = "/data/cvcqml/common/matias/tutorial_pic/cost_reconstruction/{}/".format(params)
    os.makedirs(save_dir, exist_ok=True)
    np.save(os.path.join(save_dir, "results.npy"), data)
    
    print(f"Successfully saved results for params {params} to {save_dir}")