@echo off
echo ================================================
echo VM Detection System - Installation Script
echo ================================================
echo.

echo Installing core dependencies...
pip install psutil

echo.
echo Installing optional dependencies...
pip install pynput pywin32

echo.
echo ================================================
echo Installation Complete!
echo ================================================
echo.
echo Quick Start:
echo   python cli_detector.py           - Quick scan
echo   python cli_detector.py --full    - Full scan
echo   python cli_detector.py --monitor - Monitoring
echo.
pause