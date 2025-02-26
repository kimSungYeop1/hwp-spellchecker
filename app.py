import streamlit as st
import olefile
from hanspell import spell_checker
import os

def read_hwp_text(hwp_path):
    """HWP 파일에서 텍스트 추출"""
    with olefile.OleFileIO(hwp_path) as ole:
        encoded_text = ole.openstream('BodyText').read()
        decoded_text = encoded_text.decode('utf-16')  # HWP는 UTF-16을 사용
    return decoded_text

def correct_spelling(text):
    """맞춤법 검사 및 수정"""
    results = spell_checker.check(text).as_dict()
    corrected_text = results.get('checked', text)
    return corrected_text

def save_text_to_hwp(output_path, text):
    """수정된 텍스트를 HWP 파일로 저장 (TXT 변환 후 가능)"""
    with open(output_path, "w", encoding="utf-16") as f:
        f.write(text)

# Streamlit UI 설정
st.title("📄 한글(HWP) 맞춤법 검사기")
st.write("HWP 파일을 업로드하면 맞춤법을 검사하고 수정합니다.")

uploaded_file = st.file_uploader("HWP 파일 업로드", type=['hwp'])

if uploaded_file:
    # HWP 파일 읽기
    with open("temp.hwp", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    original_text = read_hwp_text("temp.hwp")
    st.text_area("📄 원본 텍스트", original_text, height=200)
    
    # 맞춤법 검사 및 수정
    corrected_text = correct_spelling(original_text)
    st.text_area("✅ 수정된 텍스트", corrected_text, height=200)

    # 수정된 HWP 저장
    output_file = "corrected.hwp"
    save_text_to_hwp(output_file, corrected_text)
    
    # 파일 다운로드 버튼 제공
    with open(output_file, "rb") as f:
        st.download_button("📥 수정된 HWP 파일 다운로드", f, file_name="corrected.hwp")
