#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pathlib import Path
import base64
import subprocess
import time

class HTMLChartGenerator:
    """
    최적화된 HTML 차트 생성기
    - 최소 여백으로 정확한 컨텐츠 크기 캡처
    - HTML 컨테이너 실제 크기 기반 Chrome 캡처 사이즈 자동 계산
    """
    def __init__(self):
        self.output_dir = Path("/Users/dykim/dev/make-docs/images")
        self.output_dir.mkdir(exist_ok=True)
        
        # 최적화된 차트별 캡처 사이즈 매핑 (표준 설정)
        self.optimal_sizes = {
            "system_architecture": "1100,750",    # max-width 1000px + 계층구조 여백
            "market_growth": "1200,650",          # max-width 1200px + 차트 2개 배치
            "budget_distribution": "1200,650",    # max-width 1200px + 차트 2개 배치
            # 개별 차트 사이즈 (캡션 매칭용)
            "market_growth_line": "700,500",      # 라인 차트 단독
            "market_growth_regional": "700,500",  # 도넛 차트 단독
            "budget_pie": "700,500",              # 파이 차트 단독  
            "budget_trend": "700,500"             # 라인 차트 단독
        }
        
    def setup_webdriver(self):
        """WebDriver 설정 - macOS에서 사용 가능한 브라우저 확인"""
        # macOS에서 Chrome이 설치되어 있는지 확인
        chrome_paths = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Chrome.app/Contents/MacOS/Chrome"
        ]
        
        for chrome_path in chrome_paths:
            if os.path.exists(chrome_path):
                print(f"Chrome 발견: {chrome_path}")
                return True
                
        print("Chrome을 찾을 수 없습니다. HTML 파일만 생성됩니다.")
        return False
    
    def create_system_architecture_html(self):
        """시스템 구성도 HTML 생성"""
        html_content = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>첨단 민군 혁신 지원 시스템 구성도</title>
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
        .system-box {
            border: 2px solid #3498db;
            border-radius: 10px;
            padding: 15px;
            margin: 10px;
            text-align: center;
            position: relative;
            transition: all 0.3s ease;
        }
        .system-box:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(52, 152, 219, 0.3);
        }
        .level1 { background: linear-gradient(135deg, #3498db, #2980b9); color: white; font-size: 18px; font-weight: bold; }
        .level2 { background: linear-gradient(135deg, #e74c3c, #c0392b); color: white; font-size: 16px; }
        .level3 { background: linear-gradient(135deg, #f39c12, #e67e22); color: white; font-size: 14px; }
        .level4 { background: linear-gradient(135deg, #27ae60, #229954); color: white; font-size: 12px; }
        .arrow {
            position: absolute;
            font-size: 20px;
            color: #34495e;
            font-weight: bold;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin: 20px 0;
        }
        .sub-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="title">첨단 민군 혁신 지원 시스템 전체 구성도</div>
        
        <div class="grid">
            <!-- 상위 시스템 -->
            <div class="system-box level1">
                통합 관리 시스템<br>
                (Integrated Management System)
            </div>
            <div class="system-box level1">
                민군기술협력<br>플랫폼
            </div>
            <div class="system-box level1">
                기술사업화<br>지원센터
            </div>
        </div>
        
        <div style="text-align: center; margin: 20px 0;">
            <div style="font-size: 24px; color: #34495e;">↓</div>
        </div>
        
        <div class="grid">
            <!-- 핵심 기술 영역 -->
            <div class="system-box level2">
                무인체계 기술<br>
                (Unmanned Systems)
            </div>
            <div class="system-box level2">
                AI/빅데이터<br>
                (AI & Big Data)
            </div>
            <div class="system-box level2">
                통신기술<br>
                (Communication Tech)
            </div>
        </div>
        
        <div class="grid">
            <div class="system-box level2">
                센서/반도체<br>
                (Sensor & Semiconductor)
            </div>
            <div class="system-box level2">
                사이버보안<br>
                (Cybersecurity)
            </div>
            <div class="system-box level2">
                신소재/에너지<br>
                (Advanced Materials)
            </div>
        </div>
        
        <div style="text-align: center; margin: 20px 0;">
            <div style="font-size: 24px; color: #34495e;">↓</div>
        </div>
        
        <div class="grid">
            <!-- 지원 시스템 -->
            <div class="system-box level3">
                기술개발 지원<br>
                R&D Support
            </div>
            <div class="system-box level3">
                시험평가 지원<br>
                Test & Evaluation
            </div>
            <div class="system-box level3">
                인증/표준화<br>
                Certification
            </div>
        </div>
        
        <div style="text-align: center; margin: 20px 0;">
            <div style="font-size: 24px; color: #34495e;">↓</div>
        </div>
        
        <div class="grid">
            <!-- 결과 영역 -->
            <div class="system-box level4">
                국산화 성과<br>
                Localization
            </div>
            <div class="system-box level4">
                수출 성과<br>
                Export Achievement
            </div>
            <div class="system-box level4">
                기술사업화<br>
                Tech Commercialization
            </div>
        </div>
    </div>
</body>
</html>
        """
        
        html_file = self.output_dir / "system_architecture.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(html_file)
    
    def create_market_growth_html(self):
        """시장 성장 차트 HTML 생성"""
        html_content = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>한국 방산 수출 성장 추이</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
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
        .chart-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-top: 20px;
        }
        .chart-box {
            background: #f0f0f0;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .chart-title {
            text-align: center;
            font-size: 16px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 15px;
        }
        canvas {
            max-height: 280px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="title">한국 방산 수출 성장 추이 및 전망</div>
        
        <div class="chart-container">
            <div class="chart-box">
                <div class="chart-title">방산 수출 성장 추이 (억 달러)</div>
                <canvas id="growthChart"></canvas>
            </div>
            <div class="chart-box">
                <div class="chart-title">글로벌 방산시장 지역별 성장 전망 (2030)</div>
                <canvas id="regionalChart"></canvas>
            </div>
        </div>
    </div>

    <script>
        // 방산 수출 성장 추이 차트
        const growthCtx = document.getElementById('growthChart').getContext('2d');
        new Chart(growthCtx, {
            type: 'line',
            data: {
                labels: ['2019', '2021', '2023', '2024 목표', '2025', '2027', '2030'],
                datasets: [
                    {
                        label: '실적',
                        data: [45, 93, 140, null, null, null, null],
                        borderColor: '#3498db',
                        backgroundColor: 'rgba(52, 152, 219, 0.1)',
                        pointBackgroundColor: '#3498db',
                        pointBorderWidth: 3,
                        pointRadius: 6,
                        tension: 0.4
                    },
                    {
                        label: '2024 목표',
                        data: [null, null, null, 200, null, null, null],
                        borderColor: '#e74c3c',
                        backgroundColor: 'transparent',
                        pointBackgroundColor: '#e74c3c',
                        pointBorderWidth: 3,
                        pointRadius: 8,
                        pointStyle: 'star'
                    },
                    {
                        label: '최적 시나리오',
                        data: [null, null, null, null, 180, 220, 250],
                        borderColor: '#27ae60',
                        borderDash: [5, 5],
                        backgroundColor: 'rgba(39, 174, 96, 0.1)',
                        pointBackgroundColor: '#27ae60',
                        pointBorderWidth: 2,
                        pointRadius: 5,
                        tension: 0.4
                    },
                    {
                        label: '기준 시나리오',
                        data: [null, null, null, null, 170, 200, 220],
                        borderColor: '#f39c12',
                        backgroundColor: 'rgba(243, 156, 18, 0.1)',
                        pointBackgroundColor: '#f39c12',
                        pointBorderWidth: 2,
                        pointRadius: 5,
                        tension: 0.4
                    },
                    {
                        label: '보수 시나리오',
                        data: [null, null, null, null, 160, 180, 180],
                        borderColor: '#e67e22',
                        borderDash: [2, 2],
                        backgroundColor: 'rgba(230, 126, 34, 0.1)',
                        pointBackgroundColor: '#e67e22',
                        pointBorderWidth: 2,
                        pointRadius: 4,
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 15,
                            usePointStyle: true
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 280,
                        title: {
                            display: true,
                            text: '수출액 (억 달러)',
                            font: { size: 14, weight: 'bold' }
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: '연도',
                            font: { size: 14, weight: 'bold' }
                        }
                    }
                }
            }
        });

        // 지역별 시장 성장 차트
        const regionalCtx = document.getElementById('regionalChart').getContext('2d');
        new Chart(regionalCtx, {
            type: 'doughnut',
            data: {
                labels: ['아시아태평양 (4.2%)', '유럽 (3.8%)', '북미 (2.9%)', '중동 (3.5%)', '기타 (2.1%)'],
                datasets: [{
                    data: [1280, 1150, 2100, 920, 450],
                    backgroundColor: [
                        '#2c3e50',  // 다크 네이비 - 아시아태평양
                        '#34495e',  // 다크 그레이 - 유럽
                        '#3498db',  // 블루 - 북미
                        '#e74c3c',  // 레드 - 중동
                        '#f39c12'   // 오렌지 - 기타
                    ],
                    borderWidth: 3,
                    borderColor: '#fff',
                    hoverBorderWidth: 5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 15,
                            font: { size: 12 }
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.label + ': ' + context.parsed + '억 달러';
                            }
                        }
                    }
                },
                backgroundColor: '#f5f5f5'
            }
        });
    </script>
</body>
</html>
        """
        
        html_file = self.output_dir / "market_growth_trends.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(html_file)
    
    def create_budget_distribution_html(self):
        """예산 배분 차트 HTML 생성"""
        html_content = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>투자 배분 및 추이</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
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
        .chart-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-top: 20px;
        }
        .chart-box {
            background: #f0f0f0;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .chart-title {
            text-align: center;
            font-size: 16px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 15px;
        }
        canvas {
            max-height: 280px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="title">총 투자 3,500억원 분야별 배분 및 연도별 추이</div>
        
        <div class="chart-container">
            <div class="chart-box">
                <div class="chart-title">분야별 투자 배분</div>
                <canvas id="distributionChart"></canvas>
            </div>
            <div class="chart-box">
                <div class="chart-title">연도별 투자 규모 추이</div>
                <canvas id="trendChart"></canvas>
            </div>
        </div>
    </div>

    <script>
        // 분야별 투자 배분 차트
        const distributionCtx = document.getElementById('distributionChart').getContext('2d');
        new Chart(distributionCtx, {
            type: 'pie',
            data: {
                labels: ['무인체계', 'AI/빅데이터', '통신기술', '센서/반도체', '기타 신기술'],
                datasets: [{
                    data: [1050, 700, 875, 525, 350],
                    backgroundColor: [
                        '#2c3e50',  // 다크 네이비 - 무인체계
                        '#34495e',  // 다크 그레이 - AI/빅데이터  
                        '#3498db',  // 블루 - 통신기술
                        '#e74c3c',  // 레드 - 센서/반도체
                        '#f39c12'   // 오렌지 - 기타 신기술
                    ],
                    borderWidth: 3,
                    borderColor: '#fff',
                    hoverBorderWidth: 5,
                    hoverOffset: 10
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 15,
                            font: { size: 12 },
                            generateLabels: function(chart) {
                                const data = chart.data;
                                if (data.labels.length && data.datasets.length) {
                                    return data.labels.map((label, i) => {
                                        const value = data.datasets[0].data[i];
                                        const percentage = ((value / data.datasets[0].data.reduce((a, b) => a + b, 0)) * 100).toFixed(1);
                                        return {
                                            text: `${label} (${value}억원, ${percentage}%)`,
                                            fillStyle: data.datasets[0].backgroundColor[i],
                                            index: i
                                        };
                                    });
                                }
                                return [];
                            }
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const total = context.dataset.data.reduce((sum, value) => sum + value, 0);
                                const percentage = ((context.parsed / total) * 100).toFixed(1);
                                return `${context.label}: ${context.parsed}억원 (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });

        // 연도별 투자 추이 차트
        const trendCtx = document.getElementById('trendChart').getContext('2d');
        new Chart(trendCtx, {
            type: 'line',
            data: {
                labels: ['2024', '2025', '2026', '2027', '2028', '2029', '2030'],
                datasets: [
                    {
                        label: '총 투자액',
                        data: [230, 420, 580, 700, 580, 470, 520],
                        borderColor: '#e74c3c',
                        backgroundColor: 'rgba(231, 76, 60, 0.1)',
                        pointBackgroundColor: '#e74c3c',
                        pointBorderWidth: 3,
                        pointRadius: 6,
                        tension: 0.4,
                        fill: true
                    },
                    {
                        label: '정부 예산',
                        data: [100, 180, 250, 300, 250, 200, 220],
                        borderColor: '#3498db',
                        borderDash: [5, 5],
                        backgroundColor: 'rgba(52, 152, 219, 0.1)',
                        pointBackgroundColor: '#3498db',
                        pointBorderWidth: 2,
                        pointRadius: 5,
                        tension: 0.4
                    },
                    {
                        label: '민간 투자',
                        data: [130, 240, 330, 400, 330, 270, 300],
                        borderColor: '#27ae60',
                        borderDash: [2, 2],
                        backgroundColor: 'rgba(39, 174, 96, 0.1)',
                        pointBackgroundColor: '#27ae60',
                        pointBorderWidth: 2,
                        pointRadius: 5,
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 15,
                            usePointStyle: true
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 750,
                        title: {
                            display: true,
                            text: '투자액 (억원)',
                            font: { size: 14, weight: 'bold' }
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: '연도',
                            font: { size: 14, weight: 'bold' }
                        }
                    }
                }
            }
        });
    </script>
</body>
</html>
        """
        
        html_file = self.output_dir / "budget_distribution.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(html_file)
    
    def create_market_growth_line_chart_html(self):
        """시장 성장 라인 차트 HTML 생성 (개별)"""
        html_content = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>한국 방산 수출 성장 추이</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
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
            max-width: 600px;
            width: 100%;
        }
        .title {
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #3498db;
        }
        canvas {
            max-height: 350px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="title">한국 방산 수출 성장 추이 (2019-2030)</div>
        <canvas id="growthChart"></canvas>
    </div>

    <script>
        // 방산 수출 성장 추이 차트
        const growthCtx = document.getElementById('growthChart').getContext('2d');
        new Chart(growthCtx, {
            type: 'line',
            data: {
                labels: ['2019', '2021', '2023', '2024 목표', '2025', '2027', '2030'],
                datasets: [
                    {
                        label: '실적',
                        data: [45, 93, 140, null, null, null, null],
                        borderColor: '#3498db',
                        backgroundColor: 'rgba(52, 152, 219, 0.1)',
                        pointBackgroundColor: '#3498db',
                        pointBorderWidth: 3,
                        pointRadius: 6,
                        tension: 0.4
                    },
                    {
                        label: '2024 목표',
                        data: [null, null, null, 200, null, null, null],
                        borderColor: '#e74c3c',
                        backgroundColor: 'transparent',
                        pointBackgroundColor: '#e74c3c',
                        pointBorderWidth: 3,
                        pointRadius: 8,
                        pointStyle: 'star'
                    },
                    {
                        label: '최적 시나리오',
                        data: [null, null, null, null, 180, 220, 250],
                        borderColor: '#27ae60',
                        borderDash: [5, 5],
                        backgroundColor: 'rgba(39, 174, 96, 0.1)',
                        pointBackgroundColor: '#27ae60',
                        pointBorderWidth: 2,
                        pointRadius: 5,
                        tension: 0.4
                    },
                    {
                        label: '기준 시나리오',
                        data: [null, null, null, null, 170, 200, 220],
                        borderColor: '#f39c12',
                        backgroundColor: 'rgba(243, 156, 18, 0.1)',
                        pointBackgroundColor: '#f39c12',
                        pointBorderWidth: 2,
                        pointRadius: 5,
                        tension: 0.4
                    },
                    {
                        label: '보수 시나리오',
                        data: [null, null, null, null, 160, 180, 180],
                        borderColor: '#e67e22',
                        borderDash: [2, 2],
                        backgroundColor: 'rgba(230, 126, 34, 0.1)',
                        pointBackgroundColor: '#e67e22',
                        pointBorderWidth: 2,
                        pointRadius: 4,
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 15,
                            usePointStyle: true
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 280,
                        title: {
                            display: true,
                            text: '수출액 (억 달러)',
                            font: { size: 14, weight: 'bold' }
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: '연도',
                            font: { size: 14, weight: 'bold' }
                        }
                    }
                }
            }
        });
    </script>
</body>
</html>
        """
        
        html_file = self.output_dir / "market_growth_line.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(html_file)
    
    def create_market_growth_regional_chart_html(self):
        """지역별 시장 성장 도넛 차트 HTML 생성 (개별)"""
        html_content = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>글로벌 방산시장 지역별 성장 전망</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
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
            max-width: 600px;
            width: 100%;
        }
        .title {
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #3498db;
        }
        canvas {
            max-height: 350px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="title">글로벌 방산시장 지역별 성장 전망 (2024-2030)</div>
        <canvas id="regionalChart"></canvas>
    </div>

    <script>
        // 지역별 시장 성장 차트
        const regionalCtx = document.getElementById('regionalChart').getContext('2d');
        new Chart(regionalCtx, {
            type: 'doughnut',
            data: {
                labels: ['아시아태평양 (4.2%)', '유럽 (3.8%)', '북미 (2.9%)', '중동 (3.5%)', '기타 (2.1%)'],
                datasets: [{
                    data: [1280, 1150, 2100, 920, 450],
                    backgroundColor: [
                        '#2c3e50',  // 다크 네이비 - 아시아태평양
                        '#34495e',  // 다크 그레이 - 유럽
                        '#3498db',  // 블루 - 북미
                        '#e74c3c',  // 레드 - 중동
                        '#f39c12'   // 오렌지 - 기타
                    ],
                    borderWidth: 3,
                    borderColor: '#fff',
                    hoverBorderWidth: 5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 15,
                            font: { size: 12 }
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.label + ': ' + context.parsed + '억 달러';
                            }
                        }
                    }
                }
            }
        });
    </script>
</body>
</html>
        """
        
        html_file = self.output_dir / "market_growth_regional.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(html_file)
    
    def create_budget_pie_chart_html(self):
        """예산 배분 파이 차트 HTML 생성 (개별)"""
        html_content = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>분야별 투자 배분</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
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
            max-width: 600px;
            width: 100%;
        }
        .title {
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #3498db;
        }
        canvas {
            max-height: 350px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="title">총 투자 3,500억원 분야별 배분</div>
        <canvas id="distributionChart"></canvas>
    </div>

    <script>
        // 분야별 투자 배분 차트
        const distributionCtx = document.getElementById('distributionChart').getContext('2d');
        new Chart(distributionCtx, {
            type: 'pie',
            data: {
                labels: ['무인체계', 'AI/빅데이터', '통신기술', '센서/반도체', '기타 신기술'],
                datasets: [{
                    data: [1050, 700, 875, 525, 350],
                    backgroundColor: [
                        '#2c3e50',  // 다크 네이비 - 무인체계
                        '#34495e',  // 다크 그레이 - AI/빅데이터  
                        '#3498db',  // 블루 - 통신기술
                        '#e74c3c',  // 레드 - 센서/반도체
                        '#f39c12'   // 오렌지 - 기타 신기술
                    ],
                    borderWidth: 3,
                    borderColor: '#fff',
                    hoverBorderWidth: 5,
                    hoverOffset: 10
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 15,
                            font: { size: 12 },
                            generateLabels: function(chart) {
                                const data = chart.data;
                                if (data.labels.length && data.datasets.length) {
                                    return data.labels.map((label, i) => {
                                        const value = data.datasets[0].data[i];
                                        const percentage = ((value / data.datasets[0].data.reduce((a, b) => a + b, 0)) * 100).toFixed(1);
                                        return {
                                            text: `${label} (${value}억원, ${percentage}%)`,
                                            fillStyle: data.datasets[0].backgroundColor[i],
                                            index: i
                                        };
                                    });
                                }
                                return [];
                            }
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const total = context.dataset.data.reduce((sum, value) => sum + value, 0);
                                const percentage = ((context.parsed / total) * 100).toFixed(1);
                                return `${context.label}: ${context.parsed}억원 (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });
    </script>
</body>
</html>
        """
        
        html_file = self.output_dir / "budget_pie.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(html_file)
    
    def create_budget_trend_chart_html(self):
        """연도별 투자 추이 차트 HTML 생성 (개별)"""
        html_content = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>연도별 투자 규모 추이</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
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
            max-width: 600px;
            width: 100%;
        }
        .title {
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #3498db;
        }
        canvas {
            max-height: 350px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="title">연도별 투자 규모 추이 (2024-2030)</div>
        <canvas id="trendChart"></canvas>
    </div>

    <script>
        // 연도별 투자 추이 차트
        const trendCtx = document.getElementById('trendChart').getContext('2d');
        new Chart(trendCtx, {
            type: 'line',
            data: {
                labels: ['2024', '2025', '2026', '2027', '2028', '2029', '2030'],
                datasets: [
                    {
                        label: '총 투자액',
                        data: [230, 420, 580, 700, 580, 470, 520],
                        borderColor: '#e74c3c',
                        backgroundColor: 'rgba(231, 76, 60, 0.1)',
                        pointBackgroundColor: '#e74c3c',
                        pointBorderWidth: 3,
                        pointRadius: 6,
                        tension: 0.4,
                        fill: true
                    },
                    {
                        label: '정부 예산',
                        data: [100, 180, 250, 300, 250, 200, 220],
                        borderColor: '#3498db',
                        borderDash: [5, 5],
                        backgroundColor: 'rgba(52, 152, 219, 0.1)',
                        pointBackgroundColor: '#3498db',
                        pointBorderWidth: 2,
                        pointRadius: 5,
                        tension: 0.4
                    },
                    {
                        label: '민간 투자',
                        data: [130, 240, 330, 400, 330, 270, 300],
                        borderColor: '#27ae60',
                        borderDash: [2, 2],
                        backgroundColor: 'rgba(39, 174, 96, 0.1)',
                        pointBackgroundColor: '#27ae60',
                        pointBorderWidth: 2,
                        pointRadius: 5,
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 15,
                            usePointStyle: true
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 750,
                        title: {
                            display: true,
                            text: '투자액 (억원)',
                            font: { size: 14, weight: 'bold' }
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: '연도',
                            font: { size: 14, weight: 'bold' }
                        }
                    }
                }
            }
        });
    </script>
</body>
</html>
        """
        
        html_file = self.output_dir / "budget_trend.html"
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
        """HTML 파일을 PNG로 캡처 - macOS 스크린샷 사용"""
        try:
            # macOS의 Chrome을 사용하여 HTML을 PNG로 변환
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
                
        except subprocess.TimeoutExpired:
            print("Chrome 스크린샷 타임아웃")
            return False
        except Exception as e:
            print(f"HTML to PNG 변환 실패: {e}")
            return False
    
    def generate_all_charts(self):
        """모든 HTML 차트 생성 및 PNG 변환 (개별 차트 포함)"""
        charts_to_generate = [
            # 기존 통합 차트
            ("system_architecture", self.create_system_architecture_html),
            ("market_growth_trends", self.create_market_growth_html),
            ("budget_distribution", self.create_budget_distribution_html),
            # 개별 차트 (캡션 매칭용)
            ("market_growth_line", self.create_market_growth_line_chart_html),
            ("market_growth_regional", self.create_market_growth_regional_chart_html),
            ("budget_pie", self.create_budget_pie_chart_html),
            ("budget_trend", self.create_budget_trend_chart_html)
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
    
    def cleanup(self):
        """정리 작업"""
        pass  # subprocess 방식에서는 특별한 정리 작업이 필요하지 않음

if __name__ == "__main__":
    generator = HTMLChartGenerator()
    
    try:
        print("HTML 기반 차트 생성 시작...")
        results = generator.generate_all_charts()
        
        print("\n=== 생성 결과 ===")
        for chart_name, html_file, png_file in results:
            print(f"{chart_name}:")
            if html_file:
                print(f"  HTML: {html_file}")
            if png_file:
                print(f"  PNG: {png_file}")
            print()
                
        print("모든 HTML 차트 생성이 완료되었습니다!")
        
    finally:
        generator.cleanup()