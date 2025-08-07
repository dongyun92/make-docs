#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle
import numpy as np

# 한글 폰트 설정
plt.rcParams['font.family'] = ['Arial Unicode MS', 'AppleGothic', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def create_swot_matrix():
    """SWOT 분석 매트릭스 생성"""
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # SWOT 영역 정의
    strengths = [
        "• 세계 최고 반도체 기술력 (60% 점유율)",
        "• 5G 상용화 세계 최초",
        "• 조선 세계 1위",
        "• K-방산 브랜드 인지도 상승",
        "• 정부 강력한 정책 지원"
    ]
    
    weaknesses = [
        "• 핵심부품 해외의존 (정밀센서 80%)",
        "• 중소기업 기술력 격차",
        "• 국방R&D 민수전환률 저조 (30%)",
        "• 국제표준 대응 미흡"
    ]
    
    opportunities = [
        "• 글로벌 방산시장 성장 (3.1% CAGR)",
        "• 아태지역 급성장 (4.2% CAGR)",
        "• 무인체계 시장 급성장 (2배 확대)",
        "• 신흥국 수요 증가",
        "• 민수전환 기회"
    ]
    
    threats = [
        "• 미-중 기술패권 경쟁 심화",
        "• 수출통제 강화 (ITAR, EAR)",
        "• 경쟁국 정부지원 확대",
        "• 글로벌 공급망 재편 위험"
    ]
    
    # 배경 색상 설정
    colors = {
        'S': '#E8F5E8',  # 연한 초록
        'W': '#FFE8E8',  # 연한 빨강
        'O': '#E8E8FF',  # 연한 파랑
        'T': '#FFF8E8'   # 연한 노랑
    }
    
    # SWOT 사분면 그리기
    # Strengths (좌상)
    rect_s = Rectangle((0, 0.5), 0.5, 0.5, facecolor=colors['S'], edgecolor='black', linewidth=2)
    ax.add_patch(rect_s)
    
    # Weaknesses (우상)
    rect_w = Rectangle((0.5, 0.5), 0.5, 0.5, facecolor=colors['W'], edgecolor='black', linewidth=2)
    ax.add_patch(rect_w)
    
    # Opportunities (좌하)
    rect_o = Rectangle((0, 0), 0.5, 0.5, facecolor=colors['O'], edgecolor='black', linewidth=2)
    ax.add_patch(rect_o)
    
    # Threats (우하)
    rect_t = Rectangle((0.5, 0), 0.5, 0.5, facecolor=colors['T'], edgecolor='black', linewidth=2)
    ax.add_patch(rect_t)
    
    # 제목 추가
    ax.text(0.25, 0.95, 'Strengths (강점)', ha='center', va='top', fontsize=14, fontweight='bold')
    ax.text(0.75, 0.95, 'Weaknesses (약점)', ha='center', va='top', fontsize=14, fontweight='bold')
    ax.text(0.25, 0.45, 'Opportunities (기회)', ha='center', va='top', fontsize=14, fontweight='bold')
    ax.text(0.75, 0.45, 'Threats (위협)', ha='center', va='top', fontsize=14, fontweight='bold')
    
    # 텍스트 추가
    def add_text_list(x, y_start, text_list, box_height=0.4):
        y_step = box_height / (len(text_list) + 1)
        for i, text in enumerate(text_list):
            ax.text(x, y_start - (i + 1) * y_step, text, ha='center', va='center', 
                   fontsize=9, wrap=True)
    
    add_text_list(0.25, 0.9, strengths)
    add_text_list(0.75, 0.9, weaknesses)
    add_text_list(0.25, 0.4, opportunities)
    add_text_list(0.75, 0.4, threats)
    
    # 전략 방향 표시 (하단)
    strategy_text = """
전략 방향:
SO: 강점 기반 기회 활용 → 핵심기술 해외진출 가속화
WO: 약점 보완을 통한 기회 포착 → 중소기업 역량강화
ST: 강점 활용 위협 대응 → 기술주권 확보 및 표준화 선도
WT: 약점 보완 위협 최소화 → 공급망 다변화 및 자립도 제고
    """
    
    ax.text(0.5, -0.15, strategy_text, ha='center', va='top', fontsize=10,
           bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgray', alpha=0.8))
    
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.25, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('첨단 민군 혁신 지원 시스템 SWOT 분석', fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig('/Users/dykim/dev/make-docs/images/swot_analysis.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

if __name__ == "__main__":
    create_swot_matrix()
    print("✓ SWOT 분석 매트릭스 생성 완료")