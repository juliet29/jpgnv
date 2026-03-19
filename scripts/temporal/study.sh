#!/bin/bash

## I AM A TEST SCRIPT

## TO RUN:
# make executable:
# chmod +x ../path/exec.sh
# srun ../path/exec.sh

## BINDING TO TEST LOCATIONS
BINDS="--bind $HOME/projects/jpgnv:/jpgnv \
  --bind $SCRATCH/jpgnv/test_run:/jpgnv/run \
  --bind $SCRATCH/msherlock/test_results/eplus:/jpgnv/samples"

# USING THE ACTUAL SCRIPT THAT WILL BE RUN
PIPELINE=$HOME/projects/jpgnv/scripts/temporal/pipeline.sh

chmod +x $PIPELINE
apptainer exec $BINDS $HOME/images/jpgnv2.sif $PIPELINE
