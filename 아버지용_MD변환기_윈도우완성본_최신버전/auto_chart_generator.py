#!/usr/bin/env python3
"""
마크다운 내용을 분석해서 자동으로 차트를 생성하는 시스템
"""
import re
import os
import json
from typing import Dict, List, Tuple, Any

class AutoChartGenerator:
    """마크다운 분석 기반 자동 차트 생성기"""
    
    def __init__(self):
        self.chart_counter = 0
        self.generated_charts = []
        
    def analyze_and_generate_charts(self, md_content: str) -> List[Dict]:
        """마크다운 내용을 분석해서 필요한 차트들을 생성"""
        charts = []
        
        # 1. 표 데이터에서 차트 생성
        table_charts = self._extract_charts_from_tables(md_content)
        charts.extend(table_charts)
        
        # 2. ```chart 블록에서 차트 생성  
        chart_block_charts = self._extract_charts_from_blocks(md_content)
        charts.extend(chart_block_charts)
        
        # 3. 텍스트에서 수치 데이터 추출해서 차트 생성
        text_charts = self._extract_charts_from_text(md_content)
        charts.extend(text_charts)
        
        return charts
    
    def _extract_charts_from_tables(self, content: str) -> List[Dict]:
        """표 데이터에서 차트를 자동 생성"""
        charts = []
        
        # 마크다운 표 패턴 찾기 (단순화된 패턴)
        # 헤더 + 구분선 + 데이터 행들 패턴
        lines = content.split('\n')
        tables_found = []
        
        for i, line in enumerate(lines):
            if line.strip().startswith('|') and line.strip().endswith('|'):
                # 다음 줄이 구분선인지 확인
                if i + 1 < len(lines) and re.match(r'^\|[\s\-:]+\|', lines[i + 1]):
                    # 표 시작점 발견, 데이터 행들 수집
                    table_lines = [line, lines[i + 1]]  # 헤더 + 구분선
                    j = i + 2
                    while j < len(lines) and lines[j].strip().startswith('|') and lines[j].strip().endswith('|'):
                        table_lines.append(lines[j])
                        j += 1
                    
                    if len(table_lines) >= 3:  # 헤더 + 구분선 + 최소 1개 데이터
                        table_text = '\n'.join(table_lines)
                        tables_found.append((i, table_text))
        
        # 발견된 표들을 처리
        for line_num, full_table in tables_found:
            lines = [line.strip() for line in full_table.split('\n') if line.strip()]
            
            if len(lines) < 3:
                continue
                
            # 헤더와 데이터 분리
            header = [cell.strip() for cell in lines[0].split('|')[1:-1]]
            data_lines = lines[2:]  # 구분선 제외
            
            # 숫자 컬럼 찾기
            numeric_columns = self._find_numeric_columns(header, data_lines)
            
            if len(numeric_columns) >= 2:  # x축, y축 최소 2개 필요
                chart_data = self._parse_table_data(header, data_lines, numeric_columns)
                
                # 표 제목 또는 캡션 찾기
                title = self._find_table_title(content, line_num)
                
                chart = self._create_chart_from_table_data(chart_data, title)
                if chart:
                    charts.append(chart)
        
        return charts
    
    def _extract_charts_from_blocks(self, content: str) -> List[Dict]:
        """```chart 블록에서 차트 생성"""
        charts = []
        
        # chart 블록 패턴
        chart_pattern = r'```chart\s*\n(.*?)\n```'
        chart_blocks = re.finditer(chart_pattern, content, re.DOTALL)
        
        for block in chart_blocks:
            chart_config = block.group(1).strip()
            
            try:
                # JSON 형태로 파싱 시도
                config = json.loads(chart_config)
                chart = self._create_chart_from_config(config)
                if chart:
                    charts.append(chart)
            except json.JSONDecodeError:
                # YAML 형태 파싱 시도
                chart = self._parse_yaml_chart_config(chart_config)
                if chart:
                    charts.append(chart)
        
        return charts
    
    def _extract_charts_from_text(self, content: str) -> List[Dict]:
        """텍스트에서 수치 데이터를 찾아 차트 생성"""
        charts = []
        
        # 년도별 데이터 패턴 (예: 2021년 100억, 2022년 120억...)
        yearly_pattern = r'(\d{4})년?\s*([^\s,]+)?\s*(\d+(?:[.,]\d+)*)\s*(억|만|천)?'
        yearly_matches = re.findall(yearly_pattern, content)
        
        if len(yearly_matches) >= 3:  # 최소 3개 데이터 포인트
            chart = self._create_yearly_trend_chart(yearly_matches)
            if chart:
                charts.append(chart)
        
        # 비율 데이터 패턴 (예: A사 25%, B사 30%...)
        percentage_pattern = r'([가-힣A-Za-z\s]+)\s*(\d+(?:\.\d+)?)\s*%'
        percentage_matches = re.findall(percentage_pattern, content)
        
        if len(percentage_matches) >= 3:  # 최소 3개 항목
            chart = self._create_pie_chart(percentage_matches)
            if chart:
                charts.append(chart)
        
        return charts
    
    def _find_numeric_columns(self, headers: List[str], data_lines: List[str]) -> List[int]:
        """숫자 데이터를 포함한 컬럼 인덱스 찾기"""
        numeric_cols = []
        
        if not data_lines:
            return numeric_cols
            
        sample_row = [cell.strip() for cell in data_lines[0].split('|')[1:-1]]
        
        for i, cell in enumerate(sample_row):
            # 숫자 패턴 확인 (쉼표, 소수점, 단위 포함)
            if re.match(r'^\d+(?:[.,]\d+)*\s*[%원달러억만천]?$', cell.replace(',', '')):
                numeric_cols.append(i)
                
        return numeric_cols
    
    def _parse_table_data(self, headers: List[str], data_lines: List[str], numeric_columns: List[int]) -> Dict:
        """표 데이터를 차트 데이터 형태로 파싱"""
        data = {
            'categories': [],
            'series': {},
            'headers': headers
        }
        
        for line in data_lines:
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            if len(cells) < len(headers):
                continue
                
            # 첫 번째 컬럼을 카테고리로 사용
            category = cells[0]
            data['categories'].append(category)
            
            # 숫자 컬럼들을 시리즈로 추가
            for col_idx in numeric_columns:
                if col_idx < len(cells) and col_idx < len(headers):
                    series_name = headers[col_idx]
                    if series_name not in data['series']:
                        data['series'][series_name] = []
                    
                    # 숫자 추출
                    value_str = cells[col_idx].replace(',', '')
                    value = self._extract_numeric_value(value_str)
                    data['series'][series_name].append(value)
        
        return data
    
    def _extract_numeric_value(self, value_str: str) -> float:
        """문자열에서 숫자 값 추출"""
        # 단위 처리
        multipliers = {'천': 1000, '만': 10000, '억': 100000000, 'K': 1000, 'M': 1000000, 'B': 1000000000}
        
        # 퍼센트 처리
        if '%' in value_str:
            num_str = value_str.replace('%', '').strip()
            return float(num_str) if num_str else 0
            
        # 단위 확인
        multiplier = 1
        for unit, mult in multipliers.items():
            if unit in value_str:
                multiplier = mult
                value_str = value_str.replace(unit, '').strip()
                break
        
        # 숫자 추출
        num_match = re.search(r'(\d+(?:\.\d+)?)', value_str)
        if num_match:
            return float(num_match.group(1)) * multiplier
        return 0
    
    def _find_table_title(self, content: str, line_num: int) -> str:
        """표의 제목이나 캡션 찾기"""
        lines = content.split('\n')
        
        # 표 이전 몇 줄에서 제목 찾기
        for i in range(max(0, line_num - 3), line_num):
            if i < len(lines):
                line = lines[i].strip()
                if line and not line.startswith('|') and not line.startswith('#') and not line.startswith('□'):
                    return line
        
        # 표 이후 캡션 찾기 
        for i in range(line_num + 3, min(len(lines), line_num + 6)):
            if i < len(lines):
                line = lines[i].strip()
                if line.startswith('<표') or line.startswith('<그림'):
                    return line
                
        return "데이터 차트"
    
    def _create_chart_from_table_data(self, data: Dict, title: str) -> Dict:
        """표 데이터로부터 차트 생성"""
        self.chart_counter += 1
        chart_id = f"auto_chart_{self.chart_counter}"
        
        # 적절한 차트 타입 결정
        chart_type = self._determine_chart_type(data)
        
        chart_config = {
            'id': chart_id,
            'title': title,
            'type': chart_type,
            'data': data,
            'filename': f"images/{chart_id}.html"
        }
        
        # HTML 파일 생성
        html_content = self._generate_chart_html(chart_config)
        
        # 파일 저장
        os.makedirs('images', exist_ok=True)
        with open(chart_config['filename'], 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        return chart_config
    
    def _determine_chart_type(self, data: Dict) -> str:
        """데이터 특성에 따라 적절한 차트 타입 결정"""
        categories = data.get('categories', [])
        series_count = len(data.get('series', {}))
        
        # 년도 데이터인 경우 라인 차트
        if any(re.match(r'\d{4}', str(cat)) for cat in categories):
            return 'line'
        
        # 비율이나 퍼센트 데이터인 경우
        series_values = list(data.get('series', {}).values())
        if series_values and len(series_values[0]) > 0:
            # 모든 값이 100 이하이고 소수점이 있으면 퍼센트로 간주
            first_series = series_values[0]
            if all(isinstance(v, (int, float)) and 0 <= v <= 100 for v in first_series if v):
                return 'pie' if series_count == 1 else 'bar'
        
        # 시리즈가 여러 개면 bar, 하나면 pie
        return 'bar' if series_count > 1 else 'pie'
    
    def _generate_chart_html(self, config: Dict) -> str:
        """차트 설정에 따라 HTML 생성"""
        chart_type = config['type']
        data = config['data']
        title = config['title']
        
        if chart_type == 'line':
            return self._generate_line_chart_html(data, title)
        elif chart_type == 'pie':
            return self._generate_pie_chart_html(data, title)
        else:  # bar
            return self._generate_bar_chart_html(data, title)
    
    def _generate_line_chart_html(self, data: Dict, title: str) -> str:
        """라인 차트 HTML 생성"""
        categories = data['categories']
        series = data['series']
        
        datasets = []
        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']
        
        for i, (series_name, values) in enumerate(series.items()):
            color = colors[i % len(colors)]
            datasets.append({
                'label': series_name,
                'data': values,
                'borderColor': color,
                'backgroundColor': color + '20',
                'tension': 0.3
            })
        
        return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ margin: 0; padding: 20px; font-family: Arial, sans-serif; }}
        .container {{ width: 800px; height: 400px; }}
    </style>
</head>
<body>
    <div class="container">
        <canvas id="chart"></canvas>
    </div>
    <script>
        const ctx = document.getElementById('chart').getContext('2d');
        new Chart(ctx, {{
            type: 'line',
            data: {{
                labels: {json.dumps(categories, ensure_ascii=False)},
                datasets: {json.dumps(datasets, ensure_ascii=False)}
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ position: 'top' }}
                }},
                scales: {{
                    y: {{ 
                        beginAtZero: true,
                        max: {self._calculate_y_axis_max(datasets)}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>'''

    def _generate_pie_chart_html(self, data: Dict, title: str) -> str:
        """파이 차트 HTML 생성"""
        categories = data['categories']
        # 첫 번째 시리즈 사용
        series = list(data['series'].values())[0] if data['series'] else []
        
        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c', '#e67e22']
        
        return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ margin: 0; padding: 20px; font-family: Arial, sans-serif; }}
        .container {{ width: 500px; height: 500px; margin: 0 auto; }}
    </style>
</head>
<body>
    <div class="container">
        <canvas id="chart"></canvas>
    </div>
    <script>
        const ctx = document.getElementById('chart').getContext('2d');
        new Chart(ctx, {{
            type: 'pie',
            data: {{
                labels: {json.dumps(categories, ensure_ascii=False)},
                datasets: [{{
                    data: {json.dumps(series)},
                    backgroundColor: {json.dumps(colors[:len(categories)])}
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ position: 'right' }}
                }}
            }}
        }});
    </script>
</body>
</html>'''

    def _generate_bar_chart_html(self, data: Dict, title: str) -> str:
        """바 차트 HTML 생성"""
        categories = data['categories']
        series = data['series']
        
        datasets = []
        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']
        
        for i, (series_name, values) in enumerate(series.items()):
            color = colors[i % len(colors)]
            datasets.append({
                'label': series_name,
                'data': values,
                'backgroundColor': color,
                'borderColor': color,
                'borderWidth': 1
            })
        
        return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ margin: 0; padding: 20px; font-family: Arial, sans-serif; }}
        .container {{ width: 800px; height: 400px; }}
    </style>
</head>
<body>
    <div class="container">
        <canvas id="chart"></canvas>
    </div>
    <script>
        const ctx = document.getElementById('chart').getContext('2d');
        new Chart(ctx, {{
            type: 'bar',
            data: {{
                labels: {json.dumps(categories, ensure_ascii=False)},
                datasets: {json.dumps(datasets, ensure_ascii=False)}
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ position: 'top' }}
                }},
                scales: {{
                    y: {{ 
                        beginAtZero: true,
                        max: {self._calculate_y_axis_max(datasets)}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>'''

    def _create_yearly_trend_chart(self, matches: List[Tuple]) -> Dict:
        """년도별 추이 차트 생성"""
        # 구현 생략 (복잡도 관리)
        return None
        
    def _create_pie_chart(self, matches: List[Tuple]) -> Dict:
        """비율 데이터 파이 차트 생성"""
        # 구현 생략 (복잡도 관리) 
        return None
    
    def _calculate_y_axis_max(self, datasets: List[Dict]) -> int:
        """데이터셋을 기반으로 Y축 최대값 계산 - 개선된 로직"""
        max_value = 0
        min_value = float('inf')
        
        for dataset in datasets:
            if 'data' in dataset:
                for value in dataset['data']:
                    if isinstance(value, (int, float)):
                        max_value = max(max_value, float(value))
                        min_value = min(min_value, float(value))
        
        # 최대값이 0이면 기본값 사용
        if max_value == 0:
            return 100
            
        # 연도 데이터인지 확인 (2000 이상 값들)
        if max_value >= 2000 and min_value >= 2000:
            # 연도 데이터는 실제 값 범위만 표시
            return int(max_value + 5)
        
        # 퍼센트 데이터인지 확인 (0~100 범위)
        if max_value <= 100 and min_value >= 0:
            if max_value <= 10:
                return 12  # 0~10 범위는 12까지
            elif max_value <= 30:
                return 35  # 0~30 범위는 35까지
            elif max_value <= 50:
                return 55  # 0~50 범위는 55까지
            else:
                return 105  # 그 외는 105까지
        
        # 일반 숫자 데이터 처리
        if max_value <= 50:
            return int(max_value * 1.2 + 5)  # 20% 여백 + 5
        elif max_value <= 200:
            return int((max_value * 1.15 + 10) // 10) * 10  # 15% 여백, 10 단위
        elif max_value <= 1000:
            return int((max_value * 1.1 + 50) // 50) * 50  # 10% 여백, 50 단위  
        else:
            return int((max_value * 1.1 + 100) // 100) * 100  # 10% 여백, 100 단위
        
    def _create_chart_from_config(self, config: Dict) -> Dict:
        """설정에서 차트 생성"""
        self.chart_counter += 1
        chart_id = f"config_chart_{self.chart_counter}"
        
        chart_config = {
            'id': chart_id,
            'title': config.get('title', '차트'),
            'type': config.get('type', 'bar'),
            'data': config.get('data', {}),
            'filename': f"images/{chart_id}.html"
        }
        
        # HTML 파일 생성
        html_content = self._generate_chart_html(chart_config)
        
        # 파일 저장
        os.makedirs('images', exist_ok=True)
        with open(chart_config['filename'], 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        return chart_config
        
    def _parse_yaml_chart_config(self, config_str: str) -> Dict:
        """YAML 형태 차트 설정 파싱"""
        # 구현 생략 (복잡도 관리)
        return None


if __name__ == "__main__":
    # 테스트
    generator = AutoChartGenerator()
    
    with open('template_example.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    charts = generator.analyze_and_generate_charts(content)
    print(f"생성된 차트 수: {len(charts)}")
    
    # 디버그 정보 출력  
    table_pattern = r'^\|.*\|\s*\n\|[\s\-:]*\|\s*\n(\|.*\|\s*\n)+'
    tables = list(re.finditer(table_pattern, content, re.MULTILINE))
    print(f"발견된 표 수: {len(tables)}")
    
    chart_pattern = r'```chart\s*\n(.*?)\n```'
    chart_blocks = list(re.finditer(chart_pattern, content, re.DOTALL))
    print(f"발견된 chart 블록 수: {len(chart_blocks)}")
    
    for chart in charts:
        print(f"- {chart['title']} ({chart['type']}): {chart['filename']}")