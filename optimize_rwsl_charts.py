#!/usr/bin/env python3
import os
import re
import subprocess
import glob

def optimize_html_file(file_path):
    """HTML 파일을 최적화합니다."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # CSS 최적화 - body 태그
    body_pattern = r'body\s*{[^}]+}'
    body_replacement = """body {
            margin: 0;
            padding: 20px;
            width: 860px;
            height: 560px;
            overflow: hidden;
            font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
            background: white;
            box-sizing: border-box;
        }"""
    
    content = re.sub(body_pattern, body_replacement, content)
    
    # chart-container 최적화
    container_pattern = r'\.chart-container\s*{[^}]+}'
    container_replacement = """.chart-container {
            height: 520px;
            overflow: hidden;
            background: white;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            max-width: 830px;
            margin: 0 auto;
        }"""
    
    content = re.sub(container_pattern, container_replacement, content)
    
    # 제목 폰트 크기 최적화
    title_pattern = r'\.chart-title\s*{[^}]+}'
    title_replacement = """.chart-title {
            text-align: center;
            font-size: 16px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
        }"""
    
    content = re.sub(title_pattern, title_replacement, content)
    
    # 부제목 폰트 크기 최적화
    subtitle_pattern = r'\.chart-subtitle\s*{[^}]+}'
    subtitle_replacement = """.chart-subtitle {
            text-align: center;
            font-size: 12px;
            color: #7f8c8d;
            margin-bottom: 20px;
        }"""
    
    content = re.sub(subtitle_pattern, subtitle_replacement, content)
    
    # Chart.js 폰트 크기 최적화
    content = re.sub(r'size:\s*1[2-9]', 'size: 11', content)
    content = re.sub(r'size:\s*2[0-9]', 'size: 11', content)
    
    # 다른 폰트 크기들을 11px로 조정
    content = re.sub(r'font-size:\s*1[2-9]px', 'font-size: 11px', content)
    content = re.sub(r'font-size:\s*2[0-9]px', 'font-size: 16px', content)  # 제목은 16px 유지
    
    # 특정 클래스들 최적화
    content = re.sub(r'\.milestone-year\s*{[^}]+}', 
                     """.milestone-year {
            font-weight: bold;
            font-size: 12px;
            color: #2c3e50;
            margin-bottom: 6px;
        }""", content)
    
    content = re.sub(r'\.milestone-amount\s*{[^}]+}',
                     """.milestone-amount {
            font-size: 14px;
            font-weight: bold;
            color: #e74c3c;
            margin-bottom: 4px;
        }""", content)
    
    content = re.sub(r'\.milestone-target\s*{[^}]+}',
                     """.milestone-target {
            font-size: 9px;
            color: #7f8c8d;
        }""", content)
    
    # 범례 라벨 최적화
    content = re.sub(r'font-size:\s*1[0-1]px', 'font-size: 11px', content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Optimized: {os.path.basename(file_path)}")

def capture_html_to_png(html_file):
    """HTML 파일을 PNG로 캡처합니다."""
    html_path = html_file
    png_path = html_file.replace('.html', '.png')
    
    cmd = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "--headless",
        "--disable-gpu",
        "--hide-scrollbars",
        "--force-device-scale-factor=1",
        "--window-size=900,600",
        f"--screenshot={png_path}",
        html_path
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"✓ Captured: {os.path.basename(png_path)}")
        else:
            print(f"✗ Error capturing {os.path.basename(html_path)}: {result.stderr}")
    except subprocess.TimeoutExpired:
        print(f"✗ Timeout capturing {os.path.basename(html_path)}")
    except Exception as e:
        print(f"✗ Error capturing {os.path.basename(html_path)}: {e}")

def main():
    # images 디렉토리의 모든 rwsl HTML 파일 찾기
    images_dir = "/Users/dykim/dev/make-docs/images"
    html_files = glob.glob(os.path.join(images_dir, "rwsl_*.html"))
    
    print(f"Found {len(html_files)} RWSL HTML files to optimize")
    print("=" * 50)
    
    for html_file in sorted(html_files):
        print(f"Processing: {os.path.basename(html_file)}")
        
        # HTML 파일 최적화
        optimize_html_file(html_file)
        
        # PNG 캡처
        capture_html_to_png(html_file)
        
        print()
    
    print("=" * 50)
    print(f"✓ Optimization and capture completed for {len(html_files)} files!")
    
    # 캡처된 파일들 확인
    png_files = glob.glob(os.path.join(images_dir, "rwsl_*.png"))
    print(f"✓ Created {len(png_files)} PNG files:")
    for png_file in sorted(png_files):
        size = os.path.getsize(png_file)
        print(f"  - {os.path.basename(png_file)} ({size:,} bytes)")

if __name__ == "__main__":
    main()