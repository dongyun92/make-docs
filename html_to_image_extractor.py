#!/usr/bin/env python3
"""
HTML 차트 자동 이미지 추출기
html2canvas 라이브러리를 사용하여 HTML 파일에서 이미지를 자동으로 추출
"""

import os
import glob
from typing import List

def add_html2canvas_to_file(html_file_path: str) -> str:
    """HTML 파일에 html2canvas 기능을 추가하여 자동 이미지 추출이 가능하도록 수정"""
    
    with open(html_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # html2canvas 라이브러리 및 자동 추출 스크립트 추가
    html2canvas_script = '''
    <!-- html2canvas 라이브러리 -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    
    <!-- 자동 이미지 추출 스크립트 -->
    <script>
        window.addEventListener('load', function() {
            // 페이지 로드 후 1초 대기 (차트 렌더링 완료 대기)
            setTimeout(function() {
                // 전체 body를 캡처
                html2canvas(document.body, {
                    useCORS: true,
                    allowTaint: true,
                    scale: 2, // 고해상도 캡처
                    backgroundColor: '#ffffff',
                    width: 900,
                    height: 600
                }).then(function(canvas) {
                    // 이미지로 변환
                    const imgData = canvas.toDataURL('image/png');
                    
                    // 다운로드 링크 생성
                    const fileName = window.location.pathname.split('/').pop().replace('.html', '.png');
                    const downloadLink = document.createElement('a');
                    downloadLink.href = imgData;
                    downloadLink.download = fileName;
                    downloadLink.textContent = '이미지 다운로드';
                    downloadLink.style.cssText = 'position: fixed; top: 10px; right: 10px; z-index: 9999; background: #007bff; color: white; padding: 10px; border-radius: 5px; text-decoration: none; font-family: Arial;';
                    
                    document.body.appendChild(downloadLink);
                    
                    // 자동으로 다운로드 시작 (옵션)
                    // downloadLink.click();
                    
                    console.log('이미지 추출 완료. 다운로드 버튼이 우상단에 생성되었습니다.');
                }).catch(function(error) {
                    console.error('이미지 추출 실패:', error);
                });
            }, 1000);
        });
    </script>
'''
    
    # </head> 태그 바로 앞에 스크립트 삽입
    if '</head>' in content:
        content = content.replace('</head>', html2canvas_script + '\n</head>')
    else:
        # head 태그가 없는 경우 body 시작 부분에 삽입
        content = content.replace('<body>', '<body>\n' + html2canvas_script)
    
    # 수정된 파일 저장
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ html2canvas 기능 추가 완료: {os.path.basename(html_file_path)}")
    return html_file_path

def create_image_extractor_html(html_files: List[str]) -> str:
    """모든 HTML 파일의 이미지를 한 번에 추출할 수 있는 통합 페이지 생성"""
    
    extractor_html = '''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HTML 차트 이미지 일괄 추출기</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
        }
        .chart-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .chart-item {
            border: 2px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            text-align: center;
            background: #fafafa;
        }
        .chart-item h3 {
            margin: 0 0 15px 0;
            color: #555;
        }
        .chart-frame {
            width: 100%;
            height: 400px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        .extract-btn {
            background: #28a745;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            margin-top: 10px;
        }
        .extract-btn:hover {
            background: #218838;
        }
        .extract-all-btn {
            background: #007bff;
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            display: block;
            margin: 20px auto;
        }
        .extract-all-btn:hover {
            background: #0056b3;
        }
        .progress {
            margin: 20px 0;
            text-align: center;
            font-weight: bold;
        }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
</head>
<body>
    <div class="container">
        <h1>🎯 RWSL 차트 이미지 일괄 추출기</h1>
        
        <div class="chart-grid">
'''
    
    # 각 HTML 파일에 대한 항목 추가
    for i, html_file in enumerate(html_files, 1):
        filename = os.path.basename(html_file)
        chart_name = filename.replace('.html', '').replace('_', ' ').title()
        
        extractor_html += f'''
            <div class="chart-item">
                <h3>{i}. {chart_name}</h3>
                <iframe id="chart_{i}" class="chart-frame" src="{filename}"></iframe>
                <button class="extract-btn" onclick="extractChart({i}, '{filename}')">이미지 추출</button>
            </div>
'''
    
    extractor_html += '''
        </div>
        
        <button class="extract-all-btn" onclick="extractAllCharts()">🎯 모든 차트 이미지 일괄 추출</button>
        
        <div class="progress" id="progress"></div>
    </div>
    
    <script>
        let extractedCount = 0;
        const totalCharts = ''' + str(len(html_files)) + ''';
        
        function extractChart(index, filename) {
            const iframe = document.getElementById('chart_' + index);
            
            // iframe 내용을 캡처하는 것은 보안상 제한이 있으므로
            // 새 창에서 해당 HTML을 열어서 추출하도록 안내
            const newWindow = window.open(filename, '_blank', 'width=900,height=600');
            
            // 새 창이 로드되면 자동으로 이미지 추출 시작
            newWindow.onload = function() {
                setTimeout(() => {
                    newWindow.html2canvas(newWindow.document.body, {
                        useCORS: true,
                        allowTaint: true,
                        scale: 2,
                        backgroundColor: '#ffffff'
                    }).then(canvas => {
                        const imgData = canvas.toDataURL('image/png');
                        const downloadLink = newWindow.document.createElement('a');
                        downloadLink.href = imgData;
                        downloadLink.download = filename.replace('.html', '.png');
                        downloadLink.click();
                        
                        newWindow.close();
                        extractedCount++;
                        updateProgress();
                    });
                }, 2000);
            };
        }
        
        function extractAllCharts() {
            extractedCount = 0;
            updateProgress();
            
            const htmlFiles = [''' + ', '.join([f'"{os.path.basename(f)}"' for f in html_files]) + '''];
            
            htmlFiles.forEach((filename, index) => {
                setTimeout(() => {
                    extractChart(index + 1, filename);
                }, index * 3000); // 3초 간격으로 순차 추출
            });
        }
        
        function updateProgress() {
            const progress = document.getElementById('progress');
            progress.textContent = `추출 진행률: ${extractedCount}/${totalCharts} (${Math.round(extractedCount/totalCharts*100)}%)`;
        }
    </script>
</body>
</html>'''
    
    # 추출기 HTML 파일 저장
    extractor_file = '/Users/dykim/dev/make-docs/images/chart_image_extractor.html'
    with open(extractor_file, 'w', encoding='utf-8') as f:
        f.write(extractor_html)
    
    print(f"✅ 통합 이미지 추출기 생성 완료: {extractor_file}")
    return extractor_file

def process_rwsl_charts():
    """RWSL 차트 HTML 파일들을 처리하여 이미지 추출 기능 추가"""
    
    # images 폴더의 모든 HTML 파일 찾기
    html_pattern = '/Users/dykim/dev/make-docs/images/*.html'
    html_files = glob.glob(html_pattern)
    
    if not html_files:
        print("❌ images 폴더에서 HTML 파일을 찾을 수 없습니다.")
        return
    
    print(f"🔍 발견된 HTML 파일: {len(html_files)}개")
    
    # 각 HTML 파일에 html2canvas 기능 추가
    processed_files = []
    for html_file in html_files:
        try:
            processed_file = add_html2canvas_to_file(html_file)
            processed_files.append(processed_file)
        except Exception as e:
            print(f"❌ 파일 처리 실패 {html_file}: {e}")
    
    if processed_files:
        # 통합 추출기 페이지 생성
        extractor_file = create_image_extractor_html(processed_files)
        
        print(f"\n🎉 처리 완료!")
        print(f"📊 처리된 HTML 파일: {len(processed_files)}개")
        print(f"🎯 통합 추출기: {extractor_file}")
        print(f"\n📋 사용 방법:")
        print(f"1. {extractor_file} 파일을 브라우저에서 열기")
        print(f"2. '모든 차트 이미지 일괄 추출' 버튼 클릭")
        print(f"3. 각 차트가 새 창에서 열리며 자동으로 PNG 파일 다운로드")
        print(f"4. 다운로드된 이미지들을 images 폴더로 이동")

if __name__ == "__main__":
    process_rwsl_charts()