#!/bin/bash
#SBATCH --job-name=n32facebook
#SBATCH --output=n32fb.out
#SBATCH --error=n32fb.err
#SBATCH --nodes=2
#SBATCH --ntasks=32
#SBATCH --mem=64G

# Load necessary modules (if needed)
#module load python

# Activate your virtual environment (if needed)
# source /path/to/your/venv/bin/activate
source ~/miniconda3/etc/profile.d/conda.sh
conda activate new_mpi_env

# Run your Python script
mpiexec python facebook.py