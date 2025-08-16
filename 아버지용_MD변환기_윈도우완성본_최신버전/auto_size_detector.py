#!/usr/bin/env python3
"""
브라우저로 HTML을 로드하고 body의 실제 크기를 자동으로 측정하는 시스템
"""

import subprocess
import json
import os
from pathlib import Path

class AutoSizeDetector:
    def __init__(self):
        self.chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        self.html_files = [
            "market_growth_line.html",
            "budget_pie.html", 
            "trl_roadmap.html",
            "system_architecture.html",
            "swot_analysis.html",
            "risk_matrix.html"
        ]
    
    def get_body_size(self, html_file):
        """JavaScript로 body의 실제 렌더링된 크기를 측정"""
        
        # JavaScript 코드 - body의 실제 크기 측정
        js_code = """
        // Chart.js가 완전히 로드될 때까지 대기
        setTimeout(() => {
            const body = document.body;
            const rect = body.getBoundingClientRect();
            const style = window.getComputedStyle(body);
            
            // padding과 margin 포함한 실제 필요 크기
            const totalWidth = Math.ceil(rect.width + 
                                       parseFloat(style.marginLeft || 0) + 
                                       parseFloat(style.marginRight || 0));
            const totalHeight = Math.ceil(rect.height + 
                                        parseFloat(style.marginTop || 0) + 
                                        parseFloat(style.marginBottom || 0));
            
            console.log('BODY_SIZE:' + JSON.stringify({
                width: totalWidth,
                height: totalHeight,
                method: 'body_rect_measurement'
            }));
        }, 2000); // Chart.js 로딩 대기
        """
        
        # 임시 JavaScript 파일 생성
        js_file = f"temp_size_{Path(html_file).stem}.js"
        with open(js_file, 'w') as f:
            f.write(js_code)
        
        try:
            # Chrome으로 HTML 로드하고 JavaScript 실행
            cmd = [
                self.chrome_path,
                "--headless",
                "--disable-gpu",
                "--disable-web-security",
                "--run-all-compositor-stages-before-draw",
                "--virtual-time-budget=3000",  # 3초 대기
                f"--evaluate-script={js_file}",
                f"file://{Path(html_file).absolute()}"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            # 콘솔 출력에서 크기 정보 추출
            for line in result.stderr.split('\n'):
                if 'BODY_SIZE:' in line:
                    size_data = json.loads(line.split('BODY_SIZE:')[1])
                    return size_data
            
            # fallback: 기본 크기
            return {"width": 800, "height": 600, "method": "fallback"}
            
        except Exception as e:
            print(f"크기 측정 실패 {html_file}: {e}")
            return {"width": 800, "height": 600, "method": "error_fallback"}
        
        finally:
            # 임시 파일 정리
            if os.path.exists(js_file):
                os.remove(js_file)
    
    def detect_all_sizes(self):
        """모든 HTML 파일의 크기 자동 측정"""
        sizes = {}
        
        print("=== 자동 크기 측정 시작 ===\n")
        
        for html_file in self.html_files:
            html_path = Path("images") / html_file
            if html_path.exists():
                print(f"📏 {html_file} 크기 측정 중...")
                size_info = self.get_body_size(str(html_path))
                sizes[html_file.replace('.html', '')] = size_info
                print(f"   ✅ {size_info['width']}x{size_info['height']} ({size_info['method']})")
            else:
                print(f"   ❌ {html_file} 파일 없음")
                
        print(f"\n=== 측정 완료 ===")
        
        # 결과를 JSON 파일로 저장
        with open("auto_detected_sizes.json", "w", encoding="utf-8") as f:
            json.dump(sizes, f, indent=2, ensure_ascii=False)
        
        print("💾 크기 정보가 auto_detected_sizes.json에 저장되었습니다.")
        return sizes

if __name__ == "__main__":
    detector = AutoSizeDetector()
    detected_sizes = detector.detect_all_sizes()