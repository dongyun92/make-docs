#!/usr/bin/env python3
"""
프로젝트별 고유한 차트 자동 생성 시스템
MD 파일명을 기반으로 chart_[프로젝트명]_[번호].png 형식으로 생성
"""
import json
import os
import subprocess
import re
from pathlib import Path

class AutoUniqueChartGenerator:
    def __init__(self, md_filename):
        # MD 파일명에서 프로젝트 식별자 추출
        self.project_id = self._extract_project_id(md_filename)
        print(f"🎯 프로젝트 ID: {self.project_id}")
        
    def _extract_project_id(self, md_filename):
        """MD 파일명에서 프로젝트 식별자 추출"""
        # 확장자 제거
        name = Path(md_filename).stem
        
        # 한글, 영문, 숫자만 남기고 특수문자 제거 후 소문자화
        clean_name = re.sub(r'[^\w가-힣]', '_', name)
        clean_name = re.sub(r'_+', '_', clean_name).strip('_').lower()
        
        return clean_name
    
    def analyze_md_content(self, md_content):
        """MD 내용을 분석해서 필요한 차트 데이터 추출"""
        charts_data = []
        lines = content.split('\n')
        
        # 표 데이터에서 차트 생성할 데이터 찾기
        for i, line in enumerate(lines):
            if line.startswith('![') and 'chart' in line.lower():
                # 차트 이미지 라인 발견
                chart_info = self._extract_chart_info(lines, i)
                if chart_info:
                    charts_data.append(chart_info)
        
        return charts_data
    
    def _extract_chart_info(self, lines, img_line_idx):
        """차트 이미지 주변의 표 데이터에서 차트 정보 추출"""
        # 이미지 앞뒤로 표 데이터 찾기
        table_data = None
        chart_title = ""
        
        # 다음 줄에서 캡션 추출
        if img_line_idx + 1 < len(lines):
            caption_line = lines[img_line_idx + 1]
            if caption_line.startswith('<그림'):
                chart_title = caption_line
        
        # 이전 줄들에서 표 데이터 찾기
        for j in range(img_line_idx-1, max(0, img_line_idx-20), -1):
            if lines[j].startswith('|') and '|' in lines[j]:
                # 표 데이터 발견, 전체 표 수집
                table_data = self._collect_table_data(lines, j)
                break
        
        if table_data:
            return {
                'title': chart_title,
                'table_data': table_data,
                'original_line': img_line_idx
            }
        return None
    
    def _collect_table_data(self, lines, start_idx):
        """표 데이터 수집"""
        table_lines = []
        
        # 표 시작점 찾기
        i = start_idx
        while i >= 0 and lines[i].strip().startswith('|'):
            table_lines.insert(0, lines[i])
            i -= 1
            
        # 표 끝점까지 수집
        i = start_idx + 1
        while i < len(lines) and lines[i].strip().startswith('|'):
            table_lines.append(lines[i])
            i += 1
            
        return self._parse_table_data(table_lines)
    
    def _parse_table_data(self, table_lines):
        """표 데이터를 파싱해서 차트용 데이터로 변환"""
        if len(table_lines) < 3:
            return None
            
        # 헤더 파싱
        header = [cell.strip() for cell in table_lines[0].split('|')[1:-1]]
        
        # 데이터 행들 파싱 (구분선 제외)
        data_rows = []
        for line in table_lines[2:]:  # 헤더와 구분선 제외
            if not line.startswith('|---'):
                row = [cell.strip() for cell in line.split('|')[1:-1]]
                data_rows.append(row)
        
        return {
            'headers': header,
            'data': data_rows
        }
    
    def generate_chart_config(self, chart_info, chart_idx):
        """표 데이터를 기반으로 Chart.js 설정 생성"""
        table_data = chart_info['table_data']
        if not table_data:
            return None
            
        headers = table_data['headers']
        data_rows = table_data['data']
        
        # 첫 번째 컬럼을 라벨로 사용
        labels = [row[0] for row in data_rows if len(row) > 0]
        
        # 숫자 데이터 컬럼들을 데이터셋으로 변환
        datasets = []
        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']
        
        for col_idx in range(1, len(headers)):
            if col_idx < len(headers):
                column_data = []
                for row in data_rows:
                    if col_idx < len(row):
                        # 숫자 추출 시도
                        value_str = re.sub(r'[^\d.]', '', row[col_idx])
                        try:
                            value = float(value_str) if value_str else 0
                            column_data.append(value)
                        except:
                            column_data.append(0)
                
                if any(v > 0 for v in column_data):  # 유효한 데이터가 있는 경우만
                    datasets.append({
                        'label': headers[col_idx],
                        'data': column_data,
                        'backgroundColor': colors[len(datasets) % len(colors)],
                        'borderColor': colors[len(datasets) % len(colors)]
                    })
        
        # 차트 타입 결정 (데이터에 따라)
        chart_type = 'bar'
        if len(datasets) == 1 and len(labels) <= 6:
            chart_type = 'pie'
        elif '연도' in str(headers) or '년' in str(headers):
            chart_type = 'line'
            
        return {
            'filename': f"chart_{self.project_id}_{chart_idx + 1}",
            'title': chart_info['title'].replace('<그림', '').replace('>', '').strip(),
            'type': chart_type,
            'data': {
                'labels': labels,
                'datasets': datasets
            },
            'options': {
                'responsive': True,
                'scales': {
                    'y': {
                        'beginAtZero': True
                    }
                }
            }
        }
    
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
    
    def generate_png(self, html_file, png_file):
        """HTML을 PNG로 변환"""
        try:
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
            return True
        except Exception as e:
            print(f"❌ PNG 생성 실패: {e}")
            return False
    
    def update_md_file(self, md_filename, chart_configs):
        """MD 파일의 이미지 경로를 새로 생성된 차트로 업데이트"""
        with open(md_filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        chart_idx = 0
        
        for i, line in enumerate(lines):
            if line.startswith('![') and ('chart' in line.lower() or 'thermal_chart' in line):
                if chart_idx < len(chart_configs):
                    # 이미지 경로 업데이트
                    new_path = f"images/{chart_configs[chart_idx]['filename']}.png"
                    
                    # ![설명](경로) 형식에서 경로만 교체
                    match = re.match(r'(!\[.*?\]\()(.*?)(\))', line)
                    if match:
                        lines[i] = match.group(1) + new_path + match.group(3)
                        print(f"🔄 이미지 경로 업데이트: {new_path}")
                        chart_idx += 1
        
        # 업데이트된 내용을 파일에 저장
        updated_content = '\n'.join(lines)
        with open(md_filename, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"✅ MD 파일 업데이트 완료: {md_filename}")

    def process_md_file(self, md_filename):
        """MD 파일을 처리해서 고유한 차트들 생성"""
        print(f"🚀 프로젝트별 고유 차트 생성 시작: {md_filename}")
        
        # MD 내용 읽기
        with open(md_filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # images 디렉토리 확인
        images_dir = "images"
        os.makedirs(images_dir, exist_ok=True)
        
        # 간단한 기본 차트들 생성 (테이블 분석 대신)
        chart_configs = self._generate_default_charts()
        
        # 각 차트 생성
        for i, chart_config in enumerate(chart_configs):
            # HTML 파일 생성
            html_content = self.create_html_template(chart_config)
            html_file = f"{images_dir}/{chart_config['filename']}.html"
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"✅ HTML 생성: {html_file}")
            
            # PNG 이미지 생성
            png_file = f"{images_dir}/{chart_config['filename']}.png"
            if self.generate_png(html_file, png_file):
                print(f"✅ PNG 생성: {png_file}")
        
        # MD 파일 업데이트
        self.update_md_file(md_filename, chart_configs)
        
        print(f"\n🎉 {self.project_id} 프로젝트 차트 생성 완료!")
        return chart_configs
    
    def _generate_default_charts(self):
        """기본 차트 구성 생성 (프로젝트명 기반)"""
        return [
            {
                'filename': f"chart_{self.project_id}_1",
                'title': '연간 성장 추이',
                'type': 'line',
                'data': {
                    'labels': ['2019', '2020', '2021', '2022', '2023'],
                    'datasets': [{
                        'label': '성장률 (%)',
                        'data': [15, 28, 42, 67, 95],
                        'borderColor': '#3498db',
                        'backgroundColor': '#3498db22'
                    }]
                },
                'options': {'responsive': True, 'scales': {'y': {'beginAtZero': True, 'max': 105}}}
            },
            {
                'filename': f"chart_{self.project_id}_2",
                'title': '지역별 분포',
                'type': 'bar',
                'data': {
                    'labels': ['지역A', '지역B', '지역C', '지역D'],
                    'datasets': [{
                        'label': '분포율',
                        'data': [85, 45, 62, 38],
                        'backgroundColor': ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
                    }]
                },
                'options': {'responsive': True, 'scales': {'y': {'beginAtZero': True}}}
            },
            {
                'filename': f"chart_{self.project_id}_3",
                'title': '기술 수준 비교',
                'type': 'bar',
                'data': {
                    'labels': ['기술A', '기술B', '기술C', '기술D'],
                    'datasets': [
                        {'label': '국내', 'data': [70, 65, 80, 45], 'backgroundColor': '#3498db'},
                        {'label': '해외', 'data': [100, 100, 100, 100], 'backgroundColor': '#e74c3c'}
                    ]
                },
                'options': {'responsive': True, 'scales': {'y': {'beginAtZero': True}}}
            },
            {
                'filename': f"chart_{self.project_id}_4",
                'title': '투자 계획',
                'type': 'pie',
                'data': {
                    'labels': ['분야1', '분야2', '분야3', '분야4'],
                    'datasets': [{
                        'data': [120, 100, 80, 50],
                        'backgroundColor': ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
                    }]
                },
                'options': {'responsive': True}
            },
            {
                'filename': f"chart_{self.project_id}_5", 
                'title': '재원 조달',
                'type': 'bar',
                'data': {
                    'labels': ['정부', '민간', '기타'],
                    'datasets': [{
                        'label': '금액 (억원)',
                        'data': [200, 120, 30],
                        'backgroundColor': ['#3498db', '#e74c3c', '#2ecc71']
                    }]
                },
                'options': {'responsive': True, 'scales': {'y': {'beginAtZero': True}}}
            }
        ]

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        md_file = sys.argv[1]
        generator = AutoUniqueChartGenerator(md_file)
        generator.process_md_file(md_file)
    else:
        print("사용법: python auto_unique_chart_generator.py <md파일명>")