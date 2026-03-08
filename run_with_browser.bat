@echo off
title Video Generator
echo Starting Video Generator...

REM Install dependencies
pip install -r requirements.txt

REM Start server and open browser
echo.
echo Server starting at: http://127.0.0.1:5000
echo Opening browser in 3 seconds...
echo.

REM Start server in background and open browser
start /B python app.py
timeout /t 3 /nobreak >nul 2>&1
start http://127.0.0.1:5000

echo Video Generator is running!
echo.
echo Press any key to stop the server...
pause >nul
