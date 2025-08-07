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


def convert_with_prompt_templates(md_file: str, output_file: str, business_topic: str = None) -> bool:
    """
    프롬프트 템플릿 기반 변환 (향후 확장용)
    
    Args:
        md_file: MD 파일 경로
        output_file: 출력 파일 경로
        business_topic: 사업 주제 (차트 생성 시 사용)
        
    Returns:
        변환 성공 여부
    """
    try:
        print(f"📋 프롬프트 템플릿 기반 변환: {md_file}")
        
        # 기본 변환 (HTML 파일 없이)
        converter = HTMLBasedConverter()
        converter.enhanced_converter.convert(md_file, output_file)
        
        print(f"✅ 기본 변환 완료: {output_file}")
        print("💡 향후 프롬프트 템플릿 기반 차트 자동 생성 기능이 추가될 예정입니다.")
        
        return True
        
    except Exception as e:
        print(f"❌ 변환 실패: {str(e)}")
        return False


if __name__ == "__main__":
    # 테스트 코드
    converter = HTMLBasedConverter()
    
    # 테스트 파일들
    test_md = "attack_drone_defense_system.md"
    test_htmls = [
        "images/chart_attack_drone_defense_system_1.html",
        "images/chart_attack_drone_defense_system_2.html"
    ]
    test_output = "output/test_enhanced_conversion.docx"
    
    if os.path.exists(test_md):
        success = converter.convert_md_with_htmls(test_md, test_htmls, test_output)
        if success:
            print("✅ 테스트 변환 성공!")
        else:
            print("❌ 테스트 변환 실패!")
    else:
        print(f"테스트 파일 {test_md}을 찾을 수 없습니다.")