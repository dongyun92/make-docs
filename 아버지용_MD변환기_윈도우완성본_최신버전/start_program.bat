@echo off
echo ==========================================
echo   MD to DOCX Converter (Latest Version)
echo ==========================================
echo.
echo Starting program...
cd /d "%~dp0"

echo Detecting best Python version...
py -3.13 --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Using Python 3.13 via launcher
    py -3.13 gui_converter.py
) else (
    py -3.12 --version >nul 2>&1
    if %errorlevel% equ 0 (
        echo Using Python 3.12 via launcher  
        py -3.12 gui_converter.py
    ) else (
        echo Using default Python
        py gui_converter.py
    )
)
if %errorlevel% neq 0 (
    echo.
    echo X Program failed to start
    echo Please check if setup was completed successfully
    pause
)
echo.
echo Program closed.