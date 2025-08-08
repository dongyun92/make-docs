#!/usr/bin/env python3
"""RWSL 문서 변환"""

from universal_md_converter import UniversalMDConverter

def main():
    converter = UniversalMDConverter()
    result = converter.convert("RWSL_항공시스템_사업계획서.md")
    print(f"\n🎉 RWSL 문서 변환 완료!\n파일: {result}")

if __name__ == "__main__":
    main()