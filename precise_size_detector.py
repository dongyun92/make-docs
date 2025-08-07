#!/usr/bin/env python3
"""
더 정확한 body 크기 측정을 위한 스크립트
개발자 도구에서 확인할 수 있는 방식 구현
"""

import subprocess
import json
import time
from pathlib import Path

def create_size_measurement_html(original_html):
    """크기 측정용 HTML 생성"""
    
    # 원본 HTML 읽기
    with open(original_html, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 크기 측정 JavaScript 추가
    measurement_js = """
<script>
window.addEventListener('load', function() {
    // Chart.js가 완전히 로드되기까지 대기
    setTimeout(function() {
        const body = document.body;
        const rect = body.getBoundingClientRect();
        const computedStyle = window.getComputedStyle(body);
        
        // 실제 필요한 크기 계산 (padding, margin 포함)
        const actualWidth = Math.ceil(rect.width);
        const actualHeight = Math.ceil(rect.height);
        
        // 결과를 페이지에 표시
        const resultDiv = document.createElement('div');
        resultDiv.style.position = 'fixed';
        resultDiv.style.top = '10px';
        resultDiv.style.left = '10px';
        resultDiv.style.background = 'rgba(0,0,0,0.8)';
        resultDiv.style.color = 'white';
        resultDiv.style.padding = '10px';
        resultDiv.style.fontSize = '14px';
        resultDiv.style.fontFamily = 'monospace';
        resultDiv.style.zIndex = '9999';
        resultDiv.style.borderRadius = '5px';
        
        resultDiv.innerHTML = `
            <strong>Body 크기 측정 결과:</strong><br>
            Width: ${actualWidth}px<br>
            Height: ${actualHeight}px<br>
            <br>
            <strong>Chrome 캡처 명령어:</strong><br>
            --window-size=${actualWidth},${actualHeight}
        `;
        
        document.body.appendChild(resultDiv);
        
        // 콘솔에도 출력
        console.log('PRECISE_SIZE:', JSON.stringify({
            width: actualWidth,
            height: actualHeight,
            file: '${Path(original_html).name}'
        }));
        
    }, 3000); // 3초 대기 (Chart.js 완전 로딩)
});
</script>
</body>
"""
    
    # </body> 태그 직전에 측정 스크립트 삽입
    modified_content = content.replace('</body>', measurement_js)
    
    # 임시 파일로 저장
    temp_file = f"temp_measure_{Path(original_html).name}"
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(modified_content)
    
    return temp_file

def measure_and_open_all():
    """모든 HTML에 크기 측정 기능 추가하고 브라우저에서 열기"""
    
    html_files = [
        "images/market_growth_line.html",
        "images/budget_pie.html", 
        "images/trl_roadmap.html",
        "images/system_architecture.html",
        "images/swot_analysis.html",
        "images/risk_matrix.html"
    ]
    
    print("=== 정확한 크기 측정을 위한 HTML 생성 ===\n")
    
    temp_files = []
    
    for html_file in html_files:
        if Path(html_file).exists():
            print(f"📏 {Path(html_file).name} 측정용 HTML 생성...")
            temp_file = create_size_measurement_html(html_file)
            temp_files.append(temp_file)
            
            # 크롬에서 열기
            subprocess.run([
                "open", "-a", "Google Chrome", 
                f"file://{Path(temp_file).absolute()}"
            ])
            
            print(f"   ✅ {temp_file} 브라우저에서 열림")
        else:
            print(f"   ❌ {html_file} 파일 없음")
    
    print(f"\n=== 브라우저에서 확인하세요 ===")
    print("각 탭에서 좌상단의 크기 정보를 확인하고,")
    print("개발자 도구 콘솔에서도 PRECISE_SIZE 로그를 확인할 수 있습니다.")
    
    input("\n측정이 완료되면 Enter를 눌러주세요...")
    
    # 임시 파일들 정리
    for temp_file in temp_files:
        if Path(temp_file).exists():
            Path(temp_file).unlink()
            print(f"🗑️  {temp_file} 삭제")

if __name__ == "__main__":
    measure_and_open_all()