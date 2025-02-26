import streamlit as st
import subprocess
import os

def convert_hwp_to_txt(hwp_path):
    """unoconv를 사용하여 HWP 파일을 TXT로 변환"""
    output_path = hwp_path.replace(".hwp", ".txt")
    
    # LibreOffice를 사용하여 변환 실행
    command = f"unoconv -f txt {hwp_path}"
    
    try:
        subprocess.run(command, shell=True, check=True)
        with open(output_path, "r", encoding="utf-8") as f:
            text = f.read()
        return text
    except Exception as e:
        return f"오류 발생: {e}"

# Streamlit UI 설정
st.title("📄 HWP 맞춤법 검사기")

# 파일 업로드
uploaded_file = st.file_uploader("HWP 파일을 업로드하세요", type=["hwp"])

if uploaded_file is not None:
    # 업로드된 파일을 임시 저장
    temp_file_path = "temp.hwp"
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # HWP 파일을 TXT로 변환
    original_text = convert_hwp_to_txt(temp_file_path)
    st.text_area("📄 원본 텍스트", original_text, height=200)
    
    # 파일 삭제 (선택사항)
    os.remove(temp_file_path)


