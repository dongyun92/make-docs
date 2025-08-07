#!/usr/bin/env python3
"""
동적 크기 감지 시스템
브라우저 콘솔을 통해 실제 콘텐츠 크기를 감지하여 정확한 캡처 수행
"""

import subprocess
import json
import time
import os
from pathlib import Path

class DynamicSizeDetector:
    def __init__(self):
        self.chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        self.temp_dir = Path("temp_size_detection")
        self.temp_dir.mkdir(exist_ok=True)
    
    def add_size_detection_script(self, html_file):
        """HTML 파일에 크기 감지 JavaScript 추가"""
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # JavaScript 크기 감지 스크립트
        size_script = """
        <script>
        function getDynamicSize() {
            // 페이지 로드 완료 대기
            return new Promise((resolve) => {
                window.addEventListener('load', () => {
                    setTimeout(() => {
                        // 실제 콘텐츠 크기 계산
                        const body = document.body;
                        const html = document.documentElement;
                        
                        const width = Math.max(
                            body.scrollWidth,
                            body.offsetWidth,
                            html.clientWidth,
                            html.scrollWidth,
                            html.offsetWidth
                        );
                        
                        const height = Math.max(
                            body.scrollHeight,
                            body.offsetHeight,
                            html.clientHeight,
                            html.scrollHeight,
                            html.offsetHeight
                        );
                        
                        // 여백 추가 (각 방향 20px씩)
                        const result = {
                            width: width + 40,
                            height: height + 40,
                            detected_at: new Date().toISOString()
                        };
                        
                        // 콘솔에 JSON 형태로 출력
                        console.log('SIZE_DETECTION_RESULT:' + JSON.stringify(result));
                        resolve(result);
                    }, 500); // 렌더링 완료 대기
                });
            });
        }
        
        // 자동 실행
        getDynamicSize();
        </script>
        """
        
        # </body> 태그 바로 전에 스크립트 삽입
        if '</body>' in content:
            content = content.replace('</body>', size_script + '\n</body>')
        else:
            # body 태그가 없으면 html 끝에 추가
            content = content.replace('</html>', size_script + '\n</html>')
        
        # 임시 파일로 저장
        temp_file = self.temp_dir / f"temp_{Path(html_file).name}"
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return temp_file
    
    def detect_content_size(self, html_file):
        """브라우저를 통해 실제 콘텐츠 크기 감지"""
        print(f"콘텐츠 크기 감지 중: {html_file}")
        
        # 크기 감지 스크립트가 추가된 임시 HTML 생성
        temp_html = self.add_size_detection_script(html_file)
        
        try:
            # Chrome 헤드리스 모드로 실행하여 콘솔 로그 캡처
            cmd = [
                self.chrome_path,
                "--headless",
                "--disable-gpu",
                "--disable-web-security",
                "--no-sandbox",
                "--enable-logging",
                "--log-level=0",
                "--virtual-time-budget=5000",  # 5초 가상 시간
                f"file://{temp_html.absolute()}"
            ]
            
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            # 콘솔 출력에서 크기 정보 추출
            console_output = result.stderr
            size_info = self._extract_size_from_console(console_output)
            
            if size_info:
                print(f"감지된 크기: {size_info['width']}x{size_info['height']}")
                return size_info
            else:
                print("크기 감지 실패, 기본값 사용")
                return {"width": 1200, "height": 800}
                
        except subprocess.TimeoutExpired:
            print("크기 감지 타임아웃, 기본값 사용")
            return {"width": 1200, "height": 800}
        except Exception as e:
            print(f"크기 감지 오류: {e}, 기본값 사용")
            return {"width": 1200, "height": 800}
        finally:
            # 임시 파일 정리
            if temp_html.exists():
                temp_html.unlink()
    
    def _extract_size_from_console(self, console_output):
        """콘솔 출력에서 크기 정보 추출"""
        try:
            lines = console_output.split('\n')
            for line in lines:
                if 'SIZE_DETECTION_RESULT:' in line:
                    # JSON 부분만 추출
                    json_start = line.find('SIZE_DETECTION_RESULT:') + len('SIZE_DETECTION_RESULT:')
                    json_str = line[json_start:].strip()
                    
                    # JSON 파싱
                    size_data = json.loads(json_str)
                    return {
                        "width": int(size_data['width']),
                        "height": int(size_data['height']),
                        "detected_at": size_data.get('detected_at', '')
                    }
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"콘솔 출력 파싱 오류: {e}")
        
        return None
    
    def test_detection(self, html_file):
        """크기 감지 테스트"""
        print(f"\n=== 크기 감지 테스트: {html_file} ===")
        size_info = self.detect_content_size(html_file)
        
        print(f"결과:")
        print(f"- 폭: {size_info['width']}px")
        print(f"- 높이: {size_info['height']}px")
        if 'detected_at' in size_info:
            print(f"- 감지 시간: {size_info['detected_at']}")
        
        return size_info

if __name__ == "__main__":
    detector = DynamicSizeDetector()
    
    # 테스트할 HTML 파일들
    test_files = [
        "images/organization_chart.html",
        "images/trl_roadmap.html", 
        "images/swot_analysis.html",
        "images/risk_matrix.html"
    ]
    
    results = {}
    
    for html_file in test_files:
        if os.path.exists(html_file):
            size_info = detector.test_detection(html_file)
            results[html_file] = size_info
        else:
            print(f"파일 없음: {html_file}")
    
    print(f"\n=== 전체 감지 결과 요약 ===")
    for file, size in results.items():
        print(f"{file}: {size['width']}x{size['height']}")