#!/usr/bin/env python3
"""
모든 차트를 순수 HTML/CSS로 재생성하고 진짜 동적 크기 적용
Chart.js 의존성을 제거하고 완전한 정적 HTML 차트로 변환
"""

import os
from pathlib import Path

class ChartFixer:
    def __init__(self):
        self.output_dir = Path("images")
        self.output_dir.mkdir(exist_ok=True)
        
        # 실용적 크기 설정
        self.size_config = {
            "market_growth_line": {"width": 900, "height": 600},
            "market_growth_regional": {"width": 900, "height": 600}, 
            "budget_pie": {"width": 700, "height": 700},
            "budget_trend": {"width": 900, "height": 600},
            "trl_roadmap": {"width": 1400, "height": 650},
            "system_architecture": {"width": 1000, "height": 650},
            "swot_analysis": {"width": 800, "height": 900},
            "risk_matrix": {"width": 600, "height": 650}
        }
    
    def create_market_growth_line_chart(self):
        """순수 HTML/CSS 방산 수출 성장 추이 차트"""
        size = self.size_config["market_growth_line"]
        
        html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>한국 방산 수출 성장 추이</title>
    <style>
        body {{
            font-family: 'Malgun Gothic', sans-serif;
            margin: 0;
            padding: 0;
            background: white;
            width: {size['width']}px;
            height: {size['height']}px;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        
        .chart-container {{
            background: white;
            width: 100%;
            height: 100%;
            padding: 30px;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
        }}
        
        .chart-title {{
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 20px;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        
        .chart-area {{
            flex: 1;
            position: relative;
            display: flex;
            flex-direction: column;
        }}
        
        .y-axis {{
            position: absolute;
            left: -5px;
            top: 0;
            bottom: 60px;
            width: 50px;
            display: flex;
            flex-direction: column-reverse;
            justify-content: space-between;
            align-items: flex-end;
            font-size: 11px;
            color: #666;
        }}
        
        .chart-main {{
            margin-left: 60px;
            margin-bottom: 60px;
            flex: 1;
            position: relative;
            border-left: 2px solid #ddd;
            border-bottom: 2px solid #ddd;
        }}
        
        .grid-lines {{
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
        }}
        
        .grid-line {{
            position: absolute;
            left: 0;
            right: 0;
            height: 1px;
            background: rgba(0,0,0,0.05);
        }}
        
        .data-line {{
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
        }}
        
        .data-point {{
            position: absolute;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            border: 2px solid white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            transform: translate(-50%, -50%);
        }}
        
        .actual {{ background: #2c3e50; }}
        .target {{ background: #e74c3c; width: 10px; height: 10px; }}
        .optimistic {{ background: #27ae60; }}
        .baseline {{ background: #f39c12; }}
        .conservative {{ background: #95a5a6; }}
        
        .line-segment {{
            position: absolute;
            height: 2px;
            transform-origin: left center;
        }}
        
        .actual-line {{ background: #2c3e50; }}
        .optimistic-line {{ 
            background: #27ae60; 
            background-image: linear-gradient(90deg, #27ae60 50%, transparent 50%);
            background-size: 8px 2px;
        }}
        .baseline-line {{ background: #f39c12; }}
        .conservative-line {{ 
            background: #95a5a6;
            background-image: linear-gradient(90deg, #95a5a6 50%, transparent 50%);
            background-size: 6px 2px;
        }}
        
        .x-axis {{
            height: 50px;
            margin-left: 60px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 11px;
            color: #666;
            border-top: 1px solid #ddd;
            padding-top: 10px;
        }}
        
        .legend {{
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 15px;
            font-size: 12px;
        }}
        
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        
        .legend-color {{
            width: 12px;
            height: 12px;
            border-radius: 50%;
        }}
        
        .axis-label {{
            position: absolute;
            font-size: 12px;
            font-weight: bold;
            color: #333;
        }}
        
        .y-label {{
            left: 5px;
            top: 50%;
            transform: rotate(-90deg) translateY(-50%);
        }}
        
        .x-label {{
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
        }}
    </style>
</head>
<body>
    <div class="chart-container">
        <div class="chart-title">한국 방산 수출 성장 추이 (2019-2030)</div>
        
        <div class="chart-area">
            <!-- Y축 레이블 -->
            <div class="y-axis">
                <div>250</div>
                <div>200</div>
                <div>150</div>
                <div>100</div>
                <div>50</div>
                <div>0</div>
            </div>
            
            <!-- 차트 메인 영역 -->
            <div class="chart-main">
                <!-- 격자선 -->
                <div class="grid-lines">
                    <div class="grid-line" style="bottom: 80%;"></div>
                    <div class="grid-line" style="bottom: 60%;"></div>
                    <div class="grid-line" style="bottom: 40%;"></div>
                    <div class="grid-line" style="bottom: 20%;"></div>
                </div>
                
                <!-- 데이터 포인트 및 라인 -->
                <div class="data-line">
                    <!-- 2019년: 45억달러 (18%) -->
                    <div class="data-point actual" style="left: 5%; bottom: 18%;"></div>
                    <!-- 2021년: 93억달러 (37%) -->
                    <div class="data-point actual" style="left: 20%; bottom: 37%;"></div>
                    <!-- 2023년: 140억달러 (56%) -->
                    <div class="data-point actual" style="left: 35%; bottom: 56%;"></div>
                    
                    <!-- 실적 라인 -->
                    <div class="line-segment actual-line" style="left: 5%; bottom: 18%; width: 15%; transform: rotate(16deg);"></div>
                    <div class="line-segment actual-line" style="left: 20%; bottom: 37%; width: 15%; transform: rotate(12deg);"></div>
                    
                    <!-- 2024년 목표: 200억달러 (80%) -->
                    <div class="data-point target" style="left: 50%; bottom: 80%;"></div>
                    
                    <!-- 미래 시나리오들 -->
                    <!-- 2025년 -->
                    <div class="data-point optimistic" style="left: 65%; bottom: 72%;"></div> <!-- 180억 -->
                    <div class="data-point baseline" style="left: 65%; bottom: 68%;"></div> <!-- 170억 -->
                    <div class="data-point conservative" style="left: 65%; bottom: 64%;"></div> <!-- 160억 -->
                    
                    <!-- 2027년 -->
                    <div class="data-point optimistic" style="left: 80%; bottom: 88%;"></div> <!-- 220억 -->
                    <div class="data-point baseline" style="left: 80%; bottom: 80%;"></div> <!-- 200억 -->
                    <div class="data-point conservative" style="left: 80%; bottom: 72%;"></div> <!-- 180억 -->
                    
                    <!-- 2030년 -->
                    <div class="data-point optimistic" style="left: 95%; bottom: 100%;"></div> <!-- 250억 -->
                    <div class="data-point baseline" style="left: 95%; bottom: 88%;"></div> <!-- 220억 -->
                    <div class="data-point conservative" style="left: 95%; bottom: 72%;"></div> <!-- 180억 -->
                    
                    <!-- 미래 시나리오 라인들 -->
                    <div class="line-segment optimistic-line" style="left: 65%; bottom: 72%; width: 15%; transform: rotate(8deg);"></div>
                    <div class="line-segment optimistic-line" style="left: 80%; bottom: 88%; width: 15%; transform: rotate(6deg);"></div>
                    
                    <div class="line-segment baseline-line" style="left: 65%; bottom: 68%; width: 15%; transform: rotate(6deg);"></div>
                    <div class="line-segment baseline-line" style="left: 80%; bottom: 80%; width: 15%; transform: rotate(4deg);"></div>
                    
                    <div class="line-segment conservative-line" style="left: 65%; bottom: 64%; width: 15%; transform: rotate(4deg);"></div>
                    <div class="line-segment conservative-line" style="left: 80%; bottom: 72%; width: 15%; transform: rotate(0deg);"></div>
                </div>
                
                <!-- 축 레이블 -->
                <div class="axis-label y-label">수출액 (억 달러)</div>
                <div class="axis-label x-label">연도</div>
            </div>
            
            <!-- X축 -->
            <div class="x-axis">
                <span>2019</span>
                <span>2021</span>
                <span>2023</span>
                <span>2024 목표</span>
                <span>2025</span>
                <span>2027</span>
                <span>2030</span>
            </div>
        </div>
        
        <!-- 범례 -->
        <div class="legend">
            <div class="legend-item">
                <div class="legend-color actual"></div>
                <span>실적</span>
            </div>
            <div class="legend-item">
                <div class="legend-color target"></div>
                <span>2024 목표</span>
            </div>
            <div class="legend-item">
                <div class="legend-color optimistic"></div>
                <span>최적 시나리오</span>
            </div>
            <div class="legend-item">
                <div class="legend-color baseline"></div>
                <span>기준 시나리오</span>
            </div>
            <div class="legend-item">
                <div class="legend-color conservative"></div>
                <span>보수 시나리오</span>
            </div>
        </div>
    </div>
</body>
</html>"""
        
        with open(self.output_dir / "market_growth_line.html", 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("✅ market_growth_line.html 순수 HTML/CSS로 재생성")
    
    def create_budget_pie_chart(self):
        """순수 HTML/CSS 파이 차트"""
        size = self.size_config["budget_pie"]
        
        html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>총 투자 3,500억원 분야별 배분</title>
    <style>
        body {{
            font-family: 'Malgun Gothic', sans-serif;
            margin: 0;
            padding: 0;
            background: white;
            width: {size['width']}px;
            height: {size['height']}px;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        
        .chart-container {{
            background: white;
            width: 100%;
            height: 100%;
            padding: 30px;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        
        .chart-title {{
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 30px;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            width: 100%;
        }}
        
        .pie-container {{
            position: relative;
            width: 350px;
            height: 350px;
            border-radius: 50%;
            overflow: hidden;
            margin-bottom: 30px;
        }}
        
        .pie-slice {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border-radius: 50%;
            clip-path: polygon(50% 50%, 50% 0%, 100% 0%, 100% 100%, 50% 100%);
        }}
        
        /* 무인체계: 30% (1050억) */
        .slice-1 {{
            background: #2c3e50;
            transform: rotate(0deg);
            clip-path: polygon(50% 50%, 50% 0%, 100% 38.4%, 50% 50%);
        }}
        
        /* AI/빅데이터: 20% (700억) */  
        .slice-2 {{
            background: #34495e;
            transform: rotate(108deg);
            clip-path: polygon(50% 50%, 50% 0%, 93.3% 25%, 50% 50%);
        }}
        
        /* 통신기술: 25% (875억) */
        .slice-3 {{
            background: #3498db;
            transform: rotate(180deg);
            clip-path: polygon(50% 50%, 50% 0%, 100% 50%, 50% 50%);
        }}
        
        /* 센서/반도체: 15% (525억) */
        .slice-4 {{
            background: #e74c3c;
            transform: rotate(270deg);
            clip-path: polygon(50% 50%, 50% 0%, 75% 6.7%, 50% 50%);
        }}
        
        /* 기타 신기술: 10% (350억) */
        .slice-5 {{
            background: #f39c12;
            transform: rotate(324deg);
            clip-path: polygon(50% 50%, 50% 0%, 66.9% 17.1%, 50% 50%);
        }}
        
        .center-label {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            background: white;
            border-radius: 50%;
            width: 100px;
            height: 100px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            font-weight: bold;
            color: #2c3e50;
        }}
        
        .legend {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            width: 100%;
            max-width: 500px;
        }}
        
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 14px;
            padding: 8px;
            background: #f8f9fa;
            border-radius: 6px;
        }}
        
        .legend-color {{
            width: 20px;
            height: 20px;
            border-radius: 3px;
            flex-shrink: 0;
        }}
        
        .legend-text {{
            display: flex;
            flex-direction: column;
            gap: 2px;
        }}
        
        .legend-name {{
            font-weight: bold;
            color: #2c3e50;
        }}
        
        .legend-value {{
            font-size: 12px;
            color: #7f8c8d;
        }}
        
        /* 실제 파이 슬라이스들 (SVG 방식) */
        .svg-pie {{
            width: 350px;
            height: 350px;
        }}
    </style>
</head>
<body>
    <div class="chart-container">
        <div class="chart-title">총 투자 3,500억원 분야별 배분</div>
        
        <div class="pie-container">
            <svg class="svg-pie" viewBox="0 0 200 200">
                <!-- 무인체계: 30% -->
                <path d="M 100,100 L 100,0 A 100,100 0 0,1 190,62 Z" fill="#2c3e50"/>
                <!-- AI/빅데이터: 20% -->
                <path d="M 100,100 L 190,62 A 100,100 0 0,1 162,190 Z" fill="#34495e"/>
                <!-- 통신기술: 25% -->
                <path d="M 100,100 L 162,190 A 100,100 0 0,1 38,190 Z" fill="#3498db"/>
                <!-- 센서/반도체: 15% -->
                <path d="M 100,100 L 38,190 A 100,100 0 0,1 10,62 Z" fill="#e74c3c"/>
                <!-- 기타 신기술: 10% -->
                <path d="M 100,100 L 10,62 A 100,100 0 0,1 100,0 Z" fill="#f39c12"/>
            </svg>
            
            <div class="center-label">
                <div style="font-size: 16px;">총 투자</div>
                <div style="font-size: 20px;">3,500억</div>
            </div>
        </div>
        
        <div class="legend">
            <div class="legend-item">
                <div class="legend-color" style="background: #2c3e50;"></div>
                <div class="legend-text">
                    <div class="legend-name">무인체계</div>
                    <div class="legend-value">1,050억원 (30%)</div>
                </div>
            </div>
            
            <div class="legend-item">
                <div class="legend-color" style="background: #34495e;"></div>
                <div class="legend-text">
                    <div class="legend-name">AI/빅데이터</div>
                    <div class="legend-value">700억원 (20%)</div>
                </div>
            </div>
            
            <div class="legend-item">
                <div class="legend-color" style="background: #3498db;"></div>
                <div class="legend-text">
                    <div class="legend-name">통신기술</div>
                    <div class="legend-value">875억원 (25%)</div>
                </div>
            </div>
            
            <div class="legend-item">
                <div class="legend-color" style="background: #e74c3c;"></div>
                <div class="legend-text">
                    <div class="legend-name">센서/반도체</div>
                    <div class="legend-value">525억원 (15%)</div>
                </div>
            </div>
            
            <div class="legend-item" style="grid-column: span 2; justify-self: center;">
                <div class="legend-color" style="background: #f39c12;"></div>
                <div class="legend-text">
                    <div class="legend-name">기타 신기술</div>
                    <div class="legend-value">350억원 (10%)</div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""
        
        with open(self.output_dir / "budget_pie.html", 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("✅ budget_pie.html 순수 HTML/CSS로 재생성")
    
    def fix_existing_charts_sizes(self):
        """기존 HTML 차트들의 크기 수정"""
        
        charts_to_fix = [
            ("trl_roadmap.html", self.size_config["trl_roadmap"]),
            ("system_architecture.html", self.size_config["system_architecture"]),
            ("swot_analysis.html", self.size_config["swot_analysis"]),
            ("risk_matrix.html", self.size_config["risk_matrix"])
        ]
        
        for chart_file, size in charts_to_fix:
            file_path = self.output_dir / chart_file
            
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # body 태그의 width, height 수정
                import re
                content = re.sub(
                    r'width:\s*1200px;',
                    f"width: {size['width']}px;",
                    content
                )
                content = re.sub(
                    r'height:\s*800px;',
                    f"height: {size['height']}px;",
                    content
                )
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"✅ {chart_file} 크기 수정: {size['width']}x{size['height']}")
            else:
                print(f"❌ {chart_file} 파일이 없습니다.")
    
    def generate_all_charts(self):
        """모든 차트 생성/수정"""
        print("=== 모든 차트 수정/재생성 시작 ===\n")
        
        # Chart.js 기반 차트들을 순수 HTML/CSS로 재생성
        self.create_market_growth_line_chart()
        self.create_budget_pie_chart()
        
        # 기존 순수 HTML 차트들의 크기 수정
        self.fix_existing_charts_sizes()
        
        print(f"\n=== 모든 차트 수정 완료 ===")
        print("📊 이제 모든 차트가 순수 HTML/CSS 기반이며 적절한 크기로 설정되었습니다.")
        
        # 크기 설정을 JSON으로 저장
        import json
        with open("fixed_chart_sizes.json", "w", encoding="utf-8") as f:
            json.dump(self.size_config, f, indent=2, ensure_ascii=False)
        
        print("💾 크기 설정이 fixed_chart_sizes.json에 저장되었습니다.")

if __name__ == "__main__":
    fixer = ChartFixer()
    fixer.generate_all_charts()