#!/bin/bash
#SBATCH --job-name=n4twitter
#SBATCH --output=n4tw.out
#SBATCH --error=n4tw.err
#SBATCH --partition=memxl
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --mem=515500
#SBATCH --nodelist=cn27 
# Load necessary modules (if needed)
#module load python

# Activate your virtual environment (if needed)
# source /path/to/your/venv/bin/activate
source ~/miniconda3/etc/profile.d/conda.sh
conda activate new_mpi_env

# Run your Python script
mpiexec python twitter.py
