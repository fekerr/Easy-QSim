#!/bin/bash
#
# doit.sh: Run the quantum simulator and log stdout & stderr to a file with an
# incremented sequence number (e.g., doit_log_001.txt, doit_log_002.txt,
# etc.). After running, if the log file has 25 or fewer lines, output the whole file;
# otherwise, output only the first 25 lines.
#

# Define file name parts.
log_prefix="doit_log_"
log_suffix=".txt"

# Look for existing log files matching the pattern.
existing_logs=( ${log_prefix}[0-9][0-9][0-9]${log_suffix} )
next_num="001"

if [ -e "${existing_logs[0]}" ]; then
    max=0
    for logfile in "${existing_logs[@]}"; do
        # Extract the numeric part from the filename.
        num=$(basename "$logfile" "$log_suffix")
        num=${num#${log_prefix}}
        # Remove any leading zeros for numeric comparison.
        num=$((10#$num))
        if (( num > max )); then
            max=$num
        fi
    done
    next=$(printf "%03d" "$((max + 1))")
    next_num="$next"
fi

# Generate the new log file name.
log_file="${log_prefix}${next_num}${log_suffix}"

# Run the quantum simulator, redirecting stdout and stderr into the log file.
python qvqsim.py path/to/input_file > "$log_file" 2>&1

echo "Output logged to $log_file"

# Check the number of lines in the log file.
line_count=$(wc -l < "$log_file")
if [ "$line_count" -le 25 ]; then
    # If fewer than or equal to 25 lines, output the entire file.
    cat "$log_file"
else
    # Otherwise, output only the first 25 lines.
    head -n 25 "$log_file"
fi

# Touch a dummy stamp file to signal completion for Meson integration.
touch doit.stamp
