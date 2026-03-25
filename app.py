import streamlit as st
import pandas as pd
import json
import os

# 파일 저장 경로 설정
DATA_FILE = 'tasks.json'

# 데이터 불러오기 함수
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# 데이터 저장 함수
def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 페이지 설정
st.set_page_config(page_title="우리 반 수행평가 게시판", layout="centered")

st.title("📝 학급 수행평가 공지")
st.info("새로운 수행평가를 등록하면 아래 목록에 자동으로 추가됩니다.")

# 데이터 로드
if 'tasks' not in st.session_state:
    st.session_state.tasks = load_data()

# --- 수행평가 입력 섹션 ---
with st.expander("➕ 새로운 수행평가 추가하기", expanded=True):
    with st.form("task_form", clear_on_submit=True):
        subject = st.text_input("과목명", placeholder="예: 수학, 영어")
        content = st.text_area("수행평가 내용", placeholder="평가 내용과 준비물을 입력하세요.")
        deadline = st.date_input("마감 기한")
        
        submit_button = st.form_submit_button("등록하기")
        
        if submit_button:
            if subject and content:
                new_task = {
                    "과목": subject,
                    "내용": content,
                    "마감기한": str(deadline)
                }
                st.session_state.tasks.append(new_task)
                save_data(st.session_state.tasks)
                st.success("새로운 수행평가가 등록되었습니다!")
            else:
                st.error("과목명과 내용을 모두 입력해주세요.")

# --- 수행평가 목록 표시 섹션 ---
st.subheader("📌 현재 공지된 수행평가")

if st.session_state.tasks:
    # 표 형태로 깔끔하게 보여주기 위해 데이터프레임 변환
    df = pd.DataFrame(st.session_state.tasks)
    # 역순으로 보여주기 (최신순)
    st.table(df.iloc[::-1]) 
else:
    st.write("현재 등록된 수행평가가 없습니다. 여유로운 날이네요!")

# --- 데이터 초기화 버튼 (관리용) ---
if st.button("전체 삭제 (주의)"):
    st.session_state.tasks = []
    save_data([])
    st.rerun()
