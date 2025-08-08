#!/usr/bin/env python3
"""
HTML 차트 파일들의 높이를 고정하여 캡처 문제를 해결하는 스크립트
"""

import os
import glob

def fix_chart_height(file_path):
    """HTML 차트 파일의 높이를 고정합니다."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # body에 고정 높이 스타일 추가
    fixed_content = content.replace(
        'body {',
        '''body {
            height: 600px;
            overflow: hidden;'''
    )
    
    # chart-container에도 고정 높이 적용
    fixed_content = fixed_content.replace(
        '.chart-container {',
        '''.chart-container {
            height: 580px;
            overflow: hidden;'''
    )
    
    # spillover-network 같은 추가 요소들의 높이 제한
    if 'spillover-network' in fixed_content:
        fixed_content = fixed_content.replace(
            '.spillover-network {',
            '''.spillover-network {
                height: 250px;
                overflow: hidden;'''
        )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print(f"✅ 수정 완료: {os.path.basename(file_path)}")

def main():
    """모든 RWSL HTML 차트 파일의 높이를 고정합니다."""
    html_files = glob.glob('/Users/dykim/dev/make-docs/images/rwsl_*.html')
    
    print(f"🔧 {len(html_files)}개의 RWSL HTML 차트 파일 수정 시작...")
    
    for html_file in html_files:
        fix_chart_height(html_file)
    
    print("\n🎉 모든 차트 파일의 높이 고정 완료!")
    print("이제 다시 변환을 시도하면 차트 캡처가 올바르게 될 것입니다.")

if __name__ == "__main__":
    main()