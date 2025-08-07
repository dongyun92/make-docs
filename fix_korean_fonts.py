#!/usr/bin/env python3
"""
윈도우 한글 폰트 문제 해결을 위한 패치 스크립트
"""
import re

def fix_fonts_in_converter():
    """md_to_docx_converter.py의 폰트 문제 수정"""
    with open('md_to_docx_converter.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Arial로 변경된 부분을 다시 한글 호환으로 수정
    fixes = [
        # 기본 폰트 설정을 한글 호환으로
        (r"run\.font\.name = 'Arial'", "set_korean_font(run)"),
        (r"(\w+)_font\.name = 'Arial'", r"set_korean_font_for_style(\1_font)"),
        
        # 폰트 크기 설정이 있는 경우
        (r"run\.font\.name = 'Arial'\s+run\.font\.size = Pt\((\d+)\)", 
         r"set_korean_font(run)\n            run.font.size = Pt(\1)"),
    ]
    
    for pattern, replacement in fixes:
        content = re.sub(pattern, replacement, content)
    
    # 스타일 폰트 설정 부분 수정
    style_font_pattern = r"(\w+)_font\.name = 'Arial'"
    content = re.sub(style_font_pattern, r"set_korean_font_for_style(\1_font)", content)
    
    with open('md_to_docx_converter.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 폰트 설정 수정 완료")

if __name__ == "__main__":
    fix_fonts_in_converter()