@echo off
chcp 65001 >nul
echo ==================================================
echo  MD to DOCX 변환기 (Windows)
echo ==================================================
echo.

REM 가상환경 활성화
if not exist venv (
    echo ERROR: 가상환경이 설정되지 않았습니다.
    echo setup.bat을 먼저 실행해주세요.
    echo.
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

REM Chrome 경로 설정 (필요시 수정)
set "CHROME_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe"
if not exist "%CHROME_PATH%" (
    set "CHROME_PATH=C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
)
if not exist "%CHROME_PATH%" (
    echo WARNING: Chrome을 찾을 수 없습니다.
    echo Chrome 경로를 확인해주세요: %CHROME_PATH%
    echo.
)

REM Markdown 파일 찾기
set "md_file="
for %%f in (*.md) do (
    if not defined md_file (
        set "md_file=%%f"
    )
)

if not defined md_file (
    echo ERROR: Markdown 파일(*.md)을 찾을 수 없습니다.
    echo 이 폴더에 변환할 .md 파일을 넣어주세요.
    echo.
    dir *.md 2>nul || echo (Markdown 파일 없음)
    echo.
    pause
    exit /b 1
)

echo 발견된 Markdown 파일: %md_file%
echo.

REM 차트 이미지 생성
echo 차트 이미지를 생성합니다...
if exist images\market_growth_line.html (
    "%CHROME_PATH%" --headless --disable-gpu --hide-scrollbars --force-device-scale-factor=1 --window-size=700,600 --screenshot=images\market_growth_line.png images\market_growth_line.html 2>nul
    echo - 시장 성장 추세 차트 생성됨
)

if exist images\market_growth_regional.html (
    "%CHROME_PATH%" --headless --disable-gpu --hide-scrollbars --force-device-scale-factor=1 --window-size=700,600 --screenshot=images\market_growth_regional.png images\market_growth_regional.html 2>nul
    echo - 지역별 성장 전망 차트 생성됨
)

if exist images\budget_pie.html (
    "%CHROME_PATH%" --headless --disable-gpu --hide-scrollbars --force-device-scale-factor=1 --window-size=700,600 --screenshot=images\budget_pie.png images\budget_pie.html 2>nul
    echo - 예산 분배 차트 생성됨
)

if exist images\budget_trend.html (
    "%CHROME_PATH%" --headless --disable-gpu --hide-scrollbars --force-device-scale-factor=1 --window-size=700,600 --screenshot=images\budget_trend.png images\budget_trend.html 2>nul
    echo - 예산 추세 차트 생성됨
)

echo.

REM DOCX 변환 실행
echo Markdown을 DOCX로 변환합니다...
python md_to_docx_converter.py "%md_file%"

if %errorlevel% == 0 (
    echo.
    echo ==================================================
    echo  변환이 완료되었습니다!
    echo ==================================================
    echo.
    echo 생성된 파일들:
    for %%f in (*.docx) do (
        echo - %%f
    )
    echo.
    echo 이미지 파일들:
    if exist images\*.png (
        for %%f in (images\*.png) do (
            echo - %%f
        )
    )
    echo.
) else (
    echo.
    echo ERROR: 변환 중 오류가 발생했습니다.
    echo 오류 내용을 확인하고 다시 시도해주세요.
    echo.
)

echo 아무 키나 눌러서 종료하세요...
pause >nul