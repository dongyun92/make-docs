"""
향상된 MD to DOCX 변환기 - HTML 파일 기반 이미지 배치 지원
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.shared import OxmlElement, qn
from chart_placement_rules import ImagePlacementProcessor
from simple_thermal_converter import SimpleThermalConverter


class EnhancedMDConverter(SimpleThermalConverter):
    """HTML 파일 기반 이미지 배치를 지원하는 향상된 MD 변환기"""
    
    def __init__(self):
        super().__init__()
        self.image_processor = ImagePlacementProcessor()
    
    def convert_with_html_files(self, md_file_path: str, html_files: List[str], output_path: str):
        """
        HTML 파일들을 함께 처리하여 MD를 DOCX로 변환합니다.
        
        Args:
            md_file_path: 원본 MD 파일 경로
            html_files: HTML 파일들 경로 리스트
            output_path: 출력 DOCX 파일 경로
        """
        print(f"📋 향상된 변환 시작: {os.path.basename(md_file_path)}")
        print(f"📊 HTML 파일 {len(html_files)}개와 함께 처리합니다.")
        
        # HTML 파일들을 처리하여 이미지가 삽입된 MD 내용 생성
        if html_files:
            enhanced_md_content = self.image_processor.process_md_with_html_files(md_file_path, html_files)
            
            # 임시 MD 파일 생성
            temp_md_path = str(Path(md_file_path).parent / f"temp_{Path(md_file_path).name}")
            with open(temp_md_path, 'w', encoding='utf-8') as f:
                f.write(enhanced_md_content)
            
            try:
                # 향상된 MD 내용으로 변환
                self.convert(temp_md_path, output_path)
                print(f"✅ 이미지 포함 변환 완료: {output_path}")
            finally:
                # 임시 파일 삭제
                if os.path.exists(temp_md_path):
                    os.remove(temp_md_path)
        else:
            # HTML 파일이 없으면 기본 변환
            self.convert(md_file_path, output_path)
            print(f"✅ 기본 변환 완료: {output_path}")
    
    def process_image_with_smart_placement(self, lines: List[str], start_idx: int) -> int:
        """
        스마트 이미지 배치를 지원하는 이미지 처리
        """
        line = lines[start_idx].strip()
        
        # 기본 이미지 처리
        result = super().process_image(lines, start_idx)
        
        # 추가 스마트 배치 로직이 필요하면 여기에 추가
        
        return result
    
    def enhance_document_formatting(self):
        """문서 서식 향상"""
        # 페이지 여백 설정
        sections = self.document.sections
        for section in sections:
            section.top_margin = Inches(1)
            section.bottom_margin = Inches(1)
            section.left_margin = Inches(1)
            section.right_margin = Inches(1)
        
        # 기본 폰트 설정
        style = self.document.styles['Normal']
        font = style.font
        font.name = 'Malgun Gothic'
        font.size = Pt(11)


class HTMLBasedConverter:
    """HTML 파일 기반 변환 시스템의 메인 클래스"""
    
    def __init__(self):
        self.enhanced_converter = EnhancedMDConverter()
    
    def convert_md_with_htmls(self, md_file: str, html_files: List[str], output_file: str) -> bool:
        """
        MD 파일과 HTML 파일들을 함께 처리하여 DOCX 생성
        
        Args:
            md_file: MD 파일 경로
            html_files: HTML 파일들 경로 리스트
            output_file: 출력 DOCX 파일 경로
            
        Returns:
            변환 성공 여부
        """
        try:
            # HTML 파일들이 PNG로 변환되었는지 확인
            self._verify_png_files(html_files)
            
            # 향상된 변환 실행
            self.enhanced_converter.convert_with_html_files(md_file, html_files, output_file)
            
            # 문서 서식 향상
            self.enhanced_converter.enhance_document_formatting()
            
            print(f"✅ 전체 변환 프로세스 완료: {output_file}")
            return True
            
        except Exception as e:
            print(f"❌ 변환 중 오류 발생: {str(e)}")
            return False
    
    def _verify_png_files(self, html_files: List[str]):
        """HTML 파일들에 대응하는 PNG 파일들이 존재하는지 확인"""
        images_dir = Path("images")
        missing_pngs = []
        
        for html_file in html_files:
            html_path = Path(html_file)
            png_file = images_dir / f"{html_path.stem}.png"
            
            if not png_file.exists():
                missing_pngs.append(str(png_file))
        
        if missing_pngs:
            print(f"⚠️ 다음 PNG 파일들이 누락되었습니다:")
            for png in missing_pngs:
                print(f"  - {png}")
            print("HTML 파일들이 먼저 캡처되었는지 확인해주세요.")


def convert_with_comprehensive_approach(md_file: str, output_file: str, business_topic: str = None) -> bool:
    """
    포괄적 프롬프트 기반 변환 (Claude 포괄적 생성 결과 활용)
    
    Args:
        md_file: MD 파일 경로
        output_file: 출력 파일 경로
        business_topic: 사업 주제 (참고용)
        
    Returns:
        변환 성공 여부
    """
    try:
        print(f"📋 포괄적 프롬프트 결과 변환: {md_file}")
        
        # 기본 변환 (Claude가 생성한 MD 파일 변환)
        converter = HTMLBasedConverter()
        converter.enhanced_converter.convert(md_file, output_file)
        
        print(f"✅ 기본 변환 완료: {output_file}")
        print("💡 HTML 파일들이 있다면 GUI에서 함께 선택하여 완전한 변환을 수행하세요.")
        
        return True
        
    except Exception as e:
        print(f"❌ 변환 실패: {str(e)}")
        return False


def show_comprehensive_prompt_example(business_topic: str = "AI 챗봇 서비스"):
    """포괄적 프롬프트 예시를 출력합니다."""
    from prompt_templates import BusinessPlanPromptTemplates
    
    templates = BusinessPlanPromptTemplates()
    
    print("="*80)
    print("포괄적 사업계획서 생성 프롬프트 예시")
    print("="*80)
    
    example_prompt = templates.generate_example_prompt(business_topic)
    print(example_prompt)
    
    print("="*80)
    print("위 프롬프트를 Claude에게 전달하면:")
    print("1. 완전한 사업계획서 MD 파일")
    print("2. 관련된 모든 HTML 차트 파일들")
    print("3. 파일명 기반으로 자동 매칭되는 구조")
    print("가 모두 생성됩니다.")
    print("="*80)


if __name__ == "__main__":
    # 포괄적 프롬프트 예시 출력
    show_comprehensive_prompt_example("재래식 무기 탑재 공격드론 방어시스템")
    
    # 테스트 코드
    converter = HTMLBasedConverter()
    
    # 테스트 파일들
    test_md = "attack_drone_defense_system.md"
    test_htmls = [
        "images/market_growth_line.html",
        "images/budget_pie.html",
        "images/risk_matrix.html"
    ]
    test_output = "output/test_comprehensive_conversion.docx"
    
    if os.path.exists(test_md):
        success = converter.convert_md_with_htmls(test_md, test_htmls, test_output)
        if success:
            print("✅ 테스트 변환 성공!")
        else:
            print("❌ 테스트 변환 실패!")
    else:
        print(f"테스트 파일 {test_md}을 찾을 수 없습니다.")
        print("포괄적 프롬프트를 사용하여 Claude로부터 MD 파일과 HTML 파일들을 생성하세요.")