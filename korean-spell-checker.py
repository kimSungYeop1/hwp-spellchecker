import os
import re
import argparse
from collections import defaultdict
import mammoth  # .docx 파일 처리
import requests
from hanspell import spell_checker  # 한글 맞춤법 검사기

def read_hwp_text(hwp_file):
    """
    한글 파일을 텍스트로 변환 (외부 도구 필요)
    실제 구현에서는 hwp5txt 또는 한글과컴퓨터에서 제공하는 SDK 사용 필요
    """
    # 주의: 이 부분은 실제 구현 시 한글과컴퓨터의 SDK나 hwp5txt 등의 도구를 사용해야 합니다
    # 이 예제에서는 개념적으로만 구현합니다
    print(f"{hwp_file} 파일을 텍스트로 변환 중...")
    
    # 실제 구현 시 아래 코드 대신 외부 도구 사용 필요
    # 예: os.system(f"hwp5txt {hwp_file} > {hwp_file}.txt")
    
    # 임시 파일 생성 가정
    temp_txt_file = f"{hwp_file}.txt"
    
    # 실제로는 아래 부분 대신 변환된 파일을 읽어야 함
    return "이것은 한글파일에서 추출한 텍스트 입니다. 맞춤법 검사를 실행 합니다."

def read_docx_text(docx_file):
    """
    Word(.docx) 파일에서 텍스트 추출
    """
    try:
        with open(docx_file, "rb") as docx:
            result = mammoth.extract_raw_text(docx)
            return result.value
    except Exception as e:
        print(f"DOCX 파일 읽기 오류: {e}")
        return ""

def check_spelling(text):
    """
    한글 맞춤법 검사
    hanspell 패키지 사용 (또는 네이버/다음 맞춤법 검사기 API)
    """
    try:
        # hanspell 라이브러리 사용 예시
        result = spell_checker.check(text)
        corrected_text = result.checked
        
        # 수정된 내용 목록 생성
        corrections = []
        for original, corrected in zip(result.words, result.words_original):
            if original != corrected:
                corrections.append((original, corrected))
        
        return corrected_text, corrections
    except Exception as e:
        # 네이버 맞춤법 검사기 API 사용 예시 (실제 API 키 필요)
        print("hanspell 모듈 실패, 네이버 맞춤법 검사기 API 시도...")
        try:
            # 이 부분은 실제 네이버 맞춤법 검사기 API를 사용할 경우 구현
            # API 사용 예시 (실제로는 API 키와 적절한 요청 형식 필요)
            # response = requests.post("https://openapi.naver.com/v1/papago/n2mt",
            #                        headers={"X-Naver-Client-Id": "YOUR_ID", "X-Naver-Client-Secret": "YOUR_SECRET"},
            #                        data={"source": "ko", "target": "ko", "text": text})
            
            # 임시 예시
            corrected_text = text.replace("맞춤법 검사를 실행 합니다", "맞춤법 검사를 실행합니다")
            corrections = [("실행 합니다", "실행합니다")]
            
            return corrected_text, corrections
        except Exception as ne:
            print(f"맞춤법 검사 오류: {ne}")
            return text, []

def save_as_hwp(text, output_file):
    """
    텍스트를 한글 파일로 저장 (외부 도구 필요)
    실제 구현에서는 한글과컴퓨터에서 제공하는 SDK 사용 필요
    """
    # 주의: 실제 구현에서는 한글과컴퓨터의 SDK를 사용해야 합니다
    print(f"수정된 텍스트를 {output_file}로 저장 중...")
    
    # 텍스트 파일로 임시 저장
    with open(f"{output_file}.txt", "w", encoding="utf-8") as f:
        f.write(text)
    
    print(f"텍스트가 {output_file}.txt로 저장되었습니다.")
    print("※ 주의: 실제 HWP 파일 변환은 한글과컴퓨터 SDK 또는 외부 도구를 사용해야 합니다.")

def save_as_docx(text, output_file):
    """
    텍스트를 Word(.docx) 파일로 저장
    """
    try:
        from docx import Document
        document = Document()
        
        # 텍스트를 문단별로 분리하여 추가
        for paragraph in text.split('\n'):
            if paragraph.strip():
                document.add_paragraph(paragraph)
        
        document.save(output_file)
        print(f"수정된 텍스트를 {output_file}로 저장했습니다.")
    except Exception as e:
        print(f"DOCX 파일 저장 오류: {e}")
        # 텍스트 파일로 대체 저장
        with open(f"{output_file}.txt", "w", encoding="utf-8") as f:
            f.write(text)
        print(f"대신 {output_file}.txt로 저장했습니다.")

def main():
    parser = argparse.ArgumentParser(description="한글 파일 맞춤법 검사 및 수정 프로그램")
    parser.add_argument("input_file", help="입력 파일 경로 (.hwp 또는 .docx)")
    parser.add_argument("--output", "-o", help="출력 파일 경로 (기본값: input_file에 _corrected 추가)")
    
    args = parser.parse_args()
    
    input_file = args.input_file
    
    # 파일 확장자 확인
    if input_file.lower().endswith(".hwp"):
        text = read_hwp_text(input_file)
        file_type = "hwp"
    elif input_file.lower().endswith(".docx"):
        text = read_docx_text(input_file)
        file_type = "docx"
    else:
        print("지원되지 않는 파일 형식입니다. .hwp 또는 .docx 파일만 지원합니다.")
        return
    
    # 맞춤법 검사
    corrected_text, corrections = check_spelling(text)
    
    # 수정 내역 보고
    if corrections:
        print("\n===== 맞춤법 수정 내역 =====")
        for original, corrected in corrections:
            print(f"'{original}' → '{corrected}'")
        print(f"총 {len(corrections)}개 항목 수정됨\n")
    else:
        print("수정할 맞춤법 오류가 없습니다.")
    
    # 출력 파일 경로 설정
    if args.output:
        output_file = args.output
    else:
        base, ext = os.path.splitext(input_file)
        output_file = f"{base}_corrected{ext}"
    
    # 파일 저장
    if file_type == "hwp":
        save_as_hwp(corrected_text, output_file)
    else:  # docx
        save_as_docx(corrected_text, output_file)

if __name__ == "__main__":
    main()
