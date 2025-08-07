#!/usr/bin/env python3
"""
풀스크린 캡처 시스템 - 최대 크기로 열어서 확실한 캡처
"""

import subprocess
from pathlib import Path

def fullscreen_capture_all():
    """최대 크기 Chrome으로 캡처"""
    
    html_files = [
        "images/market_growth_line.html",
        "images/budget_pie.html", 
        "images/trl_roadmap.html",
        "images/system_architecture.html",
        "images/swot_analysis.html",
        "images/risk_matrix.html"
    ]
    
    # 맥북 최대 해상도 (일반적인 맥북 프로 기준)
    MAX_WIDTH = 1920
    MAX_HEIGHT = 1200
    
    print(f"🖥️  풀스크린 캡처 시스템 - {MAX_WIDTH}x{MAX_HEIGHT}")
    print("=" * 50)
    
    for html_file in html_files:
        if not Path(html_file).exists():
            continue
            
        filename = Path(html_file).name
        output_file = html_file.replace('.html', '.png')
        
        print(f"📸 {filename} 풀스크린 캡처 중...")
        
        try:
            subprocess.run([
                '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
                '--headless',
                '--disable-gpu',
                '--disable-web-security',
                '--hide-scrollbars',
                '--force-device-scale-factor=1',
                '--disable-extensions',
                '--run-all-compositor-stages-before-draw',
                '--disable-background-timer-throttling',
                '--disable-renderer-backgrounding',
                '--start-maximized',  # 최대화로 시작
                f'--window-size={MAX_WIDTH},{MAX_HEIGHT}',  # 최대 크기 지정
                '--virtual-time-budget=4000',
                f'--screenshot={output_file}',
                f'file://{Path(html_file).absolute()}'
            ], check=True, timeout=12)
            
            if Path(output_file).exists():
                file_size = Path(output_file).stat().st_size
                print(f"   ✅ 완료: {file_size:,} bytes")
            else:
                print(f"   ❌ 파일 생성 실패")
                
        except Exception as e:
            print(f"   ❌ 캡처 실패: {e}")
    
    print("\n🎉 풀스크린 캡처 완료!")
    print("이제 모든 콘텐츠가 여유있게 담겨있을 것입니다.")

if __name__ == "__main__":
    fullscreen_capture_all()