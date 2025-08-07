#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pathlib import Path
import subprocess

class AdditionalHTMLChartGenerator:
    """
    최적화된 추가 HTML 차트 생성기
    - 최소 여백으로 정확한 컨텐츠 크기 캡처  
    - HTML 컨테이너 실제 크기 기반 Chrome 캡처 사이즈 자동 계산
    """
    def __init__(self):
        self.output_dir = Path("/Users/dykim/dev/make-docs/images")
        self.output_dir.mkdir(exist_ok=True)
        
        # 최적화된 차트별 캡처 사이즈 매핑 (표준 설정) 
        self.optimal_sizes = {
            "trl_roadmap": "1200,900",       # max-width 1200px + TRL 매트릭스 높이
            "organization_chart": "1000,700", # max-width 1000px + 조직 계층 높이
            "risk_matrix": "800,750",        # max-width 800px + 매트릭스 + 범례
            "swot_analysis": "1000,750"      # max-width 1000px + SWOT + 전략 섹션
        }
    
    def create_trl_roadmap_html(self):
        """TRL 로드맵 HTML 생성"""
        html_content = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>5대 핵심기술 TRL 기반 개발 로드맵</title>
    <style>
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
            max-width: 1200px;
            width: 100%;
        }
        .title {
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 3px solid #3498db;
        }
        .roadmap-grid {
            display: grid;
            grid-template-rows: auto auto auto auto auto auto;
            gap: 20px;
            margin-top: 20px;
        }
        .tech-row {
            display: grid;
            grid-template-columns: 200px repeat(9, 1fr);
            gap: 10px;
            align-items: center;
        }
        .tech-name {
            background: linear-gradient(135deg, #2c3e50, #34495e);
            color: white;
            padding: 15px;
            border-radius: 8px;
            font-weight: bold;
            text-align: center;
            font-size: 14px;
        }
        .trl-level {
            height: 40px;
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 12px;
            color: white;
            position: relative;
            border: 2px solid transparent;
        }
        .trl-1 { background: linear-gradient(135deg, #e74c3c, #c0392b); }
        .trl-2 { background: linear-gradient(135deg, #e67e22, #d35400); }
        .trl-3 { background: linear-gradient(135deg, #f39c12, #e67e22); }
        .trl-4 { background: linear-gradient(135deg, #f1c40f, #f39c12); }
        .trl-5 { background: linear-gradient(135deg, #27ae60, #229954); }
        .trl-6 { background: linear-gradient(135deg, #16a085, #138d75); }
        .trl-7 { background: linear-gradient(135deg, #2980b9, #21618c); }
        .trl-8 { background: linear-gradient(135deg, #8e44ad, #7d3c98); }
        .trl-9 { background: linear-gradient(135deg, #2c3e50, #1b2631); }
        .current-level {
            border-color: #f1c40f;
            border-width: 3px;
            box-shadow: 0 0 15px rgba(241, 196, 15, 0.6);
        }
        .target-level {
            border-color: #e74c3c;
            border-width: 3px;
            box-shadow: 0 0 15px rgba(231, 76, 60, 0.6);
        }
        .timeline {
            display: grid;
            grid-template-columns: 200px repeat(9, 1fr);
            gap: 10px;
            margin-bottom: 20px;
            align-items: center;
        }
        .timeline-label {
            font-weight: bold;
            text-align: center;
            color: #2c3e50;
        }
        .year {
            text-align: center;
            font-weight: bold;
            color: #3498db;
            background: #ecf0f1;
            padding: 8px;
            border-radius: 6px;
        }
        .legend {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 20px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
        }
        .legend-item {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 14px;
        }
        .legend-box {
            width: 20px;
            height: 20px;
            border-radius: 4px;
            border: 2px solid;
        }
        .legend-current {
            background: #27ae60;
            border-color: #f1c40f;
        }
        .legend-target {
            background: #e74c3c;
            border-color: #e74c3c;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="title">5대 핵심기술 TRL 기반 개발 로드맵</div>
        
        <div class="timeline">
            <div class="timeline-label">기술분야 / TRL단계</div>
            <div class="year">TRL 1</div>
            <div class="year">TRL 2</div>
            <div class="year">TRL 3</div>
            <div class="year">TRL 4</div>
            <div class="year">TRL 5</div>
            <div class="year">TRL 6</div>
            <div class="year">TRL 7</div>
            <div class="year">TRL 8</div>
            <div class="year">TRL 9</div>
        </div>
        
        <div class="roadmap-grid">
            <!-- 무인체계 기술 -->
            <div class="tech-row">
                <div class="tech-name">무인체계<br>기술</div>
                <div class="trl-level trl-1">완료</div>
                <div class="trl-level trl-2">완료</div>
                <div class="trl-level trl-3">완료</div>
                <div class="trl-level trl-4">완료</div>
                <div class="trl-level trl-5 current-level">현재</div>
                <div class="trl-level trl-6">2025</div>
                <div class="trl-level trl-7">2026</div>
                <div class="trl-level trl-8">2028</div>
                <div class="trl-level trl-9 target-level">2030</div>
            </div>
            
            <!-- AI/빅데이터 -->
            <div class="tech-row">
                <div class="tech-name">AI/빅데이터<br>기술</div>
                <div class="trl-level trl-1">완료</div>
                <div class="trl-level trl-2">완료</div>
                <div class="trl-level trl-3">완료</div>
                <div class="trl-level trl-4 current-level">현재</div>
                <div class="trl-level trl-5">2024</div>
                <div class="trl-level trl-6">2025</div>
                <div class="trl-level trl-7">2027</div>
                <div class="trl-level trl-8">2029</div>
                <div class="trl-level trl-9 target-level">2030</div>
            </div>
            
            <!-- 통신기술 -->
            <div class="tech-row">
                <div class="tech-name">통신기술</div>
                <div class="trl-level trl-1">완료</div>
                <div class="trl-level trl-2">완료</div>
                <div class="trl-level trl-3">완료</div>
                <div class="trl-level trl-4">완료</div>
                <div class="trl-level trl-5">완료</div>
                <div class="trl-level trl-6 current-level">현재</div>
                <div class="trl-level trl-7">2025</div>
                <div class="trl-level trl-8">2027</div>
                <div class="trl-level trl-9 target-level">2030</div>
            </div>
            
            <!-- 센서/반도체 -->
            <div class="tech-row">
                <div class="tech-name">센서/반도체<br>기술</div>
                <div class="trl-level trl-1">완료</div>
                <div class="trl-level trl-2">완료</div>
                <div class="trl-level trl-3 current-level">현재</div>
                <div class="trl-level trl-4">2024</div>
                <div class="trl-level trl-5">2025</div>
                <div class="trl-level trl-6">2026</div>
                <div class="trl-level trl-7">2028</div>
                <div class="trl-level trl-8">2029</div>
                <div class="trl-level trl-9 target-level">2030</div>
            </div>
            
            <!-- 신소재/에너지 -->
            <div class="tech-row">
                <div class="tech-name">신소재/에너지<br>기술</div>
                <div class="trl-level trl-1">완료</div>
                <div class="trl-level trl-2 current-level">현재</div>
                <div class="trl-level trl-3">2024</div>
                <div class="trl-level trl-4">2025</div>
                <div class="trl-level trl-5">2026</div>
                <div class="trl-level trl-6">2027</div>
                <div class="trl-level trl-7">2028</div>
                <div class="trl-level trl-8">2029</div>
                <div class="trl-level trl-9 target-level">2030</div>
            </div>
        </div>
        
        <div class="legend">
            <div class="legend-item">
                <div class="legend-box legend-current"></div>
                <span>현재 개발 단계</span>
            </div>
            <div class="legend-item">
                <div class="legend-box legend-target"></div>
                <span>목표 달성 단계 (2030)</span>
            </div>
        </div>
    </div>
</body>
</html>
        """
        
        html_file = self.output_dir / "trl_roadmap.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(html_file)
    
    def create_organization_chart_html(self):
        """조직도 HTML 생성"""
        html_content = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>첨단 민군 혁신 지원 시스템 추진 조직도</title>
    <style>
        body {
            font-family: 'Malgun Gothic', sans-serif;
            margin: 0;
            padding: 20px;
            background: #f8f9fa;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: auto;
        }
        .container {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            max-width: 1000px;
            width: 100%;
        }
        .title {
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 3px solid #3498db;
        }
        .org-level {
            margin: 20px 0;
            text-align: center;
        }
        .org-box {
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            padding: 15px 20px;
            border-radius: 10px;
            margin: 10px;
            display: inline-block;
            font-weight: bold;
            box-shadow: 0 8px 16px rgba(52, 152, 219, 0.3);
            transition: transform 0.3s ease;
            position: relative;
        }
        .org-box:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 24px rgba(52, 152, 219, 0.4);
        }
        .level-1 {
            background: linear-gradient(135deg, #2c3e50, #34495e);
            font-size: 18px;
            padding: 20px 30px;
        }
        .level-2 {
            background: linear-gradient(135deg, #3498db, #2980b9);
            font-size: 16px;
        }
        .level-3 {
            background: linear-gradient(135deg, #e74c3c, #c0392b);
            font-size: 14px;
        }
        .level-4 {
            background: linear-gradient(135deg, #27ae60, #229954);
            font-size: 13px;
        }
        .level-5 {
            background: linear-gradient(135deg, #f39c12, #e67e22);
            font-size: 12px;
        }
        .connector {
            height: 20px;
            width: 2px;
            background: #34495e;
            margin: 0 auto;
        }
        .horizontal-line {
            height: 2px;
            background: #34495e;
            margin: 10px auto;
            width: 80%;
        }
        .grid-3 {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            max-width: 800px;
            margin: 0 auto;
        }
        .grid-2 {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            max-width: 600px;
            margin: 0 auto;
        }
        .grid-4 {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            max-width: 900px;
            margin: 0 auto;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="title">첨단 민군 혁신 지원 시스템 추진 조직도</div>
        
        <!-- 최상위 -->
        <div class="org-level">
            <div class="org-box level-1">사업추진위원회<br>(총괄책임기관)</div>
        </div>
        
        <div class="connector"></div>
        
        <!-- 2단계 -->
        <div class="org-level">
            <div class="grid-3">
                <div class="org-box level-2">기술개발<br>총괄기관</div>
                <div class="org-box level-2">시험평가<br>전담기관</div>
                <div class="org-box level-2">사업화지원<br>전담기관</div>
            </div>
        </div>
        
        <div class="horizontal-line"></div>
        
        <!-- 3단계 - 기술분야별 -->
        <div class="org-level">
            <div class="grid-2">
                <div class="org-box level-3">민간기업<br>컨소시엄</div>
                <div class="org-box level-3">정부출연<br>연구기관</div>
            </div>
        </div>
        
        <div class="connector"></div>
        
        <!-- 4단계 - 세부 조직 -->
        <div class="org-level">
            <div class="grid-4">
                <div class="org-box level-4">무인체계<br>개발팀</div>
                <div class="org-box level-4">AI/빅데이터<br>개발팀</div>
                <div class="org-box level-4">통신기술<br>개발팀</div>
                <div class="org-box level-4">센서/반도체<br>개발팀</div>
            </div>
        </div>
        
        <div class="connector"></div>
        
        <!-- 5단계 - 지원 조직 -->
        <div class="org-level">
            <div class="grid-3">
                <div class="org-box level-5">품질관리팀</div>
                <div class="org-box level-5">기술사업화팀</div>
                <div class="org-box level-5">국제협력팀</div>
            </div>
        </div>
        
        <div style="margin-top: 30px; padding: 15px; background: #f8f9fa; border-radius: 10px; text-align: center;">
            <strong style="color: #2c3e50;">참여기관:</strong>
            <span style="color: #7f8c8d;">대기업 5개사, 중소기업 15개사, 정부출연연 8개 기관, 대학 12개교</span>
        </div>
    </div>
</body>
</html>
        """
        
        html_file = self.output_dir / "organization_chart.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(html_file)
    
    def create_risk_matrix_html(self):
        """리스크 매트릭스 HTML 생성"""
        html_content = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>리스크 매트릭스</title>
    <style>
        body {
            font-family: 'Malgun Gothic', sans-serif;
            margin: 0;
            padding: 20px;
            background: #f8f9fa;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: auto;
        }
        .container {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            max-width: 800px;
            width: 100%;
        }
        .title {
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 3px solid #3498db;
        }
        .matrix-container {
            position: relative;
            margin: 30px 0;
        }
        .matrix {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            grid-template-rows: repeat(4, 1fr);
            gap: 2px;
            width: 400px;
            height: 400px;
            margin: 0 auto;
            border: 2px solid #34495e;
            border-radius: 8px;
            overflow: hidden;
        }
        .matrix-cell {
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            font-size: 12px;
            font-weight: bold;
        }
        .low-low { background: linear-gradient(135deg, #2ecc71, #27ae60); }
        .low-medium { background: linear-gradient(135deg, #f1c40f, #f39c12); }
        .low-high { background: linear-gradient(135deg, #e67e22, #d35400); }
        .medium-low { background: linear-gradient(135deg, #f1c40f, #f39c12); }
        .medium-medium { background: linear-gradient(135deg, #e67e22, #d35400); }
        .medium-high { background: linear-gradient(135deg, #e74c3c, #c0392b); }
        .high-low { background: linear-gradient(135deg, #e67e22, #d35400); }
        .high-medium { background: linear-gradient(135deg, #e74c3c, #c0392b); }
        .high-high { background: linear-gradient(135deg, #8e44ad, #7d3c98); }
        .risk-point {
            position: absolute;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            border: 3px solid white;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
            cursor: pointer;
            transition: transform 0.3s ease;
        }
        .risk-point:hover {
            transform: scale(1.2);
        }
        .risk-1 { background: #e74c3c; top: 25%; left: 25%; }
        .risk-2 { background: #f39c12; top: 25%; left: 50%; }
        .risk-3 { background: #3498db; top: 50%; left: 25%; }
        .risk-4 { background: #27ae60; top: 50%; left: 50%; }
        .risk-5 { background: #9b59b6; top: 75%; left: 50%; }
        .axis-label {
            position: absolute;
            font-weight: bold;
            font-size: 16px;
            color: #2c3e50;
        }
        .x-axis {
            bottom: -40px;
            left: 50%;
            transform: translateX(-50%);
        }
        .y-axis {
            left: -80px;
            top: 50%;
            transform: translateY(-50%) rotate(-90deg);
        }
        .scale-labels {
            position: absolute;
        }
        .x-scale {
            bottom: -20px;
            font-size: 12px;
            color: #7f8c8d;
        }
        .y-scale {
            left: -40px;
            font-size: 12px;
            color: #7f8c8d;
            transform: translateY(-50%);
        }
        .legend {
            margin-top: 40px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }
        .legend-title {
            font-weight: bold;
            margin-bottom: 15px;
            color: #2c3e50;
            text-align: center;
        }
        .legend-items {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
        }
        .legend-item {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 13px;
        }
        .legend-color {
            width: 16px;
            height: 16px;
            border-radius: 50%;
            border: 2px solid white;
            box-shadow: 0 1px 3px rgba(0,0,0,0.3);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="title">리스크 매트릭스 - 발생확률 vs 영향도</div>
        
        <div class="matrix-container">
            <div class="matrix">
                <!-- 4x4 매트릭스 -->
                <div class="matrix-cell high-high"></div>
                <div class="matrix-cell high-high"></div>
                <div class="matrix-cell high-medium"></div>
                <div class="matrix-cell high-low"></div>
                
                <div class="matrix-cell high-high"></div>
                <div class="matrix-cell high-medium">
                    <div class="risk-point risk-1" title="핵심기술개발실패"></div>
                </div>
                <div class="matrix-cell medium-medium">
                    <div class="risk-point risk-3" title="국제정세변화"></div>
                </div>
                <div class="matrix-cell medium-low"></div>
                
                <div class="matrix-cell high-medium">
                    <div class="risk-point risk-2" title="기술변화대응"></div>
                </div>
                <div class="matrix-cell medium-medium">
                    <div class="risk-point risk-4" title="환율변동"></div>
                </div>
                <div class="matrix-cell medium-low"></div>
                <div class="matrix-cell low-low"></div>
                
                <div class="matrix-cell medium-high"></div>
                <div class="matrix-cell medium-medium">
                    <div class="risk-point risk-5" title="예산삭감"></div>
                </div>
                <div class="matrix-cell low-low"></div>
                <div class="matrix-cell low-low"></div>
            </div>
            
            <!-- 축 레이블 -->
            <div class="axis-label x-axis">발생확률</div>
            <div class="axis-label y-axis">영향도</div>
            
            <!-- 척도 레이블 -->
            <div class="scale-labels x-scale" style="left: 12%;">낮음</div>
            <div class="scale-labels x-scale" style="left: 37%;">중간</div>
            <div class="scale-labels x-scale" style="left: 62%;">높음</div>
            <div class="scale-labels x-scale" style="left: 87%;">매우높음</div>
            
            <div class="scale-labels y-scale" style="top: 87%;">낮음</div>
            <div class="scale-labels y-scale" style="top: 62%;">중간</div>
            <div class="scale-labels y-scale" style="top: 37%;">높음</div>
            <div class="scale-labels y-scale" style="top: 12%;">매우높음</div>
        </div>
        
        <div class="legend">
            <div class="legend-title">주요 리스크 요인</div>
            <div class="legend-items">
                <div class="legend-item">
                    <div class="legend-color" style="background: #e74c3c;"></div>
                    <span>핵심기술개발실패 (고확률-고영향)</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #f39c12;"></div>
                    <span>기술변화대응 (중확률-고영향)</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #3498db;"></div>
                    <span>국제정세변화 (고확률-중영향)</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #27ae60;"></div>
                    <span>환율변동 (중확률-중영향)</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #9b59b6;"></div>
                    <span>예산삭감 (중확률-저영향)</span>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
        """
        
        html_file = self.output_dir / "risk_matrix.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(html_file)
    
    def create_swot_analysis_html(self):
        """SWOT 분석 HTML 생성"""
        html_content = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SWOT 분석</title>
    <style>
        body {
            font-family: 'Malgun Gothic', sans-serif;
            margin: 0;
            padding: 20px;
            background: #f8f9fa;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: auto;
        }
        .container {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            max-width: 1000px;
            width: 100%;
        }
        .title {
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 3px solid #3498db;
        }
        .swot-matrix {
            display: grid;
            grid-template-columns: 1fr 1fr;
            grid-template-rows: 1fr 1fr;
            gap: 3px;
            height: 500px;
            margin: 20px 0;
            border: 3px solid #2c3e50;
            border-radius: 12px;
            overflow: hidden;
        }
        .swot-quadrant {
            padding: 25px;
            display: flex;
            flex-direction: column;
            position: relative;
        }
        .strengths {
            background: linear-gradient(135deg, #2ecc71, #27ae60);
            color: white;
        }
        .weaknesses {
            background: linear-gradient(135deg, #e74c3c, #c0392b);
            color: white;
        }
        .opportunities {
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
        }
        .threats {
            background: linear-gradient(135deg, #f39c12, #e67e22);
            color: white;
        }
        .quadrant-title {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 15px;
            text-align: center;
            padding-bottom: 10px;
            border-bottom: 2px solid rgba(255,255,255,0.3);
        }
        .quadrant-content {
            flex: 1;
            font-size: 13px;
            line-height: 1.6;
        }
        .quadrant-content ul {
            margin: 0;
            padding-left: 20px;
        }
        .quadrant-content li {
            margin-bottom: 8px;
            list-style-type: none;
            position: relative;
        }
        .quadrant-content li:before {
            content: "▶";
            position: absolute;
            left: -15px;
            color: rgba(255,255,255,0.8);
        }
        .strategy-section {
            margin-top: 30px;
            padding: 25px;
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            border-radius: 10px;
            border-left: 5px solid #3498db;
        }
        .strategy-title {
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 15px;
            text-align: center;
        }
        .strategy-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        .strategy-item {
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border-left: 4px solid;
        }
        .so-strategy { border-left-color: #2ecc71; }
        .wo-strategy { border-left-color: #e74c3c; }
        .st-strategy { border-left-color: #3498db; }
        .wt-strategy { border-left-color: #f39c12; }
        .strategy-label {
            font-weight: bold;
            font-size: 14px;
            margin-bottom: 8px;
        }
        .strategy-text {
            font-size: 13px;
            color: #555;
            line-height: 1.5;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="title">첨단 민군 혁신 지원 시스템 SWOT 분석</div>
        
        <div class="swot-matrix">
            <!-- Strengths -->
            <div class="swot-quadrant strengths">
                <div class="quadrant-title">Strengths (강점)</div>
                <div class="quadrant-content">
                    <ul>
                        <li>세계 최고 반도체 기술력 (60% 점유율)</li>
                        <li>5G 상용화 세계 최초 달성</li>
                        <li>조선산업 세계 1위 기술력</li>
                        <li>K-방산 브랜드 인지도 급속 상승</li>
                        <li>정부 강력한 정책 지원</li>
                        <li>우수한 ICT 인프라 구축</li>
                        <li>높은 기술개발 역량</li>
                    </ul>
                </div>
            </div>
            
            <!-- Weaknesses -->
            <div class="swot-quadrant weaknesses">
                <div class="quadrant-title">Weaknesses (약점)</div>
                <div class="quadrant-content">
                    <ul>
                        <li>핵심부품 해외의존 (정밀센서 80%)</li>
                        <li>중소기업 기술력 격차 심화</li>
                        <li>국방R&D 민수전환률 저조 (30%)</li>
                        <li>국제표준 대응 미흡</li>
                        <li>글로벌 마케팅 역량 부족</li>
                        <li>핵심기술 인력 부족</li>
                    </ul>
                </div>
            </div>
            
            <!-- Opportunities -->
            <div class="swot-quadrant opportunities">
                <div class="quadrant-title">Opportunities (기회)</div>
                <div class="quadrant-content">
                    <ul>
                        <li>글로벌 방산시장 성장 (3.1% CAGR)</li>
                        <li>아태지역 급속 성장 (4.2% CAGR)</li>
                        <li>무인체계 시장 급성장 (2배 확대)</li>
                        <li>신흥국 수요 급증</li>
                        <li>민수전환 기회 확대</li>
                        <li>4차 산업혁명 기술 융합</li>
                        <li>국제공동개발 확대</li>
                    </ul>
                </div>
            </div>
            
            <!-- Threats -->
            <div class="swot-quadrant threats">
                <div class="quadrant-title">Threats (위협)</div>
                <div class="quadrant-content">
                    <ul>
                        <li>미-중 기술패권 경쟁 심화</li>
                        <li>수출통제 강화 (ITAR, EAR)</li>
                        <li>경쟁국 정부지원 확대</li>
                        <li>글로벌 공급망 재편 위험</li>
                        <li>기술보호주의 확산</li>
                        <li>신기술 변화 가속화</li>
                    </ul>
                </div>
            </div>
        </div>
        
        <div class="strategy-section">
            <div class="strategy-title">전략 방향</div>
            <div class="strategy-grid">
                <div class="strategy-item so-strategy">
                    <div class="strategy-label">SO 전략: 강점 기반 기회 활용</div>
                    <div class="strategy-text">
                        핵심기술 경쟁력을 바탕으로 해외진출 가속화<br>
                        • 5G/반도체 기술 활용 무인체계 선도<br>
                        • 아태지역 전략적 진출 확대
                    </div>
                </div>
                
                <div class="strategy-item wo-strategy">
                    <div class="strategy-label">WO 전략: 약점 보완을 통한 기회 포착</div>
                    <div class="strategy-text">
                        중소기업 역량강화로 기회 활용<br>
                        • 핵심부품 국산화 추진<br>
                        • 민수전환 생태계 구축
                    </div>
                </div>
                
                <div class="strategy-item st-strategy">
                    <div class="strategy-label">ST 전략: 강점 활용 위협 대응</div>
                    <div class="strategy-text">
                        기술주권 확보 및 표준화 선도<br>
                        • 핵심기술 자립도 제고<br>
                        • 국제표준 주도권 확보
                    </div>
                </div>
                
                <div class="strategy-item wt-strategy">
                    <div class="strategy-label">WT 전략: 약점 보완 위협 최소화</div>
                    <div class="strategy-text">
                        공급망 다변화 및 자립도 제고<br>
                        • 핵심부품 공급선 다변화<br>
                        • 기술보호 체계 강화
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
        """
        
        html_file = self.output_dir / "swot_analysis.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(html_file)
    
    def get_optimal_window_size(self, html_file_path):
        """HTML 파일명 기반으로 최적 캡처 사이즈 반환 (표준 설정)"""
        for chart_type, size in self.optimal_sizes.items():
            if chart_type in html_file_path:
                return size
        return "1000,600"  # 기본값
    
    def capture_html_to_png(self, html_file_path, output_png_path):
        """HTML 파일을 PNG로 캡처"""
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
            
            # 표준 최적화된 캡처 사이즈 자동 선택
            window_size = self.get_optimal_window_size(html_file_path)
            
            cmd = [
                chrome_path,
                "--headless",
                "--disable-gpu",
                "--disable-web-security",
                "--hide-scrollbars",
                "--force-device-scale-factor=1",
                "--window-size=" + window_size,
                "--virtual-time-budget=5000",
                "--run-all-compositor-stages-before-draw",
                "--screenshot=" + output_png_path,
                "file://" + html_file_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and os.path.exists(output_png_path):
                return True
            else:
                print(f"Chrome 스크린샷 실패: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"HTML to PNG 변환 실패: {e}")
            return False
    
    def generate_additional_charts(self):
        """추가 HTML 차트 생성 및 PNG 변환"""
        charts_to_generate = [
            ("trl_roadmap", self.create_trl_roadmap_html),
            ("organization_chart", self.create_organization_chart_html),
            ("risk_matrix", self.create_risk_matrix_html),
            ("swot_analysis", self.create_swot_analysis_html)
        ]
        
        results = []
        
        for chart_name, generator_func in charts_to_generate:
            try:
                print(f"{chart_name} HTML 차트 생성 중...")
                html_file = generator_func()
                
                # PNG로 변환
                png_file = str(self.output_dir / f"{chart_name}.png")
                if self.capture_html_to_png(html_file, png_file):
                    print(f"✓ {chart_name} PNG 변환 완료")
                    results.append((chart_name, html_file, png_file))
                else:
                    print(f"✗ {chart_name} PNG 변환 실패")
                    results.append((chart_name, html_file, None))
                    
            except Exception as e:
                print(f"✗ {chart_name} 생성 실패: {e}")
                results.append((chart_name, None, None))
        
        return results

if __name__ == "__main__":
    generator = AdditionalHTMLChartGenerator()
    
    print("추가 HTML 기반 차트 생성 시작...")
    results = generator.generate_additional_charts()
    
    print("\n=== 생성 결과 ===")
    for chart_name, html_file, png_file in results:
        print(f"{chart_name}:")
        if html_file:
            print(f"  HTML: {html_file}")
        if png_file:
            print(f"  PNG: {png_file}")
        print()
            
    print("모든 추가 HTML 차트 생성이 완료되었습니다!")