import os
import subprocess

# Create the Bash script content with corrected escape sequences
bash_script_content = r"""#!/bin/bash

input_file="${1:-testcase.txt}"
output_file="${2:-output.txt}"

awk -F ';' '
function ceil(x) {
    return (x == int(x)) ? x : int(x) + (x > 0)
}
function round_up(val) {
    scaled = val * 10
    return ceil(scaled) / 10
}

{
    # Skip invalid lines (exactly two fields required)
    if (NF != 2) next
    if ($2 !~ /^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$/) next

    city = $1
    value = $2 + 0

    # Update statistics
    if (city in min) {
        if (value < min[city]) min[city] = value
        if (value > max[city]) max[city] = value
        sum[city] += value
        count[city]++
    } else {
        min[city] = max[city] = sum[city] = value
        count[city] = 1
    }
}
END {
    for (city in sum) {
        avg = sum[city] / count[city]
        printf "%s=%.1f/%.1f/%.1f\n", 
            city, 
            round_up(min[city]), 
            round_up(avg), 
            round_up(max[city])
    }
}' "$input_file" | sort -t '=' -k1,1 > "$output_file"
"""

script_name = "script.sh"

try:
    # Write the Bash script to a file with Unix-style line endings
    with open(script_name, "w", newline="\n") as f:
        f.write(bash_script_content)

    # Make the script executable
    os.chmod(script_name, 0o755)

    # Execute the script
    subprocess.run(["bash", script_name], check=True)

except subprocess.CalledProcessError as e:
    print(f"Error executing the script: {e}")
finally:
    # Cleanup: Delete the script if needed
    # pass
    if os.path.exists(script_name):
        os.remove(script_name)
