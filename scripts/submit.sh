#!/bin/bash
#SBATCH --job-name=jpgnv
#SBATCH --mail-user=jnwagwu@stanford.edu
#SBATCH --mail-type=ALL
#
# %A = Job ID, %a = Array Index (the "chunk")
#SBATCH --output=/scratch/users/jnwagwu/submit/jpgnv/%A/log.out
#SBATCH --error=/scratch/users/jnwagwu/submit/jpgnv/%A/log.err
#
#SBATCH --partition="serc" # run on serc partition
#SBATCH --ntasks=1
#SBATCH --time=12:00:00 # 12 hours
#SBATCH --cpus-per-task=4  # 4 cores
#SBATCH --mem-per-cpu=4G  # 4GB per core / 16GB total
#

BINDS="--bind $HOME/projects/jpgnv:/jpgnv \
  --bind $SCRATCH/jpgnv/run:/jpgnv/run \
  --bind $SCRATCH/msherlock/run/results/eplus/snakemake:/jpgnv/samples"
# Make output dir
mkdir -p "/scratch/users/jnwagwu/submit/jpgnv"
# run apptainer script
# apptainer run $BINDS images/jpgnv2.sif
PIPELINE=$HOME/projects/jpgnv/scripts/pipeline.sh

chmod +x $PIPELINE
apptainer exec $BINDS $HOME/images/jpgnv2.sif $PIPELINE
