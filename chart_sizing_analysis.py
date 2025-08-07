#!/usr/bin/env python3
"""
고정 크기 레이아웃에서 콘텐츠 오버플로우/언더플로우 문제 분석 도구
"""

import os
import re
from pathlib import Path

def analyze_chart_layouts():
    """각 HTML 차트의 레이아웃 구조와 콘텐츠 밀도를 분석"""
    
    charts_dir = Path("images")
    analysis_results = {}
    
    chart_files = [
        "system_architecture.html",
        "trl_roadmap.html", 
        "organization_chart.html",
        "risk_matrix.html",
        "swot_analysis.html",
        "gantt_schedule.html",
        "budget_pie.html",
        "budget_trend.html",
        "market_growth_line.html",
        "market_growth_regional.html"
    ]
    
    for chart_file in chart_files:
        file_path = charts_dir / chart_file
        if file_path.exists():
            chart_name = chart_file.replace('.html', '')
            analysis_results[chart_name] = analyze_single_chart(file_path)
    
    print_analysis_report(analysis_results)
    return analysis_results

def analyze_single_chart(file_path):
    """개별 차트 HTML 파일 분석"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    analysis = {
        'file_size': len(content),
        'content_density': 'unknown',
        'layout_type': 'unknown',
        'potential_overflow_risk': 'low',
        'content_elements': 0,
        'text_density': 'unknown',
        'grid_complexity': 'simple'
    }
    
    # 콘텐츠 요소 개수 계산
    div_count = len(re.findall(r'<div', content))
    text_content = re.findall(r'>[^<]+<', content)
    text_length = sum(len(text.strip(' ><')) for text in text_content if text.strip(' ><'))
    
    analysis['content_elements'] = div_count
    analysis['total_text_length'] = text_length
    
    # 레이아웃 타입 감지
    if 'grid-template-columns' in content:
        grid_matches = re.findall(r'grid-template-columns:\s*([^;]+)', content)
        if grid_matches:
            max_columns = max(len(re.findall(r'1fr|repeat\((\d+)', match)) for match in grid_matches)
            analysis['grid_complexity'] = f"{max_columns} columns max"
            analysis['layout_type'] = 'css_grid'
    elif 'display: flex' in content:
        analysis['layout_type'] = 'flexbox'
    else:
        analysis['layout_type'] = 'block'
    
    # 콘텐츠 밀도 평가
    if text_length > 2000:
        analysis['content_density'] = 'high'
        analysis['potential_overflow_risk'] = 'high'
    elif text_length > 1000:
        analysis['content_density'] = 'medium' 
        analysis['potential_overflow_risk'] = 'medium'
    else:
        analysis['content_density'] = 'low'
        analysis['potential_overflow_risk'] = 'low'
        
    # 텍스트 밀도
    if div_count > 0:
        text_per_element = text_length / div_count
        if text_per_element > 50:
            analysis['text_density'] = 'high'
        elif text_per_element > 20:
            analysis['text_density'] = 'medium'
        else:
            analysis['text_density'] = 'low'
    
    # 특정 패턴 감지
    if 'matrix' in content.lower():
        analysis['chart_type'] = 'matrix'
    elif 'roadmap' in content.lower() or 'trl' in content.lower():
        analysis['chart_type'] = 'roadmap'
    elif 'swot' in content.lower():
        analysis['chart_type'] = 'swot'
    elif 'org' in content.lower():
        analysis['chart_type'] = 'organization'
    else:
        analysis['chart_type'] = 'other'
        
    return analysis

def print_analysis_report(results):
    """분석 결과 리포트 출력"""
    
    print("=" * 80)
    print("📊 고정 크기 레이아웃 콘텐츠 분석 리포트")
    print("=" * 80)
    
    # 오버플로우 위험 순으로 정렬
    risk_order = {'high': 3, 'medium': 2, 'low': 1}
    sorted_charts = sorted(results.items(), 
                          key=lambda x: risk_order.get(x[1]['potential_overflow_risk'], 0), 
                          reverse=True)
    
    for chart_name, analysis in sorted_charts:
        risk_level = analysis['potential_overflow_risk']
        risk_emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(risk_level, '⚪')
        
        print(f"\n{risk_emoji} {chart_name.upper()}")
        print(f"   레이아웃 타입: {analysis['layout_type']}")
        print(f"   콘텐츠 밀도: {analysis['content_density']}")
        print(f"   텍스트 밀도: {analysis['text_density']}")
        print(f"   그리드 복잡도: {analysis['grid_complexity']}")
        print(f"   총 텍스트 길이: {analysis['total_text_length']}자")
        print(f"   콘텐츠 요소: {analysis['content_elements']}개")
        print(f"   오버플로우 위험: {risk_level.upper()}")
        
        # 개선 제안
        if risk_level == 'high':
            print("   💡 개선 제안:")
            if analysis['text_density'] == 'high':
                print("      - 텍스트 길이 단축 또는 폰트 크기 축소")
            if analysis['content_density'] == 'high':
                print("      - 콘텐츠 요소 수 감소 또는 레이아웃 최적화")
            if 'columns' in analysis['grid_complexity']:
                print("      - 그리드 열 수 감소 검토")
    
    print("\n" + "=" * 80)
    print("📋 요약 분석")
    print("=" * 80)
    
    high_risk = [name for name, data in results.items() if data['potential_overflow_risk'] == 'high']
    medium_risk = [name for name, data in results.items() if data['potential_overflow_risk'] == 'medium']
    low_risk = [name for name, data in results.items() if data['potential_overflow_risk'] == 'low']
    
    print(f"🔴 고위험 차트 ({len(high_risk)}개): {', '.join(high_risk) if high_risk else '없음'}")
    print(f"🟡 중위험 차트 ({len(medium_risk)}개): {', '.join(medium_risk) if medium_risk else '없음'}")  
    print(f"🟢 저위험 차트 ({len(low_risk)}개): {', '.join(low_risk) if low_risk else '없음'}")
    
    print("\n🎯 주요 발견사항:")
    
    # 가장 복잡한 차트
    most_complex = max(results.items(), key=lambda x: x[1]['total_text_length'])
    print(f"   - 가장 복잡한 차트: {most_complex[0]} ({most_complex[1]['total_text_length']}자)")
    
    # 레이아웃 타입별 분포
    layout_types = {}
    for data in results.values():
        layout_type = data['layout_type']
        layout_types[layout_type] = layout_types.get(layout_type, 0) + 1
    
    print(f"   - 레이아웃 타입 분포: {dict(layout_types)}")
    
    print("\n💡 전반적 개선 방안:")
    print("   1. 고위험 차트는 텍스트 내용 축소 또는 폰트 크기 조정")
    print("   2. CSS Grid 복잡도가 높은 차트는 열 수 감소 검토")  
    print("   3. 1200x800 캔버스에 최적화된 콘텐츠 밀도 유지")
    print("   4. 반응형 텍스트 크기 및 적응형 레이아웃 적용")

if __name__ == "__main__":
    analyze_chart_layouts()