import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="우리 반 수행평가", layout="centered")

# 1. 구글 시트 ID (주소창의 d/와 /edit 사이의 문자열)
# 이미 본인의 시트 ID로 설정해 두었습니다.
SHEET_ID = "1uz275qask-1pt4x1MpMXWq7AkGBLx2H6az_9RUvwB3c"
READ_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# 2. ★여기에 붙여넣으세요!★ 
# 아까 Apps Script에서 복사한 '웹 앱 URL'을 아래 큰따옴표 안에 넣으세요.
API_URL = "https://script.google.com/macros/s/AKfycbynSubYs1Dv_Z1a6283UuHxkLe9KZfmLvtFZxYvv76KIbx86tBAqIazUOFCGV4oKuAIFQ/exec"

st.title("📝 학급 수행평가 게시판")
st.info("수행평가 내용을 입력하고 등록 버튼을 눌러주세요.")

# --- 데이터 입력 폼 ---
with st.form("add_form", clear_on_submit=True):
    col1, col2 = st.columns([2, 1])
    with col1:
        sub = st.text_input("과목명", placeholder="예: 국어")
    with col2:
        date = st.date_input("마감일")
    
    con = st.text_area("수행평가 상세 내용")
    submit = st.form_submit_button("🚀 등록하기")
    
    if submit:
        if sub and con:
            try:
                # 구글 앱 스크립트로 데이터 전송
                response = requests.post(API_URL, json={
                    "subject": sub,
                    "content": con,
                    "deadline": str(date)
                })
                if "Success" in response.text:
                    st.success("데이터가 구글 시트에 안전하게 기록되었습니다!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("전송은 됐으나 응답이 올바르지 않습니다.")
            except Exception as e:
                st.error(f"연결 오류: API 주소를 다시 확인해주세요. ({e})")
        else:
            st.warning("과목명과 내용을 모두 입력해주세요.")

st.markdown("---")

# --- 데이터 표시 ---
st.subheader("📌 현재 수행평가 목록")
try:
    # 실시간으로 시트 읽어오기
    df = pd.read_csv(READ_URL)
    if not df.empty:
        # 최신순 정렬
        st.table(df.iloc[::-1])
    else:
        st.write("아직 등록된 수행평가가 없습니다.")
except:
    st.write("데이터를 불러오는 중입니다. 잠시만 기다려주세요...")
