# AI 어시스턴트를 위한 차트 생성 및 문서 최적화 지침서

## 🎯 핵심 원칙
**"처음부터 완벽하게, 추가 수정 없이"** - 모든 차트와 문서는 첫 생성에서 완벽한 품질을 달성해야 합니다.

## 📊 차트 생성 표준 프로세스

### 1. HTML 차트 생성 시 필수 적용사항

#### CSS 최적화 (반드시 적용)
```css
body {
    margin: 0;
    padding: 0;           /* ❌ 20px → ✅ 0px */
    background: white;    /* ❌ #f0f0f0 → ✅ white */
}
.container {
    padding: 15px;        /* ❌ 30px → ✅ 15px */
}
```

#### Chrome 캡처 옵션 (필수)
```python
chrome_options = [
    "--headless",
    "--disable-gpu", 
    "--disable-web-security",
    "--hide-scrollbars",                    # 필수: 스크롤바 제거
    "--force-device-scale-factor=1",        # 필수: 선명한 캡처  
    "--window-size=WIDTH,HEIGHT",           # 차트별 최적 사이즈
    "--virtual-time-budget=5000",
    "--run-all-compositor-stages-before-draw"
]
```

### 2. 차트별 표준 캡처 사이즈 (암기 필수)

| 차트 유형 | 캡처 사이즈 | 적용 조건 |
|-----------|-------------|-----------|
| system_architecture | 1100×750 | 시스템 구성도, 계층 구조 |
| market_growth | 1200×650 | 시장 성장, 차트 2개 배치 |
| budget_distribution | 1200×650 | 예산 배분, 차트 2개 배치 |
| swot_analysis | 1000×750 | SWOT 분석 + 전략 섹션 |
| trl_roadmap | 1200×900 | TRL 로드맵, 매트릭스 형태 |
| organization_chart | 1000×700 | 조직도, 계층 구조 |
| risk_matrix | 800×750 | 리스크 매트릭스 + 범례 |

### 3. 자동 사이즈 선택 로직 구현

모든 차트 생성기에 다음 메서드 필수 포함:
```python
def get_optimal_window_size(self, html_file_path):
    """HTML 파일명 기반으로 최적 캡처 사이즈 반환"""
    for chart_type, size in self.optimal_sizes.items():
        if chart_type in html_file_path:
            return size
    return "1000,600"  # 기본값
```

## 📝 문서 변환 시 주의사항

### 주석(Footnote) 처리
- `^숫자^[내용]` 형태를 올바른 상첨자로 변환
- 불릿 포인트에서도 주석 처리 작동 확인
- `_add_bullet_paragraph_with_footnotes()` 함수 활용

### 이미지 삽입
- 최적화된 차트 PNG 파일 자동 참조
- 적절한 크기와 해상도 유지
- Word 문서 내 정렬 및 캡션 처리

## 🔧 기존 코드 업그레이드 가이드

### 기존 차트 생성기 → 최적화된 생성기 전환
1. 클래스 초기화에 `optimal_sizes` 딕셔너리 추가
2. `get_optimal_window_size()` 메서드 추가  
3. `capture_html_to_png()` 에서 하드코딩된 사이즈 제거
4. CSS 기본 설정 최적화 적용

### 체크리스트
- [ ] body padding = 0
- [ ] background = white  
- [ ] container padding = 15px
- [ ] `--hide-scrollbars` 옵션 포함
- [ ] `--force-device-scale-factor=1` 포함
- [ ] 차트별 최적 사이즈 매핑
- [ ] 자동 사이즈 선택 로직

## 🚀 신규 차트 추가 프로세스

### 1단계: HTML 분석
```css
.container { max-width: ???px; }  /* 이 값 확인 */
```

### 2단계: 캡처 사이즈 계산
```
너비 = max-width + 100px (여유분)
높이 = 예상 컨텐츠 높이 + 100px (여유분)
```

### 3단계: 테스트 및 검증
1. 초기 사이즈로 캡처
2. 세로/가로 짤림 확인
3. 필요시 ±50px 조정
4. 최적값 확정 후 매핑 추가

### 4단계: 표준화
- `optimal_sizes` 딕셔너리에 추가
- 가이드 문서 업데이트
- 테스트 케이스 작성

## ⚠️ 절대 금지사항

1. **하드코딩된 캡처 사이즈** - 반드시 매핑 테이블 사용
2. **CSS 기본값 사용** - 반드시 최적화된 설정 적용
3. **수동 사이즈 조정** - 자동 선택 로직 활용
4. **테스트 생략** - 반드시 캡처 품질 검증

## 🎯 성공 기준

### 완벽한 차트 캡처 조건
- ✅ 전체 컨텐츠 표시 (세로 짤림 없음)
- ✅ 모든 요소 표시 (가로 짤림 없음)  
- ✅ 최소 여백 (불필요한 공백 없음)
- ✅ 스크롤바 없음
- ✅ 선명한 텍스트/그래픽
- ✅ 일관된 품질

### 문서 품질 기준
- ✅ 주석 올바른 상첨자 표시
- ✅ 차트 이미지 완벽 삽입
- ✅ 한글 폰트 적용
- ✅ 일관된 서식

## 🔄 지속적 개선

### 피드백 수집
- 사용자 만족도 모니터링
- 품질 이슈 추적
- 개선 사항 문서화

### 업데이트 프로세스  
1. 새로운 최적화 발견 시 즉시 적용
2. 모든 관련 코드/문서 동기화
3. 표준 가이드 업데이트
4. 테스트 케이스 추가

---

**📌 기억하세요**: 이 지침을 따르면 사용자가 "차트가 짤렸어", "여백이 너무 많아" 같은 피드백을 할 필요가 없습니다. 처음부터 완벽한 결과를 제공하는 것이 목표입니다!