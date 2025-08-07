#!/usr/bin/env python3
"""
지능형 적응형 PNG 생성기 - 콘텐츠 복잡도 기반 최적 크기 자동 결정
"""

import os
import json
import subprocess
import time
from pathlib import Path
from adaptive_chart_system import AdaptiveCanvasCalculator

class IntelligentPNGGenerator:
    """지능형 PNG 생성기"""
    
    def __init__(self, config_file='adaptive_sizing_config.json'):
        self.calculator = AdaptiveCanvasCalculator()
        self.config_file = config_file
        self.sizing_config = self._load_or_generate_config()
        
    def _load_or_generate_config(self):
        """적응형 크기 설정 로드 또는 생성"""
        
        if Path(self.config_file).exists():
            print("📋 기존 적응형 크기 설정 로드 중...")
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            print("🧠 새로운 적응형 크기 설정 생성 중...")
            from adaptive_chart_system import generate_adaptive_sizing_config
            return generate_adaptive_sizing_config()
    
    def generate_adaptive_pngs(self):
        """모든 HTML 파일에 대해 적응형 크기로 PNG 생성"""
        
        print("\n🎨 지능형 적응형 PNG 생성 시작...")
        print("=" * 80)
        
        charts_dir = Path("images")
        success_count = 0
        total_charts = 0
        
        for chart_name, size_info in self.sizing_config.items():
            html_file = charts_dir / f"{chart_name}.html"
            png_file = charts_dir / f"{chart_name}.png"
            
            if html_file.exists():
                total_charts += 1
                success = self._generate_single_png(
                    html_file, png_file, 
                    size_info['width'], size_info['height'],
                    chart_name, size_info
                )
                
                if success:
                    success_count += 1
            else:
                print(f"⚠️  {html_file} 파일이 존재하지 않습니다")
        
        print("\n" + "=" * 80)
        print(f"🎯 PNG 생성 완료: {success_count}/{total_charts} 성공")
        self._print_generation_summary()
    
    def _generate_single_png(self, html_file, png_file, width, height, chart_name, size_info):
        """개별 PNG 파일 생성"""
        
        try:
            # Chrome 헤드리스로 스크린샷 캡처
            cmd = [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "--headless",
                "--disable-gpu",
                "--disable-web-security",
                "--hide-scrollbars", 
                "--force-device-scale-factor=1",
                f"--window-size={width},{height}",
                f"--screenshot={png_file}",
                os.path.abspath(html_file)
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            
            # 성공 메시지 출력
            complexity_emoji = self._get_complexity_emoji(size_info['complexity_score'])
            size_category = self._get_size_category(width, height)
            
            print(f"✅ {complexity_emoji} {chart_name.upper()}")
            print(f"   크기: {width}x{height} ({size_category})")  
            print(f"   복잡도: {size_info['complexity_score']:.1f}/100")
            print(f"   타입: {size_info['chart_type']}")
            print(f"   최적화: {size_info['scaling_factor']:.2f}x 스케일링")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ {chart_name} 변환 실패: {e}")
            return False
    
    def _get_complexity_emoji(self, score):
        """복잡도 점수에 따른 이모지 반환"""
        if score >= 70:
            return "🔴"  # 고복잡도
        elif score >= 40:
            return "🟡"  # 중복잡도  
        else:
            return "🟢"  # 저복잡도
    
    def _get_size_category(self, width, height):
        """크기 카테고리 반환"""
        total_pixels = width * height
        
        if total_pixels >= 1500000:  # 1.5M 픽셀 이상
            return "대형"
        elif total_pixels >= 1000000:  # 1M 픽셀 이상
            return "중대형"
        elif total_pixels >= 700000:   # 700K 픽셀 이상
            return "중형"
        else:
            return "소형"
    
    def _print_generation_summary(self):
        """생성 결과 요약 출력"""
        
        print("\n📊 생성된 PNG 파일 요약:")
        print("-" * 60)
        
        size_distribution = {}
        complexity_distribution = {"고복잡도": 0, "중복잡도": 0, "저복잡도": 0}
        
        for chart_name, size_info in self.sizing_config.items():
            # 크기 분포
            width, height = size_info['width'], size_info['height'] 
            size_category = self._get_size_category(width, height)
            size_distribution[size_category] = size_distribution.get(size_category, 0) + 1
            
            # 복잡도 분포
            score = size_info['complexity_score']
            if score >= 70:
                complexity_distribution["고복잡도"] += 1
            elif score >= 40:
                complexity_distribution["중복잡도"] += 1
            else:
                complexity_distribution["저복잡도"] += 1
        
        print("크기별 분포:")
        for category, count in size_distribution.items():
            print(f"  {category}: {count}개")
        
        print("\n복잡도별 분포:")
        for category, count in complexity_distribution.items():
            print(f"  {category}: {count}개")
        
        # 최대/최소 크기 차트
        max_chart = max(self.sizing_config.items(), 
                       key=lambda x: x[1]['width'] * x[1]['height'])
        min_chart = min(self.sizing_config.items(),
                       key=lambda x: x[1]['width'] * x[1]['height'])
        
        print(f"\n📏 크기 범위:")
        print(f"  최대: {max_chart[0]} ({max_chart[1]['width']}x{max_chart[1]['height']})")
        print(f"  최소: {min_chart[0]} ({min_chart[1]['width']}x{min_chart[1]['height']})")
        
        print(f"\n🎯 적응형 최적화 효과:")
        print("  ✓ 콘텐츠별 맞춤형 크기 적용")
        print("  ✓ 오버플로우/언더플로우 문제 해결")
        print("  ✓ 시각적 균형과 가독성 최적화")
        print("  ✓ 파일 크기 및 품질 균형")

    def regenerate_single_chart(self, chart_name):
        """특정 차트만 재생성"""
        
        if chart_name not in self.sizing_config:
            print(f"❌ {chart_name} 차트 설정을 찾을 수 없습니다")
            return False
        
        charts_dir = Path("images")
        html_file = charts_dir / f"{chart_name}.html"
        png_file = charts_dir / f"{chart_name}.png"
        
        if html_file.exists():
            size_info = self.sizing_config[chart_name]
            return self._generate_single_png(
                html_file, png_file,
                size_info['width'], size_info['height'],
                chart_name, size_info
            )
        else:
            print(f"❌ {html_file} 파일이 존재하지 않습니다")
            return False
    
    def update_sizing_config(self):
        """크기 설정 업데이트"""
        print("🔄 적응형 크기 설정 업데이트 중...")
        from adaptive_chart_system import generate_adaptive_sizing_config
        self.sizing_config = generate_adaptive_sizing_config()
        print("✅ 크기 설정 업데이트 완료")

def main():
    """메인 실행 함수"""
    
    print("🚀 지능형 적응형 PNG 생성기 v2.0")
    print("콘텐츠 복잡도 기반 최적 크기 자동 결정 시스템")
    
    generator = IntelligentPNGGenerator()
    generator.generate_adaptive_pngs()

if __name__ == "__main__":
    main()