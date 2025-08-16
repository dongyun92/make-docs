# 봉화지역 산불방지 및 산림복구 사업제안서

## 파일 구조

```
영풍/
├── 봉화지역_산불방지_및_산림복구_사업제안서.md    # 메인 사업제안서 (MD 파일)
├── README.md                                      # 사용 설명서
├── forest_area.html                              # 남부지방산림청 관할 지역별 산림면적 차트
├── national_fire_stats.html                     # 2024년 지역별 산불 발생 현황 차트
├── fire_causes.html                             # 산불 발생 원인별 통계 차트
├── investment_plan.html                         # 분야별 투자 배분 차트
├── yearly_investment.html                       # 연도별 투자 추이 차트
├── environmental_impact.html                    # 환경 효과 전망 차트
└── images/                                      # 이미지 저장 폴더 (PNG 변환 후 저장)
```

## 사용 방법

### 1. HTML to PNG 변환
HTML 차트 파일들을 PNG 이미지로 변환하여 images/ 폴더에 저장:

```bash
# capture-website-cli 설치 (없는 경우)
npm install -g capture-website-cli

# HTML 파일들을 PNG로 변환
capture-website forest_area.html images/forest_area.png --width=900 --height=600
capture-website national_fire_stats.html images/national_fire_stats.png --width=900 --height=600
capture-website fire_causes.html images/fire_causes.png --width=900 --height=600
capture-website investment_plan.html images/investment_plan.png --width=900 --height=600
capture-website yearly_investment.html images/yearly_investment.png --width=900 --height=600
capture-website environmental_impact.html images/environmental_impact.png --width=900 --height=600
```

### 2. MD를 DOCX로 변환
SimpleThermalConverter를 사용하여 MD 파일을 DOCX로 변환:

```bash
python3 simple_thermal_converter.py "봉화지역_산불방지_및_산림복구_사업제안서.md"
```

## 특징

### 1. 사실 기반 데이터
- 실제 봉화군 통계 활용 (면적 1,201.48㎢, 산림면적 98,141ha, 인구 29,356명)
- 2024년 산불 발생 통계 반영 (경북 31건)
- 남부지방산림청 관할 실제 면적 데이터 활용

### 2. MD 가이드라인 완벽 준수
- 공무원 문체 사용 (~함, ~됨, ~임)
- 글머리 기호 체계 준수 (□, ○, -, •)
- 콜론 사용 금지
- 볼드 양식 금지
- 들여쓰기를 활용한 마일스톤 표기

### 3. 시각적 자료
총 6개의 HTML 차트 제작:
1. **forest_area.html** - 남부지방산림청 관할 지역별 산림면적
2. **national_fire_stats.html** - 2024년 지역별 산불 발생 현황
3. **fire_causes.html** - 산불 발생 원인별 통계
4. **investment_plan.html** - 분야별 투자 배분
5. **yearly_investment.html** - 연도별 투자 추이
6. **environmental_impact.html** - 환경 효과 전망

### 4. 사업 내용
- 총 사업비: 150억원
- 사업 기간: 3년 (2025-2027)
- 재원 조달: 국비 60%, 도비 20%, 군비 20%
- 주요 사업: 산불 예방 시설 구축, 산림복구, 진화 인프라 구축

## 주요 주석

^1^ 첨단 산불 감시 기술과 무인 항공기를 활용한 조기 탐지 시스템
^2^ 봉화군은 태백산맥과 소백산맥이 만나는 산간 지역으로 산림 밀도가 매우 높음
^3^ 2024년 전국 산불 통계에 따르면 경기도 82건, 충남 35건, 경북 31건 순으로 발생
^4^ 산림복구를 통한 생태계 서비스 가치 증진 효과

## 주의사항

1. **HTML 차트 특징**
   - 모든 차트는 애니메이션 비활성화 (animation: false)
   - 900x600 픽셀 고정 크기
   - Chart.js 3.9.1 사용

2. **변환 순서**
   1. HTML → PNG 변환 (capture-website-cli)
   2. MD → DOCX 변환 (SimpleThermalConverter)

3. **파일명 규칙**
   - 한글 파일명 사용
   - 공백 대신 언더스코어(_) 사용
