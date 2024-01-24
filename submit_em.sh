#!/bin/bash

# Script for coordinating and running MD simulations

# Define variables

TEMP=$1
HOST=$2
N_SUB=$3
NAME="$4"
INP1=em1.inp
INP2=em2.inp
INP=protein.inp
N_LINES=$((N_SUB * (N_SUB - 1) / 2))

# Check if temp dir exists and create if needed
if [ ! -d "Setup" ]; then
    mkdir "Setup" || { echo "Failed to create directory: Setup"; exit 1; }
fi


cd "Setup" || { echo "Failed to change to directory: Setup"; exit 1; }

# Write hostname to hostfile
printf "%s" "$HOST" > hostfile

# Create a reusable sed function
sed_replace() {
    local input_file="$1"
    local output_file="$2"
    local pattern1="$3"
    local replacement1="$4"
    local pattern2="$5"
    local replacement2="$6"
    local source_file="../$input_file"
    sed -e "s/$pattern1/$replacement1/g" -e "s/$pattern2/$replacement2/g"  "$source_file" > "$output_file"
}

# Use the sed_replace function to avoid repeating sed commands
sed_replace "$INP1" "$INP1" "1-n" "1-$N_SUB" "Protein" "$NAME"  | tee "$INP1"
sed_replace "$INP2" "$INP2" "1-n" "1-$N_SUB" "Protein" "$NAME"  | tee "$INP2"

# Run simulations and include error handling
for i in 1 2; do
    mpirun -hostfile hostfile cafemol "./em${i}.inp" > "$i.out"
    wait
    awk 'n==1{print} $0~/MODEL         2/{n=1}' "em${i}.pdb" > "em${i}cg.pdb" # process PDB files
    wait
done
