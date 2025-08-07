@echo off
echo ==========================================
echo   Business Plan Generator Setup
echo ==========================================
echo.

echo [Step 1] Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo X Python not found
    echo Please install Python from https://www.python.org/downloads/
    echo IMPORTANT: Check "Add Python to PATH" during installation
    pause
    exit /b 1
)
echo OK Python found
python --version

echo.
echo [Step 2] Installing required libraries...
echo Installing: python-docx
python -m pip install python-docx --user
echo Installing: pillow  
python -m pip install pillow --user
echo Installing: beautifulsoup4
python -m pip install beautifulsoup4 --user
echo Installing: lxml
python -m pip install lxml --user
echo Installing: requests
python -m pip install requests --user

echo.
echo Verifying installations...
python -c "import docx; print('python-docx: OK')" 2>nul || echo "python-docx: FAILED"
python -c "import PIL; print('pillow: OK')" 2>nul || echo "pillow: FAILED"  
python -c "import bs4; print('beautifulsoup4: OK')" 2>nul || echo "beautifulsoup4: FAILED"
python -c "import lxml; print('lxml: OK')" 2>nul || echo "lxml: FAILED"
python -c "import requests; print('requests: OK')" 2>nul || echo "requests: FAILED"

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
echo   Setup completed!
echo   Run "start_program.bat" to begin
echo ==========================================
pause