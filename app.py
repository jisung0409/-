import streamlit as st
import pandas as pd
import requests

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="30508 김지성의 수행평가 게시판", 
    layout="centered", 
    page_icon="📋"
)

# 2. 구글 시트 및 API 정보 (본인 정보 유지)
SHEET_ID = "1uz275qask-1pt4x1MpMXWq7AkGBLx2H6az_9RUvwB3c"
READ_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# ★ 중요: 아까 성공했던 구글 웹 앱 URL을 여기에 다시 넣으세요 ★
API_URL = "https://script.google.com/macros/s/AKfycbynSubYs1Dv_Z1a6283UuHxkLe9KZfmLvtFZxYvv76KIbx86tBAqIazUOFCGV4oKuAIFQ/exec"

# --- 상단 헤더 및 제작자 정보 ---
st.title("📝 우리 반 수행평가 알림판")
st.caption("👨‍💻 제작자: **30508 김지성** (제작자 증명)")

# --- 이용 안내 및 경고 문구 ---
with st.sidebar:
    st.header("📢 이용 안내")
    st.info("""
    - 이 페이지는 우리 반 친구들 모두와 **실시간으로 공유**됩니다.
    - 누구나 수행평가를 직접 추가할 수 있습니다.
    - **주의:** 장난이나 비속어 등 이상한 내용을 적으면 안 됩니다. 
    - 건전한 학급 문화를 위해 협조해 주세요!
    """)
    st.write("---")
    st.success("데이터는 구글 시트에 안전하게 보관됩니다.")

st.markdown("---")

# --- 수행평가 등록 섹션 ---
st.subheader("➕ 새로운 수행평가 추가")
with st.form("task_form", clear_on_submit=True):
    col1, col2 = st.columns([2, 1])
    with col1:
        subject = st.text_input("과목명", placeholder="예: 수학, 영어")
    with col2:
        deadline = st.date_input("마감 기한")
    
    content = st.text_area("수행평가 상세 내용 및 준비물", placeholder="친구들이 알기 쉽게 자세히 적어주세요.")
    
    submit_button = st.form_submit_button("🚀 수행평가 등록하기")

    if submit_button:
        if subject and content:
            # 등록 중임을 알리는 상태 표시
            with st.spinner("데이터를 공유 시트에 기록 중입니다..."):
                try:
                    response = requests.post(API_URL, json={
                        "subject": subject,
                        "content": content,
                        "deadline": str(deadline)
                    })
                    if "Success" in response.text:
                        # 2. 등록 성공 시 메시지 띄우기
                        st.success("✅ 등록 성공! 친구들과 정보가 공유되었습니다.")
                        st.balloons() # 축하 효과
                        st.rerun()
                    else:
                        st.error("등록에 실패했습니다. 다시 시도해 주세요.")
                except Exception as e:
                    st.error(f"서버 연결 오류: {e}")
        else:
            st.warning("과목명과 내용을 모두 입력해 주세요.")

st.markdown("---")

# --- 수행평가 목록 표시 섹션 ---
st.subheader("📌 현재 공유 중인 수행평가")

try:
    # 실시간 데이터 로드
    df = pd.read_csv(READ_URL)
    
    if not df.empty:
        # 최신 등록순으로 보여주기
        st.table(df.iloc[::-1])
    else:
        st.info("아직 등록된 수행평가가 없습니다. 첫 번째 소식을 알려보세요!")
except:
    st.warning("데이터를 불러오는 중입니다. 잠시 후 새로고침(F5) 해주세요.")

# --- 하단 제작자 표시 ---
st.markdown("---")
st.center_text = st.markdown(
    "<p style='text-align: center; color: gray;'>Designed by 30508 김지성 | All data is synced with Google Sheets</p>", 
    unsafe_allow_html=True
)
