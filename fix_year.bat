@echo off
setlocal enabledelayedexpansion

rem Recurse through all subdirectories
echo "Starting"
rem Define the command to run the Python script with all passed parameters
set CMD=python x:\2\_mov\__fixsubs\fix_year.py . -L -R %*

rem Execute the Python script using the command stored in CMD
echo %CMD%
%CMD%
if errorlevel 1 exit /b 1

rem Call the function to delete garbage
call :delete_garbage

echo.
exit /b

rem Function to delete specific elements
:delete_garbage
rem echo "Deleting text files"
for /d %%d in (*) do (
    rem echo [%%d] BAT: Checking movie folder: %%d
    pushd %%d
    if exist RARBG.TXT del RARBG.TXT
    if exist RARBG_DO_NOT_MIRROR.exe del RARBG_DO_NOT_MIRROR.exe
    for %%f in (NEW*.txt) do if exist "%%f" del "%%f"
    for %%f in (YTS*.txt) do if exist "%%f" del "%%f"
    for %%f in (YIF*.txt) do if exist "%%f" del "%%f"
    for %%f in ("[TGx]Downloaded from torrentgalaxy*.txt") do if exist "%%f" del "%%f"
    for %%f in (WWW*.jpg) do if exist "%%f" del "%%f"
    popd
)
exit /b

endlocal
