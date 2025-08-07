#!/usr/bin/env python3
"""
공격드론 방어시스템 전용 차트 생성기
"""
import json
import os
import subprocess

class AttackDroneChartGenerator:
    def __init__(self):
        self.chart_configs = [
            {
                "filename": "attack_drone_chart_1",
                "title": "연도별 공격드론 위협 증가 추이",
                "type": "line",
                "data": {
                    "labels": ["2019", "2020", "2021", "2022", "2023"],
                    "datasets": [{
                        "label": "공격 사건 (건)",
                        "data": [15, 28, 42, 67, 95],
                        "borderColor": "#e74c3c",
                        "backgroundColor": "#e74c3c22",
                        "tension": 0.1
                    }]
                },
                "options": {
                    "responsive": True,
                    "scales": {
                        "y": {
                            "beginAtZero": True,
                            "max": 105
                        }
                    }
                }
            },
            {
                "filename": "attack_drone_chart_2", 
                "title": "지역별 드론 공격 발생 현황",
                "type": "bar",
                "data": {
                    "labels": ["중동", "유럽", "아시아", "아프리카", "기타"],
                    "datasets": [{
                        "label": "공격 사건 수",
                        "data": [85, 45, 62, 38, 27],
                        "backgroundColor": [
                            "#3498db", "#e74c3c", "#2ecc71", "#f39c12", "#9b59b6"
                        ]
                    }]
                },
                "options": {
                    "responsive": True,
                    "scales": {
                        "y": {
                            "beginAtZero": True,
                            "max": 95
                        }
                    }
                }
            },
            {
                "filename": "attack_drone_chart_3",
                "title": "기술 분야별 국내외 수준 격차",
                "type": "bar",
                "data": {
                    "labels": ["레이더 탐지", "전자광학", "음향 탐지", "RF 탐지", "AI 융합"],
                    "datasets": [
                        {
                            "label": "국내 수준 (%)",
                            "data": [70, 65, 60, 80, 45],
                            "backgroundColor": "#3498db"
                        },
                        {
                            "label": "해외 선진국 (%)", 
                            "data": [100, 100, 100, 100, 100],
                            "backgroundColor": "#e74c3c"
                        }
                    ]
                },
                "options": {
                    "responsive": True,
                    "scales": {
                        "y": {
                            "beginAtZero": True,
                            "max": 105
                        }
                    }
                }
            },
            {
                "filename": "attack_drone_chart_4",
                "title": "분야별 투자 계획",
                "type": "pie",
                "data": {
                    "labels": ["센서 개발", "무력화 장비", "AI/SW 개발", "통합 시스템", "시험 평가"],
                    "datasets": [{
                        "data": [120, 100, 80, 30, 20],
                        "backgroundColor": [
                            "#3498db", "#e74c3c", "#2ecc71", "#f39c12", "#9b59b6"
                        ]
                    }]
                },
                "options": {
                    "responsive": True,
                    "plugins": {
                        "legend": {
                            "position": "bottom"
                        }
                    }
                }
            },
            {
                "filename": "attack_drone_chart_5",
                "title": "투자 재원 조달 계획",
                "type": "bar",
                "data": {
                    "labels": ["정부 지원", "기업 투자", "기타"],
                    "datasets": [{
                        "label": "금액 (억원)",
                        "data": [200, 120, 30],
                        "backgroundColor": ["#3498db", "#e74c3c", "#2ecc71"]
                    }]
                },
                "options": {
                    "responsive": True,
                    "scales": {
                        "y": {
                            "beginAtZero": True,
                            "max": 220
                        }
                    }
                }
            }
        ]
        
    def create_html_template(self, chart_config):
        """Chart.js HTML 템플릿 생성"""
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{chart_config['title']}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            font-family: 'Arial', sans-serif;
            background-color: white;
        }}
        .chart-container {{
            position: relative;
            width: 100%;
            height: 400px;
        }}
    </style>
</head>
<body>
    <div class="chart-container">
        <canvas id="myChart"></canvas>
    </div>
    
    <script>
        const ctx = document.getElementById('myChart').getContext('2d');
        const myChart = new Chart(ctx, {{
            type: '{chart_config['type']}',
            data: {json.dumps(chart_config['data'], ensure_ascii=False)},
            options: {json.dumps(chart_config['options'], ensure_ascii=False)}
        }});
    </script>
</body>
</html>"""

    def generate_all_charts(self):
        """모든 차트 생성"""
        print("🚁 공격드론 방어시스템 차트 생성 시작...")
        
        # images 디렉토리 확인
        images_dir = "images"
        os.makedirs(images_dir, exist_ok=True)
        
        for chart_config in self.chart_configs:
            # HTML 파일 생성
            html_content = self.create_html_template(chart_config)
            html_file = f"{images_dir}/{chart_config['filename']}.html"
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
                
            print(f"✅ HTML 생성: {html_file}")
            
            # PNG 이미지 생성
            png_file = f"{images_dir}/{chart_config['filename']}.png"
            
            try:
                # Chrome으로 스크린샷 촬영
                chrome_cmd = [
                    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                    "--headless",
                    "--disable-gpu", 
                    "--hide-scrollbars",
                    "--force-device-scale-factor=1",
                    "--window-size=900,600",
                    f"--screenshot={png_file}",
                    html_file
                ]
                
                subprocess.run(chrome_cmd, check=True, capture_output=True)
                print(f"✅ PNG 생성: {png_file}")
                
            except subprocess.CalledProcessError as e:
                print(f"❌ PNG 생성 실패: {e}")
                
        print("\n🎉 공격드론 방어시스템 차트 생성 완료!")

if __name__ == "__main__":
    generator = AttackDroneChartGenerator()
    generator.generate_all_charts()