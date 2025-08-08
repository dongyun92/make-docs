#!/usr/bin/env python3
"""
RWSL HTML 차트들에서 모든 애니메이션 효과를 제거하는 스크립트
Chart.js의 animation 설정을 false로 변경
"""

import os
import re
import glob

def remove_animations_from_html(file_path: str) -> bool:
    """HTML 파일에서 Chart.js 애니메이션을 제거"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Chart.js 설정에서 animation 관련 설정 찾기 및 제거
        patterns_to_replace = [
            # animation: { duration: 2000 } 형태
            (r'animation:\s*\{[^}]*\}', 'animation: false'),
            # animation: true 형태
            (r'animation:\s*true', 'animation: false'),
            # "animation": { "duration": 2000 } 형태
            (r'"animation":\s*\{[^}]*\}', '"animation": false'),
            # "animation": true 형태
            (r'"animation":\s*true', '"animation": false'),
        ]
        
        for pattern, replacement in patterns_to_replace:
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
        
        # 애니메이션 설정이 없으면 options에 추가
        if 'animation:' not in content and '"animation"' not in content:
            # Chart.js 옵션 블록 찾기
            options_pattern = r'(options:\s*\{)'
            if re.search(options_pattern, content):
                content = re.sub(options_pattern, r'\1\n            animation: false,', content)
            else:
                # options가 없으면 data 다음에 추가
                data_pattern = r'(data:\s*\{[^}]*\}[^}]*\})'
                if re.search(data_pattern, content, re.DOTALL):
                    content = re.sub(data_pattern, r'\1,\n        options: {\n            animation: false\n        }', content, flags=re.DOTALL)
        
        # 변경사항이 있으면 파일 저장
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 애니메이션 제거 완료: {os.path.basename(file_path)}")
            return True
        else:
            print(f"⚠️  애니메이션 설정 없음: {os.path.basename(file_path)}")
            return False
            
    except Exception as e:
        print(f"❌ 처리 실패 {os.path.basename(file_path)}: {e}")
        return False

def remove_all_animations():
    """모든 RWSL HTML 파일에서 애니메이션 제거"""
    
    # RWSL HTML 파일들 찾기
    html_files = glob.glob('/Users/dykim/dev/make-docs/images/rwsl*.html')
    
    print(f"🎯 RWSL 차트 파일 발견: {len(html_files)}개")
    
    modified_count = 0
    
    for i, html_file in enumerate(html_files, 1):
        print(f"\n[{i}/{len(html_files)}]")
        
        if remove_animations_from_html(html_file):
            modified_count += 1
    
    print(f"\n🎉 애니메이션 제거 완료!")
    print(f"✅ 수정된 파일: {modified_count}개")
    print(f"📝 전체 파일: {len(html_files)}개")

if __name__ == "__main__":
    remove_all_animations()