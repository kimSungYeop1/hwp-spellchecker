import streamlit as st
import pyhwp
import os

def read_hwp_text(hwp_path):
    """HWP 파일에서 텍스트 추출"""
    try:
        with pyhwp.HWPReader.from_path(hwp_path) as doc:
            text = doc.to_text()
        return text
    except Exception as e:
        return f"HWP 파일을 읽는 중 오류 발생: {e}"

# Streamlit UI 설정
st.title("📄 HWP 맞춤법 검사기")

# 파일 업로드
uploaded_file = st.file_uploader("HWP 파일을 업로드하세요", type=["hwp"])

if uploaded_file is not None:
    # 업로드된 파일을 임시 저장
    temp_file_path = "temp.hwp"
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # HWP 파일 읽기
    original_text = read_hwp_text(temp_file_path)
    st.text_area("📄 원본 텍스트", original_text, height=200)
    
    # 파일 삭제 (선택사항)
    os.remove(temp_file_path)

