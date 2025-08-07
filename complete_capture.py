#!/usr/bin/env python3
"""
완전한 Computed Style 캡처 - 놓친 파일들까지 모두 포함
"""

import subprocess
import json
import time
from pathlib import Path
import tempfile

def detect_computed_size(html_file):
    """Computed Style에서 width, height 읽기"""
    
    # Computed Style 읽기 JavaScript
    computed_detection_js = '''
    window.addEventListener('load', function() {
        setTimeout(function() {
            const body = document.body;
            const computedStyle = window.getComputedStyle(body);
            
            // Computed에서 직접 width, height 읽기
            const computedWidth = parseFloat(computedStyle.width);
            const computedHeight = parseFloat(computedStyle.height);
            
            // 실제 렌더링된 크기와 비교
            const actualWidth = Math.max(
                computedWidth,
                body.scrollWidth,
                body.offsetWidth,
                body.clientWidth
            );
            
            const actualHeight = Math.max(
                computedHeight, 
                body.scrollHeight,
                body.offsetHeight,
                body.clientHeight
            );
            
            // 안전 마진 추가
            const finalWidth = Math.ceil(actualWidth) + 50;
            const finalHeight = Math.ceil(actualHeight) + 50;
            
            console.log('COMPUTED_SIZE_DETECTION:', JSON.stringify({
                computedWidth: computedWidth,
                computedHeight: computedHeight,
                actualWidth: actualWidth,
                actualHeight: actualHeight,
                finalWidth: finalWidth,
                finalHeight: finalHeight,
                file: window.location.pathname.split('/').pop()
            }));
            
            // 결과를 title에 저장
            document.title = `COMPUTED:${finalWidth}x${finalHeight}:${document.title}`;
            
        }, 3500); // Chart.js 완전 로딩 대기
    });
    '''
    
    # 원본 HTML 읽기
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # JavaScript 주입
    modified_content = content.replace(
        '</head>', 
        f'<script>{computed_detection_js}</script>\n</head>'
    )
    
    # 임시 파일 생성
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as tmp:
        tmp.write(modified_content)
        temp_file = tmp.name
    
    try:
        # Chrome에서 Computed 크기 감지
        result = subprocess.run([
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            '--headless',
            '--disable-gpu', 
            '--disable-web-security',
            '--virtual-time-budget=6000',  # 6초 대기
            '--dump-dom',
            f'file://{Path(temp_file).absolute()}'
        ], capture_output=True, text=True, timeout=12)
        
        # title에서 크기 정보 추출
        if 'COMPUTED:' in result.stdout:
            for line in result.stdout.split('\n'):
                if 'COMPUTED:' in line and '<title>' in line:
                    try:
                        size_part = line.split('COMPUTED:')[1].split(':')[0]
                        if 'x' in size_part:
                            width, height = map(int, size_part.split('x'))
                            return width, height
                    except:
                        pass
        
        # 개선된 기본값
        filename = Path(html_file).name
        computed_fallbacks = {
            'market_growth_line.html': (950, 650),
            'budget_pie.html': (650, 650),
            'budget_trend.html': (950, 650),
            'budget_distribution.html': (950, 650),
            'market_growth_regional.html': (950, 650),
            'trl_roadmap.html': (1450, 750),
            'system_architecture.html': (1150, 750),
            'swot_analysis.html': (900, 950),
            'risk_matrix.html': (700, 750),
            'organization_chart.html': (1200, 850),
            'gantt_schedule.html': (1400, 700)
        }
        
        return computed_fallbacks.get(filename, (900, 700))
        
    except Exception as e:
        print(f"   ⚠️  Computed 크기 감지 실패: {e}")
        return (900, 700)
    finally:
        # 임시 파일 삭제
        try:
            Path(temp_file).unlink()
        except:
            pass

def complete_capture_all():
    """모든 HTML 파일에 대한 완전한 캡처"""
    
    # 모든 HTML 파일 포함
    html_files = [
        "images/market_growth_line.html",
        "images/market_growth_regional.html",
        "images/budget_pie.html", 
        "images/budget_trend.html",
        "images/budget_distribution.html",
        "images/trl_roadmap.html",
        "images/system_architecture.html",
        "images/swot_analysis.html",
        "images/risk_matrix.html",
        "images/organization_chart.html",
        "images/gantt_schedule.html"
    ]
    
    print("🎯 완전한 Computed Style 캡처 시스템 - 모든 파일 포함")
    print("=" * 60)
    
    completed = 0
    total = len([f for f in html_files if Path(f).exists()])
    
    for html_file in html_files:
        if not Path(html_file).exists():
            print(f"⚠️  {Path(html_file).name} 파일 없음")
            continue
            
        filename = Path(html_file).name
        print(f"\n📐 {filename} Computed 크기 감지...")
        
        # 1. Computed Style에서 정확한 크기 감지
        width, height = detect_computed_size(html_file)
        print(f"   📏 Computed 크기: {width}x{height}")
        
        # 2. 감지된 크기로 정확한 캡처
        output_file = html_file.replace('.html', '.png')
        
        try:
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
                '--virtual-time-budget=5000',
                f'--screenshot={output_file}',
                f'file://{Path(html_file).absolute()}'
            ], check=True, timeout=15)
            
            if Path(output_file).exists():
                file_size = Path(output_file).stat().st_size
                completed += 1
                print(f"   ✅ 완료: {file_size:,} bytes ({completed}/{total})")
            else:
                print(f"   ❌ 파일 생성 실패")
                
        except Exception as e:
            print(f"   ❌ 캡처 실패: {e}")
    
    print(f"\n🎉 완전한 캡처 완료: {completed}/{total}개 파일!")

if __name__ == "__main__":
    complete_capture_all()