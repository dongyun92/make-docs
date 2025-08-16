#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import sys
import subprocess
import threading
import platform
from pathlib import Path
from auto_unique_chart_generator import AutoUniqueChartGenerator

class MDToDOCXConverter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MD to DOCX 변환기")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # 운영체제 확인
        self.is_windows = platform.system() == "Windows"
        self.is_macos = platform.system() == "Darwin"
        
        # Chrome 경로 설정
        self.chrome_paths = self._get_chrome_paths()
        self.chrome_path = self._find_chrome()
        
        # 변수 초기화
        self.selected_md_file = tk.StringVar()
        self.selected_html_files = []  # HTML 파일 리스트
        
        self.setup_ui()
        
    def _get_chrome_paths(self):
        """운영체제별 Chrome 경로 목록"""
        if self.is_windows:
            return [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            ]
        elif self.is_macos:
            return [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            ]
        else:  # Linux
            return [
                "/usr/bin/google-chrome",
                "/usr/bin/google-chrome-stable",
                "/usr/bin/chromium-browser",
            ]
    
    def _find_chrome(self):
        """Chrome 브라우저 찾기"""
        for path in self.chrome_paths:
            if os.path.exists(path):
                return path
        return None
    
    def setup_ui(self):
        """UI 구성"""
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 제목
        title_label = ttk.Label(main_frame, text="🚀 사업계획서 자동 생성기", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # 파일 선택 섹션
        file_frame = ttk.LabelFrame(main_frame, text="파일 선택", padding="10")
        file_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        
        ttk.Label(file_frame, text="Markdown 파일:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        md_frame = ttk.Frame(file_frame)
        md_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.md_entry = ttk.Entry(md_frame, textvariable=self.selected_md_file, width=50)
        self.md_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(md_frame, text="찾아보기", 
                  command=self.browse_md_file).grid(row=0, column=1)
        
        md_frame.columnconfigure(0, weight=1)
        
        # HTML 파일들 섹션
        html_frame = ttk.LabelFrame(file_frame, text="HTML 차트 파일들 (선택사항)", padding="10")
        html_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Label(html_frame, text="HTML 파일들:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        html_select_frame = ttk.Frame(html_frame)
        html_select_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(html_select_frame, text="HTML 파일들 선택", 
                  command=self.browse_html_files).grid(row=0, column=0, padx=(0, 10))
        
        self.html_count_label = ttk.Label(html_select_frame, text="선택된 파일: 0개", foreground='gray')
        self.html_count_label.grid(row=0, column=1)
        
        self.html_listbox = tk.Listbox(html_frame, height=4, selectmode=tk.EXTENDED)
        html_scrollbar = ttk.Scrollbar(html_frame, orient="vertical", command=self.html_listbox.yview)
        self.html_listbox.configure(yscrollcommand=html_scrollbar.set)
        
        self.html_listbox.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        html_scrollbar.grid(row=2, column=1, sticky=(tk.N, tk.S), pady=(0, 5))
        
        ttk.Button(html_frame, text="선택 파일 제거", 
                  command=self.remove_selected_html).grid(row=3, column=0, sticky=tk.W)
        
        html_frame.columnconfigure(0, weight=1)
        
        
        # 상태 섹션
        status_frame = ttk.LabelFrame(main_frame, text="상태", padding="10")
        status_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        
        self.status_text = tk.Text(status_frame, height=8, width=70, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(status_frame, orient="vertical", command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        status_frame.columnconfigure(0, weight=1)
        status_frame.rowconfigure(0, weight=1)
        
        # 버튼 섹션
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=10)
        
        self.convert_btn = ttk.Button(button_frame, text="변환 시작", 
                                     command=self.start_conversion, 
                                     style='Accent.TButton' if hasattr(ttk.Style(), 'theme_names') else None)
        self.convert_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="로그 지우기", 
                  command=self.clear_log).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="종료", 
                  command=self.root.quit).pack(side=tk.LEFT)
        
        # 그리드 가중치 설정
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # 초기 상태 메시지
        self.log_message("MD to DOCX 변환기가 시작되었습니다.")
        if self.chrome_path:
            self.log_message(f"Chrome 브라우저를 찾았습니다: {self.chrome_path}")
        else:
            self.log_message("⚠️ Chrome 브라우저를 찾을 수 없습니다. 차트 생성이 제한될 수 있습니다.")
        
    def browse_md_file(self):
        """Markdown 파일 선택"""
        file_path = filedialog.askopenfilename(
            title="Markdown 파일 선택",
            filetypes=[
                ("Markdown files", "*.md"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.selected_md_file.set(file_path)
            
            
            self.log_message(f"선택된 파일: {file_path}")
    
    def browse_html_files(self):
        """HTML 파일들 선택"""
        files = filedialog.askopenfilenames(
            title="HTML 파일들 선택",
            filetypes=[
                ("HTML files", "*.html"),
                ("All files", "*.*")
            ],
            multiple=True
        )
        
        if files:
            # 기존 파일들에 추가
            for file_path in files:
                if file_path not in self.selected_html_files:
                    self.selected_html_files.append(file_path)
            
            self._update_html_display()
            self.log_message(f"HTML 파일 {len(files)}개 추가됨")
    
    def remove_selected_html(self):
        """선택된 HTML 파일들 제거"""
        selected_indices = self.html_listbox.curselection()
        
        if not selected_indices:
            messagebox.showinfo("알림", "제거할 파일을 선택해주세요.")
            return
        
        # 역순으로 제거 (인덱스 변화 방지)
        for index in reversed(selected_indices):
            if 0 <= index < len(self.selected_html_files):
                removed_file = self.selected_html_files.pop(index)
                self.log_message(f"제거됨: {os.path.basename(removed_file)}")
        
        self._update_html_display()
    
    def _update_html_display(self):
        """HTML 파일 목록 표시 업데이트"""
        # 리스트박스 클리어
        self.html_listbox.delete(0, tk.END)
        
        # 파일들 추가
        for html_file in self.selected_html_files:
            filename = os.path.basename(html_file)
            self.html_listbox.insert(tk.END, filename)
        
        # 카운트 라벨 업데이트
        count = len(self.selected_html_files)
        self.html_count_label.config(text=f"선택된 파일: {count}개")
    
    def log_message(self, message):
        """로그 메시지 추가"""
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_log(self):
        """로그 지우기"""
        self.status_text.delete(1.0, tk.END)
    
    def validate_inputs(self):
        """입력값 검증"""
        if not self.selected_md_file.get():
            messagebox.showerror("오류", "Markdown 파일을 선택해주세요.")
            return False
        
        if not os.path.exists(self.selected_md_file.get()):
            messagebox.showerror("오류", "선택된 Markdown 파일이 존재하지 않습니다.")
            return False
        
        
        return True
    
    def generate_charts(self):
        """차트 이미지 생성"""
        if not self.chrome_path:
            self.log_message("Chrome이 없어 차트 생성을 건너뜁니다.")
            return
        
        self.log_message("차트 이미지를 생성합니다...")
        
        chart_files = [
            ("images/market_growth_line.html", "images/market_growth_line.png", "시장 성장 추세"),
            ("images/market_growth_regional.html", "images/market_growth_regional.png", "지역별 성장 전망"),
            ("images/budget_pie.html", "images/budget_pie.png", "예산 분배"),
            ("images/budget_trend.html", "images/budget_trend.png", "예산 추세")
        ]
        
        for html_file, png_file, description in chart_files:
            if os.path.exists(html_file):
                try:
                    cmd = [
                        self.chrome_path,
                        "--headless",
                        "--disable-gpu",
                        "--hide-scrollbars",
                        "--force-device-scale-factor=1",
                        "--window-size=700,600",
                        f"--screenshot={png_file}",
                        html_file
                    ]
                    
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                    
                    if os.path.exists(png_file):
                        self.log_message(f"✅ {description} 차트 생성 완료")
                    else:
                        self.log_message(f"⚠️ {description} 차트 생성 실패")
                        
                except subprocess.TimeoutExpired:
                    self.log_message(f"⚠️ {description} 차트 생성 시간 초과")
                except Exception as e:
                    self.log_message(f"⚠️ {description} 차트 생성 오류: {str(e)}")
    
    def generate_all_charts(self):
        """모든 차트를 완전한 캡처 시스템으로 생성"""
        if not self.chrome_path:
            self.log_message("Chrome이 없어 차트 생성을 건너뜁니다.")
            return
            
        self.log_message("완전한 차트 캡처 시스템을 실행합니다...")
        
        try:
            # complete_capture.py 실행
            cmd = [sys.executable, "complete_capture.py"]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd(), timeout=120)
            
            if result.returncode == 0:
                self.log_message("✅ 모든 차트가 성공적으로 생성되었습니다!")
                if result.stdout:
                    self.log_message(f"차트 생성 로그: {result.stdout}")
            else:
                self.log_message("⚠️ 일부 차트 생성에 실패했습니다.")
                if result.stderr:
                    self.log_message(f"차트 생성 오류: {result.stderr}")
                # 실패해도 계속 진행
                
        except subprocess.TimeoutExpired:
            self.log_message("⚠️ 차트 생성 시간 초과 - 기본 차트 생성으로 대체")
            self.generate_charts()
        except Exception as e:
            self.log_message(f"⚠️ 차트 생성 시스템 오류: {str(e)} - 기본 차트 생성으로 대체")
            self.generate_charts()
    
    def capture_html_files(self):
        """검증된 html_to_png_converter.py 사용하여 HTML 파일들을 PNG로 변환"""
        if not self.selected_html_files:
            self.log_message("선택된 HTML 파일이 없습니다.")
            return
        
        self.log_message(f"html_to_png_converter로 HTML 파일 {len(self.selected_html_files)}개를 PNG로 변환합니다...")
        
        try:
            # 선택된 HTML 파일들이 있는 경우에만 변환
            if not self.selected_html_files:
                self.log_message("ℹ️ 선택된 HTML 파일이 없어 변환을 건너뜁니다.")
                return
                
            # html_to_png_converter 임포트 및 실행
            from html_to_png_converter import HTMLToPNGConverter
            
            converter = HTMLToPNGConverter()
            converted_count = converter.convert_selected_files(self.selected_html_files)
            
            self.log_message(f"✅ {converted_count}개 HTML 파일 변환 완료!")
            
        except Exception as e:
            self.log_message(f"⚠️ HTML 변환 오류: {str(e)}")
    
    def auto_generate_and_capture_charts(self):
        """프로젝트별 고유 차트 자동 생성 (레거시 지원)"""
        try:
            # 1. 선택된 MD 파일로 고유 차트 생성
            md_file = self.selected_md_file.get()
            self.log_message(f"📋 {os.path.basename(md_file)}에 대한 고유 차트를 생성합니다...")
            
            # 2. 고유 차트 생성기 실행
            generator = AutoUniqueChartGenerator(md_file)
            chart_configs = generator.process_md_file(md_file)
            
            self.log_message(f"✅ {len(chart_configs)}개의 고유 차트가 생성되었습니다!")
            for chart in chart_configs:
                self.log_message(f"  - {chart['filename']}.png ({chart['type']})")
            
        except Exception as e:
            self.log_message(f"⚠️ 고유 차트 생성 실패: {str(e)} - 기본 차트만 사용")
            self.generate_charts()
    
    def check_dependencies(self):
        """필수 라이브러리 설치 확인"""
        import sys
        import importlib.util
        
        self.log_message("🔍 디버깅 정보:")
        self.log_message(f"Python 버전: {sys.version}")
        self.log_message(f"Python 실행 경로: {sys.executable}")
        self.log_message(f"Python 패키지 경로들:")
        for path in sys.path:
            self.log_message(f"  - {path}")
        
        self.log_message("\n필수 라이브러리 확인 중...")
        
        required_libs = [
            ("docx", "python-docx"),
            ("bs4", "beautifulsoup4"), 
            ("PIL", "pillow"),
            ("lxml", "lxml"),
            ("requests", "requests")
        ]
        
        missing_libs = []
        
        for module_name, package_name in required_libs:
            try:
                spec = importlib.util.find_spec(module_name)
                if spec is not None:
                    self.log_message(f"✅ {package_name}: 설치됨 (위치: {spec.origin})")
                else:
                    self.log_message(f"❌ {package_name}: 미설치 - importlib.util.find_spec 결과 None")
                    missing_libs.append(package_name)
            except Exception as e:
                self.log_message(f"❌ {package_name}: 확인 실패 - 예외: {type(e).__name__}: {e}")
                missing_libs.append(package_name)
        
        if missing_libs:
            error_msg = f"다음 라이브러리가 설치되지 않았습니다:\n{', '.join(missing_libs)}\n\nsetup_final.bat를 다시 실행해주세요."
            messagebox.showerror("라이브러리 오류", error_msg)
            return False
            
        return True

    def run_conversion(self):
        """실제 변환 작업 실행"""
        try:
            # 라이브러리 확인
            if not self.check_dependencies():
                return
                
            # HTML 파일들 캡처 (선택사항)
            if self.selected_html_files:
                self.capture_html_files()
            
            # MD 파일 그대로 처리하는 범용 변환기 사용
            from universal_md_converter import UniversalMDConverter
            converter = UniversalMDConverter()
            
            # MD 파일 변환 (MD 파일과 같은 위치에 자동 저장)
            generated_path = converter.convert(self.selected_md_file.get())
            
            # 생성된 파일 경로 디버깅
            self.log_message(f"🔍 변환 결과 경로: {generated_path}")
            if generated_path:
                parent_dir = os.path.dirname(generated_path)
                self.log_message(f"🔍 상위 디렉토리: {parent_dir}")
                self.log_message(f"🔍 디렉토리 존재 여부: {os.path.exists(parent_dir)}")
                if not os.path.exists(parent_dir):
                    self.log_message(f"🔧 디렉토리 생성 시도: {parent_dir}")
                    try:
                        os.makedirs(parent_dir, exist_ok=True)
                        self.log_message(f"✅ 디렉토리 생성 완료")
                    except Exception as dir_e:
                        self.log_message(f"❌ 디렉토리 생성 실패: {dir_e}")
            
            if generated_path and os.path.exists(generated_path):
                success = True
                self.log_message(f"✅ 변환 완료: {generated_path}")
                print(f"✅ MD 파일 구조 그대로 변환 완료: {generated_path}")
            else:
                success = False
                self.log_message(f"❌ 변환 실패: 파일이 생성되지 않았습니다")
                if generated_path:
                    self.log_message(f"   예상 경로: {generated_path}")
                    self.log_message(f"   파일 존재 여부: {os.path.exists(generated_path)}")
                print(f"❌ 변환 실패: 파일이 생성되지 않았습니다")
            
            if success:
                self.log_message("✅ 문서 변환이 완료되었습니다!")
                messagebox.showinfo("완료", f"변환이 완료되었습니다!\n\n출력 파일: {generated_path}")
            else:
                self.log_message("❌ 문서 변환 중 오류가 발생했습니다.")
                messagebox.showerror("오류", "변환 중 오류가 발생했습니다.")
            
            # 레거시 차트 자동 생성 (HTML 파일이 없는 경우에만)
            if not self.selected_html_files:
                self.log_message("💡 레거시 차트 시스템으로 차트를 생성합니다...")
                self.auto_generate_and_capture_charts()
                
        except Exception as e:
            error_msg = f"변환 중 예외가 발생했습니다: {str(e)}"
            self.log_message(f"❌ {error_msg}")
            messagebox.showerror("오류", error_msg)
        
        finally:
            # 버튼 활성화
            self.convert_btn.configure(state='normal', text='변환 시작')
    
    def start_conversion(self):
        """변환 시작 (별도 스레드에서 실행)"""
        if not self.validate_inputs():
            return
        
        # 버튼 비활성화
        self.convert_btn.configure(state='disabled', text='변환 중...')
        
        # 별도 스레드에서 변환 실행
        thread = threading.Thread(target=self.run_conversion, daemon=True)
        thread.start()
    
    def run(self):
        """GUI 실행"""
        # 종료 시 이벤트 핸들러
        def on_closing():
            self.root.quit()
            self.root.destroy()
        
        self.root.protocol("WM_DELETE_WINDOW", on_closing)
        self.root.mainloop()

if __name__ == "__main__":
    # macOS에서 tkinter 이슈 해결
    if platform.system() == "Darwin":
        try:
            import matplotlib
            matplotlib.use('TkAgg')
        except ImportError:
            pass
    
    app = MDToDOCXConverter()
    app.run()