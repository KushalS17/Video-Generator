@echo off
title Video Generator
echo Starting Video Generator...

REM Install dependencies
pip install -r requirements.txt

REM Start server
echo.
echo Server starting at: http://127.0.0.1:5000
echo.
python app.py

pause
