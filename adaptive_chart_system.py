#!/usr/bin/env python3
"""
적응형 차트 크기 시스템 - 콘텐츠 복잡도 기반 동적 크기 결정
"""

import os
import re
import math
import json
from pathlib import Path

class ContentComplexityAnalyzer:
    """콘텐츠 복잡도 분석기"""
    
    def __init__(self):
        self.base_canvas_size = (1200, 800)  # 기본 캔버스
        self.min_canvas_size = (800, 600)    # 최소 크기
        self.max_canvas_size = (1600, 1200)  # 최대 크기
        
    def analyze_content_complexity(self, html_content):
        """HTML 콘텐츠의 복잡도를 다차원으로 분석"""
        
        complexity_score = {
            'text_density': self._calculate_text_density(html_content),
            'layout_complexity': self._calculate_layout_complexity(html_content),
            'element_count': self._calculate_element_complexity(html_content),
            'grid_complexity': self._calculate_grid_complexity(html_content),
            'table_complexity': self._calculate_table_complexity(html_content),
            'total_score': 0
        }
        
        # 가중치 적용하여 총점 계산
        weights = {
            'text_density': 0.3,
            'layout_complexity': 0.25,
            'element_count': 0.2,
            'grid_complexity': 0.15,
            'table_complexity': 0.1
        }
        
        total_score = sum(complexity_score[key] * weights[key] 
                         for key in weights.keys())
        complexity_score['total_score'] = total_score
        
        return complexity_score
    
    def _calculate_text_density(self, html_content):
        """텍스트 밀도 계산 (0-100)"""
        text_content = re.findall(r'>[^<]+<', html_content)
        total_text_length = sum(len(text.strip(' ><')) for text in text_content if text.strip(' ><'))
        
        # 텍스트 길이에 따른 점수 (0-100)
        if total_text_length < 500:
            return 10
        elif total_text_length < 1500:
            return 30
        elif total_text_length < 3000:
            return 60
        elif total_text_length < 5000:
            return 80
        else:
            return 100
    
    def _calculate_layout_complexity(self, html_content):
        """레이아웃 복잡도 계산 (0-100)"""
        complexity = 0
        
        # Flexbox 사용
        if 'display: flex' in html_content:
            complexity += 20
        
        # CSS Grid 사용  
        if 'display: grid' in html_content:
            complexity += 30
        
        # Position absolute/relative 사용
        position_count = len(re.findall(r'position:\s*(absolute|relative)', html_content))
        complexity += min(position_count * 10, 30)
        
        # Transform 사용
        if 'transform:' in html_content:
            complexity += 20
        
        return min(complexity, 100)
    
    def _calculate_element_complexity(self, html_content):
        """요소 개수 복잡도 계산 (0-100)"""
        div_count = len(re.findall(r'<div', html_content))
        
        if div_count < 5:
            return 10
        elif div_count < 15:
            return 25
        elif div_count < 30:
            return 50
        elif div_count < 50:
            return 75
        else:
            return 100
    
    def _calculate_grid_complexity(self, html_content):
        """CSS Grid 복잡도 계산 (0-100)"""
        grid_patterns = re.findall(r'grid-template-columns:\s*([^;]+)', html_content)
        
        if not grid_patterns:
            return 0
        
        max_columns = 0
        for pattern in grid_patterns:
            # repeat(n, 1fr) 패턴 추출
            repeat_matches = re.findall(r'repeat\((\d+)', pattern)
            if repeat_matches:
                max_columns = max(max_columns, int(repeat_matches[0]))
            
            # 1fr 개수 계산
            fr_count = pattern.count('1fr')
            max_columns = max(max_columns, fr_count)
        
        # 컬럼 수에 따른 복잡도
        if max_columns <= 2:
            return 20
        elif max_columns <= 4:
            return 50
        elif max_columns <= 6:
            return 75
        else:
            return 100
    
    def _calculate_table_complexity(self, html_content):
        """테이블 복잡도 계산 (0-100)"""
        table_count = html_content.count('<table')
        tr_count = html_content.count('<tr')
        td_count = html_content.count('<td')
        
        if table_count == 0:
            return 0
        
        # 평균 셀 수 계산
        avg_cells = td_count / table_count if table_count > 0 else 0
        
        if avg_cells < 10:
            return 20
        elif avg_cells < 30:
            return 50
        elif avg_cells < 60:
            return 75
        else:
            return 100

class AdaptiveCanvasCalculator:
    """적응형 캔버스 크기 계산기"""
    
    def __init__(self):
        self.complexity_analyzer = ContentComplexityAnalyzer()
        
        # 차트 타입별 기본 비율 설정
        self.chart_type_ratios = {
            'matrix': (1.0, 1.0),      # 정사각형 비율
            'roadmap': (1.5, 1.0),     # 가로형
            'swot': (1.2, 1.0),        # 약간 가로형
            'organization': (1.0, 1.2), # 약간 세로형  
            'gantt': (2.0, 1.0),       # 매우 가로형
            'pie': (1.0, 1.0),         # 정사각형
            'line': (1.4, 1.0),        # 가로형
            'bar': (1.4, 1.0),         # 가로형
            'default': (1.2, 1.0)      # 기본값
        }
    
    def calculate_optimal_size(self, html_file_path):
        """HTML 파일의 최적 캔버스 크기 계산"""
        
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 복잡도 분석
        complexity = self.complexity_analyzer.analyze_content_complexity(html_content)
        
        # 차트 타입 감지
        chart_type = self._detect_chart_type(html_file_path, html_content)
        
        # 기본 크기에서 복잡도에 따라 스케일링
        base_width, base_height = self.complexity_analyzer.base_canvas_size
        
        # 복잡도 기반 스케일링 팩터 (0.7 ~ 1.8)
        complexity_factor = 0.7 + (complexity['total_score'] / 100) * 1.1
        
        # 차트 타입별 비율 적용
        width_ratio, height_ratio = self.chart_type_ratios.get(chart_type, self.chart_type_ratios['default'])
        
        # 최종 크기 계산
        optimal_width = int(base_width * complexity_factor * width_ratio)
        optimal_height = int(base_height * complexity_factor * height_ratio)
        
        # 최소/최대 크기 제한 적용
        min_w, min_h = self.complexity_analyzer.min_canvas_size
        max_w, max_h = self.complexity_analyzer.max_canvas_size
        
        optimal_width = max(min_w, min(optimal_width, max_w))
        optimal_height = max(min_h, min(optimal_height, max_h))
        
        return {
            'width': optimal_width,
            'height': optimal_height,
            'complexity_score': complexity['total_score'],
            'chart_type': chart_type,
            'scaling_factor': complexity_factor,
            'aspect_ratio': width_ratio / height_ratio,
            'complexity_details': complexity
        }
    
    def _detect_chart_type(self, file_path, html_content):
        """파일명과 콘텐츠로부터 차트 타입 감지"""
        
        file_name = Path(file_path).stem.lower()
        content_lower = html_content.lower()
        
        if 'matrix' in file_name or 'matrix' in content_lower:
            return 'matrix'
        elif 'roadmap' in file_name or 'trl' in file_name:
            return 'roadmap'
        elif 'swot' in file_name or 'swot' in content_lower:
            return 'swot'
        elif 'organization' in file_name or 'org' in file_name:
            return 'organization'
        elif 'gantt' in file_name or 'schedule' in file_name:
            return 'gantt'
        elif 'pie' in file_name:
            return 'pie'
        elif 'line' in file_name or 'growth' in file_name:
            return 'line'
        elif 'bar' in file_name or 'budget' in file_name:
            return 'bar'
        else:
            return 'default'

def generate_adaptive_sizing_config():
    """모든 차트에 대한 적응형 크기 설정 생성"""
    
    calculator = AdaptiveCanvasCalculator()
    charts_dir = Path("images")
    
    chart_files = list(charts_dir.glob("*.html"))
    sizing_config = {}
    
    print("🧠 적응형 차트 크기 분석 시작...")
    print("=" * 80)
    
    for html_file in chart_files:
        chart_name = html_file.stem
        size_info = calculator.calculate_optimal_size(html_file)
        
        sizing_config[chart_name] = size_info
        
        print(f"📊 {chart_name.upper()}")
        print(f"   최적 크기: {size_info['width']}x{size_info['height']}")
        print(f"   복잡도 점수: {size_info['complexity_score']:.1f}/100")
        print(f"   차트 타입: {size_info['chart_type']}")
        print(f"   스케일링 팩터: {size_info['scaling_factor']:.2f}")
        print(f"   화면 비율: {size_info['aspect_ratio']:.2f}")
        print()
    
    # 설정을 JSON 파일로 저장
    with open('adaptive_sizing_config.json', 'w', encoding='utf-8') as f:
        json.dump(sizing_config, f, indent=2, ensure_ascii=False)
    
    print("✅ 적응형 크기 설정 저장완료: adaptive_sizing_config.json")
    
    # 요약 통계
    sizes = [(config['width'], config['height']) for config in sizing_config.values()]
    avg_width = sum(size[0] for size in sizes) / len(sizes)
    avg_height = sum(size[1] for size in sizes) / len(sizes)
    
    print("\n📋 요약 통계:")
    print(f"   평균 크기: {avg_width:.0f}x{avg_height:.0f}")
    print(f"   크기 범위: {min(s[0] for s in sizes)}~{max(s[0] for s in sizes)} x {min(s[1] for s in sizes)}~{max(s[1] for s in sizes)}")
    print(f"   총 차트 수: {len(sizing_config)}")
    
    return sizing_config

if __name__ == "__main__":
    generate_adaptive_sizing_config()