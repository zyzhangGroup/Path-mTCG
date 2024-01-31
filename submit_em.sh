#!/bin/bash

# Script for coordinating and running energy minimization jobs
# Define variables
TEMP=$1
HOST=$2
N_SUB=$3
NAME="$4"
INP1=em1.inp
INP2=em2.inp
N_LINES=$((N_SUB * (N_SUB - 1) / 2))

# Check if temp dir exists and create if needed
if [ ! -d "Setup" ]; then
    mkdir "Setup" || { echo "Failed to create directory: Setup"; exit 1; }
fi

# Change directory to "Setup" and if the operation fails, print an error message and exit the program
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


# Extract the inter-subunit contact map from the em1.ninfo file
# Use the grep command to extract lines containing "total_contact_unit" from the em1.ninfo file and redirect the output to the contmp.txt file
grep "total_contact_unit" em1.ninfo > contmp.txt

# Use the awk command to print the 4th column from the contmp.txt file and redirect the output to the all_con.txt file
awk '{print $4}' contmp.txt > all_con.txt

# Sub_con generates all_contact.txt that is a matrix of inter-subunit contact numbers
# Invoke the Sub_con script, passing the all_con.txt file as an argument to the Sub_con script and N_SUB as the second argument
./../../Script/Sub_con $N_SUB all_con.txt
 
# Copy all_contact.txt to the Result_Tq directory, preparing for processing ts files in the results
cp all_contact.txt ../../Result_Tq/