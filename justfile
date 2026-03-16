check-smk:
  uv run snakemake --list-target-rules --configfile=config/local.yaml

# -------------- PUSH PACKAGE -------------
push-tag end:
  git tag -a s0.1.{{end}} -m s0.1.{{end}}
  git push --tag


# -------------- DEPENDENCIES -------------
update-plyze:
  uv add plyze --upgrade-package plzye 

add-local-plyze:
  uv pip install -e "plyze @ /Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/plyze"
# update-plan:
#   uv add plan2eplus --upgrade-package plan2eplus 

