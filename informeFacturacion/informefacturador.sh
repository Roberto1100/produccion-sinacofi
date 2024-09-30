#!/bin/bash

# Variables
script_python="/.../informefacturacion/src/facturador.py"
informes_dir="/.../informefacturacion/informes"
respaldos_dir="/.../informefacturacion/respaldos"
logs_dir="/.../informefacturacion/logs"
log_file="/.../informefacturacion/logs/bash.log"

# Validar que los directorios existen, si no, crearlos
if [ ! -d "$informes_dir" ]; then
    echo "El directorio $informes_dir no existe. Creando..."
    mkdir -p "$informes_dir"
fi

if [ ! -d "$respaldos_dir" ]; then
    echo "El directorio $respaldos_dir no existe. Creando..."
    mkdir -p "$respaldos_dir"
fi

if [ ! -d "$logs_dir" ]; then
    echo "El directorio $logs_dir no existe. Creando..."
    mkdir -p "$logs_dir"
fi

# Ejecución del script en Python
start_time=$(date +"%Y-%m-%d %H:%M:%S")
echo "Ejecución del facturador iniciada en $start_time" | tee -a "$log_file"

python3 "$script_python" >> "$log_file" 2>&1

# Registro de finalización
end_time=$(date +"%Y-%m-%d %H:%M:%S")
echo "Ejecución finalizada en $end_time" | tee -a "$log_file"
