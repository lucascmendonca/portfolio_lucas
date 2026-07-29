#!/bin/bash
# entrypoint.sh

# define python padrão no container
export PYSPARK_PYTHON=python3
export PYSPARK_DRIVER_PYTHON=python3

# Se comando foi passado, executa; caso contrário abre um bash
if [ $# -gt 0 ]; then
  exec "$@"
else
  exec bash
fi
