#!/bin/bash
#SBATCH --job-name=n8facebook
#SBATCH --output=n8fb.out
#SBATCH --error=n8fb.err
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --mem=64G

# Load necessary modules (if needed)
#module load python

# Activate your virtual environment (if needed)
# source /path/to/your/venv/bin/activate
source ~/miniconda3/etc/profile.d/conda.sh
conda activate new_mpi_env

# Run your Python script
mpiexec python facebook.py