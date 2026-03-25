import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="우리 반 수행평가 게시판", layout="centered", page_icon="📝")

st.title("📝 학급 수행평가 공지")
st.markdown("---")

# 1. 구글 시트 연결 (Secrets의 [connections.gsheets] 설정을 사용함)
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # 시트 데이터 읽어오기 (캐시 유효시간 10초로 설정하여 실시간성 확보)
    df = conn.read(ttl=10)
except Exception as e:
    st.error(f"시트 연결 중 오류가 발생했습니다: {e}")
    st.info("💡 Tip: Streamlit Cloud의 Secrets 설정이 정확한지 확인하세요.")
    st.stop()

# 2. 새로운 수행평가 추가 양식
with st.expander("➕ 새로운 수행평가 등록하기", expanded=False):
    with st.form("add_task_form", clear_on_submit=True):
        subject = st.text_input("과목명 (예: 수학, 영어)")
        content = st.text_area("수행평가 내용 및 공지사항")
        deadline = st.date_input("마감 기한")
        
        submit_btn = st.form_submit_button("등록하기")
        
        if submit_btn:
            if subject and content:
                # 새 행 데이터 생성
                new_row = pd.DataFrame([{
                    "과목": subject,
                    "내용": content,
                    "마감기한": str(deadline)
                }])
                
                # 기존 데이터에 추가 후 구글 시트 업데이트
                updated_df = pd.concat([df, new_row], ignore_index=True)
                conn.update(data=updated_df)
                
                st.success("성공적으로 등록되었습니다!")
                st.balloons()
                # 데이터 새로고침
                st.cache_data.clear()
                st.rerun()
            else:
                st.warning("과목명과 내용을 모두 입력해주세요.")

# 3. 수행평가 목록 표시
st.subheader("📌 현재 공지된 수행평가 목록")

if not df.empty:
    # 최신 등록순으로 보여주기 위해 역순 출력
    # 인덱스(번호) 없이 깔끔하게 표로 표시
    st.table(df.iloc[::-1])
else:
    st.info("현재 등록된 수행평가가 없습니다. 깨끗하네요!")

st.markdown("---")
st.caption("관리자: 수행평가 등록 후 구글 시트에서 직접 수정도 가능합니다.")
