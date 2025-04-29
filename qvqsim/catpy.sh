#!/bin/bash

for file in *.py; do
    echo "# $file begins"
    cat "$file"
    echo "# $file ends"
    echo
done
