#!/bin/bash

# MD to DOCX 변환 스크립트
# 사용법: ./convert.sh input.md [output.docx]

if [ $# -lt 1 ]; then
    echo "사용법: $0 <input.md> [output.docx]"
    echo "예시: $0 document.md"
    echo "예시: $0 document.md custom_output.docx"
    exit 1
fi

INPUT_FILE="$1"
OUTPUT_FILE="$2"

# 입력 파일 존재 확인
if [ ! -f "$INPUT_FILE" ]; then
    echo "오류: 입력 파일을 찾을 수 없습니다: $INPUT_FILE"
    exit 1
fi

# 가상환경 활성화 및 변환 실행
echo "MD to DOCX 변환을 시작합니다..."
echo "입력 파일: $INPUT_FILE"

# 가상환경이 없다면 생성
if [ ! -d "venv" ]; then
    echo "가상환경을 생성합니다..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# output 폴더가 없으면 생성
mkdir -p output

# 변환 실행
if [ -n "$OUTPUT_FILE" ]; then
    # 출력 파일이 지정된 경우, output 폴더에 저장
    OUTPUT_PATH="output/$OUTPUT_FILE"
    python md_to_docx_converter.py "$INPUT_FILE" "$OUTPUT_PATH"
else
    python md_to_docx_converter.py "$INPUT_FILE"
fi

if [ $? -eq 0 ]; then
    echo "변환이 완료되었습니다!"
else
    echo "변환 중 오류가 발생했습니다."
    exit 1
fi