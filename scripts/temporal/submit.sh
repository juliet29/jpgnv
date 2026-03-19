#!/bin/bash
#SBATCH --job-name=jpgnv
#SBATCH --mail-user=jnwagwu@stanford.edu
#SBATCH --mail-type=ALL
#
# %A = Job ID, %a = Array Index (the "chunk")
#SBATCH --output=/scratch/users/jnwagwu/submit/jpgnv/temporal/%A/log.out
#SBATCH --error=/scratch/users/jnwagwu/submit/jpgnv/temporal/%A/log.err
#
#SBATCH --partition="serc" # run on serc partition
#SBATCH --ntasks=1
#SBATCH --time=5:00:00 # 5 hours
#SBATCH --cpus-per-task=4  # 4 cores
#SBATCH --mem-per-cpu=4G  # 4GB per core / 16GB total

# TO RUN
# sbatch .../path/submit.sh

BINDS="--bind $HOME/projects/jpgnv:/jpgnv \
  --bind $SCRATCH/jpgnv/run:/jpgnv/run \
  --bind $SCRATCH/msherlock/run/results/eplus/snakemake:/jpgnv/samples"

# Make output dir
mkdir -p "/scratch/users/jnwagwu/submit/jpgnv/temporal"

# run apptainer script
PIPELINE=$HOME/projects/jpgnv/scripts/temporal/pipeline.sh

chmod +x $PIPELINE
apptainer exec $BINDS $HOME/images/jpgnv2.sif $PIPELINE
