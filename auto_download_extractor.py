#!/usr/bin/env python3
"""
Selenium을 사용하여 html2canvas로 생성된 이미지를 자동으로 다운로드
브라우저에서 직접 이미지 다운로드 버튼 클릭하여 파일 저장
"""

import os
import time
import glob
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AutoDownloadExtractor:
    def __init__(self):
        self.setup_driver()
        
    def setup_driver(self):
        """Chrome WebDriver 설정 - 다운로드 자동화"""
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1000,700')
        
        # 다운로드 디렉토리 설정
        download_dir = "/Users/dykim/dev/make-docs/auto_downloads"
        os.makedirs(download_dir, exist_ok=True)
        
        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        options.add_experimental_option("prefs", prefs)
        
        self.driver = webdriver.Chrome(options=options)
        self.download_dir = download_dir
        print(f"✅ Chrome WebDriver 초기화 완료")
        print(f"📁 다운로드 디렉토리: {download_dir}")
        
    def download_image_from_html(self, html_file_path: str) -> str:
        """HTML 파일에서 html2canvas로 이미지를 생성하고 자동 다운로드"""
        try:
            # HTML 파일을 절대 경로로 변환
            abs_path = os.path.abspath(html_file_path)
            file_url = f"file://{abs_path}"
            
            filename = os.path.basename(html_file_path)
            print(f"🔄 처리 중: {filename}")
            
            # HTML 파일 로드
            self.driver.get(file_url)
            
            # 페이지 로드 및 html2canvas 실행 대기 (자동 다운로드 버튼 생성까지)
            print("   ⏳ html2canvas 실행 및 다운로드 버튼 생성 대기...")
            time.sleep(4)
            
            # 다운로드 버튼 찾기 (우상단에 생성됨)
            try:
                download_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "이미지 다운로드"))
                )
                
                print("   📥 다운로드 버튼 클릭...")
                download_button.click()
                
                # 다운로드 완료 대기
                time.sleep(3)
                
                # 다운로드된 파일명 확인
                expected_filename = filename.replace('.html', '.png')
                download_path = os.path.join(self.download_dir, expected_filename)
                
                if os.path.exists(download_path):
                    print(f"✅ 다운로드 완료: {expected_filename}")
                    return download_path
                else:
                    print(f"❌ 다운로드 실패: 파일을 찾을 수 없음")
                    return None
                    
            except Exception as e:
                print(f"❌ 다운로드 버튼을 찾을 수 없음: {e}")
                return None
                
        except Exception as e:
            print(f"❌ 오류 발생 {filename}: {e}")
            return None
    
    def download_rwsl_charts(self):
        """RWSL 관련 HTML 차트들을 모두 다운로드"""
        
        # RWSL 관련 HTML 파일만 필터링
        all_html_files = glob.glob('/Users/dykim/dev/make-docs/images/*.html')
        rwsl_files = [f for f in all_html_files if 'rwsl' in os.path.basename(f).lower()]
        
        # 추출기 파일은 제외
        rwsl_files = [f for f in rwsl_files if 'extractor' not in os.path.basename(f).lower()]
        
        print(f"🎯 RWSL 차트 파일 발견: {len(rwsl_files)}개")
        
        downloaded_count = 0
        failed_files = []
        
        for i, html_file in enumerate(rwsl_files, 1):
            print(f"\n[{i}/{len(rwsl_files)}]")
            
            result = self.download_image_from_html(html_file)
            if result:
                downloaded_count += 1
            else:
                failed_files.append(os.path.basename(html_file))
            
            # 각 파일 처리 후 잠시 대기
            time.sleep(2)
        
        print(f"\n🎉 RWSL 차트 다운로드 완료!")
        print(f"✅ 성공: {downloaded_count}개")
        print(f"❌ 실패: {len(failed_files)}개")
        
        if failed_files:
            print(f"실패한 파일들:")
            for failed in failed_files:
                print(f"  - {failed}")
        
        # 다운로드된 파일을 images 폴더로 이동
        if downloaded_count > 0:
            self.move_to_images_folder()
        
        return downloaded_count
    
    def move_to_images_folder(self):
        """다운로드된 파일들을 images 폴더로 이동"""
        print(f"\n🔄 images 폴더로 이동 중...")
        import shutil
        
        png_files = glob.glob(os.path.join(self.download_dir, "rwsl*.png"))
        moved_count = 0
        
        for png_file in png_files:
            filename = os.path.basename(png_file)
            dest_path = f"/Users/dykim/dev/make-docs/images/{filename}"
            
            try:
                # 기존 파일이 있으면 덮어쓰기
                if os.path.exists(dest_path):
                    os.remove(dest_path)
                    
                shutil.move(png_file, dest_path)
                print(f"✅ 이동 완료: {filename}")
                moved_count += 1
            except Exception as e:
                print(f"❌ 이동 실패 {filename}: {e}")
        
        print(f"🎉 최종 완료: {moved_count}개 파일이 images 폴더로 이동됨")
    
    def close(self):
        """WebDriver 종료"""
        if hasattr(self, 'driver'):
            self.driver.quit()
            print("🔄 WebDriver 종료됨")

def main():
    """메인 함수"""
    extractor = None
    
    try:
        extractor = AutoDownloadExtractor()
        downloaded_count = extractor.download_rwsl_charts()
        
        print(f"\n📊 최종 결과: {downloaded_count}개 이미지 자동 다운로드 완료")
        
    except Exception as e:
        print(f"❌ 전체 오류: {e}")
    
    finally:
        if extractor:
            extractor.close()

if __name__ == "__main__":
    main()