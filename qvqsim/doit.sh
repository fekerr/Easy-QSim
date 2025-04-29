#!/bin/bash
# begin file doit.sh

DOITPY="quantum-sim-basic-CHSH.py"

# Define file name parts.
log_prefix="doit_log_"
log_suffix=".txt"

# Look for existing log files matching the pattern.
existing_logs=( ${log_prefix}[0-9][0-9][0-9]${log_suffix} )
next_num="001"
if [ -e "${existing_logs[0]}" ]; then
    max=0
    for logfile in "${existing_logs[@]}"; do
        num=$(basename "$logfile" "$log_suffix")
        num=${num#${log_prefix}}
        num=$((10#$num))
        if (( num > max )); then
            max=$num
        fi
    done
    next=$(printf "%03d" "$((max + 1))")
    next_num="$next"
fi

# Compute the new log file name.
log_file="${log_prefix}${next_num}${log_suffix}"

# Run the quantum simulator and redirect stdout and stderr.
python ${DOITPY} "path/to/input_file" > "$log_file" 2>&1
echo "Output logged to $log_file"

# Determine the maximum number of lines to output.
max_lines=${QVSIM_LOGOUT:-25}

# Count the lines in the log file.
line_count=$(wc -l < "$log_file")
if [ "$line_count" -le "$max_lines" ]; then
    cat "$log_file"
else
    head -n "$max_lines" "$log_file"
fi

# Touch a dummy stamp file to satisfy the custom target output.
touch doit.stamp

# end file doit.sh
