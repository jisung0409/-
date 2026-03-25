import streamlit as st
import pandas as pd
from datetime import datetime

# 페이지 설정
st.set_page_config(page_title="우리 반 수행평가", layout="centered")

# 데이터 저장을 위한 리스트 초기화 (세션 상태 이용)
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

st.title("📝 학급 수행평가 공지")

# --- 입력 섹션 ---
with st.form("task_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        subject = st.text_input("과목명")
    with col2:
        deadline = st.date_input("마감 기한")
    
    content = st.text_area("수행평가 내용")
    submit_button = st.form_submit_button("등록하기")

    if submit_button:
        if subject and content:
            new_task = {"과목": subject, "내용": content, "마감기한": str(deadline)}
            st.session_state.tasks.append(new_task)
            st.success("등록되었습니다!")
        else:
            st.error("모든 내용을 입력해주세요.")

# --- 목록 표시 섹션 ---
st.subheader("📌 수행평가 리스트")

if st.session_state.tasks:
    df = pd.DataFrame(st.session_state.tasks)
    # 최신순으로 정렬해서 보여줌
    st.table(df.iloc[::-1])
    
    # 데이터 내려받기 기능 (백업용)
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button("엑셀(CSV) 파일로 저장하기", csv, "tasks.csv", "text/csv")
else:
    st.write("아직 등록된 수행평가가 없습니다.")
