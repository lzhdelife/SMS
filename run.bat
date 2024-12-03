@echo off
ipconfig | findstr "IPv4"
echo.
python main.py
