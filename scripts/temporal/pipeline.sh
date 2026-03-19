#!/bin/bash

cd /jpgnv
echo $PWD

echo "Current version:" # Adds waiting time before try to upgrade
uv run plyze --version

# upgrade plyze to latest version
uv add plyze --upgrade-package plyze
uv sync
echo "SHOULD HAVE UPDATED PLYZE...."

echo "Updated version:"
uv run plyze --version

echo "About to run in jpgnv"
SMKCMD="uv run snakemake -c 4 --keep-going"

# Create temporal csv from all cases
$SMKCMD plyze_temporal_create_target
wait

echo "Finished running temporal.sh"
