#!/usr/bin/env python3
"""
HTML 콘텐츠의 실제 크기를 감지하여 PNG 생성
"""

import os
import subprocess
import time

def generate_smart_pngs():
    """HTML 파일들을 브라우저로 열고 콘텐츠에 맞는 크기로 PNG 생성"""
    
    # 표준 고정 크기 (모든 차트를 1200x800 캔버스에 중앙정렬)
    standard_size = (1200, 800)  # 모든 차트 통일 크기
    
    chart_names = [
        "system_architecture", "market_growth_line", "market_growth_regional", 
        "trl_roadmap", "organization_chart", "budget_pie", "budget_trend",
        "budget_distribution", "swot_analysis", "risk_matrix", 
        "market_growth_trends", "gantt_schedule"
    ]
    
    width, height = standard_size
    
    for chart_name in chart_names:
        html_file = f"images/{chart_name}.html"
        png_file = f"images/{chart_name}.png"
        
        if os.path.exists(html_file):
            try:
                # 고정 크기로 정확히 캡처 (여백 없음)
                cmd = [
                    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                    "--headless",
                    "--disable-gpu",
                    "--disable-web-security",
                    "--hide-scrollbars",
                    "--force-device-scale-factor=1",
                    f"--window-size={width},{height}",
                    f"--screenshot={png_file}",
                    os.path.abspath(html_file)
                ]
                
                subprocess.run(cmd, check=True, capture_output=True)
                print(f"✅ {chart_name}.png 생성 완료 ({width}x{height} 표준 크기)")
                
            except subprocess.CalledProcessError as e:
                print(f"❌ {chart_name} 변환 실패: {e}")
        else:
            print(f"⚠️ {html_file} 파일이 존재하지 않습니다")
    
    print(f"\n🎯 스마트 크기 조정 완료!")

if __name__ == "__main__":
    print("🧠 콘텐츠 기반 스마트 PNG 생성...")
    generate_smart_pngs()