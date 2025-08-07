@echo off
chcp 65001 >nul

echo ==================================================
echo  MD to DOCX 변환기 GUI (Windows)
echo ==================================================
echo.

REM 스크립트 경로로 이동
cd /d "%~dp0"

REM 가상환경 확인
if not exist venv (
    echo ERROR: 가상환경이 설정되지 않았습니다.
    echo setup.bat을 먼저 실행해주세요.
    echo.
    pause
    exit /b 1
)

REM 가상환경 활성화
echo 가상환경을 활성화합니다...
call venv\Scripts\activate.bat

REM 패키지 설치 확인
echo 필요한 패키지를 확인하고 설치합니다...
pip install -q python-docx==0.8.11 2>nul
pip install -q Pillow==10.0.0 2>nul

echo.

REM tkinter 확인 (Windows는 기본 설치됨)
python -c "import tkinter" 2>nul
if errorlevel 1 (
    echo ERROR: tkinter를 찾을 수 없습니다.
    echo Python을 다시 설치하고 tkinter 옵션을 선택해주세요.
    echo.
    pause
    exit /b 1
)

REM GUI 실행
echo GUI 애플리케이션을 시작합니다...
echo.

python gui_converter.py

if errorlevel 1 (
    echo.
    echo GUI 실행 중 오류가 발생했습니다.
    echo.
    pause
)