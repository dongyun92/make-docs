"""
사업계획서 내 차트 배치 규칙 및 이미지 처리 시스템
"""

import re
from typing import List, Dict, Tuple, Optional
from pathlib import Path


class ChartPlacementRules:
    """사업계획서 섹션별 차트 배치 규칙을 관리하는 클래스"""
    
    def __init__(self):
        # 섹션별 차트 배치 규칙
        self.placement_rules = {
            # 시장 관련 섹션
            "market": {
                "keywords": ["시장", "market", "동향", "규모", "성장"],
                "chart_types": ["growth_chart", "market_size_chart"],
                "position": "after_first_paragraph",
                "caption_template": "<그림 {}> {}",
                "preferred_size": (900, 600)
            },
            
            # 경쟁 분석 섹션
            "competition": {
                "keywords": ["경쟁", "competition", "비교", "경쟁사"],
                "chart_types": ["competition_chart", "technology_level"],
                "position": "after_analysis_text",
                "caption_template": "<그림 {}> {}",
                "preferred_size": (900, 600)
            },
            
            # 재무/예산 섹션
            "financial": {
                "keywords": ["예산", "사업비", "budget", "비용", "매출", "수익"],
                "chart_types": ["budget_allocation", "revenue_projection"],
                "position": "after_table_if_exists",
                "caption_template": "<그림 {}> {}",
                "preferred_size": (700, 700)  # 파이차트는 정사각형
            },
            
            # 기술 분석 섹션
            "technology": {
                "keywords": ["기술", "technology", "개발", "연구", "R&D"],
                "chart_types": ["technology_level", "development_timeline"],
                "position": "after_description",
                "caption_template": "<그림 {}> {}",
                "preferred_size": (1200, 600)  # 타임라인은 가로로 길게
            },
            
            # 위험 분석 섹션
            "risk": {
                "keywords": ["위험", "리스크", "risk", "위기"],
                "chart_types": ["risk_matrix"],
                "position": "after_list_if_exists",
                "caption_template": "<그림 {}> {}",
                "preferred_size": (800, 800)
            }
        }
        
        # 캡션 자동 생성 템플릿
        self.caption_templates = {
            "growth_chart": "{} 성장률 추이",
            "market_size_chart": "{} 시장 규모",
            "competition_chart": "경쟁사 비교 분석",
            "budget_allocation": "예산 배분 현황",
            "revenue_projection": "매출 전망",
            "technology_level": "기술 수준 비교",
            "development_timeline": "개발 일정",
            "risk_matrix": "위험 요소 매트릭스"
        }
    
    def analyze_section(self, section_title: str, section_content: str) -> Dict:
        """
        섹션을 분석하여 차트 배치 정보를 반환합니다.
        
        Args:
            section_title: 섹션 제목
            section_content: 섹션 내용
            
        Returns:
            배치 정보 딕셔너리
        """
        section_type = self._classify_section(section_title, section_content)
        
        if section_type:
            rule = self.placement_rules[section_type]
            position = self._determine_insertion_position(section_content, rule["position"])
            
            return {
                "section_type": section_type,
                "chart_types": rule["chart_types"],
                "insertion_position": position,
                "caption_template": rule["caption_template"],
                "preferred_size": rule["preferred_size"],
                "requires_chart": True
            }
        
        return {"requires_chart": False}
    
    def _classify_section(self, title: str, content: str) -> Optional[str]:
        """섹션을 분류합니다."""
        text = f"{title} {content}".lower()
        
        # 각 카테고리별로 키워드 매칭 점수 계산
        scores = {}
        for section_type, rule in self.placement_rules.items():
            score = sum(1 for keyword in rule["keywords"] if keyword in text)
            if score > 0:
                scores[section_type] = score
        
        # 가장 높은 점수를 가진 섹션 타입 반환
        if scores:
            return max(scores.items(), key=lambda x: x[1])[0]
        
        return None
    
    def _determine_insertion_position(self, content: str, position_rule: str) -> int:
        """삽입 위치를 결정합니다."""
        lines = content.split('\n')
        
        if position_rule == "after_first_paragraph":
            # 첫 번째 문단 후
            for i, line in enumerate(lines):
                if i > 0 and line.strip() == '' and lines[i-1].strip() != '':
                    return i + 1
            return min(3, len(lines))  # 기본값: 3번째 줄
        
        elif position_rule == "after_table_if_exists":
            # 테이블이 있으면 테이블 후, 없으면 중간 지점
            for i, line in enumerate(lines):
                if '|' in line and i < len(lines) - 1:
                    # 테이블 끝 찾기
                    j = i
                    while j < len(lines) and ('|' in lines[j] or lines[j].strip() == ''):
                        j += 1
                    return j + 1
            return len(lines) // 2
        
        elif position_rule == "after_analysis_text":
            # 분석 텍스트 후 (보통 중간 지점)
            return len(lines) // 2
        
        elif position_rule == "after_description":
            # 설명 후 (첫 번째 문단들 후)
            paragraph_count = 0
            for i, line in enumerate(lines):
                if line.strip() and not line.startswith('#'):
                    paragraph_count += 1
                if paragraph_count >= 2 and line.strip() == '':
                    return i + 1
            return min(5, len(lines))
        
        elif position_rule == "after_list_if_exists":
            # 리스트가 있으면 리스트 후, 없으면 끝 부분
            in_list = False
            for i, line in enumerate(lines):
                if line.strip().startswith(('-', '*', '1.', '2.')):
                    in_list = True
                elif in_list and line.strip() == '':
                    return i + 1
            return max(1, len(lines) - 2)
        
        return len(lines) // 2  # 기본값: 중간


class ImagePlacementProcessor:
    """HTML 파일들을 처리하여 MD 파일에 적절히 배치하는 클래스"""
    
    def __init__(self):
        self.placement_rules = ChartPlacementRules()
        self.image_counter = 1
    
    def process_md_with_html_files(self, md_file_path: str, html_files: List[str]) -> str:
        """
        MD 파일과 HTML 파일들을 처리하여 이미지가 삽입된 새로운 MD 내용을 반환합니다.
        
        Args:
            md_file_path: 원본 MD 파일 경로
            html_files: HTML 파일 경로 리스트
            
        Returns:
            이미지가 삽입된 MD 내용
        """
        with open(md_file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # HTML 파일들에서 PNG 생성 (실제 캡처는 GUI에서 처리)
        image_files = self._prepare_image_files(html_files)
        
        # MD 내용을 섹션별로 분석하고 이미지 삽입
        new_content = self._insert_images_by_sections(md_content, image_files)
        
        return new_content
    
    def _prepare_image_files(self, html_files: List[str]) -> List[Dict]:
        """HTML 파일 정보를 정리합니다."""
        image_files = []
        
        for html_file in html_files:
            html_path = Path(html_file)
            # HTML 파일이 이미 images/ 폴더에 있으므로 같은 폴더에서 PNG 찾기
            image_path = html_path.parent / f"{html_path.stem}.png"
            
            # HTML 파일에서 차트 타입 추정 (파일명 기반)
            chart_type = self._estimate_chart_type(html_path.name)
            
            image_files.append({
                "html_file": html_file,
                "image_file": str(image_path),
                "chart_type": chart_type,
                "filename": html_path.stem
            })
        
        return image_files
    
    def _estimate_chart_type(self, filename: str) -> str:
        """파일명에서 차트 타입을 추정합니다."""
        filename_lower = filename.lower()
        
        # 키워드 기반 차트 타입 추정
        if any(keyword in filename_lower for keyword in ['growth', '성장', 'trend']):
            return 'growth_chart'
        elif any(keyword in filename_lower for keyword in ['budget', '예산', 'pie']):
            return 'budget_allocation'
        elif any(keyword in filename_lower for keyword in ['competition', '경쟁', 'compare']):
            return 'competition_chart'
        elif any(keyword in filename_lower for keyword in ['tech', '기술', 'level']):
            return 'technology_level'
        elif any(keyword in filename_lower for keyword in ['risk', '위험', 'matrix']):
            return 'risk_matrix'
        elif any(keyword in filename_lower for keyword in ['timeline', '일정', 'schedule']):
            return 'development_timeline'
        else:
            return 'growth_chart'  # 기본값
    
    def _insert_images_by_sections(self, md_content: str, image_files: List[Dict]) -> str:
        """섹션별로 이미지를 삽입합니다."""
        lines = md_content.split('\n')
        new_lines = []
        used_images = set()
        
        i = 0
        while i < len(lines):
            line = lines[i]
            new_lines.append(line)
            
            # 헤더 섹션 감지
            if line.startswith('#') and not line.startswith('####'):
                section_title = line.lstrip('#').strip()
                
                # 다음 헤더까지의 내용 수집
                section_content = []
                j = i + 1
                while j < len(lines) and not (lines[j].startswith('#') and not lines[j].startswith('####')):
                    section_content.append(lines[j])
                    j += 1
                
                section_text = '\n'.join(section_content)
                
                # 섹션 분석
                analysis = self.placement_rules.analyze_section(section_title, section_text)
                
                if analysis.get("requires_chart"):
                    # 적합한 이미지 찾기
                    suitable_image = self._find_suitable_image(
                        image_files, analysis["chart_types"], used_images
                    )
                    
                    if suitable_image:
                        used_images.add(suitable_image["filename"])
                        
                        # 삽입 위치 계산
                        insertion_pos = analysis["insertion_position"]
                        
                        # 이미지와 캡션 생성
                        image_line, caption_line = self._create_image_markdown(
                            suitable_image, section_title, analysis
                        )
                        
                        # 섹션 내용에 이미지 삽입
                        if insertion_pos < len(section_content):
                            section_content.insert(insertion_pos, '')
                            section_content.insert(insertion_pos + 1, image_line)
                            section_content.insert(insertion_pos + 2, caption_line)
                            section_content.insert(insertion_pos + 3, '')
                        else:
                            section_content.extend(['', image_line, caption_line, ''])
                
                # 수정된 섹션 내용 추가
                new_lines.extend(section_content)
                i = j - 1  # 이미 처리한 라인들 건너뛰기
            
            i += 1
        
        return '\n'.join(new_lines)
    
    def _find_suitable_image(self, image_files: List[Dict], preferred_types: List[str], used_images: set) -> Optional[Dict]:
        """적합한 이미지를 찾습니다."""
        # 선호하는 차트 타입 순서로 검색
        for chart_type in preferred_types:
            for image_file in image_files:
                if (image_file["chart_type"] == chart_type and 
                    image_file["filename"] not in used_images):
                    return image_file
        
        # 사용되지 않은 이미지 중 아무거나
        for image_file in image_files:
            if image_file["filename"] not in used_images:
                return image_file
        
        return None
    
    def _create_image_markdown(self, image_file: Dict, section_title: str, analysis: Dict) -> Tuple[str, str]:
        """이미지 마크다운과 캡션을 생성합니다."""
        image_path = image_file["image_file"]
        
        # 이미지 마크다운
        image_line = f"![차트]({image_path})"
        
        # 캡션 생성
        chart_type = image_file["chart_type"]
        if chart_type in self.placement_rules.caption_templates:
            caption_text = self.placement_rules.caption_templates[chart_type].format(section_title)
        else:
            caption_text = f"{section_title} 관련 차트"
        
        caption_line = analysis["caption_template"].format(self.image_counter, caption_text)
        self.image_counter += 1
        
        return image_line, caption_line


if __name__ == "__main__":
    # 테스트 코드
    placement = ChartPlacementRules()
    processor = ImagePlacementProcessor()
    
    # 섹션 분석 테스트
    test_sections = [
        ("## 시장 분석", "국내외 드론 방어 시장은 최근 5년간 급속히 성장하고 있습니다."),
        ("## 예산 계획", "총 사업비는 100억원으로 계획되어 있으며, R&D 비용이 가장 큰 비중을 차지합니다."),
        ("## 기술 수준", "우리의 기술 수준은 해외 선진국 대비 70% 수준입니다.")
    ]
    
    for title, content in test_sections:
        result = placement.analyze_section(title, content)
        print(f"\n섹션: {title}")
        print(f"분석 결과: {result}")