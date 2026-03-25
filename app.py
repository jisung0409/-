import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="우리 반 수행평가 공지", layout="centered")

# --- [중요] 구글 시트 정보 설정 ---
# 시트 공유 버튼 -> '링크가 있는 모든 사용자' -> '편집자'로 설정 후 주소 복사
SHEET_URL = st.secrets["gsheets"]["spreadsheet"]
# 주소 뒷부분을 export?format=csv로 변환하여 읽기 전용 URL 생성
CSV_URL = SHEET_URL.replace('/edit#gid=', '/export?format=csv&gid=')

def load_data():
    try:
        return pd.read_csv(CSV_URL)
    except:
        return pd.DataFrame(columns=["과목", "내용", "마감기한"])

st.title("📝 학급 수행평가 게시판")

# --- 데이터 입력 섹션 ---
with st.expander("➕ 새로운 수행평가 추가하기"):
    with st.form("task_form", clear_on_submit=True):
        subject = st.text_input("과목명")
        content = st.text_area("수행평가 내용")
        deadline = st.date_input("마감 기한")
        submit_button = st.form_submit_button("등록하기")
        
        if submit_button:
            if subject and content:
                # 여기에 데이터 저장 로직이 들어갑니다.
                # (현실적으로 Streamlit Cloud에서 직접 시트 쓰기는 
                # 공식 gsheets 연결을 사용하는 것이 가장 좋습니다.)
                st.info("데이터를 저장하려면 아래 '공식 연결 설정'을 완료해야 합니다.")

# --- 데이터 표시 섹션 ---
df = load_data()
st.subheader("📌 현재 공지된 수행평가")
if not df.empty:
    st.table(df.iloc[::-1])
else:
    st.write("등록된 내용이 없습니다.")
