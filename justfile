check-smk:
  uv run snakemake --list-target-rules --configfile=config/local.yaml

# -------------- PUSH PACKAGE -------------
push-tag end:
  git tag -a s0.1.{{end}} -m s0.1.{{end}}
  git push --tag
