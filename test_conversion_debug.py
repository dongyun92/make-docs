#!/usr/bin/env python3
"""
변환 프로세스 디버깅 테스트 스크립트
HTML 변환 완료 후 DOCX 생성이 진행되지 않는 문제를 단계별로 테스트
"""

import os
import sys
from pathlib import Path

def test_basic_import():
    """기본 import 테스트"""
    print("=== 1. 기본 Import 테스트 ===")
    try:
        from enhanced_converter import HTMLBasedConverter
        print("✓ HTMLBasedConverter import 성공")
        
        converter = HTMLBasedConverter()
        print("✓ HTMLBasedConverter 초기화 성공")
        return converter
    except Exception as e:
        print(f"✗ Import 실패: {e}")
        return None

def test_png_verification(converter, html_files):
    """PNG 파일 확인 테스트"""
    print("\n=== 2. PNG 파일 확인 테스트 ===")
    try:
        converter._verify_png_files(html_files)
        print("✓ PNG 파일 확인 성공")
        return True
    except Exception as e:
        print(f"✗ PNG 파일 확인 실패: {e}")
        return False

def test_enhanced_converter_init(converter):
    """EnhancedMDConverter 초기화 테스트"""
    print("\n=== 3. EnhancedMDConverter 초기화 테스트 ===")
    try:
        enhanced = converter.enhanced_converter
        print(f"✓ EnhancedMDConverter 타입: {type(enhanced)}")
        print(f"✓ 이미지 프로세서: {type(enhanced.image_processor)}")
        return True
    except Exception as e:
        print(f"✗ EnhancedMDConverter 초기화 실패: {e}")
        return False

def test_simple_md_conversion(converter, md_file):
    """간단한 MD 변환 테스트 (HTML 없이)"""
    print("\n=== 4. 간단한 MD 변환 테스트 ===")
    try:
        temp_output = converter.enhanced_converter.convert(md_file)
        print(f"✓ 기본 변환 성공: {temp_output}")
        
        if os.path.exists(temp_output):
            print(f"✓ 출력 파일 존재: {temp_output}")
            file_size = os.path.getsize(temp_output)
            print(f"✓ 파일 크기: {file_size} bytes")
            
            # 임시 파일 삭제
            os.remove(temp_output)
            print("✓ 임시 파일 정리 완료")
            return True
        else:
            print("✗ 출력 파일이 생성되지 않음")
            return False
    except Exception as e:
        print(f"✗ 간단한 변환 실패: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_image_processor(converter, md_file, html_files):
    """이미지 프로세서 테스트"""
    print("\n=== 5. 이미지 프로세서 테스트 ===")
    try:
        enhanced_content = converter.enhanced_converter.image_processor.process_md_with_html_files(
            md_file, html_files
        )
        print(f"✓ 이미지 처리 성공")
        print(f"✓ 향상된 콘텐츠 길이: {len(enhanced_content)} 문자")
        
        # 첫 몇 줄만 출력
        lines = enhanced_content.split('\n')[:5]
        print("✓ 처리된 콘텐츠 미리보기:")
        for i, line in enumerate(lines):
            print(f"   {i+1}: {line[:80]}...")
        
        return True
    except Exception as e:
        print(f"✗ 이미지 처리 실패: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_temp_file_creation(converter, md_file, html_files):
    """임시 파일 생성 및 변환 테스트"""
    print("\n=== 6. 임시 파일 생성 및 변환 테스트 ===")
    try:
        # 이미지 처리된 콘텐츠 생성
        enhanced_content = converter.enhanced_converter.image_processor.process_md_with_html_files(
            md_file, html_files
        )
        
        # 임시 파일 생성
        temp_md_path = str(Path(md_file).parent / f"temp_{Path(md_file).name}")
        with open(temp_md_path, 'w', encoding='utf-8') as f:
            f.write(enhanced_content)
        print(f"✓ 임시 MD 파일 생성: {temp_md_path}")
        
        # 임시 파일로 변환
        temp_output = converter.enhanced_converter.convert(temp_md_path)
        print(f"✓ 임시 파일 변환 성공: {temp_output}")
        
        if os.path.exists(temp_output):
            print(f"✓ 임시 출력 파일 존재: {temp_output}")
            file_size = os.path.getsize(temp_output)
            print(f"✓ 파일 크기: {file_size} bytes")
        
        # 정리
        if os.path.exists(temp_md_path):
            os.remove(temp_md_path)
            print("✓ 임시 MD 파일 정리")
        if os.path.exists(temp_output):
            os.remove(temp_output)
            print("✓ 임시 출력 파일 정리")
            
        return True
    except Exception as e:
        print(f"✗ 임시 파일 변환 실패: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("RWSL 변환 프로세스 디버깅 테스트 시작\n")
    
    # 테스트 파일 경로
    md_file = "/Users/dykim/dev/make-docs/RWSL_항공시스템_사업계획서.md"
    html_files = [
        "/Users/dykim/dev/make-docs/images/rwsl_annual_investment_plan.html",
        "/Users/dykim/dev/make-docs/images/rwsl_future_aviation_integration.html"
    ]
    
    # 파일 존재 확인
    if not os.path.exists(md_file):
        print(f"✗ MD 파일을 찾을 수 없습니다: {md_file}")
        return
    
    print(f"✓ MD 파일 존재: {md_file}")
    
    existing_html_files = [f for f in html_files if os.path.exists(f)]
    print(f"✓ 존재하는 HTML 파일: {len(existing_html_files)}개")
    
    # 단계별 테스트 실행
    converter = test_basic_import()
    if not converter:
        return
        
    if not test_png_verification(converter, existing_html_files):
        return
        
    if not test_enhanced_converter_init(converter):
        return
        
    if not test_simple_md_conversion(converter, md_file):
        return
        
    if not test_image_processor(converter, md_file, existing_html_files):
        return
        
    if not test_temp_file_creation(converter, md_file, existing_html_files):
        return
    
    print("\n" + "="*50)
    print("✅ 모든 테스트 단계 통과!")
    print("이제 전체 convert_md_with_htmls() 메서드를 테스트해보겠습니다.")
    print("="*50)
    
    # 전체 변환 테스트
    try:
        output_file = "/Users/dykim/dev/make-docs/test_debug_output.docx"
        print(f"\n최종 변환 테스트: {output_file}")
        
        success = converter.convert_md_with_htmls(md_file, existing_html_files, output_file)
        
        if success:
            print("✅ 전체 변환 성공!")
            if os.path.exists(output_file):
                file_size = os.path.getsize(output_file)
                print(f"✓ 출력 파일 크기: {file_size} bytes")
        else:
            print("✗ 전체 변환 실패")
            
    except Exception as e:
        print(f"✗ 전체 변환 중 예외: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()