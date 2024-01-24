#!/bin/bash

# Extract job parameters
TEMP=$1
HOST=$2
N_SUB=$3
NAME="$4"
INP=protein.inp
N_LINES=$((N_SUB * (N_SUB - 1) / 2))

# Check if TEMP directory exists, create it if it doesn't
if [ ! -d "$TEMP" ]; then
    # Create the TEMP directory
    mkdir "$TEMP" || { echo "Failed to create directory: $TEMP"; exit 1; }
fi

cd "$TEMP" || { echo "Failed to change to directory: $TEMP"; exit 1; }

# Create a reusable sed function
sed_replace() {
    local input_file="$1"
    local output_file="$2"
    local pattern1="$3"
    local replacement1="$4"
    local pattern2="$5"
    local replacement2="$6"
    local pattern3="$7"
    local replacement3="$8"
    local source_file="../../Input/$input_file"
    sed -e "s/$pattern1/$replacement1/g" -e "s/$pattern2/$replacement2/g" -e "s/$pattern3/$replacement3/g" "$source_file" > "$output_file"
}

# Use the sed_replace function to avoid repeating sed commands
sed_replace "$INP" "$INP" "1-n" "1-$N_SUB" "TEMP" "$TEMP" "Protein" "$NAME" | tee "$INP"
wait
# Write hostname to hostfile
printf "%s" "$HOST" > hostfile

# Run a job and wait for its completion using INP file from TEMP directory as input, save output to TEMP.out
mpirun -hostfile hostfile cafemol "${INP}" > ${TEMP}.out
wait

# Process output using NAME.ts as input, save output to qscore_inter.txt
tail -n "$N_LINES" ${NAME}.ts | awk '{print $8}' > qscore_inter.txt
wait

# Call the test script with N_SUB and qscore_inter.txt as arguments
../../Script/T_Sub "$N_SUB" qscore_inter.txt
wait

# Copy files to q_temp directory with error handling
cp "$NAME.ts" "../../Result_Tq/$TEMP.ts" || { echo "Failed to copy $NAME.ts"; exit 1; }
cp subunit.txt "../../Result_Tq/$TEMP.txt" || { echo "Failed to copy subunit.txt"; exit 1; }
