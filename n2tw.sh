#!/bin/bash
#SBATCH --job-name=n2twitter
#SBATCH --output=n2tw.out
#SBATCH --error=n2tw.err
#SBATCH --partition=memxl
#SBATCH --nodes=1
#SBATCH --ntasks=2
#SBATCH --mem=515500
#SBATCH --nodelist=cn26
 
# Load necessary modules (if needed)
#module load python

# Activate your virtual environment (if needed)
# source /path/to/your/venv/bin/activate
source ~/miniconda3/etc/profile.d/conda.sh
conda activate new_mpi_env

# Run your Python script
mpiexec python twitter.py
