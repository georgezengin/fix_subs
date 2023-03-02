@echo off
rem ** recurse thru all subdirs
for /d %%d in (*) do (
    cd %%d
    rem echo [%%d] BAT: Checking movie folder: %%d

    if exist RARBG.TXT del RARBG.TXT
    if exist RARBG_DO_NOT_MIRROR.exe del RARBG_DO_NOT_MIRROR.exe
    if exist "[TGx]Downloaded from torrentgalaxy*.txt" del "[TGx]Downloaded from torrentgalaxy*.txt"

    python x:\2\_mov\__python\fix_year.py %1 %2
	if errorlevel 1 exit /b
    cd ..

    echo. 
)
rem pause