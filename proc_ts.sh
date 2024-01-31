#!/bin/bash

# Set variables
TEMP=$1
START_NUM=1
END_NUM=$2

# Set file names
DATA_NAME="${TEMP}.ts"
SAVE_NAME="${TEMP}_allqa.txt"

# Loop through the data range
for (( i=START_NUM; i<END_NUM; i++ )); do
    TEMP_ARN_FILE="${TEMP}-${i}_qt.dat"
    # Filter out lines containing "#$i " from DATA_NAME and save to TEMP_ARN_FILE
    grep "#$i " "${DATA_NAME}" > "${TEMP_ARN_FILE}"
   # echo "${TEMP_ARN_FILE},$i"
    for (( j=i+1; j<=END_NUM; j++ )); do
        TEMP_ARN_FILE_2="${TEMP}-${i}-${j}_qt.dat"
        # Filter out lines containing "  -$j  " from TEMP_ARN_FILE and save to TEMP_ARN_FILE_2
        grep "  -$j  " "${TEMP_ARN_FILE}" > "${TEMP_ARN_FILE_2}"
        num=$(printf %02d ${i})
        numf=$(printf %02d $[$j])
        # Extract the 8th column from TEMP_ARN_FILE_2 and save it to a file
        awk '{print $8}' "${TEMP_ARN_FILE_2}" > "${TEMP}-${num}-${numf}_qall.txt"
        #echo "${num}-${numf}_qall.txt,$j"
    done
    
    if [[ "${i}" -eq 1 ]]; then
        # If i equals 1, concatenate all files ending with -i_qall.txt into ${TEMP}_${num}_qa.txt
        paste  ${TEMP}-${num}-*_qall.txt > "${TEMP}_${num}_qa.txt"
    elif [[ "${i}" -eq "$[${END_NUM}-1]" ]]; then
        # If i equals END_NUM-1, concatenate all files ending with -j_qall.txt and also those starting with ${num}- into ${TEMP}_${numf}_qa.txt
        paste ${TEMP}-*-${numf}_qall.txt  > "${TEMP}_${numf}_qa.txt"
        paste ${TEMP}-*-${num}_qall.txt ${TEMP}-${num}-*_qall.txt > "${TEMP}_${num}_qa.txt"
    else
        # Otherwise, concatenate all files ending with -i_qall.txt and also those starting with ${num}- into ${TEMP}_${num}_qa.txt
        paste ${TEMP}-*-${num}_qall.txt ${TEMP}-${num}-*_qall.txt > "${TEMP}_${num}_qa.txt"
    fi
done

# Concatenate all _qall.txt files into ${SAVE_NAME}
paste ${TEMP}-*_qall.txt > "${SAVE_NAME}"

# Remove temporary files
rm -rf ${TEMP}-*-*.txt
rm  -rf ${TEMP}-*.dat
