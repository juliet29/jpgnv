#!/bin/bash

cd /jpgnv
ls
echo $PWD
uv sync
echo "About to run in jpgnv"
SMKCMD="uv run snakemake -c 4 --keep-going"

# JPG
$SMKCMD plyze_jpg_create_metrics_target
wait
$SMKCMD plyze_jpg_consolidate_target
wait

# QOI
$SMKCMD plyze_qoi_create_target
wait
$SMKCMD plyze_qoi_consolidate_target
