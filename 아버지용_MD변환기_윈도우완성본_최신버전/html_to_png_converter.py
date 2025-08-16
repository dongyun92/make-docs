#!/usr/bin/env python3
"""
capture-website-cli를 사용하여 HTML 파일들을 PNG로 일괄 변환
전용 도구를 사용하므로 안정적이고 간단함
"""

import os
import glob
import subprocess
import time

class HTMLToPNGConverter:
    def __init__(self, output_dir=None):
        if output_dir is None:
            self.output_dir = os.path.join(os.getcwd(), "converted_images")
        else:
            self.output_dir = output_dir
        
        # 디렉토리 생성 시 예외 처리
        try:
            os.makedirs(self.output_dir, exist_ok=True)
            print(f"📁 이미지 저장 디렉토리: {self.output_dir}")
        except Exception as e:
            print(f"❌ 디렉토리 생성 실패: {e}")
            # 임시 디렉토리 사용
            import tempfile
            self.output_dir = tempfile.mkdtemp()
            print(f"📁 임시 디렉토리 사용: {self.output_dir}")
        
    def convert_html_to_png(self, html_file_path: str) -> str:
        """HTML 파일을 PNG로 변환 (Chrome 사용)"""
        try:
            filename = os.path.basename(html_file_path).replace('.html', '.png')
            output_path = os.path.join(self.output_dir, filename)
            
            print(f"🔄 변환 중: {filename}")
            
            # 기존 파일이 있으면 삭제
            if os.path.exists(output_path):
                os.remove(output_path)
            
            # macOS Chrome 경로 (Windows 경로 제거)
            chrome_paths = [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            ]
            
            chrome_path = None
            for path in chrome_paths:
                if os.path.exists(path):
                    chrome_path = path
                    print(f"🔍 Chrome 발견: {chrome_path}")
                    break
            
            if not chrome_path:
                print("❌ Chrome을 찾을 수 없습니다")
                print("   시도한 경로들:")
                for path in chrome_paths:
                    print(f"   - {path}: {'존재함' if os.path.exists(path) else '없음'}")
                return None
            
            # 절대 경로로 변환 (macOS)
            abs_html_path = os.path.abspath(html_file_path)
            file_url = f"file://{abs_html_path}"
            
            # Chrome 헤드리스 모드로 스크린샷
            cmd = [
                chrome_path,
                "--headless",
                "--disable-gpu",
                "--hide-scrollbars",
                "--force-device-scale-factor=1",
                "--window-size=1200,1400",
                f"--screenshot={output_path}",
                file_url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if os.path.exists(output_path):
                print(f"✅ 변환 완료: {filename}")
                return output_path
            else:
                print(f"❌ 변환 실패: {filename}")
                if result.stderr:
                    print(f"   오류: {result.stderr.strip()}")
                return None
                
        except subprocess.TimeoutExpired:
            print(f"❌ 시간 초과: {os.path.basename(html_file_path)}")
            return None
        except Exception as e:
            print(f"❌ 오류 발생 {os.path.basename(html_file_path)}: {e}")
            return None
    
    def convert_selected_files(self, html_files):
        """선택된 HTML 파일들을 PNG로 변환"""
        
        if not html_files:
            print("⚠️ 변환할 HTML 파일이 없습니다.")
            return 0
            
        print(f"🎯 변환할 HTML 파일: {len(html_files)}개")
        print("📋 선택된 파일 목록:")
        for i, html_file in enumerate(html_files, 1):
            print(f"   {i}. {html_file}")
            print(f"      존재 여부: {os.path.exists(html_file)}")
        
        converted_count = 0
        failed_files = []
        
        for i, html_file in enumerate(html_files, 1):
            print(f"\n[{i}/{len(html_files)}]")
            
            result = self.convert_html_to_png(html_file)
            if result:
                converted_count += 1
                # PNG 파일을 HTML 파일과 같은 디렉토리의 images 폴더로 복사
                self.copy_png_to_source_directory(result, html_file)
            else:
                failed_files.append(os.path.basename(html_file))
            
            # 각 파일 변환 후 잠시 대기
            time.sleep(0.5)
        
        print(f"\n🎉 HTML 차트 변환 완료!")
        print(f"✅ 성공: {converted_count}개")
        print(f"❌ 실패: {len(failed_files)}개")
        
        if failed_files:
            print(f"실패한 파일들:")
            for failed in failed_files:
                print(f"  - {failed}")
        
        return converted_count
    
    def copy_png_to_source_directory(self, png_path, html_file):
        """PNG 파일을 HTML 파일과 같은 디렉토리의 images 폴더로 복사"""
        try:
            # HTML 파일이 있는 디렉토리
            html_dir = os.path.dirname(html_file)
            images_dir = os.path.join(html_dir, "images")
            os.makedirs(images_dir, exist_ok=True)
            
            # PNG 파일명
            png_filename = os.path.basename(png_path)
            destination = os.path.join(images_dir, png_filename)
            
            # 파일 복사
            import shutil
            shutil.copy2(png_path, destination)
            print(f"📁 복사 완료: {png_filename} → {images_dir}")
            
        except Exception as e:
            print(f"❌ 복사 실패 {os.path.basename(png_path)}: {e}")
    
    def copy_to_images_folder(self):
        """변환된 파일들을 images 폴더로 복사"""
        print(f"\n🔄 images 폴더로 복사 중...")
        import shutil
        
        png_files = glob.glob(os.path.join(self.output_dir, "rwsl*.png"))
        copied_count = 0
        
        for png_file in png_files:
            filename = os.path.basename(png_file)
            dest_path = f"/Users/dykim/dev/make-docs/images/{filename}"
            
            try:
                # 기존 파일이 있으면 덮어쓰기
                if os.path.exists(dest_path):
                    os.remove(dest_path)
                    
                shutil.copy2(png_file, dest_path)
                print(f"✅ 복사 완료: {filename}")
                copied_count += 1
            except Exception as e:
                print(f"❌ 복사 실패 {filename}: {e}")
        
        print(f"🎉 최종 완료: {copied_count}개 파일이 images 폴더로 복사됨")

def main():
    """메인 함수"""
    try:
        converter = HTMLToPNGConverter()
        converted_count = converter.convert_rwsl_charts()
        
        print(f"\n📊 최종 결과: {converted_count}개 HTML을 PNG로 변환 완료")
        
    except Exception as e:
        print(f"❌ 전체 오류: {e}")

if __name__ == "__main__":
    main()