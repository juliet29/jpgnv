#!/bin/bash
BINDS="--bind $HOME/projects/jpgnv:/jpgnv \
  --bind $SCRATCH/jpgnv/run:/jpgnv/run \
  --bind $SCRATCH/msherlock/run/results/eplus/snakemake:/jpgnv/samples"

abuild-jpg() {
  apptainer build images/jpgnv2.sif $HOME/recipes/jpgnv2.def
}

ashell-jpg() {
  apptainer shell $BINDS $HOME/images/jpgnv2.sif
}

aexec-jpg() {
  apptainer exec $BINDS $HOME/images/jpgnv2.sif $HOME/projects/jpgnv/scripts/pipeline.sh
}

arun-jpg() {
  apptainer run $BINDS $HOME/images/jpgnv2.sif $HOME/projects/jpgnv/scripts/pipeline.sh
}

echo "Sourced appt.sh"

export JPS="$HOME/projects/jpgnv/scripts"
