#!/bin/bash
#SBATCH --job-name=n32twitter
#SBATCH --output=n32tw.out
#SBATCH --error=n32tw.err
#SBATCH --nodes=2
#SBATCH --ntasks=32
#SBATCH --mem=257200

# Load necessary modules (if needed)
#module load python

# Activate your virtual environment (if needed)
# source /path/to/your/venv/bin/activate
source ~/miniconda3/etc/profile.d/conda.sh
conda activate new_mpi_env

# Run your Python script
mpiexec python twitter.py
