@echo off
chcp 65001 > nul
echo ==========================================
echo   사업계획서 자동 생성 시스템 (GUI 모드)
echo ==========================================
echo.

echo 🚀 GUI 변환 프로그램을 시작합니다...
cd /d "%~dp0"

python gui_converter.py
if %errorlevel% neq 0 (
    echo ❌ GUI 실행 실패
    echo Python 또는 tkinter에 문제가 있을 수 있습니다.
    pause
    exit /b 1
)