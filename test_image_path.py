#!/usr/bin/env python3
"""
이미지 경로 처리 테스트
"""

import os

def test_image_path():
    # SimpleThermalConverter의 로직과 동일하게 테스트
    image_path = "images/rwsl_traffic_growth_chart.png"
    
    # 절대 경로로 변환
    if not os.path.isabs(image_path):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(current_dir, image_path)
    else:
        full_path = image_path
        
    print(f"현재 디렉토리: {current_dir}")
    print(f"이미지 경로: {image_path}")
    print(f"절대 경로: {full_path}")
    print(f"파일 존재 여부: {os.path.exists(full_path)}")
    
    if os.path.exists(full_path):
        file_size = os.path.getsize(full_path)
        print(f"파일 크기: {file_size} bytes")
    
    # 몇 개 더 테스트
    test_files = [
        "images/rwsl_system_architecture.png",
        "images/rwsl_global_adoption_chart.png"
    ]
    
    for test_file in test_files:
        if not os.path.isabs(test_file):
            test_full_path = os.path.join(current_dir, test_file)
        print(f"{test_file} -> 존재: {os.path.exists(test_full_path)}")

if __name__ == "__main__":
    test_image_path()