#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import seaborn as sns
from pathlib import Path

# 한글 폰트 설정
plt.rcParams['font.family'] = ['Arial Unicode MS', 'Malgun Gothic', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def create_market_growth_chart():
    """한국 방산 수출 성장 추이 및 전망 차트 생성"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # 왼쪽: 방산 수출 성장 추이
    years = [2019, 2021, 2023, 2024, 2025, 2027, 2030]
    actual = [45, 93, 140, None, None, None, None]
    target = [None, None, None, 200, None, None, None]
    optimistic = [None, None, None, None, 180, 220, 250]
    baseline = [None, None, None, None, 170, 200, 220]
    conservative = [None, None, None, None, 160, 180, 180]
    
    ax1.plot([2019, 2021, 2023], [45, 93, 140], 'bo-', linewidth=3, markersize=8, label='실적')
    ax1.plot([2024], [200], 'r*', markersize=15, label='2024 목표')
    ax1.plot([2025, 2027, 2030], [180, 220, 250], 'g--', linewidth=2, marker='o', label='최적 시나리오')
    ax1.plot([2025, 2027, 2030], [170, 200, 220], 'orange', linewidth=2, marker='s', label='기준 시나리오')
    ax1.plot([2025, 2027, 2030], [160, 180, 180], 'r:', linewidth=2, marker='^', label='보수 시나리오')
    
    ax1.set_xlabel('연도', fontsize=12)
    ax1.set_ylabel('수출액 (억 달러)', fontsize=12)
    ax1.set_title('한국 방산 수출 성장 추이 및 전망', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    ax1.set_ylim(0, 280)
    
    # 오른쪽: 지역별 시장 성장 전망
    regions = ['아시아태평양', '유럽', '북미', '중동', '기타']
    market_size_2030 = [1280, 1150, 2100, 920, 450]
    growth_rates = [4.2, 3.8, 2.9, 3.5, 2.1]
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
    bars = ax2.barh(regions, market_size_2030, color=colors)
    
    # 성장률 표시
    for i, (bar, rate) in enumerate(zip(bars, growth_rates)):
        width = bar.get_width()
        ax2.text(width/2, bar.get_y() + bar.get_height()/2, 
                f'{rate}% CAGR', ha='center', va='center', fontweight='bold', fontsize=10)
    
    ax2.set_xlabel('2030년 시장 규모 (억 달러)', fontsize=12)
    ax2.set_title('글로벌 방산시장 지역별 성장 전망 (2024-2030)', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    plt.savefig('/Users/dykim/dev/make-docs/images/market_growth_trends.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

def create_budget_distribution():
    """예산 배분 파이차트 및 연도별 투자 그래프"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # 왼쪽: 분야별 투자 배분 파이차트
    tech_areas = ['무인체계', 'AI/빅데이터', '통신기술', '센서/반도체', '기타 신기술']
    investments = [1050, 700, 875, 525, 350]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
    
    wedges, texts, autotexts = ax1.pie(investments, labels=tech_areas, colors=colors, 
                                      autopct='%1.1f%%', startangle=90)
    ax1.set_title('총 투자 3,500억원 분야별 배분', fontsize=14, fontweight='bold')
    
    # 투자액 표시
    for i, (wedge, investment) in enumerate(zip(wedges, investments)):
        texts[i].set_text(f'{tech_areas[i]}\n({investment}억원)')
    
    # 오른쪽: 연도별 투자 규모 추이
    years = [2024, 2025, 2026, 2027, 2028, 2029, 2030]
    total_investment = [230, 420, 580, 700, 580, 470, 520]
    government_investment = [100, 180, 250, 300, 250, 200, 220]
    private_investment = [130, 240, 330, 400, 330, 270, 300]
    
    ax2.plot(years, total_investment, 'ro-', linewidth=3, markersize=8, label='총 투자액')
    ax2.plot(years, government_investment, 'b--', linewidth=2, marker='s', label='정부 예산')
    ax2.plot(years, private_investment, 'g:', linewidth=2, marker='^', label='민간 투자')
    
    ax2.set_xlabel('연도', fontsize=12)
    ax2.set_ylabel('투자액 (억원)', fontsize=12)
    ax2.set_title('연도별 투자 규모 추이 (2024-2030)', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    ax2.set_ylim(0, 750)
    
    # 최고점 표시
    max_year_idx = total_investment.index(max(total_investment))
    ax2.annotate(f'최고점: {years[max_year_idx]}년 {max(total_investment)}억원', 
                xy=(years[max_year_idx], max(total_investment)), 
                xytext=(years[max_year_idx], max(total_investment) + 50),
                arrowprops=dict(arrowstyle='->', color='red'),
                fontsize=10, ha='center')
    
    plt.tight_layout()
    plt.savefig('/Users/dykim/dev/make-docs/images/budget_distribution.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

def create_risk_matrix():
    """리스크 매트릭스 히트맵"""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # 리스크 데이터
    risks = ['핵심기술개발실패', '기술변화대응', '국제정세변화', '환율변동', '예산삭감']
    probability = [3, 2, 3, 2, 2]  # 1:낮음, 2:중간, 3:높음
    impact = [3, 3, 2, 2, 1]  # 1:낮음, 2:중간, 3:높음
    
    # 매트릭스 생성
    matrix = np.zeros((4, 4))
    risk_positions = []
    
    for i, (prob, imp, risk) in enumerate(zip(probability, impact, risks)):
        matrix[4-imp, prob] = 1
        risk_positions.append((prob, imp, risk, i))
    
    # 히트맵 생성
    im = ax.imshow(matrix, cmap='Reds', alpha=0.6)
    
    # 축 설정
    ax.set_xlim(-0.5, 3.5)
    ax.set_ylim(-0.5, 3.5)
    ax.set_xticks([0, 1, 2, 3])
    ax.set_xticklabels(['', '낮음', '중간', '높음'])
    ax.set_yticks([0, 1, 2, 3])
    ax.set_yticklabels(['높음', '중간', '낮음', ''])
    ax.set_xlabel('발생확률', fontsize=14)
    ax.set_ylabel('영향도', fontsize=14)
    ax.set_title('리스크 매트릭스', fontsize=16, fontweight='bold')
    
    # 리스크 포인트 표시
    colors = ['red', 'orange', 'gold', 'lightblue', 'lightgreen']
    for prob, imp, risk, idx in risk_positions:
        ax.scatter(prob, 4-imp, s=500, c=colors[idx], alpha=0.8, edgecolors='black', linewidth=2)
        ax.annotate(risk, (prob, 4-imp), xytext=(5, 5), textcoords='offset points',
                   fontsize=9, ha='left', va='bottom', 
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
    
    # 격자 추가
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/Users/dykim/dev/make-docs/images/risk_matrix.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

if __name__ == "__main__":
    print("차트 생성 시작...")
    create_market_growth_chart()
    print("✓ 시장 성장 차트 생성 완료")
    
    create_budget_distribution()
    print("✓ 예산 배분 차트 생성 완료")
    
    create_risk_matrix()
    print("✓ 리스크 매트릭스 생성 완료")
    
    print("모든 차트 생성이 완료되었습니다!")