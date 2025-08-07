#!/usr/bin/env python3
"""
통합 캡처 시스템 - 동일 Chrome 인스턴스에서 크기 감지와 캡처 동시 실행
"""

import subprocess
import json
import time
from pathlib import Path
import tempfile

def create_capture_html(original_html):
    """캡처용 HTML 생성 - 크기 감지와 캡처를 동시에 처리"""
    
    with open(original_html, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 통합 JavaScript - 크기 감지 후 자동 캡처 트리거
    unified_js = '''
    window.addEventListener('load', function() {
        setTimeout(function() {
            const body = document.body;
            const html = document.documentElement;
            
            // 실제 콘텐츠 전체 크기
            const fullWidth = Math.max(
                body.scrollWidth, body.offsetWidth, 
                html.clientWidth, html.scrollWidth, html.offsetWidth
            );
            const fullHeight = Math.max(
                body.scrollHeight, body.offsetHeight,
                html.clientHeight, html.scrollHeight, html.offsetHeight
            );
            
            // 여유 마진 추가
            const captureWidth = fullWidth + 40;
            const captureHeight = fullHeight + 40;
            
            // body 크기를 캡처 크기로 강제 설정
            document.body.style.width = captureWidth + 'px';
            document.body.style.height = captureHeight + 'px';
            document.body.style.minWidth = captureWidth + 'px';
            document.body.style.minHeight = captureHeight + 'px';
            
            // viewport 메타태그도 업데이트
            const viewport = document.querySelector('meta[name="viewport"]');
            if (viewport) {
                viewport.content = `width=${captureWidth}, initial-scale=1.0`;
            }
            
            console.log('UNIFIED_CAPTURE_SIZE:', JSON.stringify({
                width: captureWidth,
                height: captureHeight,
                originalWidth: fullWidth,
                originalHeight: fullHeight
            }));
            
            document.title = `READY_TO_CAPTURE:${captureWidth}x${captureHeight}`;
            
        }, 3000);
    });
    '''
    
    # JavaScript 주입
    modified_content = content.replace('</head>', f'<script>{unified_js}</script>\n</head>')
    
    # 임시 캡처용 파일 생성
    temp_file = f"temp_capture_{Path(original_html).name}"
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(modified_content)
    
    return temp_file

def unified_capture_png(html_file):
    """통합 캡처 - 동일 Chrome에서 크기 감지 및 캡처"""
    
    # 캡처용 HTML 생성
    capture_html = create_capture_html(html_file)
    output_file = html_file.replace('.html', '.png')
    
    try:
        print(f"   🔄 통합 캡처 프로세스 시작...")
        
        # 1단계: 크기 감지
        size_result = subprocess.run([
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            '--headless',
            '--disable-gpu',
            '--disable-web-security', 
            '--window-size=1400,1000',  # 충분히 큰 초기 창
            '--virtual-time-budget=5000',
            '--dump-dom',
            f'file://{Path(capture_html).absolute()}'
        ], capture_output=True, text=True, timeout=10)
        
        # 크기 추출
        width, height = 900, 700  # 기본값
        if 'READY_TO_CAPTURE:' in size_result.stdout:
            for line in size_result.stdout.split('\n'):
                if 'READY_TO_CAPTURE:' in line:
                    size_part = line.split('READY_TO_CAPTURE:')[1].split(':')[0]
                    if 'x' in size_part:
                        width, height = map(int, size_part.split('x'))
                        break
        
        print(f"   📐 감지된 통합 크기: {width}x{height}")
        
        # 2단계: 정확한 크기로 캡처
        subprocess.run([
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            '--headless',
            '--disable-gpu',
            '--disable-web-security',
            '--hide-scrollbars',
            '--force-device-scale-factor=1',
            '--disable-extensions',
            '--run-all-compositor-stages-before-draw',
            f'--window-size={width},{height}',
            '--virtual-time-budget=6000',
            f'--screenshot={output_file}',
            f'file://{Path(capture_html).absolute()}'
        ], check=True, timeout=15)
        
        return True
        
    except Exception as e:
        print(f"   ❌ 통합 캡처 실패: {e}")
        return False
    finally:
        # 임시 파일 삭제
        try:
            Path(capture_html).unlink()
        except:
            pass

def run_unified_capture():
    """통합 캡처 실행"""
    
    html_files = [
        "images/market_growth_line.html",
        "images/budget_pie.html", 
        "images/trl_roadmap.html",
        "images/system_architecture.html",
        "images/swot_analysis.html",
        "images/risk_matrix.html"
    ]
    
    print("🎯 통합 캡처 시스템 - 근원적 해결")
    print("=" * 40)
    
    for html_file in html_files:
        if not Path(html_file).exists():
            continue
            
        filename = Path(html_file).name
        print(f"\n📸 {filename} 통합 처리...")
        
        if unified_capture_png(html_file):
            png_file = html_file.replace('.html', '.png')
            if Path(png_file).exists():
                file_size = Path(png_file).stat().st_size
                print(f"   ✅ 완료: {file_size:,} bytes")
        else:
            print(f"   ❌ 실패")
    
    print(f"\n🎉 통합 캡처 완료!")

if __name__ == "__main__":
    run_unified_capture()