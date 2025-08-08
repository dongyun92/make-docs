#!/usr/bin/env python3
"""
Chrome 헤드리스 캡처 멈춤 문제 해결 스크립트
18개 차트 연속 캡처시 마지막에 프로세스가 정지하는 문제를 해결합니다.
"""

import subprocess
import time
import os
import psutil
from pathlib import Path

def kill_all_chrome_processes():
    """모든 Chrome 프로세스를 강제 종료합니다."""
    try:
        # Chrome 관련 모든 프로세스 찾기
        chrome_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name'] and 'chrome' in proc.info['name'].lower():
                    chrome_processes.append(proc)
                elif proc.info['cmdline'] and any('chrome' in str(cmd).lower() for cmd in proc.info['cmdline']):
                    chrome_processes.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        # 프로세스 종료
        for proc in chrome_processes:
            try:
                print(f"Chrome 프로세스 종료: PID {proc.pid}")
                proc.terminate()
                time.sleep(0.5)
                if proc.is_running():
                    proc.kill()
                    time.sleep(0.5)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
                
        print(f"총 {len(chrome_processes)}개의 Chrome 프로세스를 종료했습니다.")
        time.sleep(2)  # 프로세스가 완전히 종료될 시간 대기
        
    except Exception as e:
        print(f"Chrome 프로세스 종료 중 오류: {e}")
        # 시스템 명령어로 강제 종료 시도
        try:
            subprocess.run(['pkill', '-f', 'chrome'], check=False, capture_output=True)
            subprocess.run(['pkill', '-f', 'Chrome'], check=False, capture_output=True)
            time.sleep(2)
        except Exception:
            pass

def capture_html_to_png_safe(html_file, png_file, max_retries=3):
    """Chrome 헤드리스로 HTML을 PNG로 안전하게 변환합니다."""
    
    chrome_cmd = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "--headless",
        "--disable-gpu", 
        "--hide-scrollbars",
        "--force-device-scale-factor=1",
        "--window-size=900,600",
        "--disable-web-security",
        "--disable-features=VizDisplayCompositor",
        "--disable-background-timer-throttling",
        "--disable-backgrounding-occluded-windows", 
        "--disable-renderer-backgrounding",
        "--disable-background-networking",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--single-process",
        "--disable-extensions",
        "--disable-plugins",
        f"--screenshot={png_file}",
        f"file://{html_file}"
    ]
    
    for attempt in range(max_retries):
        try:
            print(f"  시도 {attempt + 1}/{max_retries}: {Path(html_file).name}")
            
            # 이전 Chrome 프로세스 정리
            if attempt > 0:
                kill_all_chrome_processes()
                time.sleep(1)
            
            # Chrome 실행
            result = subprocess.run(
                chrome_cmd,
                timeout=30,  # 30초 타임아웃
                capture_output=True,
                text=True
            )
            
            # 결과 확인
            if os.path.exists(png_file) and os.path.getsize(png_file) > 1000:
                print(f"    ✓ 성공: {Path(png_file).name}")
                return True
            else:
                print(f"    ✗ 실패: 파일이 생성되지 않았거나 크기가 너무 작습니다")
                if os.path.exists(png_file):
                    os.remove(png_file)
                    
        except subprocess.TimeoutExpired:
            print(f"    ✗ 타임아웃: Chrome 프로세스를 강제 종료합니다")
            kill_all_chrome_processes()
            
        except Exception as e:
            print(f"    ✗ 오류: {e}")
            
        # 다음 시도 전 대기
        if attempt < max_retries - 1:
            time.sleep(2)
    
    return False

def convert_all_rwsl_charts():
    """모든 RWSL 차트를 안전하게 변환합니다."""
    
    images_dir = Path("/Users/dykim/dev/make-docs/images")
    
    # RWSL 관련 HTML 파일 찾기
    html_files = list(images_dir.glob("rwsl*.html"))
    
    if not html_files:
        print("RWSL HTML 파일을 찾을 수 없습니다.")
        return False
        
    print(f"총 {len(html_files)}개의 RWSL 차트를 변환합니다...")
    
    # 시작 전 Chrome 프로세스 정리
    kill_all_chrome_processes()
    
    success_count = 0
    batch_size = 3  # 배치 크기를 3개로 제한
    
    for i, html_file in enumerate(html_files):
        png_file = html_file.with_suffix('.png')
        
        print(f"\n[{i+1}/{len(html_files)}] 변환 중: {html_file.name}")
        
        if capture_html_to_png_safe(str(html_file), str(png_file)):
            success_count += 1
        else:
            print(f"    ⚠️  변환 실패: {html_file.name}")
        
        # 배치 단위로 Chrome 프로세스 정리
        if (i + 1) % batch_size == 0 and i < len(html_files) - 1:
            print(f"\n  📋 배치 완료 ({i+1}/{len(html_files)}), Chrome 프로세스 정리 중...")
            kill_all_chrome_processes()
            time.sleep(3)  # 더 긴 대기 시간
    
    # 최종 정리
    kill_all_chrome_processes()
    
    print(f"\n{'='*50}")
    print(f"변환 완료: {success_count}/{len(html_files)}개 성공")
    print(f"{'='*50}")
    
    return success_count == len(html_files)

if __name__ == "__main__":
    print("RWSL 차트 변환 시작...")
    success = convert_all_rwsl_charts()
    
    if success:
        print("✅ 모든 차트 변환이 성공적으로 완료되었습니다!")
    else:
        print("⚠️  일부 차트 변환에 실패했습니다.")