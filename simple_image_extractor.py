#!/usr/bin/env python3
"""
Chrome 헤드리스 모드를 사용한 HTML 차트 이미지 추출기
selenium 없이 Chrome CLI로 직접 스크린샷 촬영
"""

import os
import glob
import subprocess
import time

class SimpleImageExtractor:
    def __init__(self):
        self.output_dir = "/Users/dykim/dev/make-docs/extracted_images"
        os.makedirs(self.output_dir, exist_ok=True)
        print(f"📁 이미지 저장 디렉토리: {self.output_dir}")
        
    def extract_image_from_html(self, html_file_path: str) -> str:
        """HTML 파일에서 Chrome 헤드리스로 이미지 추출"""
        try:
            # HTML 파일을 절대 경로로 변환
            abs_path = os.path.abspath(html_file_path)
            file_url = f"file://{abs_path}"
            
            # 출력 파일명 생성
            filename = os.path.basename(html_file_path).replace('.html', '.png')
            output_path = os.path.join(self.output_dir, filename)
            
            print(f"🔄 처리 중: {filename}")
            
            # Chrome 헤드리스 명령어
            chrome_cmd = [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "--headless",
                "--disable-gpu",
                "--hide-scrollbars", 
                "--force-device-scale-factor=1",
                "--window-size=900,600",
                f"--screenshot={output_path}",
                file_url
            ]
            
            # Chrome 실행
            result = subprocess.run(chrome_cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and os.path.exists(output_path):
                print(f"✅ 이미지 추출 완료: {filename}")
                return output_path
            else:
                print(f"❌ Chrome 실행 실패: {filename}")
                if result.stderr:
                    print(f"   오류: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            print(f"❌ 시간 초과: {os.path.basename(html_file_path)}")
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
            print(f"\n[{i}/{len(rwsl_files)}]")
            
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
            print(f"실패한 파일들:")
            for failed in failed_files:
                print(f"  - {failed}")
        
        # 추출된 파일 목록 표시
        if extracted_count > 0:
            print(f"\n📋 추출된 파일들:")
            png_files = glob.glob(os.path.join(self.output_dir, "rwsl*.png"))
            for png_file in sorted(png_files):
                print(f"  📄 {os.path.basename(png_file)}")
        
        return extracted_count

def main():
    """메인 함수"""
    try:
        extractor = SimpleImageExtractor()
        extracted_count = extractor.extract_rwsl_charts()
        
        print(f"\n📊 최종 결과: {extracted_count}개 이미지 추출 완료")
        print(f"📁 저장 위치: {extractor.output_dir}")
        
        # images 폴더로 복사하기
        if extracted_count > 0:
            print(f"\n🔄 images 폴더로 복사 중...")
            import shutil
            
            png_files = glob.glob(os.path.join(extractor.output_dir, "rwsl*.png"))
            copied_count = 0
            
            for png_file in png_files:
                filename = os.path.basename(png_file)
                dest_path = f"/Users/dykim/dev/make-docs/images/{filename}"
                
                try:
                    shutil.copy2(png_file, dest_path)
                    print(f"✅ 복사 완료: {filename}")
                    copied_count += 1
                except Exception as e:
                    print(f"❌ 복사 실패 {filename}: {e}")
            
            print(f"\n🎉 최종 완료: {copied_count}개 파일이 images 폴더에 저장됨")
        
    except Exception as e:
        print(f"❌ 전체 오류: {e}")

if __name__ == "__main__":
    main()