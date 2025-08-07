#!/usr/bin/env python3
"""
간트차트 생성 스크립트
"""

import plotly.figure_factory as ff
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd

def create_gantt_chart():
    """대드론 방어 시스템 프로젝트 간트차트 생성"""
    
    # 프로젝트 일정 데이터 (2024-2027)
    tasks = [
        # 1단계: 핵심 기술 개발 (2024-2025)
        {"Task": "1단계: 핵심기술개발", "Start": "2024-03-01", "Finish": "2024-12-31", "Resource": "기술개발팀"},
        {"Task": "  - AI 탐지 알고리즘 개발", "Start": "2024-03-01", "Finish": "2024-08-31", "Resource": "AI팀"},
        {"Task": "  - 프로토타입 제작", "Start": "2024-09-01", "Finish": "2024-12-31", "Resource": "개발팀"},
        
        # 2단계: 시스템 통합 개발 (2025-2026)  
        {"Task": "2단계: 시스템통합개발", "Start": "2025-01-01", "Finish": "2025-12-31", "Resource": "통합팀"},
        {"Task": "  - 실용화 기술 개발", "Start": "2025-01-01", "Finish": "2025-06-30", "Resource": "개발팀"},
        {"Task": "  - 실외 환경 테스트", "Start": "2025-07-01", "Finish": "2025-12-31", "Resource": "테스트팀"},
        
        # 3단계: 실전 배치 준비 (2026-2027)
        {"Task": "3단계: 실전배치준비", "Start": "2026-01-01", "Finish": "2026-12-31", "Resource": "배치팀"},
        {"Task": "  - 제품화 기술 완성", "Start": "2026-01-01", "Finish": "2026-06-30", "Resource": "제품팀"},
        {"Task": "  - 양산 체계 구축", "Start": "2026-07-01", "Finish": "2026-12-31", "Resource": "생산팀"},
        
        # 주요 마일스톤
        {"Task": "마일스톤: 사업시작", "Start": "2024-03-01", "Finish": "2024-03-01", "Resource": "마일스톤"},
        {"Task": "마일스톤: 1단계완료(TRL6)", "Start": "2024-12-31", "Finish": "2024-12-31", "Resource": "마일스톤"},
        {"Task": "마일스톤: 2단계완료(시제품)", "Start": "2025-12-31", "Finish": "2025-12-31", "Resource": "마일스톤"},
        {"Task": "마일스톤: 사업완료(양산준비)", "Start": "2026-12-31", "Finish": "2026-12-31", "Resource": "마일스톤"},
    ]
    
    # 색상 매핑
    colors = {
        "기술개발팀": "#2E86AB",
        "AI팀": "#A23B72", 
        "개발팀": "#F18F01",
        "통합팀": "#C73E1D",
        "테스트팀": "#6A994E",
        "배치팀": "#577590",
        "제품팀": "#F2CC8F",
        "생산팀": "#81B29A",
        "마일스톤": "#E07A5F"
    }
    
    # 간트차트 생성
    fig = ff.create_gantt(
        tasks, 
        colors=colors, 
        index_col='Resource', 
        show_colorbar=True,
        group_tasks=True,
        showgrid_x=True, 
        showgrid_y=True,
        title="대드론 방어 시스템 개발 프로젝트 일정"
    )
    
    # 레이아웃 설정
    fig.update_layout(
        title={
            'text': "대드론 방어 시스템 개발 프로젝트 간트차트",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'family': 'Arial, sans-serif'}
        },
        xaxis_title="기간 (2024-2027)",
        font=dict(family="Arial, sans-serif", size=12),
        height=600,
        width=1000,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    # X축 설정 (분기별 표시)
    fig.update_xaxes(
        tickmode='linear',
        tick0='2024-01-01',
        dtick='M3',  # 3개월 간격
        tickformat='%Y-%m',
        tickangle=45
    )
    
    # HTML 파일로 저장
    fig.write_html("images/gantt_schedule.html")
    
    # PNG로도 저장 (가능한 경우)
    try:
        fig.write_image("images/gantt_schedule.png", width=1000, height=600)
        print("✅ 간트차트 PNG 파일 생성 완료")
    except:
        print("⚠️ PNG 생성 실패 - kaleido 패키지 필요. HTML만 생성됨")
    
    print("✅ 간트차트 HTML 파일 생성 완료: images/gantt_schedule.html")

if __name__ == "__main__":
    create_gantt_chart()