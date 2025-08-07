#!/usr/bin/env python3
"""
안전 캡처 시스템 - 충분한 여유 높이로 확실한 잘림 방지
"""

import subprocess
from pathlib import Path

def safe_capture_all():
    """안전한 여유 크기로 캡처"""
    
    # 확실히 큰 크기로 설정 (높이 특히 여유있게)
    safe_sizes = {
        "images/market_growth_line.html": (900, 750),  # +100 높이
        "images/budget_pie.html": (800, 800),          # +50 높이
        "images/trl_roadmap.html": (1400, 800),        # +150 높이
        "images/system_architecture.html": (1100, 900), # +200 높이
        "images/swot_analysis.html": (850, 1000),       # +150 높이
        "images/risk_matrix.html": (700, 800)           # +150 높이
    }
    
    print("🛡️  안전 캡처 시스템 - 여유 높이로 확실한 보호")
    print("=" * 50)
    
    for html_file, (width, height) in safe_sizes.items():
        if not Path(html_file).exists():
            continue
            
        filename = Path(html_file).name
        output_file = html_file.replace('.html', '.png')
        
        print(f"📸 {filename} → {width}x{height}")
        
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
                f'--window-size={width},{height}',
                '--virtual-time-budget=5000',
                f'--screenshot={output_file}',
                f'file://{Path(html_file).absolute()}'
            ], check=True, timeout=15)
            
            if Path(output_file).exists():
                file_size = Path(output_file).stat().st_size
                print(f"   ✅ 완료: {file_size:,} bytes")
            else:
                print(f"   ❌ 파일 생성 실패")
                
        except Exception as e:
            print(f"   ❌ 캡처 실패: {e}")

if __name__ == "__main__":
    safe_capture_all()