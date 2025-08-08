#!/usr/bin/env python3
import os
import re
import subprocess
import glob

def fix_title_fonts(file_path):
    """제목 폰트 크기를 16px로 수정합니다."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 제목 폰트 크기를 16px로 수정
    content = re.sub(r'\.chart-title\s*{[^}]*font-size:\s*11px[^}]*}', 
                     lambda m: m.group(0).replace('font-size: 11px', 'font-size: 16px'), 
                     content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Fixed title font: {os.path.basename(file_path)}")

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
            print(f"✓ Re-captured: {os.path.basename(png_path)}")
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
    
    print(f"Fixing title fonts for {len(html_files)} RWSL HTML files")
    print("=" * 50)
    
    for html_file in sorted(html_files):
        # HTML 파일의 제목 폰트 수정
        fix_title_fonts(html_file)
        
        # PNG 재캡처
        capture_html_to_png(html_file)
    
    print("=" * 50)
    print(f"✓ Title font fix and re-capture completed for {len(html_files)} files!")

if __name__ == "__main__":
    main()