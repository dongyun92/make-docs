#!/usr/bin/env python3
"""
개선된 동적 크기 감지 시스템
Puppeteer 스타일의 JavaScript 실행으로 정확한 크기 감지
"""

import subprocess
import json
import time
import os
from pathlib import Path
import tempfile

class DynamicSizeDetectorV2:
    def __init__(self):
        self.chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        self.temp_dir = Path("temp_size_detection")
        self.temp_dir.mkdir(exist_ok=True)
    
    def create_size_detection_html(self, original_html):
        """크기 감지용 HTML 파일 생성"""
        with open(original_html, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 크기 감지 및 결과 저장 스크립트
        detection_script = """
        <script>
        async function detectAndSaveSize() {
            // 페이지 완전 로딩 대기
            await new Promise(resolve => {
                if (document.readyState === 'complete') {
                    resolve();
                } else {
                    window.addEventListener('load', resolve);
                }
            });
            
            // 추가 렌더링 시간 대기
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            // 실제 콘텐츠 크기 계산
            const body = document.body;
            const html = document.documentElement;
            
            // 모든 요소의 경계 상자 계산
            const allElements = document.querySelectorAll('*');
            let maxRight = 0;
            let maxBottom = 0;
            
            allElements.forEach(el => {
                const rect = el.getBoundingClientRect();
                maxRight = Math.max(maxRight, rect.right);
                maxBottom = Math.max(maxBottom, rect.bottom);
            });
            
            // scroll 크기와 비교하여 최대값 사용
            const scrollWidth = Math.max(body.scrollWidth, html.scrollWidth, maxRight);
            const scrollHeight = Math.max(body.scrollHeight, html.scrollHeight, maxBottom);
            
            const result = {
                width: Math.ceil(scrollWidth) + 40,  // 여백 20px씩
                height: Math.ceil(scrollHeight) + 40,
                detected_at: new Date().toISOString(),
                method: 'boundingRect_and_scroll'
            };
            
            // 결과를 페이지 제목으로 저장 (쉽게 추출 가능)
            document.title = 'SIZE_RESULT:' + JSON.stringify(result);
            
            // body에도 데이터 속성으로 저장
            document.body.setAttribute('data-detected-size', JSON.stringify(result));
            
            console.log('Detection completed:', result);
        }
        
        // 스크립트 실행
        detectAndSaveSize();
        </script>
        """
        
        # body 끝에 스크립트 추가
        if '</body>' in content:
            content = content.replace('</body>', detection_script + '\n</body>')
        else:
            content = content.replace('</html>', detection_script + '\n</html>')
        
        # 임시 파일 생성
        temp_file = self.temp_dir / f"detect_{Path(original_html).name}"
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return temp_file
    
    def detect_content_size(self, html_file):
        """개선된 크기 감지"""
        print(f"크기 감지 중: {html_file}")
        
        # 감지용 HTML 생성
        detection_html = self.create_size_detection_html(html_file)
        
        try:
            # Chrome으로 페이지 로드 및 JavaScript 실행
            cmd = [
                self.chrome_path,
                "--headless",
                "--disable-gpu",
                "--disable-web-security", 
                "--no-sandbox",
                "--run-all-compositor-stages-before-draw",
                "--disable-background-timer-throttling",
                "--disable-backgrounding-occluded-windows",
                "--disable-renderer-backgrounding",
                f"--dump-dom",
                f"file://{detection_html.absolute()}"
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=15
            )
            
            # HTML DOM에서 크기 정보 추출
            dom_content = result.stdout
            size_info = self._extract_size_from_dom(dom_content)
            
            if size_info:
                print(f"감지된 크기: {size_info['width']}x{size_info['height']} ({size_info['method']})")
                return size_info
            
            # DOM에서 추출 실패시 title에서 추출 시도
            size_info = self._extract_size_from_title(dom_content)
            if size_info:
                print(f"감지된 크기 (title): {size_info['width']}x{size_info['height']}")
                return size_info
            
            print("크기 감지 실패, 기본값 사용")
            return self._get_fallback_size(html_file)
            
        except Exception as e:
            print(f"크기 감지 오류: {e}")
            return self._get_fallback_size(html_file)
        finally:
            # 임시 파일 정리
            if detection_html.exists():
                detection_html.unlink()
    
    def _extract_size_from_dom(self, dom_content):
        """DOM 내용에서 크기 정보 추출"""
        try:
            # data-detected-size 속성 찾기
            import re
            pattern = r'data-detected-size="([^"]*)"'
            match = re.search(pattern, dom_content)
            
            if match:
                json_str = match.group(1).replace('&quot;', '"')
                size_data = json.loads(json_str)
                return {
                    "width": int(size_data['width']),
                    "height": int(size_data['height']),
                    "method": size_data.get('method', 'dom_attribute'),
                    "detected_at": size_data.get('detected_at', '')
                }
        except Exception as e:
            print(f"DOM 파싱 오류: {e}")
        
        return None
    
    def _extract_size_from_title(self, dom_content):
        """title 태그에서 크기 정보 추출"""
        try:
            import re
            pattern = r'<title>SIZE_RESULT:([^<]*)</title>'
            match = re.search(pattern, dom_content)
            
            if match:
                json_str = match.group(1)
                size_data = json.loads(json_str)
                return {
                    "width": int(size_data['width']),
                    "height": int(size_data['height']),
                    "method": size_data.get('method', 'title'),
                    "detected_at": size_data.get('detected_at', '')
                }
        except Exception as e:
            print(f"Title 파싱 오류: {e}")
        
        return None
    
    def _get_fallback_size(self, html_file):
        """파일별 기본 크기 반환"""
        # 차트별 예상 크기 (기존 적응형 시스템 결과 기반)
        fallback_sizes = {
            "organization_chart.html": {"width": 1400, "height": 900},
            "trl_roadmap.html": {"width": 1350, "height": 750}, 
            "swot_analysis.html": {"width": 1200, "height": 900},
            "risk_matrix.html": {"width": 1200, "height": 800},
            "system_architecture.html": {"width": 1350, "height": 600},
            "gantt_schedule.html": {"width": 1600, "height": 1200}
        }
        
        filename = Path(html_file).name
        return fallback_sizes.get(filename, {"width": 1200, "height": 800})
    
    def batch_detect_sizes(self, html_files):
        """여러 파일의 크기 일괄 감지"""
        results = {}
        
        print("=== 동적 크기 감지 시작 ===\n")
        
        for html_file in html_files:
            if os.path.exists(html_file):
                size_info = self.detect_content_size(html_file)
                results[html_file] = size_info
                print()
            else:
                print(f"파일 없음: {html_file}\n")
        
        # 결과 요약
        print("=== 크기 감지 결과 요약 ===")
        for file, size in results.items():
            method = size.get('method', 'fallback')
            print(f"{Path(file).name}: {size['width']}x{size['height']} ({method})")
        
        return results

if __name__ == "__main__":
    detector = DynamicSizeDetectorV2()
    
    # 테스트할 HTML 파일들
    test_files = [
        "images/organization_chart.html",
        "images/trl_roadmap.html",
        "images/swot_analysis.html", 
        "images/risk_matrix.html",
        "images/system_architecture.html"
    ]
    
    # 일괄 크기 감지 실행
    results = detector.batch_detect_sizes(test_files)