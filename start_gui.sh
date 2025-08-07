#!/bin/bash

# MD to DOCX 변환기 GUI 실행 스크립트 (macOS/Linux)

echo "==================================================="
echo "  MD to DOCX 변환기 GUI (macOS/Linux)"
echo "==================================================="
echo

# 스크립트 경로로 이동
cd "$(dirname "$0")"

# Python 확인
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3가 설치되지 않았습니다."
    echo "Python 3.7 이상을 설치해주세요."
    echo "https://www.python.org/downloads/"
    echo
    exit 1
fi

echo "Python 버전 확인..."
python3 --version
echo

# 가상환경 확인 및 생성
if [ ! -d "venv" ]; then
    echo "가상환경을 생성합니다..."
    python3 -m venv venv
    echo
fi

# 가상환경 활성화
echo "가상환경을 활성화합니다..."
source venv/bin/activate

# 패키지 설치 확인
echo "필요한 패키지를 확인하고 설치합니다..."
pip install -q python-docx==0.8.11
pip install -q Pillow==10.0.0

echo

# tkinter 설치 확인 (macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    if ! python3 -c "import tkinter" 2>/dev/null; then
        echo "tkinter가 설치되지 않았습니다."
        echo "다음 명령으로 설치하세요:"
        echo "brew install python-tk"
        echo
        exit 1
    fi
fi

# GUI 실행
echo "GUI 애플리케이션을 시작합니다..."
echo

python3 gui_converter.py