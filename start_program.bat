@echo off
echo ==========================================
echo   Business Plan Generator
echo ==========================================
echo.
echo Starting program...
cd /d "%~dp0"
python gui_converter.py
if %errorlevel% neq 0 (
    echo.
    echo X Program failed to start
    echo Please check if setup was completed successfully
    pause
)
echo.
echo Program closed.