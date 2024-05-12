#!/bin/bash
#SBATCH --job-name=n64twitter
#SBATCH --output=n64tw.out
#SBATCH --error=n64tw.err
#SBATCH --nodes=1
#SBATCH --ntasks=64
#SBATCH --mem=64G

# Load necessary modules (if needed)
#module load python

# Activate your virtual environment (if needed)
# source /path/to/your/venv/bin/activate
source ~/miniconda3/etc/profile.d/conda.sh
conda activate new_mpi_env

# Run your Python script
mpiexec python twitter.py