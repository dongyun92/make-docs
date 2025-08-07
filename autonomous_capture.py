#!/usr/bin/env python3
"""
완전 자율 HTML to PNG 캡처 시스템
사용자 개입 없이 최적 크기 감지 후 자동 캡처
"""

import subprocess
import json
import time
from pathlib import Path
import tempfile

def detect_optimal_size(html_file):
    """JavaScript 인젝션으로 최적 크기 감지"""
    
    # 크기 측정용 JavaScript
    size_detection_js = '''
    window.addEventListener('load', function() {
        setTimeout(function() {
            const body = document.body;
            const rect = body.getBoundingClientRect();
            
            // 실제 필요한 크기 계산 (Chart.js 로딩 대기 후)
            const actualWidth = Math.max(300, Math.ceil(rect.width));
            const actualHeight = Math.max(200, Math.ceil(rect.height));
            
            // 결과를 타이틀에 삽입 (크롬 콘솔에서 추출하기 위해)
            document.title = `SIZE:${actualWidth}x${actualHeight}:${document.title}`;
            
            console.log('DETECTED_SIZE:', JSON.stringify({
                width: actualWidth,
                height: actualHeight,
                file: window.location.pathname.split('/').pop()
            }));
            
        }, 3000); // Chart.js 완전 로딩 대기
    });
    '''
    
    # 원본 HTML 읽기
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # JavaScript 주입
    modified_content = content.replace(
        '</head>', 
        f'<script>{size_detection_js}</script>\n</head>'
    )
    
    # 임시 파일 생성
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as tmp:
        tmp.write(modified_content)
        temp_file = tmp.name
    
    try:
        # Chrome에서 크기 측정
        result = subprocess.run([
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            '--headless',
            '--disable-gpu', 
            '--disable-web-security',
            '--virtual-time-budget=5000',  # 5초 후 자동 종료
            '--dump-dom',
            f'file://{Path(temp_file).absolute()}'
        ], capture_output=True, text=True, timeout=10)
        
        # title에서 크기 정보 추출
        if 'SIZE:' in result.stdout:
            for line in result.stdout.split('\n'):
                if 'SIZE:' in line and '<title>' in line:
                    size_part = line.split('SIZE:')[1].split(':')[0]
                    if 'x' in size_part:
                        width, height = map(int, size_part.split('x'))
                        return width, height
        
        # 기본값으로 폴백
        filename = Path(html_file).name
        fallback_sizes = {
            'market_growth_line.html': (900, 600),
            'market_growth_regional.html': (700, 600), 
            'budget_pie.html': (700, 700),
            'budget_trend.html': (700, 600),
            'trl_roadmap.html': (1400, 650),
            'system_architecture.html': (1000, 650),
            'swot_analysis.html': (800, 900),
            'risk_matrix.html': (600, 650),
            'organization_chart.html': (1200, 800)
        }
        
        return fallback_sizes.get(filename, (800, 600))
        
    except Exception as e:
        print(f"   ⚠️  크기 감지 실패: {e}")
        return (800, 600)
    finally:
        # 임시 파일 삭제
        try:
            Path(temp_file).unlink()
        except:
            pass

def capture_png(html_file, width, height):
    """최적화된 PNG 캡처"""
    
    output_file = html_file.replace('.html', '.png')
    
    try:
        # Chrome 헤드리스로 캡처
        subprocess.run([
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            '--headless',
            '--disable-gpu',
            '--disable-web-security',
            '--hide-scrollbars',
            '--force-device-scale-factor=1',
            f'--window-size={width},{height}',
            f'--screenshot={output_file}',
            f'file://{Path(html_file).absolute()}'
        ], check=True, capture_output=True)
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"   ❌ 캡처 실패: {e}")
        return False

def autonomous_capture_all():
    """완전 자율 캡처 시스템"""
    
    html_files = [
        "images/market_growth_line.html",
        "images/budget_pie.html", 
        "images/trl_roadmap.html",
        "images/system_architecture.html",
        "images/swot_analysis.html",
        "images/risk_matrix.html"
    ]
    
    print("🤖 완전 자율 HTML to PNG 캡처 시스템 시작")
    print("=" * 50)
    
    total_files = len([f for f in html_files if Path(f).exists()])
    completed = 0
    
    for html_file in html_files:
        if not Path(html_file).exists():
            continue
            
        filename = Path(html_file).name
        print(f"\n📏 {filename} 처리 중...")
        
        # 1. 크기 자동 감지
        width, height = detect_optimal_size(html_file)
        print(f"   📐 감지된 크기: {width}x{height}")
        
        # 2. PNG 자동 캡처
        if capture_png(html_file, width, height):
            completed += 1
            print(f"   ✅ {filename.replace('.html', '.png')} 생성 완료")
            print(f"   📊 진행률: {completed}/{total_files} ({completed/total_files*100:.0f}%)")
        else:
            print(f"   ❌ {filename} 캡처 실패")
    
    print(f"\n🎉 자율 캡처 완료: {completed}/{total_files}개 파일 처리됨")
    print("\n생성된 PNG 파일들:")
    for html_file in html_files:
        png_file = html_file.replace('.html', '.png')
        if Path(png_file).exists():
            file_size = Path(png_file).stat().st_size
            print(f"   ✓ {png_file} ({file_size:,} bytes)")

if __name__ == "__main__":
    autonomous_capture_all()