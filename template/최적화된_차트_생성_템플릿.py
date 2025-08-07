#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
최적화된 HTML 차트 생성 템플릿
- 최소 여백으로 정확한 컨텐츠 크기 캡처
- HTML 컨테이너 실제 크기 기반 Chrome 캡처 사이즈 계산
- 모든 차트 유형에 대한 표준 최적화 설정 포함
"""

import os
from pathlib import Path
import subprocess

class OptimizedHTMLChartGenerator:
    def __init__(self, output_dir_path="/Users/dykim/dev/make-docs/images"):
        self.output_dir = Path(output_dir_path)
        self.output_dir.mkdir(exist_ok=True)
        
        # 최적화된 기본 CSS 설정 (모든 차트 공통)
        self.optimized_css_base = """
        body {
            font-family: 'Malgun Gothic', sans-serif;
            margin: 0;
            padding: 0;
            background: white;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: auto;
        }
        .container {
            background: white;
            border-radius: 15px;
            padding: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            width: 100%;
        }
        """
        
        # 차트별 최적 캡처 사이즈 매핑 (HTML 컨테이너 실제 크기 기반)
        self.chart_size_mapping = {
            "system_architecture": "1100,750",    # max-width 1000px + padding + 계층구조
            "market_growth": "1200,650",          # max-width 1200px + padding + 차트 2개
            "budget_distribution": "1200,650",    # max-width 1200px + padding + 차트 2개
            "swot_analysis": "1000,750",          # max-width 1000px + padding + 매트릭스 + 전략
            "trl_roadmap": "1200,900",            # max-width 1200px + padding + TRL 매트릭스
            "organization_chart": "1000,700",     # max-width 1000px + padding + 조직 계층
            "risk_matrix": "800,750",             # max-width 800px + padding + 매트릭스 + 범례
        }
        
        # 최적화된 Chrome 캡처 옵션
        self.chrome_options = [
            "--headless",
            "--disable-gpu", 
            "--disable-web-security",
            "--hide-scrollbars",                  # 스크롤바 제거
            "--force-device-scale-factor=1",      # 선명한 캡처
            "--virtual-time-budget=5000",
            "--run-all-compositor-stages-before-draw"
        ]

    def get_optimal_window_size(self, html_file_path):
        """HTML 파일명 기반으로 최적 캡처 사이즈 반환"""
        for chart_type, size in self.chart_size_mapping.items():
            if chart_type in html_file_path:
                return size
        return "1000,600"  # 기본값

    def create_html_template(self, title, content_html, max_width="1000px"):
        """최적화된 HTML 템플릿 생성"""
        return f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        {self.optimized_css_base}
        .container {{
            max-width: {max_width};
        }}
        .title {{
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 3px solid #3498db;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="title">{title}</div>
        {content_html}
    </div>
</body>
</html>
        """

    def capture_html_to_png(self, html_file_path, output_png_path):
        """최적화된 HTML to PNG 캡처"""
        try:
            chrome_paths = [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "/Applications/Chrome.app/Contents/MacOS/Chrome"
            ]
            
            chrome_path = None
            for path in chrome_paths:
                if os.path.exists(path):
                    chrome_path = path
                    break
            
            if not chrome_path:
                print("Chrome을 찾을 수 없어 PNG 변환을 건너뜁니다.")
                return False
            
            # HTML 파일명 기반 최적 사이즈 자동 설정
            window_size = self.get_optimal_window_size(html_file_path)
            
            cmd = [chrome_path] + self.chrome_options + [
                f"--window-size={window_size}",
                f"--screenshot={output_png_path}",
                f"file://{html_file_path}"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and os.path.exists(output_png_path):
                print(f"✓ 최적화된 캡처 완료: {window_size} -> {output_png_path}")
                return True
            else:
                print(f"Chrome 스크린샷 실패: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"HTML to PNG 변환 실패: {e}")
            return False

    def generate_chart(self, chart_name, generator_func):
        """단일 차트 생성 및 최적화된 캡처"""
        try:
            print(f"{chart_name} 최적화된 차트 생성 중...")
            html_file = generator_func()
            
            # PNG로 변환
            png_file = str(self.output_dir / f"{chart_name}.png")
            if self.capture_html_to_png(html_file, png_file):
                return (chart_name, html_file, png_file)
            else:
                print(f"✗ {chart_name} PNG 변환 실패")
                return (chart_name, html_file, None)
                
        except Exception as e:
            print(f"✗ {chart_name} 생성 실패: {e}")
            return (chart_name, None, None)

# 사용 예시:
if __name__ == "__main__":
    generator = OptimizedHTMLChartGenerator()
    
    # 예시 차트 생성 함수
    def create_sample_chart():
        content = '''
        <div style="text-align: center; padding: 20px;">
            <h2>샘플 차트</h2>
            <p>최적화된 설정이 적용된 차트입니다.</p>
        </div>
        '''
        html_content = generator.create_html_template("샘플 차트", content)
        html_file = generator.output_dir / "sample_chart.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        return str(html_file)
    
    result = generator.generate_chart("sample_chart", create_sample_chart)
    print(f"생성 결과: {result}")