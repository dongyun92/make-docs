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
        self.output_directory = tk.StringVar()
        self.output_filename = tk.StringVar()
        
        # 기본값 설정
        self.output_directory.set(str(Path.cwd()))
        
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
        title_label = ttk.Label(main_frame, text="MD to DOCX 변환기", 
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
        
        # 출력 설정 섹션
        output_frame = ttk.LabelFrame(main_frame, text="출력 설정", padding="10")
        output_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        
        ttk.Label(output_frame, text="출력 폴더:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        dir_frame = ttk.Frame(output_frame)
        dir_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.dir_entry = ttk.Entry(dir_frame, textvariable=self.output_directory, width=50)
        self.dir_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(dir_frame, text="찾아보기", 
                  command=self.browse_output_dir).grid(row=0, column=1)
        
        dir_frame.columnconfigure(0, weight=1)
        
        ttk.Label(output_frame, text="파일명 (선택사항):").grid(row=2, column=0, sticky=tk.W, pady=(10, 5))
        self.filename_entry = ttk.Entry(output_frame, textvariable=self.output_filename, width=50)
        self.filename_entry.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Label(output_frame, text="※ 비워두면 원본 파일명으로 자동 생성됩니다", 
                 font=('Arial', 8), foreground='gray').grid(row=4, column=0, sticky=tk.W)
        
        # 상태 섹션
        status_frame = ttk.LabelFrame(main_frame, text="상태", padding="10")
        status_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        
        self.status_text = tk.Text(status_frame, height=8, width=70, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(status_frame, orient="vertical", command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        status_frame.columnconfigure(0, weight=1)
        status_frame.rowconfigure(0, weight=1)
        
        # 버튼 섹션
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=10)
        
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
            
            # 출력 파일명 자동 설정
            base_name = Path(file_path).stem
            self.output_filename.set(f"{base_name}.docx")
            
            self.log_message(f"선택된 파일: {file_path}")
    
    def browse_output_dir(self):
        """출력 폴더 선택"""
        directory = filedialog.askdirectory(title="출력 폴더 선택")
        if directory:
            self.output_directory.set(directory)
            self.log_message(f"출력 폴더: {directory}")
    
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
        
        if not self.output_directory.get():
            messagebox.showerror("오류", "출력 폴더를 선택해주세요.")
            return False
        
        if not os.path.exists(self.output_directory.get()):
            messagebox.showerror("오류", "출력 폴더가 존재하지 않습니다.")
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
    
    def run_conversion(self):
        """실제 변환 작업 실행"""
        try:
            # 출력 파일 경로 생성
            if self.output_filename.get():
                output_file = os.path.join(self.output_directory.get(), self.output_filename.get())
            else:
                base_name = Path(self.selected_md_file.get()).stem
                output_file = os.path.join(self.output_directory.get(), f"{base_name}.docx")
            
            self.log_message(f"출력 파일: {output_file}")
            
            # 차트 생성
            self.generate_charts()
            
            # 가상환경 Python 경로 사용
            venv_python = os.path.join(os.getcwd(), 'venv', 'bin', 'python3')
            if os.path.exists(venv_python):
                python_cmd = venv_python
            else:
                python_cmd = sys.executable
            
            # 변환 스크립트 실행
            self.log_message("문서 변환을 시작합니다...")
            
            cmd = [python_cmd, "md_to_docx_converter.py", self.selected_md_file.get(), output_file]
            
            self.log_message(f"실행 명령: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())
            
            if result.returncode == 0:
                self.log_message("✅ 변환이 성공적으로 완료되었습니다!")
                self.log_message(f"생성된 파일: {output_file}")
                
                # 성공 메시지박스
                messagebox.showinfo("변환 완료", 
                    f"변환이 완료되었습니다!\n\n생성된 파일: {output_file}")
                
            else:
                self.log_message(f"❌ 변환 중 오류가 발생했습니다:")
                self.log_message(f"오류 내용: {result.stderr}")
                messagebox.showerror("변환 실패", f"변환 중 오류가 발생했습니다:\n{result.stderr}")
                
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