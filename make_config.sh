#!/bin/bash

create_config() {
  local NAME=$1
  cat <<EOF >config/$NAME.yaml
  pathvars:
    samples_loc: "/jpgnv/samples/$NAME"
EOF
}

# first has different syntax
cat <<EOF >config/0k1k.yaml
  pathvars:
    samples_loc: "/jpgnv/samples/01k"
EOF

create_config "2k3k"
create_config "3k4k"
create_config "4k5k"
