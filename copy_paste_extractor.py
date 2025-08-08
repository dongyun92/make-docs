#!/usr/bin/env python3
"""
우클릭 -> 이미지 복사 -> 클립보드에서 PNG 파일로 저장하는 방식
Selenium으로 우클릭 복사 자동화 후 클립보드 내용을 파일로 저장
"""

import os
import time
import glob
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import subprocess
from PIL import ImageGrab
import io

class CopyPasteExtractor:
    def __init__(self):
        self.setup_driver()
        self.output_dir = "/Users/dykim/dev/make-docs/copied_images"
        os.makedirs(self.output_dir, exist_ok=True)
        print(f"📁 이미지 저장 디렉토리: {self.output_dir}")
        
    def setup_driver(self):
        """Chrome WebDriver 설정"""
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1000,700')
        
        self.driver = webdriver.Chrome(options=options)
        print(f"✅ Chrome WebDriver 초기화 완료")
        
    def copy_image_from_html(self, html_file_path: str) -> str:
        """HTML 파일에서 차트를 우클릭으로 복사하여 클립보드에서 파일로 저장"""
        try:
            # HTML 파일을 절대 경로로 변환
            abs_path = os.path.abspath(html_file_path)
            file_url = f"file://{abs_path}"
            
            filename = os.path.basename(html_file_path).replace('.html', '.png')
            print(f"🔄 처리 중: {filename}")
            
            # HTML 파일 로드
            self.driver.get(file_url)
            
            # 페이지 로드 및 차트 렌더링 대기
            time.sleep(3)
            
            # canvas 요소 찾기 (Chart.js는 canvas를 사용)
            try:
                canvas = self.driver.find_element(By.TAG_NAME, "canvas")
                print("   🎯 차트 canvas 요소 발견")
                
                # canvas 우클릭
                actions = ActionChains(self.driver)
                actions.context_click(canvas).perform()
                print("   🖱️  차트 우클릭 실행")
                
                time.sleep(1)
                
                # 컨텍스트 메뉴에서 "이미지 복사" 클릭 (macOS Chrome)
                try:
                    # macOS에서는 보통 "Copy image" 메뉴가 있음
                    copy_menu = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Copy image') or contains(text(), '이미지 복사')]"))
                    )
                    copy_menu.click()
                    print("   📋 '이미지 복사' 메뉴 클릭")
                    
                except Exception as e:
                    print(f"   ❌ 컨텍스트 메뉴를 찾을 수 없음: {e}")
                    # ESC로 메뉴 닫기
                    actions.send_keys('\ue00c').perform()  # ESC key
                    
                    # 대안: JavaScript로 canvas를 클립보드에 복사
                    print("   🔄 JavaScript로 클립보드 복사 시도...")
                    self.driver.execute_script("""
                        const canvas = document.querySelector('canvas');
                        canvas.toBlob(function(blob) {
                            const item = new ClipboardItem({'image/png': blob});
                            navigator.clipboard.write([item]);
                        });
                    """)
                
                time.sleep(2)
                
                # 클립보드에서 이미지 가져와서 파일로 저장
                try:
                    # PIL을 사용해서 클립보드에서 이미지 가져오기
                    image = ImageGrab.grabclipboard()
                    if image:
                        output_path = os.path.join(self.output_dir, filename)
                        image.save(output_path, 'PNG')
                        print(f"✅ 클립보드에서 이미지 저장 완료: {filename}")
                        return output_path
                    else:
                        print("❌ 클립보드에 이미지가 없음")
                        return None
                        
                except Exception as e:
                    print(f"❌ 클립보드 처리 실패: {e}")
                    return None
                    
            except Exception as e:
                print(f"❌ canvas 요소를 찾을 수 없음: {e}")
                return None
                
        except Exception as e:
            print(f"❌ 오류 발생 {filename}: {e}")
            return None
    
    def copy_rwsl_charts(self):
        """RWSL 관련 HTML 차트들을 모두 복사"""
        
        # RWSL 관련 HTML 파일만 필터링
        all_html_files = glob.glob('/Users/dykim/dev/make-docs/images/*.html')
        rwsl_files = [f for f in all_html_files if 'rwsl' in os.path.basename(f).lower()]
        
        # 추출기 파일은 제외
        rwsl_files = [f for f in rwsl_files if 'extractor' not in os.path.basename(f).lower()]
        
        print(f"🎯 RWSL 차트 파일 발견: {len(rwsl_files)}개")
        
        copied_count = 0
        failed_files = []
        
        for i, html_file in enumerate(rwsl_files, 1):
            print(f"\n[{i}/{len(rwsl_files)}]")
            
            result = self.copy_image_from_html(html_file)
            if result:
                copied_count += 1
            else:
                failed_files.append(os.path.basename(html_file))
            
            # 각 파일 처리 후 잠시 대기
            time.sleep(2)
        
        print(f"\n🎉 RWSL 차트 복사 완료!")
        print(f"✅ 성공: {copied_count}개")
        print(f"❌ 실패: {len(failed_files)}개")
        
        if failed_files:
            print(f"실패한 파일들:")
            for failed in failed_files:
                print(f"  - {failed}")
        
        # 복사된 파일을 images 폴더로 이동
        if copied_count > 0:
            self.move_to_images_folder()
        
        return copied_count
    
    def move_to_images_folder(self):
        """복사된 파일들을 images 폴더로 이동"""
        print(f"\n🔄 images 폴더로 이동 중...")
        import shutil
        
        png_files = glob.glob(os.path.join(self.output_dir, "rwsl*.png"))
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
        extractor = CopyPasteExtractor()
        copied_count = extractor.copy_rwsl_charts()
        
        print(f"\n📊 최종 결과: {copied_count}개 이미지 클립보드 복사 완료")
        
    except Exception as e:
        print(f"❌ 전체 오류: {e}")
    
    finally:
        if extractor:
            extractor.close()

if __name__ == "__main__":
    main()