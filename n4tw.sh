#!/bin/bash
#SBATCH --job-name=n4twitter
#SBATCH --output=n4tw.out
#SBATCH --error=n4tw.err
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --mem=64G

# Load necessary modules (if needed)
#module load python

# Activate your virtual environment (if needed)
# source /path/to/your/venv/bin/activate
source ~/miniconda3/etc/profile.d/conda.sh
conda activate new_mpi_env

# Run your Python script
mpiexec python twitter.py