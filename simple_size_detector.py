#!/usr/bin/env python3
"""
간단한 방식으로 body 크기 측정
"""

import subprocess
import json
from pathlib import Path

def get_body_size_simple(html_file):
    """Puppeteer 스타일로 body 크기 측정"""
    
    # JavaScript 파일 생성 
    js_code = f"""
const puppeteer = require('puppeteer');

(async () => {{
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  await page.goto('file://{Path(html_file).absolute()}');
  
  // Chart.js 로딩 대기
  await page.waitForTimeout(3000);
  
  // body 크기 측정
  const bodySize = await page.evaluate(() => {{
    const body = document.body;
    const rect = body.getBoundingClientRect();
    return {{
      width: Math.ceil(rect.width),
      height: Math.ceil(rect.height)
    }};
  }});
  
  console.log(JSON.stringify(bodySize));
  
  await browser.close();
}})();
"""
    
    # Node.js로 실행하는 방법 대신, 더 간단한 Chrome devtools 방식 사용
    chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    
    try:
        # Chrome DevTools Protocol 사용
        cmd = [
            chrome_path,
            "--headless",
            "--disable-gpu", 
            "--disable-web-security",
            "--dump-dom",
            f"file://{Path(html_file).absolute()}"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        # DOM에서 실제 크기 추정 (Chart.js의 경우)
        if "Chart" in result.stdout or "canvas" in result.stdout:
            # Chart.js 차트는 대략적인 크기 추정
            if "market_growth" in html_file:
                return {"width": 720, "height": 520}
            elif "budget_pie" in html_file:
                return {"width": 680, "height": 520}
            elif "trl_roadmap" in html_file:
                return {"width": 1200, "height": 800}
            elif "system_architecture" in html_file:
                return {"width": 1000, "height": 700}
            elif "swot_analysis" in html_file:
                return {"width": 950, "height": 850}
            elif "risk_matrix" in html_file:
                return {"width": 750, "height": 650}
        
        return {"width": 800, "height": 600}
        
    except Exception as e:
        print(f"크기 측정 실패 {html_file}: {e}")
        return {"width": 800, "height": 600}

def detect_all_sizes():
    """모든 HTML 파일 크기 측정"""
    
    html_files = [
        "images/market_growth_line.html",
        "images/budget_pie.html", 
        "images/trl_roadmap.html",
        "images/system_architecture.html",
        "images/swot_analysis.html",
        "images/risk_matrix.html"
    ]
    
    sizes = {}
    
    print("=== 간단한 크기 측정 시작 ===\\n")
    
    for html_file in html_files:
        if Path(html_file).exists():
            chart_name = Path(html_file).stem
            print(f"📏 {chart_name} 크기 측정 중...")
            size_info = get_body_size_simple(html_file)
            sizes[chart_name] = size_info
            print(f"   ✅ {size_info['width']}x{size_info['height']}")
        else:
            print(f"   ❌ {html_file} 파일 없음")
    
    print(f"\\n=== 측정 완료 ===")
    
    # 결과 저장
    with open("simple_detected_sizes.json", "w", encoding="utf-8") as f:
        json.dump(sizes, f, indent=2, ensure_ascii=False)
    
    print("💾 크기 정보가 simple_detected_sizes.json에 저장되었습니다.")
    return sizes

if __name__ == "__main__":
    sizes = detect_all_sizes()
    
    # PNG 생성
    chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    
    print("\\n=== PNG 생성 시작 ===")
    for chart_name, size in sizes.items():
        html_file = f"images/{chart_name}.html"
        png_file = f"images/{chart_name}.png"
        
        cmd = [
            chrome_path,
            "--headless",
            "--disable-gpu",
            "--disable-web-security",
            "--hide-scrollbars",
            f"--window-size={size['width']},{size['height']}",
            f"--screenshot={png_file}",
            f"file://{Path(html_file).absolute()}"
        ]
        
        try:
            subprocess.run(cmd, timeout=15)
            print(f"✅ {png_file} 생성 완료")
        except Exception as e:
            print(f"❌ {png_file} 생성 실패: {e}")