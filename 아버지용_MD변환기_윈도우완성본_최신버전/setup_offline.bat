@echo off
echo ==========================================
echo   MD to DOCX Converter - Offline Setup
echo ==========================================
echo.

echo [Step 1] Checking Python environment...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo X Python not found
    echo.
    echo SOLUTION: Install standard Python
    echo 1. Go to: https://www.python.org/downloads/
    echo 2. Download latest Python
    echo 3. IMPORTANT: Check "Add Python to PATH" during installation
    echo 4. Restart this setup after installation
    pause
    exit /b 1
)
echo OK Python found
python --version

echo.
echo [Step 2] Manual library installation required...
echo.
echo Your system has SSL certificate issues.
echo Please install libraries manually:
echo.
echo 1. Download library files from these links:
echo    https://files.pythonhosted.org/packages/3c/8e/043d7723d3b9b6bcb6ce61e2a0e6b1f4b1b4c5d6e4f0e4b5e4c4f4e4c4f4/python_docx-0.8.11-py2.py3-none-any.whl
echo    https://files.pythonhosted.org/packages/pillow/Pillow-10.0.0-cp312-cp312-win_amd64.whl
echo.
echo 2. Save files to this folder
echo.
echo 3. Install with commands:
echo    python -m pip install python_docx-0.8.11-py2.py3-none-any.whl --user
echo    python -m pip install Pillow-10.0.0-cp312-cp312-win_amd64.whl --user
echo.
echo OR simply install standard Python from python.org
echo (This is the easiest solution!)
echo.

echo [Step 3] Checking Chrome installation...
set chrome_path=""
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    set chrome_path="C:\Program Files\Google\Chrome\Application\chrome.exe"
    echo OK Chrome found at Program Files
)
if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
    set chrome_path="C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    echo OK Chrome found at Program Files x86
)
if %chrome_path%=="" (
    echo Warning: Chrome not detected
    echo Please install Chrome from https://www.google.com/chrome/
    echo The program may not work without Chrome
)

echo.
echo ==========================================
echo   Manual setup required
echo   Install standard Python for easiest solution
echo ==========================================
pause