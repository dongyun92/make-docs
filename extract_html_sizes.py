#!/usr/bin/env python3
"""
HTML 파일에서 실제 크기를 추출하여 정확한 PNG 생성
"""

import os
import re
import subprocess

def extract_size_from_html(html_file):
    """HTML 파일에서 컨테이너 크기 추출"""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # .container 스타일에서 width와 height 추출
        container_match = re.search(r'\.container\s*\{[^}]*width:\s*(\d+)px[^}]*height:\s*(\d+)px[^}]*\}', content)
        if container_match:
            width = int(container_match.group(1))
            height = int(container_match.group(2))
            
            # padding 고려 (일반적으로 15px씩 양쪽)
            padding_match = re.search(r'padding:\s*(\d+)px', content)
            if padding_match:
                padding = int(padding_match.group(1))
                total_width = width + (padding * 2)
                total_height = height + (padding * 2)
            else:
                total_width = width + 30  # 기본 padding
                total_height = height + 30
                
            return total_width, total_height
        
        # 다른 패턴들도 확인
        width_match = re.search(r'width:\s*(\d+)px', content)
        height_match = re.search(r'height:\s*(\d+)px', content)
        
        if width_match and height_match:
            return int(width_match.group(1)) + 50, int(height_match.group(1)) + 50
            
    except Exception as e:
        print(f"⚠️ {html_file} 크기 추출 실패: {e}")
        
    # 기본 크기 반환
    return 800, 600

def generate_accurate_pngs():
    """HTML의 정확한 크기로 PNG 생성"""
    
    html_files = [f for f in os.listdir('images/') if f.endswith('.html')]
    
    for html_file in html_files:
        html_path = f"images/{html_file}"
        png_file = html_file.replace('.html', '.png')
        png_path = f"images/{png_file}"
        
        # HTML에서 실제 크기 추출
        width, height = extract_size_from_html(html_path)
        
        print(f"📐 {html_file}: {width}x{height}")
        
        try:
            cmd = [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "--headless",
                "--disable-gpu",
                "--hide-scrollbars", 
                "--force-device-scale-factor=1",
                f"--window-size={width},{height}",
                f"--screenshot={png_path}",
                html_path
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ {png_file} 생성 완료 (정확한 크기: {width}x{height})")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ {png_file} 변환 실패: {e}")

if __name__ == "__main__":
    print("🔍 HTML 파일에서 실제 크기 추출하여 PNG 생성...")
    generate_accurate_pngs()
    print("✨ 정확한 크기로 PNG 생성 완료!")