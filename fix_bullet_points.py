#!/usr/bin/env python3
"""RWSL MD 파일의 불릿포인트를 가이드라인에 맞게 수정"""

import re

def fix_bullet_points():
    """불릿포인트를 올바른 체계로 수정"""
    
    with open('RWSL_항공시스템_사업계획서.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    fixed_lines = []
    
    for line in lines:
        original_line = line
        
        # 1단계: ○를 □로 변경 (단, 이미 들여쓰기된 것은 제외)
        if line.strip().startswith('○ '):
            # 들여쓰기가 없는 경우만 □로 변경
            if not line.startswith('  '):
                line = line.replace('○ ', '□ ')
        
        # 2단계: 들여쓰기 없는 - 를 ○로 변경 (2칸 들여쓰기 추가)
        elif line.strip().startswith('- ') and not line.startswith('  '):
            content_part = line.strip()[2:]  # '- ' 제거
            line = f'  ○ {content_part}'
        
        # 3단계: 들여쓰기 없는 • 를 ○로 변경 (2칸 들여쓰기 추가)
        elif line.strip().startswith('• ') and not line.startswith('  '):
            content_part = line.strip()[2:]  # '• ' 제거
            line = f'  ○ {content_part}'
            
        # 4단계: ①②③④⑤ 등을 ○로 변경 (2칸 들여쓰기 추가)
        elif re.match(r'^[①②③④⑤⑥⑦⑧⑨⑩] ', line.strip()):
            content_part = re.sub(r'^[①②③④⑤⑥⑦⑧⑨⑩] ', '', line.strip())
            line = f'  ○ {content_part}'
        
        # 볼드 텍스트 제거 (**텍스트** → 텍스트)
        line = re.sub(r'\*\*(.*?)\*\*', r'\1', line)
        
        # 공무원 문체 적용
        line = re.sub(r'합니다\.', '함', line)
        line = re.sub(r'됩니다\.', '됨', line) 
        line = re.sub(r'입니다\.', '임', line)
        
        # 콜론 제거
        line = re.sub(r'함:', '함', line)
        line = re.sub(r'됨:', '됨', line)
        line = re.sub(r'임:', '임', line)
        
        fixed_lines.append(line)
    
    # 수정된 내용 저장
    with open('RWSL_항공시스템_사업계획서.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(fixed_lines))
    
    print('✅ 불릿포인트 체계 수정 완료')
    print('📋 수정된 체계:')
    print('   □ 주요 항목 (1단계)')
    print('     ○ 세부 항목 (2단계)')
    print('       - 하위 항목 (3단계)')
    print('         • 최하위 항목 (4단계)')

if __name__ == "__main__":
    fix_bullet_points()