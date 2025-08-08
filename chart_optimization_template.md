# Chrome 캡처 최적화 HTML 차트 생성 요청 템플릿

## 기본 요구사항

다음 18개 RWSL 프로젝트 차트를 Chrome 900x600 캡처에 최적화하여 재생성해주세요:

1. rwsl_traffic_growth_chart.html - 국내 주요공항 항공교통량 증가 추이
2. rwsl_system_architecture.html - RWSL 통합 시스템 구성도  
3. rwsl_global_adoption_chart.html - 글로벌 드론탐지 시장 성장률
4. rwsl_budget_pie_chart.html - RWSL 예산 배분 현황
5. rwsl_budget_trend_chart.html - 연도별 예산 변화 추이
6. rwsl_organization_chart.html - RWSL 조직구조도
7. rwsl_risk_matrix.html - 위험도 매트릭스 분석
8. rwsl_trl_roadmap.html - 기술성숙도 로드맵
9. rwsl_swot_analysis.html - SWOT 분석 차트
10. rwsl_market_growth_line.html - 시장 성장률 선형 차트
11. rwsl_market_growth_regional.html - 지역별 시장 성장률
12. rwsl_technology_comparison.html - 기술 비교 분석
13. rwsl_cost_analysis.html - 비용 분석 차트
14. rwsl_timeline_gantt.html - 프로젝트 타임라인
15. rwsl_performance_metrics.html - 성능 지표 대시보드
16. rwsl_competitive_analysis.html - 경쟁사 분석
17. rwsl_revenue_projection.html - 수익 예측 차트
18. rwsl_implementation_phases.html - 구현 단계별 계획

## 캡처 최적화 기술 요구사항

### 1. 크롬 헤들리스 캡처 설정
```
--headless --disable-gpu --hide-scrollbars --force-device-scale-factor=1 --window-size=900,600
```

### 2. Body 스타일 최적화
```css
body {
    margin: 0;
    padding: 20px;
    width: 860px;  /* 900px - (20px * 2) */
    height: 560px; /* 600px - (20px * 2) */
    overflow: hidden;
    font-family: 'Malgun Gothic', sans-serif;
    background: white;
    box-sizing: border-box;
}
```

### 3. 차트 컨테이너 최적화
- **정확한 크기**: 개발자 도구 → Elements → Computed에서 실제 렌더링 크기 확인
- **고정 높이**: body height 560px 내에 모든 요소가 들어가도록 조정
- **오버플로우 방지**: overflow: hidden으로 잘림 방지
- **여백 계산**: 제목, 범례, 축 레이블을 포함한 전체 차트가 560px 안에 완전히 표시

### 4. 폰트 및 텍스트 최적화
- **한글 폰트**: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif 순서로 지정
- **폰트 크기**: 제목 16px, 축 레이블 12px, 범례 10px (가독성 확보)
- **텍스트 색상**: 충분한 대비율로 가독성 보장

### 5. 색상 및 스타일 최적화
- **고대비 색상**: 인쇄 및 프레젠테이션에 적합한 색상 팔레트
- **선명한 테두리**: 차트 요소 구분이 명확하도록
- **배경**: 흰색 배경으로 통일

## 검증 방법

생성된 각 HTML 파일에 대해:
1. Chrome 개발자 도구에서 Elements → body → Computed 크기 확인
2. 실제 캡처 테스트로 잘림 없음 확인
3. 900x600 PNG 이미지로 저장하여 품질 검증

## 파일 명명 규칙

각 파일은 기존 이름 유지:
- `rwsl_[목적]_chart.html` 형식
- 동일한 디렉토리 (`images/`) 에 저장

이 템플릿에 따라 18개 차트를 모두 재생성해주시면, Chrome 헤들리스 캡처에 최적화된 고품질 이미지를 얻을 수 있습니다.