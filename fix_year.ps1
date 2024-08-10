# Function to delete specific elements
function Clear-Garbage {
    # Array of file masks to delete
    $fileMasks = @(
        "RARBG.TXT",
        "RARBG_DO_NOT_MIRROR.exe",
        "NEW*.txt",
        "YTS*.txt",
        "[TGx]Downloaded from torrentgalaxy*.txt",
        "WWW*.jpg",
        "ExtraTorrent*.*"
    )
    
    $directories = Get-ChildItem -Directory
    foreach ($dir in $directories) {
        # Explicitly convert the directory name to a string
        $dirName = $dir.Name
        $escapedPath = $dir.FullName -replace '\[', '``[' -replace '\]', '``]'
        Write-Host "[$dirName] PS: Checking movie folder: $dirName"
        if (Test-Path -Path $escapedPath) {
            Push-Location -Path $escapedPath
        #    Push-Location -Path $dir.FullName
            foreach ($mask in $fileMasks) {
                Write-Host "`tChecking [$mask]: " -NoNewLine
                if (Test-Path $mask) {
                    $files = Get-ChildItem -Path $mask -ErrorAction SilentlyContinue

                    if ($files) {
                        Write-Host "`tFound files like [$mask]"
                        foreach ($file in $files) {
                            Write-Output "`t`tFound: $($file.FullName)"
                            # Uncomment the next line if you want to delete the file
                            # Remove-Item -Path $file.FullName -Force
                            Write-Output "`t`tDeleted $($file.FullName)"
                        }
                    } else {
                        Write-Output "`t`tNothing found for $mask"
                    }
                    #Write-Output "Deleted $mask"
                } else {
                    Write-Output "`tNothing found"
                }
            }
        } else {
            Write-Host "`t*** Directory error: $($dir.FullName)`a"
        }

        Pop-Location
    }
}

# Define the command to run the Python script with all passed parameters
$pythonScriptPath = "x:\2\_mov\__fixsubs\fix_year.py"
$pythonCommand = "python"

# Execute the Python script
Write-Host "Starting"
Write-Host $pythonCommand
# Start the process
$process = Start-Process -FilePath "$pythonCommand" -ArgumentList "$pythonScriptPath $args" -NoNewWindow -RedirectStandardOutput "output.txt" -RedirectStandardError "error.txt" -PassThru -Wait

# Read and display output in real-time
Get-Content "output.txt" -Wait | ForEach-Object { Write-Host $_ }
Get-Content "error.txt" -Wait | ForEach-Object { Write-Host $_ }

# Check exit code
if ($process.ExitCode -ne 0) {
    Write-Host "Error occurred during execution."
    Exit 1
}
#if (-not (Invoke-Expression $pythonCommand)) {
    #Exit 1
#}

Clear-Garbage


Write-Host
