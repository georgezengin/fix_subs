#!/bin/bash

delete_elements() {
    local elements_to_delete=(
        "RARBG.TXT"
        "RARBG_DO_NOT_MIRROR.exe"
        "NEW*.txt"
        "YTS*.txt"
        "[TGx]Downloaded from torrentgalaxy*.txt"
    )
    
    for element in "${elements_to_delete[@]}"; do
        if [ -f "$element" ]; then
            rm "$element"
            echo "Deleted file: $element"
        elif [ -d "$element" ]; then
            rm -r "$element"
            echo "Deleted directory: $element"
        elif ls "$element" 1> /dev/null 2>&1; then
            rm "$element"
            echo "Deleted matching files: $element"
        fi
    done
}

# Recurse through all subdirectories
for d in */ ; do
    echo "[$d] BASH: Checking movie folder: $d"
    
    # Change to the directory
    cd "$d" || continue

    # Call the function to delete elements
    delete_elements

    # Define the command to run the Python script with all passed parameters
    CMD=(python x:/2/_mov/__fixsubs/fix_year.py "$@")

    # Execute the Python script using the command stored in CMD
    if ! "${CMD[@]}"; then
        exit 1
    fi
    
    # Change back to the parent directory
    cd ..

    echo ""
done
