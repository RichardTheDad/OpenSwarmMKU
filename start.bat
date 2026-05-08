@echo off
cd /d "%~dp0"
"C:\Users\Richard\AppData\Local\Python\bin\python.exe" swarm.py
if %errorlevel% neq 0 (
    echo.
    echo Swarm exited with error code %errorlevel%
    pause
)
