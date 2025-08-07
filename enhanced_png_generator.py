#!/usr/bin/env python3
"""
개선된 PNG 생성기
실용적 HTML 분석과 동적 크기 감지를 결합한 최적화된 이미지 생성
"""

import subprocess
import json
import os
from pathlib import Path
import time

class EnhancedPNGGenerator:
    def __init__(self):
        self.chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        self.output_dir = Path("images")
        self.output_dir.mkdir(exist_ok=True)
        
        # 실용적 크기 설정 로드
        self.sizing_config = self._load_sizing_config()
    
    def _load_sizing_config(self):
        """크기 설정 로드"""
        config_file = "practical_sizing_config.json"
        
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            print(f"크기 설정 파일 {config_file}이 없습니다. 기본값 사용.")
            return {}
    
    def generate_optimized_png(self, html_file, png_file, chart_name):
        """최적화된 PNG 생성"""
        print(f"\n=== {chart_name} PNG 생성 시작 ===")
        
        # 크기 정보 가져오기
        size_info = self.sizing_config.get(chart_name, {
            "width": 1200,
            "height": 800,
            "method": "default"
        })
        
        width = size_info["width"]
        height = size_info["height"]
        method = size_info.get("method", "default")
        
        print(f"HTML 파일: {html_file}")
        print(f"출력 파일: {png_file}")
        print(f"크기: {width}x{height} (방법: {method})")
        
        # Chrome 명령어 구성
        cmd = [
            self.chrome_path,
            "--headless",
            "--disable-gpu",
            "--disable-web-security",
            "--hide-scrollbars", 
            "--force-device-scale-factor=1",
            f"--window-size={width},{height}",
            f"--screenshot={png_file}",
            f"file://{Path(html_file).absolute()}"
        ]
        
        try:
            # Chrome 실행
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # 결과 확인
            if result.returncode == 0 and os.path.exists(png_file):
                file_size = os.path.getsize(png_file)
                print(f"✅ 성공! 파일 크기: {file_size:,} bytes")
                
                # 상세 정보 반환
                return {
                    "success": True,
                    "file": png_file,
                    "size": f"{width}x{height}",
                    "file_size": file_size,
                    "method": method
                }
            else:
                print(f"❌ 실패! Chrome 종료 코드: {result.returncode}")
                if result.stderr:
                    print(f"오류: {result.stderr}")
                    
                return {
                    "success": False,
                    "error": f"Chrome 실행 실패 (코드: {result.returncode})"
                }
                
        except subprocess.TimeoutExpired:
            print("❌ 타임아웃! Chrome 실행 시간 초과")
            return {
                "success": False, 
                "error": "실행 시간 초과"
            }
        except Exception as e:
            print(f"❌ 오류! {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def batch_generate_pngs(self):
        """모든 HTML 파일의 PNG 일괄 생성"""
        
        # HTML 파일 목록 생성
        html_files = []
        chart_mappings = {}
        
        for chart_name in self.sizing_config.keys():
            html_file = self.output_dir / f"{chart_name}.html"
            png_file = self.output_dir / f"{chart_name}.png"
            
            if html_file.exists():
                html_files.append(str(html_file))
                chart_mappings[str(html_file)] = {
                    "chart_name": chart_name,
                    "png_file": str(png_file)
                }
            else:
                print(f"HTML 파일 없음: {html_file}")
        
        # 조직도는 워드 표로 대체하므로 제외
        if "organization_chart" in chart_mappings:
            print("조직도는 워드 표로 생성하므로 PNG 생성에서 제외합니다.")
        
        print(f"\n=== 개선된 PNG 일괄 생성 시작 ===")
        print(f"총 {len(html_files)}개 파일 처리 예정")
        
        results = {}
        successful = 0
        failed = 0
        
        # 각 파일별 PNG 생성
        for html_file in html_files:
            mapping = chart_mappings[html_file]
            chart_name = mapping["chart_name"]
            png_file = mapping["png_file"]
            
            # 조직도 건너뛰기
            if chart_name == "organization_chart":
                print(f"\n건너뛰기: {chart_name} (워드 표로 대체)")
                continue
            
            # PNG 생성 실행
            result = self.generate_optimized_png(html_file, png_file, chart_name)
            results[chart_name] = result
            
            if result["success"]:
                successful += 1
            else:
                failed += 1
            
            # 잠시 대기 (시스템 부하 방지)
            time.sleep(0.5)
        
        # 결과 요약
        print(f"\n=== 생성 결과 요약 ===")
        print(f"성공: {successful}개")
        print(f"실패: {failed}개")
        print(f"총 처리: {successful + failed}개")
        
        # 상세 결과
        print(f"\n=== 상세 결과 ===")
        for chart_name, result in results.items():
            if result["success"]:
                print(f"✅ {chart_name}: {result['size']} ({result['method']})")
            else:
                print(f"❌ {chart_name}: {result['error']}")
        
        # 결과를 JSON으로 저장
        with open("enhanced_generation_results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n상세 결과가 enhanced_generation_results.json에 저장되었습니다.")
        
        return results
    
    def generate_specific_charts(self, chart_names):
        """특정 차트들만 생성"""
        print(f"지정된 차트들만 생성: {', '.join(chart_names)}")
        
        results = {}
        
        for chart_name in chart_names:
            html_file = self.output_dir / f"{chart_name}.html"
            png_file = self.output_dir / f"{chart_name}.png"
            
            if html_file.exists():
                result = self.generate_optimized_png(str(html_file), str(png_file), chart_name)
                results[chart_name] = result
            else:
                print(f"HTML 파일 없음: {html_file}")
                results[chart_name] = {
                    "success": False,
                    "error": "HTML 파일 없음"
                }
        
        return results
    
    def validate_generated_images(self):
        """생성된 이미지들의 품질 검증"""
        print("\n=== 생성된 이미지 품질 검증 ===")
        
        validation_results = {}
        
        for chart_name in self.sizing_config.keys():
            if chart_name == "organization_chart":
                continue  # 조직도는 워드 표로 대체
            
            png_file = self.output_dir / f"{chart_name}.png"
            
            if png_file.exists():
                file_size = os.path.getsize(png_file)
                
                # 기본 품질 검증 (파일 크기 기준)
                if file_size > 10000:  # 10KB 이상
                    status = "✅ 양호"
                elif file_size > 1000:   # 1KB 이상
                    status = "⚠️  확인필요"
                else:
                    status = "❌ 불량"
                
                validation_results[chart_name] = {
                    "file_size": file_size,
                    "status": status,
                    "size_config": f"{self.sizing_config[chart_name]['width']}x{self.sizing_config[chart_name]['height']}"
                }
                
                print(f"{status} {chart_name}: {file_size:,} bytes ({validation_results[chart_name]['size_config']})")
            else:
                validation_results[chart_name] = {
                    "file_size": 0,
                    "status": "❌ 파일없음",
                    "size_config": "N/A"
                }
                print(f"❌ 파일없음 {chart_name}")
        
        return validation_results

if __name__ == "__main__":
    generator = EnhancedPNGGenerator()
    
    print("개선된 PNG 생성기 시작...")
    
    # 모든 차트 PNG 생성
    results = generator.batch_generate_pngs()
    
    # 생성된 이미지 품질 검증
    print("\n" + "="*50)
    validation = generator.validate_generated_images()
    
    print(f"\n✨ 개선된 PNG 생성 완료!")
    print(f"📁 생성된 파일들을 {generator.output_dir}/ 폴더에서 확인하세요.")
    print(f"📊 조직도는 조직도_워드표_간단버전.docx 파일을 확인하세요.")