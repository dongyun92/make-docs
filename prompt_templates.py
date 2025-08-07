"""
포괄적 사업계획서 생성을 위한 프롬프트 템플릿 시스템
"""

class BusinessPlanPromptTemplates:
    """포괄적 사업계획서 생성을 위한 프롬프트 템플릿"""
    
    def __init__(self):
        self.comprehensive_template = """
{business_topic} 사업계획서를 작성하려해. {format_requirements}에 맞춰 마크다운형식으로 작성해줘. 
다이어그램, 표, 차트 등 시각화 자료를 각각 html로 만들어서 활용할 수 있게 해줘.

**사업계획서 구조**:
1. **사업 개요**
2. **시장 분석**
3. **경쟁 분석**
4. **기술 분석**
5. **사업 모델**
6. **마케팅 전략**
7. **재무 계획**
8. **위험 분석**
9. **향후 계획**

**시각화 자료 요구사항**:
- 각 섹션에 적절한 차트나 다이어그램을 HTML 파일로 생성
- 파일명은 섹션 내용과 연관되도록 명명 (예: market_growth_chart.html, budget_allocation.html)
- 사업계획서 MD 파일에서 해당 HTML 파일명을 이미지로 참조

**HTML 파일 생성 규칙**:
- 완전한 HTML 파일 (<!DOCTYPE html>로 시작)
- 한글 폰트 지원 ('Malgun Gothic', 'Arial', sans-serif)
- 제목 없이 순수 차트/다이어그램만
- 적절한 크기 (차트: 900x600px, 파이차트: 700x700px)
- 현실적이고 의미있는 데이터 사용

**마크다운 이미지 참조 형식**:
![차트](images/파일명.png)
<그림 번호> 캡션

**필수 시각화 자료**:
- 시장 성장률 추이 차트 (market_growth_line.html)
- 지역별 시장 규모 (market_regional.html)
- 경쟁사 비교 분석 (competition_analysis.html)
- 기술 수준 비교 (technology_level.html)
- 예산 배분 (budget_pie.html)
- 매출 전망 (revenue_projection.html)
- 위험 매트릭스 (risk_matrix.html)

해당 HTML에서 내가 알아서 캡처할테니 사업계획서에 자료들 필요한 위치에 해당 필요 파일명으로 배치해주면 내가 인식해서 거기에 캡처해당그림을 넣을게.
        """
        
        # 기존 개별 차트 템플릿도 유지 (호환성)
        self.individual_templates = {
            "market_analysis": {
                "growth_chart": """
다음 조건에 맞는 시장 성장률 차트 HTML을 생성해주세요:

**주제**: {business_topic}
**차트 타입**: 선 그래프 (Line Chart)
**데이터 요구사항**:
- 최근 5년간 시장 성장률 (2019-2023)
- 실제 업계 트렌드에 맞는 현실적인 수치
- Y축 최대값은 데이터 최대값의 1.2배로 설정

**스타일 요구사항**:
- 한글 폰트 지원 ('Malgun Gothic', 'Arial', sans-serif)
- 차트 크기: 900x600px
- 제목 없이 순수 차트만
- 범례는 한글로 표시
- 격자선 표시

**출력 형식**: 완전한 HTML 파일 (<!DOCTYPE html>로 시작)
                """,
                
                "market_size_chart": """
다음 조건에 맞는 시장 규모 차트 HTML을 생성해주세요:

**주제**: {business_topic}
**차트 타입**: 막대 그래프 (Bar Chart)
**데이터 요구사항**:
- 지역별 시장 규모 (국내/해외 비교)
- 단위: 억원 또는 조원
- 현실적인 시장 규모 데이터

**스타일 요구사항**:
- 한글 폰트 지원
- 차트 크기: 900x600px
- Y축은 데이터에 적합한 스케일링
- 색상: 블루 계열

**출력 형식**: 완전한 HTML 파일
                """
            },
            
            "financial_analysis": {
                "budget_allocation": """
다음 조건에 맞는 예산 배분 차트 HTML을 생성해주세요:

**주제**: {business_topic}
**차트 타입**: 파이 차트 (Pie Chart)
**데이터 요구사항**:
- R&D, 마케팅, 운영비, 인건비, 기타 항목
- 각 항목별 현실적인 비율
- 총 예산 규모에 맞는 분배

**스타일 요구사항**:
- 각 섹션별 다른 색상
- 퍼센트 라벨 표시
- 차트 크기: 700x700px

**출력 형식**: 완전한 HTML 파일
                """,
                
                "revenue_projection": """
다음 조건에 맞는 매출 전망 차트 HTML을 생성해주세요:

**주제**: {business_topic}
**차트 타입**: 복합 차트 (매출+이익률)
**데이터 요구사항**:
- 향후 5년간 매출 예상 (막대그래프)
- 연도별 이익률 (선그래프)
- 현실적인 성장 곡선

**스타일 요구사항**:
- 매출: 파란색 막대
- 이익률: 빨간색 선
- 이중 Y축 사용

**출력 형식**: 완전한 HTML 파일
                """
            },
            
            "technology_analysis": {
                "technology_level": """
다음 조건에 맞는 기술 수준 비교 차트 HTML을 생성해주세요:

**주제**: {business_topic}
**차트 타입**: 그룹화된 막대 그래프
**데이터 요구사항**:
- 핵심 기술 영역별 국내/해외 수준 비교
- 기술성숙도 1-10 스케일
- 5-7개 기술 영역

**스타일 요구사항**:
- 국내: 파란색, 해외: 빨간색
- Y축 최대값: 10
- 범례 표시

**출력 형식**: 완전한 HTML 파일
                """,
                
                "development_timeline": """
다간 조건에 맞는 개발 타임라인 차트 HTML을 생성해주세요:

**주제**: {business_topic}
**차트 타입**: 간트 차트 스타일
**데이터 요구사항**:
- 주요 개발 단계별 일정
- 단계간 의존성 표시
- 마일스톤 표시

**스타일 요구사항**:
- 단계별 다른 색상
- 진행률 표시
- 차트 크기: 1200x600px

**출력 형식**: 완전한 HTML 파일
                """
            },
            
            "risk_analysis": {
                "risk_matrix": """
다음 조건에 맞는 위험 매트릭스 차트 HTML을 생성해주세요:

**주제**: {business_topic}
**차트 타입**: 산점도 (Scatter Plot)
**데이터 요구사항**:
- X축: 발생 가능성 (1-5)
- Y축: 영향도 (1-5)
- 주요 위험 요소 5-8개

**스타일 요구사항**:
- 위험도별 색상 구분
- 각 점에 위험 요소명 라벨
- 배경에 위험도 구역 표시

**출력 형식**: 완전한 HTML 파일
                """
            }
        }
    
    def get_comprehensive_prompt(self, business_topic: str, format_requirements: str = "표준 사업계획서 양식") -> str:
        """
        포괄적 사업계획서 생성 프롬프트를 반환합니다.
        
        Args:
            business_topic: 사업 주제
            format_requirements: 양식 요구사항
            
        Returns:
            포맷된 포괄적 프롬프트 문자열
        """
        return self.comprehensive_template.format(
            business_topic=business_topic,
            format_requirements=format_requirements
        )
    
    def get_individual_prompt(self, category: str, chart_type: str, business_topic: str) -> str:
        """
        개별 차트 생성 프롬프트를 가져옵니다. (호환성 유지)
        
        Args:
            category: 분석 카테고리 (market_analysis, financial_analysis 등)
            chart_type: 차트 타입
            business_topic: 사업 주제
            
        Returns:
            포맷된 프롬프트 문자열
        """
        if category in self.individual_templates and chart_type in self.individual_templates[category]:
            return self.individual_templates[category][chart_type].format(business_topic=business_topic)
        else:
            return self._generate_generic_prompt(chart_type, business_topic)
    
    def _generate_generic_prompt(self, chart_type: str, business_topic: str) -> str:
        """기본 프롬프트 생성"""
        return f"""
다음 조건에 맞는 {chart_type} 차트 HTML을 생성해주세요:

**주제**: {business_topic}
**차트 타입**: {chart_type}
**데이터 요구사항**:
- 해당 주제에 적합한 현실적인 데이터
- 의미있는 비교 항목들
- 적절한 수치 범위

**스타일 요구사항**:
- 한글 폰트 지원 ('Malgun Gothic', 'Arial', sans-serif)
- 차트 크기: 900x600px
- 제목 없이 순수 차트만
- 적절한 색상 조합
- 범례 및 라벨 표시

**출력 형식**: 완전한 HTML 파일 (<!DOCTYPE html>로 시작)
        """
    
    def get_all_categories(self) -> list:
        """사용 가능한 모든 카테고리 반환"""
        return list(self.individual_templates.keys())
    
    def get_chart_types(self, category: str) -> list:
        """특정 카테고리의 모든 차트 타입 반환"""
        if category in self.individual_templates:
            return list(self.individual_templates[category].keys())
        return []
    
    def generate_example_prompt(self, business_topic: str) -> str:
        """
        사용자에게 보여줄 예시 프롬프트를 생성합니다.
        
        Args:
            business_topic: 사업 주제
            
        Returns:
            예시 프롬프트 문자열
        """
        return f"""
예시 프롬프트:

{business_topic} 사업계획서를 작성하려해. 표준 사업계획서 양식에 맞춰 마크다운형식으로 작성해줘. 
다이어그램, 표, 차트 등 시각화 자료를 각각 html로 만들어서 활용할 수 있게 해줘.

해당 html에서 내가 알아서 캡처할테니 사업계획서에 자료들 필요한 위치에 해당 필요 파일명으로 배치해주면 내가 인식해서 거기에 캡처해당그림을 넣을게.

위 프롬프트를 Claude에게 전달하면 완전한 사업계획서와 필요한 HTML 차트들이 모두 생성됩니다.
        """


class BusinessPlanChartMatcher:
    """사업계획서 섹션과 적절한 차트 타입을 매칭하는 클래스"""
    
    def __init__(self):
        self.section_mapping = {
            # 시장 분석 관련 섹션
            "시장 분석": ["market_analysis", "growth_chart"],
            "시장동향": ["market_analysis", "growth_chart"],
            "시장 규모": ["market_analysis", "market_size_chart"],
            "경쟁 분석": ["market_analysis", "competition_chart"],
            "경쟁사 분석": ["market_analysis", "competition_chart"],
            
            # 재무 분석 관련 섹션
            "사업비": ["financial_analysis", "budget_allocation"],
            "예산": ["financial_analysis", "budget_allocation"],
            "예산 계획": ["financial_analysis", "budget_allocation"],
            "수익성": ["financial_analysis", "revenue_projection"],
            "매출 전망": ["financial_analysis", "revenue_projection"],
            "손익": ["financial_analysis", "revenue_projection"],
            
            # 기술 분석 관련 섹션
            "기술 분석": ["technology_analysis", "technology_level"],
            "기술 수준": ["technology_analysis", "technology_level"],
            "개발 계획": ["technology_analysis", "development_timeline"],
            "일정": ["technology_analysis", "development_timeline"],
            "로드맵": ["technology_analysis", "development_timeline"],
            
            # 위험 분석 관련 섹션
            "위험 분석": ["risk_analysis", "risk_matrix"],
            "리스크": ["risk_analysis", "risk_matrix"],
            "위험 요소": ["risk_analysis", "risk_matrix"]
        }
    
    def match_section_to_chart(self, section_title: str) -> tuple:
        """
        섹션 제목을 기반으로 적절한 차트 타입을 찾습니다.
        
        Args:
            section_title: 사업계획서 섹션 제목
            
        Returns:
            (category, chart_type) 튜플
        """
        section_title = section_title.strip()
        
        # 정확한 매칭 시도
        if section_title in self.section_mapping:
            return tuple(self.section_mapping[section_title])
        
        # 부분 매칭 시도
        for keyword, mapping in self.section_mapping.items():
            if keyword in section_title:
                return tuple(mapping)
        
        # 기본 매칭 (시장 분석으로 기본 설정)
        return ("market_analysis", "growth_chart")


if __name__ == "__main__":
    # 사용 예시
    templates = BusinessPlanPromptTemplates()
    matcher = BusinessPlanChartMatcher()
    
    # 사업 주제
    business_topic = "재래식 무기를 탑재한 공격 드론 방어 시스템"
    
    print("="*80)
    print("새로운 포괄적 사업계획서 생성 방식")
    print("="*80)
    
    # 포괄적 프롬프트 생성
    comprehensive_prompt = templates.get_comprehensive_prompt(business_topic)
    print(comprehensive_prompt)
    
    print("\n" + "="*80)
    print("사용자 예시 프롬프트")
    print("="*80)
    
    # 예시 프롬프트
    example = templates.generate_example_prompt(business_topic)
    print(example)
    
    print("\n" + "="*80)
    print("기존 개별 차트 생성 방식 (호환성)")
    print("="*80)
    
    # 개별 섹션별 프롬프트 생성 예시 (기존 방식)
    sections = ["시장 분석", "예산 계획", "기술 수준", "위험 분석"]
    
    for section in sections:
        category, chart_type = matcher.match_section_to_chart(section)
        prompt = templates.get_individual_prompt(category, chart_type, business_topic)
        
        print(f"\n{'-'*50}")
        print(f"섹션: {section}")
        print(f"카테고리: {category}, 차트타입: {chart_type}")
        print(f"{'-'*50}")
        print(prompt[:200] + "...")  # 첫 200자만 표시