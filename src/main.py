#!/bin/bash

input_file="${1:-testcase.txt}"
output_file="${2:-output.txt}"

awk -F ';' '
function ceil(x) {
    return (x == int(x)) ? x : int(x) + (x > 0)
}
function round_up(val) {
    return ceil(val * 10) / 10
}

{
    # Skip invalid lines (exactly two fields required and second field is a number)
    if (NF != 2 || $2 !~ /^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?/) return

    city = $1
    value = $2 + 0

    # Initialize statistics for the city if not already done
    if (!(city in min)) {
        min[city] = max[city] = sum[city] = value
        count[city] = 1
    } else {
        if (value < min[city]) min[city] = value
        if (value > max[city]) max[city] = value
        sum[city] += value
        count[city]++
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
