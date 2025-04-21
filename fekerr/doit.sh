#!/bin/bash
#
# doit.sh: Run the quantum simulator and log stdout & stderr to a file with an
# incremented sequence number (e.g., doit_log_001.txt, doit_log_002.txt, etc.)
#

# Define log filename parts
log_prefix="doit_log_"
log_suffix=".txt"

# Find all existing log files matching the pattern
existing_logs=( ${log_prefix}[0-9][0-9][0-9]${log_suffix} )
next_num="001"

if [ -e "${existing_logs[0]}" ]; then
    max=0
    for logfile in "${existing_logs[@]}"; do
        # Extract the numeric part from the filename
        num=$(basename "$logfile" "$log_suffix")
        num=${num#${log_prefix}}
        # Remove any leading zeros for arithmetic comparison
        num=$((10#$num))
        if (( num > max )); then
            max=$num
        fi
    done
    next=$(printf "%03d" "$((max + 1))")
    next_num="$next"
fi

# Compute the new log file name
log_file="${log_prefix}${next_num}${log_suffix}"

# Run the simulator and redirect stdout and stderr to the log file
python qvqsim.py path/to/input_file > "$log_file" 2>&1

# Optionally, echo the name of the log file for reference:
echo "Output logged to $log_file"
