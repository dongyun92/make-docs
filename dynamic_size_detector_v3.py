#!/usr/bin/env python3
"""
실용적 동적 크기 감지 시스템
HTML 파일을 분석해 CSS/콘텐츠 기반으로 적절한 크기 계산
"""

import os
import re
from pathlib import Path
import json

class PracticalSizeDetector:
    def __init__(self):
        self.base_padding = 80  # 기본 패딩
        
    def analyze_html_content(self, html_file):
        """HTML 콘텐츠 분석을 통한 크기 계산"""
        print(f"HTML 분석 중: {html_file}")
        
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 파일별 특화된 분석
        filename = Path(html_file).name
        
        if "organization_chart" in filename:
            return self._analyze_org_chart(content)
        elif "trl_roadmap" in filename:
            return self._analyze_trl_roadmap(content)
        elif "swot_analysis" in filename:
            return self._analyze_swot_analysis(content)
        elif "risk_matrix" in filename:
            return self._analyze_risk_matrix(content)
        elif "system_architecture" in filename:
            return self._analyze_system_architecture(content)
        else:
            return self._analyze_generic_chart(content)
    
    def _analyze_org_chart(self, content):
        """조직도 HTML 분석"""
        # 조직도는 5단계 계층 구조
        levels = re.findall(r'<div class="org-level">', content)
        level_count = len(levels)
        
        # 각 레벨의 박스 수 계산
        boxes = re.findall(r'<div class="org-box[^"]*">', content)
        box_count = len(boxes)
        
        # 그리드 구조 분석
        grid_3 = len(re.findall(r'grid-3', content))
        grid_4 = len(re.findall(r'grid-4', content))
        
        # 크기 계산
        # 세로: 제목(80) + 레벨 수 * 60 + 연결선 * 20 + 하단 여백(100)
        height = 80 + (level_count * 60) + ((level_count - 1) * 20) + 100
        
        # 가로: 최대 4개 그리드이므로 4 * 200 + 여백
        width = max(800, 4 * 200 + 200)  # 최소 800px
        
        return {
            "width": width + self.base_padding,
            "height": height + self.base_padding,
            "method": "org_chart_analysis",
            "details": f"{level_count}개 레벨, {box_count}개 박스"
        }
    
    def _analyze_trl_roadmap(self, content):
        """TRL 로드맵 분석"""
        # TRL 단계 수 계산 (보통 TRL 1-9)
        trl_stages = len(re.findall(r'TRL \d+', content))
        
        # 기술 트랙 수 계산
        tech_tracks = len(re.findall(r'기술|AI|통신|센서|무인', content))
        
        # 그리드 구조에서 행/열 계산
        grid_match = re.search(r'grid-template-rows:[^;]*repeat\((\d+)', content)
        rows = int(grid_match.group(1)) if grid_match else 5
        
        # 크기 계산 - 가로형 로드맵
        width = max(1200, trl_stages * 120 + 300)  # TRL 단계 * 120px + 여백
        height = max(600, rows * 80 + 150)  # 행 수 * 80px + 여백
        
        return {
            "width": width + self.base_padding,
            "height": height + self.base_padding, 
            "method": "trl_roadmap_analysis",
            "details": f"{trl_stages}개 TRL 단계, {rows}개 기술 트랙"
        }
    
    def _analyze_swot_analysis(self, content):
        """SWOT 분석 차트 분석"""
        # SWOT 4사분면 구조
        swot_sections = len(re.findall(r'(Strengths|Weaknesses|Opportunities|Threats)', content))
        
        # 텍스트 길이로 높이 추정
        text_content = re.sub(r'<[^>]+>', '', content)
        text_length = len(text_content.replace(' ', ''))
        
        # 기본 2x2 그리드 + 하단 전략 섹션
        width = 600  # SWOT 기본 정사각형 구조
        height = 500  # 4사분면 + 전략 섹션
        
        # 텍스트가 많으면 높이 증가
        if text_length > 2000:
            height += 200
        
        return {
            "width": width + self.base_padding,
            "height": height + self.base_padding,
            "method": "swot_analysis",
            "details": f"{swot_sections}개 SWOT 섹션, 텍스트 {text_length}자"
        }
    
    def _analyze_risk_matrix(self, content):
        """리스크 매트릭스 분석"""
        # 5x5 또는 3x3 매트릭스 구조 감지
        matrix_size = 5 if '5x5' in content else 3
        
        # 리스크 항목 수 계산
        risk_items = len(re.findall(r'(위험|리스크|Risk)', content, re.IGNORECASE))
        
        # 매트릭스 크기에 따른 계산
        cell_size = 80
        width = matrix_size * cell_size + 200  # 매트릭스 + 축 라벨 여백
        height = matrix_size * cell_size + 200
        
        return {
            "width": width + self.base_padding,
            "height": height + self.base_padding,
            "method": "risk_matrix_analysis", 
            "details": f"{matrix_size}x{matrix_size} 매트릭스, {risk_items}개 리스크"
        }
    
    def _analyze_system_architecture(self, content):
        """시스템 아키텍처 분석"""
        # 컴포넌트/박스 수 계산
        components = len(re.findall(r'<div class="[^"]*box[^"]*"', content))
        
        # 그리드 구조 분석
        grid_cols_match = re.search(r'grid-template-columns:[^;]*repeat\((\d+)', content)
        cols = int(grid_cols_match.group(1)) if grid_cols_match else 3
        
        grid_rows_match = re.search(r'grid-template-rows:[^;]*repeat\((\d+)', content) 
        rows = int(grid_rows_match.group(1)) if grid_rows_match else 3
        
        # 아키텍처 다이어그램은 보통 가로형
        width = max(1000, cols * 250)  # 컬럼 수 * 250px
        height = max(600, rows * 150)   # 행 수 * 150px
        
        return {
            "width": width + self.base_padding,
            "height": height + self.base_padding,
            "method": "system_architecture_analysis",
            "details": f"{cols}x{rows} 그리드, {components}개 컴포넌트"
        }
    
    def _analyze_generic_chart(self, content):
        """일반 차트 분석"""
        # 기본 차트 크기
        width = 1000
        height = 700
        
        # 테이블이 있으면 크기 증가
        if '<table' in content:
            width += 200
            height += 200
        
        # 텍스트 양에 따른 조정
        text_content = re.sub(r'<[^>]+>', '', content)
        if len(text_content) > 3000:
            width += 200
            height += 200
        
        return {
            "width": width + self.base_padding,
            "height": height + self.base_padding,
            "method": "generic_analysis",
            "details": "일반 차트"
        }
    
    def batch_analyze(self, html_files):
        """여러 파일 일괄 분석"""
        results = {}
        
        print("=== 실용적 크기 분석 시작 ===\n")
        
        for html_file in html_files:
            if os.path.exists(html_file):
                size_info = self.analyze_html_content(html_file)
                results[html_file] = size_info
                
                print(f"분석 결과: {Path(html_file).name}")
                print(f"  크기: {size_info['width']}x{size_info['height']}")
                print(f"  방법: {size_info['method']}")
                print(f"  상세: {size_info['details']}")
                print()
            else:
                print(f"파일 없음: {html_file}\n")
        
        # 결과 요약 및 JSON 저장
        print("=== 분석 결과 요약 ===")
        sizing_config = {}
        
        for file, size in results.items():
            filename = Path(file).name
            chart_name = filename.replace('.html', '')
            
            sizing_config[chart_name] = {
                "width": size['width'],
                "height": size['height'],
                "method": size['method'],
                "details": size['details']
            }
            
            print(f"{filename}: {size['width']}x{size['height']} ({size['method']})")
        
        # 설정 파일 저장
        with open('practical_sizing_config.json', 'w', encoding='utf-8') as f:
            json.dump(sizing_config, f, indent=2, ensure_ascii=False)
        
        print(f"\n크기 설정이 practical_sizing_config.json에 저장되었습니다.")
        
        return results

if __name__ == "__main__":
    detector = PracticalSizeDetector()
    
    # HTML 파일 목록
    html_files = [
        "images/organization_chart.html",
        "images/trl_roadmap.html", 
        "images/swot_analysis.html",
        "images/risk_matrix.html",
        "images/system_architecture.html",
        "images/market_growth_line.html",
        "images/market_growth_regional.html",
        "images/budget_pie.html",
        "images/budget_trend.html"
    ]
    
    # 실용적 크기 분석 실행
    results = detector.batch_analyze(html_files)