import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="우리 반 수행평가 게시판", layout="centered")

st.title("📝 학급 수행평가 공지 (Google Sheets 연동)")

# 구글 시트 연결 설정
conn = st.connection("gsheets", type=GSheetsConnection)

# 기존 데이터 불러오기
df = conn.read(ttl="1m") # 1분마다 캐시 갱신

# --- 수행평가 입력 섹션 ---
with st.expander("➕ 새로운 수행평가 추가하기", expanded=True):
    with st.form("task_form", clear_on_submit=True):
        subject = st.text_input("과목명")
        content = st.text_area("수행평가 내용")
        deadline = st.date_input("마감 기한")
        
        submit_button = st.form_submit_button("등록하기")
        
        if submit_button:
            if subject and content:
                # 새 데이터 생성
                new_row = pd.DataFrame([{
                    "과목": subject,
                    "내용": content,
                    "마감기한": str(deadline)
                }])
                
                # 기존 데이터에 추가
                updated_df = pd.concat([df, new_row], ignore_index=True)
                
                # 구글 시트에 업데이트 (시트 URL은 secrets에 저장됨)
                conn.update(data=updated_df)
                
                st.success("구글 시트에 성공적으로 기록되었습니다!")
                st.cache_data.clear() # 캐시 삭제 후 새로고침
                st.rerun()
            else:
                st.error("모든 필드를 입력해주세요.")

# --- 목록 표시 ---
st.subheader("📌 현재 공지된 수행평가")
if not df.empty:
    st.table(df.iloc[::-1]) # 최신순
else:
    st.write("등록된 내용이 없습니다.")
