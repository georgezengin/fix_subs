# Function to delete specific elements
function Delete-Garbage {
    # Array of file masks to delete
    $fileMasks = @(
        "RARBG.TXT",
        "RARBG_DO_NOT_MIRROR.exe",
        "NEW*.txt",
        "[TGx]Downloaded from torrentgalaxy*.txt",
        "WWW*.jpg"
    )
    
    $directories = Get-ChildItem -Directory
    foreach ($dir in $directories) {
        Write-Host "[${dir.Name}] PS: Checking movie folder: ${dir.Name}"
        Push-Location $dir.FullName
        
        foreach ($mask in $fileMasks) {
            Get-ChildItem -Path $mask -ErrorAction SilentlyContinue | Remove-Item -ErrorAction SilentlyContinue
        }

        # foreach ($element in $elementsToDelete) {
        #     if (Test-Path $element) {
        #         Remove-Item $element -Force -Recurse
        #         Write-Output "Deleted $element"
        #     }
        # }

        Pop-Location
    }
}

# Recurse through all subdirectories
Get-ChildItem -Directory | ForEach-Object {
    $d = $_.FullName
    Write-Output "[$d] PS1: Checking movie folder: $d"
    
    Push-Location $d

    # Define the command to run the Python script with all passed parameters
    $pythonScriptPath = "..\__fixsubs\fix_subs.py"
    $pythonCommand = "python $pythonScriptPath $args"
    
    # Execute the Python script
    Write-Host $pythonCommand
    # Execute the Python script using the command stored in CMD
    if (-not (Invoke-Expression $pythonCommand)) {
        Exit 1
    }
    # Call the function to cleanup dirs
    Delete-Garbage

    Pop-Location

    Write-Output ""
}

Write-Host
