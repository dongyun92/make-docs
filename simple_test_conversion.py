#!/usr/bin/env python3
"""
매우 간단한 변환 테스트 - 어디서 멈추는지 확인
"""

import os
import sys

def test_simple_import():
    print("1. Import 테스트...")
    try:
        from universal_md_converter import UniversalMDConverter
        print("✓ UniversalMDConverter import 성공")
        return True
    except Exception as e:
        print(f"✗ Import 실패: {e}")
        return False

def test_simple_init():
    print("2. 초기화 테스트...")
    try:
        from universal_md_converter import UniversalMDConverter
        converter = UniversalMDConverter()
        print("✓ UniversalMDConverter 초기화 성공")
        return converter
    except Exception as e:
        print(f"✗ 초기화 실패: {e}")
        return None

def test_file_read():
    print("3. 파일 읽기 테스트...")
    md_file = "/Users/dykim/dev/make-docs/RWSL_항공시스템_사업계획서.md"
    
    if not os.path.exists(md_file):
        print(f"✗ 파일이 존재하지 않습니다: {md_file}")
        return False
        
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        lines = content.split('\n')
        print(f"✓ 파일 읽기 성공: {len(lines)}줄")
        return True
    except Exception as e:
        print(f"✗ 파일 읽기 실패: {e}")
        return False

def main():
    print("간단한 변환 테스트 시작\n")
    
    if not test_simple_import():
        return
        
    converter = test_simple_init()
    if not converter:
        return
        
    if not test_file_read():
        return
    
    print("\n4. 실제 변환 테스트...")
    md_file = "/Users/dykim/dev/make-docs/RWSL_항공시스템_사업계획서.md"
    
    try:
        print("변환 시작...")
        # 30초 타임아웃으로 테스트
        import signal
        
        def timeout_handler(signum, frame):
            raise TimeoutError("변환이 30초 내에 완료되지 않았습니다")
            
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(30)  # 30초 타임아웃
        
        try:
            result = converter.convert(md_file)
            signal.alarm(0)  # 타이머 해제
            print(f"✓ 변환 완료: {result}")
        except TimeoutError:
            print("✗ 변환 타임아웃 - 30초 내에 완료되지 않음")
            return
        
    except Exception as e:
        print(f"✗ 변환 실패: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("✅ 모든 테스트 통과!")

if __name__ == "__main__":
    main()