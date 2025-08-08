#!/usr/bin/env python3
"""
HTML 파일들의 크기 설정을 수정하여 이미지가 잘리지 않도록 개선
"""

import os
import glob
import re

def fix_html_size(html_file_path: str):
    """HTML 파일의 크기 설정을 수정하여 전체 내용이 보이도록 개선"""
    
    with open(html_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 기존 body 스타일에서 고정 크기 제거
    body_style_pattern = r'body\s*{[^}]*}'
    
    # 새로운 body 스타일 - 자동 크기 조정
    new_body_style = '''body {
            margin: 0;
            padding: 20px;
            min-width: 900px;
            min-height: 600px;
            font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
            background: white;
            box-sizing: border-box;
        }'''
    
    # body 스타일 교체
    content = re.sub(body_style_pattern, new_body_style, content)
    
    # chart-container 크기도 수정
    container_style_pattern = r'\.chart-container\s*{[^}]*}'
    
    new_container_style = '''.chart-container {
            min-height: 500px;
            background: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            max-width: 860px;
            margin: 0 auto;
        }'''
    
    content = re.sub(container_style_pattern, new_container_style, content)
    
    # html2canvas 설정도 수정 - 자동 크기 감지
    html2canvas_pattern = r'html2canvas\(document\.body,\s*{[^}]*}\)'
    
    new_html2canvas_config = '''html2canvas(document.body, {
                    useCORS: true,
                    allowTaint: true,
                    scale: 1,
                    backgroundColor: '#ffffff'
                })'''
    
    content = re.sub(html2canvas_pattern, new_html2canvas_config, content)
    
    # 수정된 내용 저장
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 크기 설정 수정 완료: {os.path.basename(html_file_path)}")

def fix_all_rwsl_html_files():
    """모든 RWSL HTML 파일의 크기 설정 수정"""
    
    # RWSL HTML 파일들 찾기
    all_html_files = glob.glob('/Users/dykim/dev/make-docs/images/*.html')
    rwsl_files = [f for f in all_html_files if 'rwsl' in os.path.basename(f).lower()]
    
    # 추출기 파일은 제외
    rwsl_files = [f for f in rwsl_files if 'extractor' not in os.path.basename(f).lower()]
    
    print(f"🔧 RWSL HTML 파일 크기 설정 수정: {len(rwsl_files)}개")
    
    for html_file in rwsl_files:
        fix_html_size(html_file)
    
    print(f"\n🎉 모든 RWSL HTML 파일 크기 설정 수정 완료!")
    print("📋 수정 내용:")
    print("  - 고정 width/height 제거")
    print("  - min-width: 900px, min-height: 600px로 변경") 
    print("  - overflow: hidden 제거")
    print("  - html2canvas scale을 1로 조정")
    print("  - 자동 크기 감지로 전체 내용 캡처")

if __name__ == "__main__":
    fix_all_rwsl_html_files()