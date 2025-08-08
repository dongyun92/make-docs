# AI 사업계획서 작성 및 시각화 생성 프롬프트

## 🎯 미션 개요
사업계획서 템플릿을 참고하여 완전한 사업계획서를 작성하고, 필요한 시각화 자료를 HTML 차트로 생성한다. 사용자는 GUI에서 원하는 차트들을 선택하여 최종 DOCX 문서에 반영할 수 있다.

## 📋 작업 워크플로우

### 1단계: 사업계획서 MD 작성
**템플릿 기반 문서 작성:**
- `사업계획서_템플릿.md` 참고하여 구조 유지
- MD파일 작성 가이드라인 100% 준수
- 시각화가 필요한 위치에 **파일명으로 이미지 참조**

**예시:**
```markdown
## 2.3 시장 전망

국내 RWSL 시장은 연평균 15.2% 성장이 예상됨

![시장 전망](images/market_forecast_chart.png)
<그림 3> 글로벌 RWSL 시장 규모 전망 (2024-2030)

분야별 투자 현황은 다음과 같음

![투자 배분](images/investment_allocation_chart.png)  
<그림 4> 분야별 투자 배분 계획
```

### 2단계: HTML 시각화 차트 생성
**Chart.js 기반 고품질 차트 제작:**

```javascript
// 필수 설정 (애니메이션 제거)
options: {
    animation: false,  // 🚨 필수!
    responsive: true,
    maintainAspectRatio: false,
    // ... 기타 설정
}
```

**표준 HTML 템플릿:**
```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>차트 제목</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {
            margin: 0;
            padding: 20px;
            width: 900px;
            height: 600px;
            font-family: 'Malgun Gothic', sans-serif;
            background: white;
        }
        .chart-container {
            height: 500px;
            background: white;
            padding: 20px;
        }
    </style>
</head>
<body>
    <div class="chart-title">차트 제목</div>
    <div class="chart-container">
        <canvas id="chartId"></canvas>
    </div>
    <script>
        // Chart.js 코드
        // animation: false 필수!
    </script>
</body>
</html>
```

### 3단계: 파일명 매칭 규칙
**MD 이미지 참조와 HTML 파일명 일치:**

| MD 파일 이미지 참조 | HTML 파일명 | 설명 |
|-------------------|-------------|------|
| `![시장전망](images/market_forecast_chart.png)` | `market_forecast_chart.html` | 시장 전망 차트 |
| `![투자배분](images/investment_allocation.png)` | `investment_allocation.html` | 투자 배분도 |
| `![로드맵](images/project_roadmap_chart.png)` | `project_roadmap_chart.html` | 프로젝트 로드맵 |

**파일명 규칙:**
- 영문 소문자 사용
- 단어 간 언더스코어(_) 사용
- `.html` 확장자로 차트 생성
- `.png` 참조는 MD에서만 사용 (변환시 자동 매칭)

### 4단계: 차트 유형별 예시

**1) 시장 성장 추이 (Line Chart)**
```javascript
type: 'line',
data: {
    labels: ['2024', '2025', '2026', '2027', '2028'],
    datasets: [{
        label: '시장 규모 (억원)',
        data: [1200, 1850, 2640, 3420, 4500],
        borderColor: '#3498db',
        backgroundColor: 'rgba(52, 152, 219, 0.1)',
        borderWidth: 3
    }]
}
```

**2) 투자 배분 (Pie Chart)**  
```javascript
type: 'pie',
data: {
    labels: ['R&D', '인프라', '인력', '기타'],
    datasets: [{
        data: [40, 30, 20, 10],
        backgroundColor: ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
    }]
}
```

**3) 로드맵 (Horizontal Bar)**
```javascript
type: 'bar',
options: {
    indexAxis: 'y',
    // ...
}
```

## 🎨 시각화 생성 가이드

### 필수 차트 유형들
□ **시장 분석**: 시장 규모, 성장률, 경쟁사 현황
  ○ Line Chart: 시장 성장 추이  
  ○ Bar Chart: 경쟁사 비교
  ○ Pie Chart: 시장 점유율

□ **기술 분석**: 기술 수준, 개발 계획
  ○ Radar Chart: 기술 역량 비교
  ○ Gantt Chart: 개발 일정

□ **사업 계획**: 추진 전략, 조직, 일정
  ○ Organization Chart: 추진 조직
  ○ Timeline: 추진 일정
  ○ Flowchart: 업무 프로세스

□ **투자 계획**: 투자 규모, 재원 조달
  ○ Stacked Bar: 연도별 투자액
  ○ Pie Chart: 투자 배분
  ○ Waterfall: 자금 흐름

□ **기대 효과**: 경제적/사회적 효과
  ○ Area Chart: 누적 효과
  ○ Comparison Chart: Before/After
  ○ ROI Chart: 투자 회수 분석

### 데이터 현실성 확보
**실제적인 데이터 사용:**
- 정부 통계, 산업 보고서 수준의 합리적 수치
- 연도별 성장률 10-20% 내외 (과도하지 않게)
- 투자 규모는 사업 성격에 맞는 적정 수준
- 조직 구성은 실제 기업/기관 수준

## 🔧 기술적 요구사항

### HTML 차트 최적화
```css
/* 필수 스타일 */
body {
    width: 900px;        /* 고정 너비 */
    height: 600px;       /* 고정 높이 */
    font-family: 'Malgun Gothic', sans-serif;  /* 한글 폰트 */
    background: white;    /* 흰색 배경 */
}
.chart-container {
    height: 500px;       /* 차트 영역 고정 */
}
```

### Chart.js 필수 옵션
```javascript
options: {
    animation: false,              // 애니메이션 비활성화
    responsive: true,              // 반응형
    maintainAspectRatio: false,    // 비율 고정 해제
    plugins: {
        legend: {
            labels: {
                font: { family: 'Malgun Gothic' }  // 한글 폰트
            }
        }
    },
    scales: {
        x: {
            title: { 
                font: { family: 'Malgun Gothic' }
            }
        },
        y: {
            title: {
                font: { family: 'Malgun Gothic' }
            }
        }
    }
}
```

## 📁 파일 구조 및 네이밍

### 생성할 파일들
```
/images/
├── market_forecast_chart.html          # 시장 전망
├── investment_allocation_chart.html    # 투자 배분  
├── project_roadmap_chart.html         # 프로젝트 로드맵
├── technology_gap_analysis.html       # 기술 격차 분석
├── economic_benefit_chart.html        # 경제적 효과
├── employment_effect_chart.html       # 고용 창출 효과
└── ... (사업 특성에 따라 추가)
```

### MD 파일에서의 참조
```markdown
![시장 전망](images/market_forecast_chart.png)
<그림 1> 글로벌 시장 규모 전망 (2024-2030)

![투자 배분](images/investment_allocation_chart.png)
<그림 2> 분야별 투자 배분 계획
```

## ✅ 최종 체크리스트

### MD 파일 검증
- [ ] 템플릿 구조 준수
- [ ] 불릿포인트 계층구조 (□→○→-→•)  
- [ ] 공무원 문체 사용 ("~함", "~됨")
- [ ] 이미지 참조 파일명과 HTML 파일명 일치
- [ ] 캡션 형식 준수 (`<그림 N> 설명`)

### HTML 차트 검증  
- [ ] `animation: false` 설정
- [ ] 900x600 픽셀 고정 크기
- [ ] 한글 폰트 적용
- [ ] 차트 데이터의 현실성
- [ ] 파일명과 MD 참조 일치

### 사용자 경험 최적화
- [ ] GUI에서 선택 가능한 차트들
- [ ] 각 차트의 목적과 내용 명확
- [ ] 전체적인 사업계획서 완성도
- [ ] 시각적 일관성 및 전문성

## 🎯 성공 기준

**완성된 결과물:**
1. **완전한 사업계획서 MD 파일** (템플릿 기반)
2. **10-20개 고품질 HTML 차트** (애니메이션 없음)
3. **파일명 매칭 완벽** (MD ↔ HTML 일치)
4. **GUI 선택 가능** (사용자가 원하는 차트만 변환)
5. **전문적 품질** (실제 사업에 사용 가능한 수준)

**최종 사용자 워크플로우:**
1. AI가 생성한 MD 파일 + HTML 차트들 확인
2. GUI에서 필요한 차트들만 선택
3. "변환" 버튼 클릭
4. 선택된 차트들이 PNG로 변환되어 DOCX에 삽입
5. 완성된 사업계획서 DOCX 파일 획득

---

**이 프롬프트를 따르면 사용자가 GUI에서 선택적으로 차트를 변환할 수 있는 완전한 사업계획서 시스템이 구축됩니다.**