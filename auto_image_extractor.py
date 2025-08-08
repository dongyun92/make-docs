#!/usr/bin/env python3
"""
Selenium을 사용한 HTML 차트 자동 이미지 추출기
브라우저를 자동화하여 HTML 파일에서 이미지를 직접 추출하고 저장
"""

import os
import time
import glob
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AutoImageExtractor:
    def __init__(self):
        self.setup_driver()
        
    def setup_driver(self):
        """Chrome WebDriver 설정"""
        options = Options()
        # 헤드리스 모드 (백그라운드 실행)
        # options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=900,600')
        
        # 다운로드 디렉토리 설정
        download_dir = "/Users/dykim/dev/make-docs/extracted_images"
        os.makedirs(download_dir, exist_ok=True)
        
        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        options.add_experimental_option("prefs", prefs)
        
        self.driver = webdriver.Chrome(options=options)
        print(f"✅ Chrome WebDriver 초기화 완료")
        print(f"📁 이미지 저장 디렉토리: {download_dir}")
        
    def extract_image_from_html(self, html_file_path: str) -> str:
        """HTML 파일에서 이미지를 추출하여 저장"""
        try:
            # HTML 파일을 절대 경로로 변환
            abs_path = os.path.abspath(html_file_path)
            file_url = f"file://{abs_path}"
            
            print(f"🔄 처리 중: {os.path.basename(html_file_path)}")
            
            # HTML 파일 로드
            self.driver.get(file_url)
            
            # 페이지 로드 대기 (차트 렌더링 완료까지)
            time.sleep(3)
            
            # JavaScript로 html2canvas 실행하여 이미지 생성
            script = """
            return new Promise((resolve) => {
                html2canvas(document.body, {
                    useCORS: true,
                    allowTaint: true,
                    scale: 2,
                    backgroundColor: '#ffffff',
                    width: 900,
                    height: 600
                }).then(function(canvas) {
                    const imgData = canvas.toDataURL('image/png');
                    resolve(imgData);
                }).catch(function(error) {
                    console.error('캡처 실패:', error);
                    resolve(null);
                });
            });
            """
            
            # JavaScript 실행하여 이미지 데이터 얻기
            img_data = self.driver.execute_async_script(script)
            
            if img_data:
                # base64 데이터를 파일로 저장
                import base64
                img_data = img_data.split(',')[1]  # "data:image/png;base64," 부분 제거
                img_bytes = base64.b64decode(img_data)
                
                # 파일명 생성
                filename = os.path.basename(html_file_path).replace('.html', '.png')
                output_path = f"/Users/dykim/dev/make-docs/extracted_images/{filename}"
                
                with open(output_path, 'wb') as f:
                    f.write(img_bytes)
                
                print(f"✅ 이미지 추출 완료: {filename}")
                return output_path
            else:
                print(f"❌ 이미지 추출 실패: {os.path.basename(html_file_path)}")
                return None
                
        except Exception as e:
            print(f"❌ 오류 발생 {os.path.basename(html_file_path)}: {e}")
            return None
    
    def extract_rwsl_charts(self):
        """RWSL 관련 HTML 차트들을 모두 추출"""
        
        # RWSL 관련 HTML 파일만 필터링
        all_html_files = glob.glob('/Users/dykim/dev/make-docs/images/*.html')
        rwsl_files = [f for f in all_html_files if 'rwsl' in os.path.basename(f).lower()]
        
        print(f"🎯 RWSL 차트 파일 발견: {len(rwsl_files)}개")
        
        extracted_count = 0
        failed_files = []
        
        for i, html_file in enumerate(rwsl_files, 1):
            print(f"\n[{i}/{len(rwsl_files)}] 처리 중...")
            
            result = self.extract_image_from_html(html_file)
            if result:
                extracted_count += 1
            else:
                failed_files.append(os.path.basename(html_file))
            
            # 각 파일 처리 후 잠시 대기
            time.sleep(1)
        
        print(f"\n🎉 RWSL 차트 추출 완료!")
        print(f"✅ 성공: {extracted_count}개")
        print(f"❌ 실패: {len(failed_files)}개")
        
        if failed_files:
            print(f"실패한 파일들: {', '.join(failed_files)}")
        
        return extracted_count
    
    def extract_all_charts(self):
        """모든 HTML 차트를 추출"""
        
        html_files = glob.glob('/Users/dykim/dev/make-docs/images/*.html')
        
        # 추출기 파일은 제외
        html_files = [f for f in html_files if 'extractor' not in os.path.basename(f).lower()]
        
        print(f"🎯 전체 차트 파일: {len(html_files)}개")
        
        extracted_count = 0
        failed_files = []
        
        for i, html_file in enumerate(html_files, 1):
            print(f"\n[{i}/{len(html_files)}] 처리 중...")
            
            result = self.extract_image_from_html(html_file)
            if result:
                extracted_count += 1
            else:
                failed_files.append(os.path.basename(html_file))
            
            # 각 파일 처리 후 잠시 대기
            time.sleep(0.5)
        
        print(f"\n🎉 전체 차트 추출 완료!")
        print(f"✅ 성공: {extracted_count}개")
        print(f"❌ 실패: {len(failed_files)}개")
        
        if failed_files:
            print(f"실패한 파일들: {', '.join(failed_files)}")
        
        return extracted_count
    
    def close(self):
        """WebDriver 종료"""
        if hasattr(self, 'driver'):
            self.driver.quit()
            print("🔄 WebDriver 종료됨")

def main():
    """메인 함수"""
    extractor = None
    
    try:
        extractor = AutoImageExtractor()
        
        print("선택하세요:")
        print("1. RWSL 차트만 추출 (18개)")
        print("2. 모든 차트 추출 (50개)")
        
        # 기본적으로 RWSL 차트만 추출
        choice = "1"  # 자동으로 RWSL 차트 추출
        
        if choice == "1":
            extracted_count = extractor.extract_rwsl_charts()
        else:
            extracted_count = extractor.extract_all_charts()
        
        print(f"\n📊 최종 결과: {extracted_count}개 이미지 추출 완료")
        print(f"📁 저장 위치: /Users/dykim/dev/make-docs/extracted_images/")
        
    except Exception as e:
        print(f"❌ 전체 오류: {e}")
    
    finally:
        if extractor:
            extractor.close()

if __name__ == "__main__":
    main()