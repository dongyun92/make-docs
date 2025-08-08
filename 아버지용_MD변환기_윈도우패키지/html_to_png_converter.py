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
    def __init__(self):
        self.output_dir = "/Users/dykim/dev/make-docs/converted_images"
        os.makedirs(self.output_dir, exist_ok=True)
        print(f"📁 이미지 저장 디렉토리: {self.output_dir}")
        
    def convert_html_to_png(self, html_file_path: str) -> str:
        """HTML 파일을 PNG로 변환"""
        try:
            filename = os.path.basename(html_file_path).replace('.html', '.png')
            output_path = os.path.join(self.output_dir, filename)
            
            print(f"🔄 변환 중: {filename}")
            
            # 기존 파일이 있으면 삭제
            if os.path.exists(output_path):
                os.remove(output_path)
            
            # capture-website-cli 명령어 실행
            cmd = [
                'capture-website',
                html_file_path,
                '--output', output_path,
                '--width', '900',
                '--height', '600',
                '--type', 'png',
                '--full-page',
                '--overwrite'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and os.path.exists(output_path):
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
    
    def convert_rwsl_charts(self):
        """RWSL HTML 차트들을 모두 PNG로 변환"""
        
        # RWSL HTML 파일들 찾기
        all_html_files = glob.glob('/Users/dykim/dev/make-docs/images/*.html')
        rwsl_files = [f for f in all_html_files if 'rwsl' in os.path.basename(f).lower()]
        
        # 추출기 파일은 제외
        rwsl_files = [f for f in rwsl_files if 'extractor' not in os.path.basename(f).lower()]
        
        print(f"🎯 RWSL 차트 파일 발견: {len(rwsl_files)}개")
        
        converted_count = 0
        failed_files = []
        
        for i, html_file in enumerate(rwsl_files, 1):
            print(f"\n[{i}/{len(rwsl_files)}]")
            
            result = self.convert_html_to_png(html_file)
            if result:
                converted_count += 1
            else:
                failed_files.append(os.path.basename(html_file))
            
            # 각 파일 변환 후 잠시 대기
            time.sleep(1)
        
        print(f"\n🎉 RWSL 차트 변환 완료!")
        print(f"✅ 성공: {converted_count}개")
        print(f"❌ 실패: {len(failed_files)}개")
        
        if failed_files:
            print(f"실패한 파일들:")
            for failed in failed_files:
                print(f"  - {failed}")
        
        # 변환된 파일을 images 폴더로 복사
        if converted_count > 0:
            self.copy_to_images_folder()
        
        return converted_count
    
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