#!/bin/bash
#
# HTCondor Job Execution Script
#
# This script is executed on worker nodes by HTCondor.
# It sets up the environment and runs the quantum circuit simulation.
#
# Arguments:
#   $1: First rotation parameter (p1)
#   $2: Second rotation parameter (p2)
#   $3: Random seed for reproducibility
#

# Extract command-line arguments
p1=$1
p2=$2
seed=$3

# Navigate to project directory
cd ~/tutorial-pic

# Activate Python virtual environment with PennyLane
# Update this path to match your environment setup
. ~/qvenv/bin/activate

# Print job information for logging
echo "========================================="
echo "HTCondor Job Execution"
echo "Parameters: p1=$p1, p2=$p2, seed=$seed"
echo "========================================="

# Execute the quantum circuit simulation
python3 main.py --p1 $p1 --p2 $p2 --seed $seed

# Check exit status
if [ $? -eq 0 ]; then
    echo "Job completed successfully"
else
    echo "Job failed with exit code $?"
    exit 1
fi

# Deactivate virtual environment
deactivate

echo "Job finished"