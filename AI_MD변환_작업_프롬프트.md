# AI를 위한 MD to DOCX 변환 작업 프롬프트

## 🎯 핵심 미션
마크다운(MD) 파일을 고품질 Word 문서(DOCX)로 변환하고, 필요시 HTML 차트를 생성하여 완전한 비즈니스 문서를 제작한다.

## ✅ 검증된 성공 아키텍처

### 1. 변환기 선택 (절대 준수)
```bash
# ✅ 반드시 사용할 것
python3 simple_thermal_converter.py "파일명.md"

# ❌ 절대 사용 금지 (변환 중단/품질 문제)
- HTMLBasedConverter
- enhanced_converter.py  
- GUI 기반 변환기
```

### 2. 핵심 성공 요인들
- **계층적 들여쓰기**: □(0") → ○(0.1") → -(0.2") → •(0.3")
- **기호 보존**: MD 원본 기호를 Word에서 그대로 유지
- **전문 도구**: capture-website-cli로 HTML→PNG 변환
- **애니메이션 제거**: Chart.js에서 `animation: false` 필수

## 📋 표준 작업 순서

### Phase 1: MD 파일 준비
1. **가이드라인 준수 확인**
   - 불릿포인트: □ → ○ → - → • 계층 구조
   - 공무원 문체: "~함", "~됨", "~임" 
   - 볼드 양식 금지
   - 콜론(:) 사용 금지

2. **이미지 참조 검증**
   - `![설명](images/파일명.png)` 형식
   - `<그림 N> 캡션` 형식

### Phase 2: HTML 차트 처리 (필요시)
1. **차트 생성**
   ```javascript
   options: {
       animation: false,  // 🚨 필수 설정
       responsive: true,
       maintainAspectRatio: false
   }
   ```

2. **최적화 설정**
   - 해상도: 900x600 픽셀 고정
   - 폰트: 'Malgun Gothic' 또는 시스템 기본

3. **PNG 변환**
   ```bash
   # capture-website-cli 사용 권장
   capture-website 파일.html --output 이미지.png --width 900 --height 600
   ```

### Phase 3: DOCX 변환
```bash
# 단일 명령으로 변환 수행
python3 simple_thermal_converter.py "문서명.md"
```

### Phase 4: 품질 검증
- 들여쓰기 정상 적용 확인
- 이미지 표시 상태 확인  
- 캡션 및 번호 확인
- 파일 크기 적정성 확인 (차트 포함시 2-3MB 수준)

## 🚨 문제 해결 가이드

### 변환이 멈추는 경우
- **원인**: HTMLBasedConverter 사용
- **해결**: SimpleThermalConverter 직접 사용

### 들여쓰기가 안되는 경우  
- **원인**: 기호 인식 실패 또는 들여쓰기 로직 오류
- **해결**: MD 파일의 공백 및 기호 확인

### 이미지가 깨지는 경우
- **원인**: 애니메이션 진행중 캡처 또는 도구 한계
- **해결**: 
  1. HTML에서 `animation: false` 확인
  2. capture-website-cli로 재캡처
  3. 기존 PNG 파일 삭제 후 재생성

### 차트 크기가 이상한 경우
- **원인**: Chart.js `maintainAspectRatio` 설정 문제
- **해결**: HTML 컨테이너 크기 고정 (900x560)

## 💡 프로 팁

### 효율적인 작업 방법
1. **TodoWrite 도구 활용**: 복잡한 작업은 단계별로 계획
2. **병렬 도구 호출**: 여러 파일 처리시 배치 실행
3. **중간 검증**: 각 단계마다 결과물 확인

### 품질 보장
- 파일 크기로 이미지 포함 여부 판단
- ls 명령으로 최종 파일 확인
- 사용자 요구사항과 결과물 대조

### 문제 예방
- 기존 파일 덮어쓰기 전 백업 고려
- 변환 전 dependencies 확인
- 에러 발생시 단계별 디버깅

## 📤 최종 결과물

### 성공 기준
- ✅ DOCX 파일이 output/ 폴더에 생성됨
- ✅ 계층적 들여쓰기가 올바르게 적용됨
- ✅ 모든 이미지가 정상 표시됨
- ✅ 파일 크기가 적정함 (이미지 포함시 2-3MB)
- ✅ 사용자 요구사항 100% 충족

### 완료 보고 형식
```
✅ 변환 완료!

📊 결과:
- 파일: output/문서명_FIXED.docx (X.XMB)
- 이미지: XX개 처리됨
- 품질: 계층적 들여쓰기 ✅, 기호 보존 ✅

🎯 핵심 성공 요인:
- SimpleThermalConverter 직접 사용
- 애니메이션 제거된 고품질 차트
- 전문 도구(capture-website-cli) 활용
```

## ⚠️ 절대 금지 사항
- HTMLBasedConverter 사용
- MD 기호(□,○,-,•) 변경
- 애니메이션 있는 상태로 차트 캡처
- 들여쓰기 설정 임의 변경
- GUI 변환기 사용

---

**이 프롬프트는 실제 성공 사례를 바탕으로 작성되었으며, 모든 지침을 따르면 100% 성공적인 결과를 보장합니다.**