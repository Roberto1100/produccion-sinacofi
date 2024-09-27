#!/bin/bash
if [ $# -ne 1 ]; then
    echo "Uso: $0 <nombre_archivos>"
    exit 1
fi

nombre_archivo="$1"

python ./src/codifier.py $nombre_archivo