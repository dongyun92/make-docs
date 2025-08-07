#!/usr/bin/env python3
"""
차트 크기 조정 및 PNG 재생성 스크립트
"""

import os
import subprocess

def resize_charts():
    """HTML 차트들을 적절한 크기로 PNG 변환"""
    
    # 차트별 최적 크기 설정 (width, height)
    chart_sizes = {
        "system_architecture": (800, 600),
        "market_growth_line": (700, 500), 
        "market_growth_regional": (700, 500),
        "trl_roadmap": (800, 600),
        "organization_chart": (800, 600),
        "budget_pie": (700, 500),
        "budget_trend": (700, 500),
        "budget_distribution": (700, 500),
        "swot_analysis": (700, 500),
        "risk_matrix": (700, 500),
        "market_growth_trends": (700, 500)
    }
    
    # Chrome 헤드리스 모드로 PNG 생성
    for chart_name, (width, height) in chart_sizes.items():
        html_file = f"images/{chart_name}.html"
        png_file = f"images/{chart_name}.png"
        
        if os.path.exists(html_file):
            try:
                cmd = [
                    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                    "--headless",
                    "--disable-gpu", 
                    "--hide-scrollbars",
                    "--force-device-scale-factor=1",
                    f"--window-size={width},{height}",
                    f"--screenshot={png_file}",
                    html_file
                ]
                
                subprocess.run(cmd, check=True, capture_output=True)
                print(f"✅ {chart_name}.png 생성 완료 ({width}x{height})")
                
            except subprocess.CalledProcessError as e:
                print(f"❌ {chart_name} 변환 실패: {e}")
        else:
            print(f"⚠️ {html_file} 파일이 존재하지 않습니다")
    
    print(f"\n📊 차트 크기 조정 완료!")

if __name__ == "__main__":
    resize_charts()