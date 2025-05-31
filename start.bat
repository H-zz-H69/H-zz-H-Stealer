@echo off
setlocal enabledelayedexpansion

set "user=%USERNAME%"

set "PYTHONPATH=C:\Users\%user%\AppData\Local\Programs\Python\Python39\python.exe"

if exist "%PYTHONPATH%" (
    echo Found Python at %PYTHONPATH%
    set "PYEXE=%PYTHONPATH%"
    goto runscript
)

echo Python not found at %PYTHONPATH%
set /p yn=Download and install Python 3.9.11 locally? (Y/N): 
if /I not "%yn%"=="Y" (
    echo Install cancelled.
    pause
    exit /b
)

echo Downloading portable Python 3.9.11...
powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.9.11/python-3.9.11-embed-amd64.zip' -OutFile 'python-portable.zip'"

powershell -Command "Expand-Archive -Path 'python-portable.zip' -DestinationPath 'Python3911' -Force"

del python-portable.zip

if not exist "Python3911\python.exe" (
    echo Extraction failed or python.exe not found.
    pause
    exit /b
)

set "PYEXE=%cd%\Python3911\python.exe"

:runscript
"%PYEXE%" -m ensurepip --default-pip
"%PYEXE%" -m pip install --upgrade pip
"%PYEXE%" -m pip install -r requirements.txt
"%PYEXE%" main.py

pause
