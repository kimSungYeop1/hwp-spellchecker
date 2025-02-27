import os
import re
import argparse
import tempfile
import subprocess
from hanspell import spell_checker  # 한글 맞춤법 검사기

def read_hwp_text(hwp_file):
    """
    한글 파일을 텍스트로 변환 (pyhwp 사용)
    """
    try:
        # 임시 텍스트 파일 생성
        temp_txt = tempfile.mktemp(suffix='.txt')
        
        # hwp5txt 명령어로 변환 시도 (pyhwp 패키지에 포함)
        result = subprocess.run(['hwp5txt', hwp_file, '--output', temp_txt], 
                               capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"HWP 변환 오류: {result.stderr}")
            return None
        
        # 텍스트 파일 읽기
        with open(temp_txt, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # 임시 파일 삭제
        os.remove(temp_txt)
        
        return text
    except Exception as e:
        print(f"HWP 파일 읽기 오류: {e}")
        print("pyhwp 패키지가 올바르게 설치되었는지 확인하세요.")
        return None

def check_spelling(text):
    """
    한글 맞춤법 검사
    hanspell 패키지 사용
    """
    try:
        # 텍스트를 적절한 크기로 분할 (API 한도 고려)
        chunks = [text[i:i+500] for i in range(0, len(text), 500)]
        corrected_chunks = []
        all_corrections = []
        
        # 각 청크별로 맞춤법 검사
        for chunk in chunks:
            result = spell_checker.check(chunk)
            corrected_chunks.append(result.checked)
            
            # 수정된 내용 목록 생성
            for original, corrected in zip(result.words, result.words_original):
                if original != corrected:
                    all_corrections.append((original, corrected))
        
        return ''.join(corrected_chunks), all_corrections
    except Exception as e:
        print(f"맞춤법 검사 오류: {e}")
        return text, []

def save_as_hwp(text, output_file):
    """
    텍스트를 한글 파일로 저장 
    (직접 HWP 생성은 어려우므로 텍스트 파일 생성 후 안내)
    """
    txt_output = f"{os.path.splitext(output_file)[0]}.txt"
    
    # 텍스트 파일로 저장
    with open(txt_output, "w", encoding="utf-8") as f:
        f.write(text)
    
    print(f"수정된 텍스트를 {txt_output}로 저장했습니다.")
    print(f"이 텍스트 파일을 한글로 열어 다시 .hwp로 저장하실 수 있습니다.")

def main():
    parser = argparse.ArgumentParser(description="한글 파일 맞춤법 검사 및 수정 프로그램")
    parser.add_argument("input_file", help="입력 파일 경로 (.hwp)")
    parser.add_argument("--output", "-o", help="출력 파일 경로 (기본값: input_file에 _corrected 추가)")
    
    args = parser.parse_args()
    
    input_file = args.input_file
    
    # 파일 확장자 확인
    if not input_file.lower().endswith(".hwp"):
        print("지원되지 않는 파일 형식입니다. .hwp 파일만 지원합니다.")
        return
    
    # 한글 파일 텍스트 추출
    print(f"{input_file} 에서 텍스트 추출 중...")
    text = read_hwp_text(input_file)
    
    if not text:
        print("한글 파일에서 텍스트를 추출할 수 없습니다.")
        print("필요 패키지 설치: pip install git+https://github.com/mete0r/pyhwp")
        return
    
    # 맞춤법 검사
    print("맞춤법 검사 진행 중...")
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
    save_as_hwp(corrected_text, output_file)
    
    print("\n프로그램 실행이 완료되었습니다.")
    print("참고: 원본 한글 파일의 서식은 유지되지 않습니다.")

if __name__ == "__main__":
    main()
