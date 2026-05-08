@echo off
cd /d "%~dp0"
set PYTHONUTF8=1

echo Starting Agency Swarm server...
start "Agency Swarm Server" /min "C:\Users\Richard\AppData\Local\Python\bin\python.exe" server.py

echo Waiting for server to start...
timeout /t 8 /nobreak >nul

echo Starting swarm UI...
"C:\Users\Richard\AppData\Local\Python\bin\python.exe" swarm.py

if %errorlevel% neq 0 (
    echo.
    echo Swarm exited with error code %errorlevel%
    pause
)
