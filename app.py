import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="30508 김지성의 수행알리미", layout="wide")

# 2. 정보 설정 (본인의 ID와 새로운 API 주소를 넣으세요)
SHEET_ID = "1uz275qask-1pt4x1MpMXWq7AkGBLx2H6az_9RUvwB3c"
READ_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
API_URL = "https://script.google.com/macros/s/AKfycbyp29u67mqeOkUfQwy1m960us5s4MVIobSCxcRJpNqwRS7gWhrN3OztjyybbLjYxw7woA/exec"

# --- [추가] D-Day 계산 함수 ---
def get_dday(target_date_str, label):
    target_date = datetime.strptime(target_date_str, "%Y-%m-%d")
    today = datetime.now()
    delta = target_date - today
    days = delta.days + 1
    if days > 0:
        return f"{label}: **D-{days}**"
    elif days == 0:
        return f"{label}: **D-Day**"
    else:
        return f"{label}: **종료**"

# --- 상단 D-Day 섹션 ---
st.markdown("### 📅 주요 시험 일정")
d1, d2, d3 = st.columns(3)
with d1:
    st.info(get_dday("2026-04-28", "📝 중간고사"))
with d2:
    st.info(get_dday("2026-05-07", "📊 5월 모의고사"))
with d3:
    st.warning(get_dday("2026-11-19", "🎓 수능"))

st.write("---")

# --- 좌우 레이아웃 나누기 (왼쪽: 목록, 오른쪽: 추가) ---
col_list, col_add = st.columns([2, 1])

with col_add:
    st.subheader("➕ 수행평가 추가")
    with st.form("add_form", clear_on_submit=True):
        sub = st.text_input("과목명")
        date = st.date_input("마감 기한")
        con = st.text_area("상세 내용")
        img_url = st.text_input("사진 URL (선택)", placeholder="이미지 링크를 복사해 넣으세요")
        
        st.caption("⚠️ 이상한 내용을 적으면 사망할지도 모릅니다")
        submit = st.form_submit_button("등록하기")
        
        if submit and sub and con:
            response = requests.post(API_URL, json={
                "subject": sub,
                "content": con,
                "deadline": str(date),
                "image_url": img_url
            })
            if "Success" in response.text:
                st.success("등록 성공!")
                st.rerun()

with col_list:
    st.subheader("📌 현재 공유 중인 수행평가")
    try:
        # 실시간 데이터 로드 (캐시 방지를 위해 파라미터 추가)
        df = pd.read_csv(READ_URL + f"&t={datetime.now().timestamp()}")
        
        if not df.empty:
            # 컬럼명이 시트와 맞는지 확인 (보통 4번째 열이 image_url)
            # 만약 시트 첫 행에 제목이 없다면 header=None으로 읽어야 할 수도 있습니다.
            df.columns = ["과목", "내용", "마감기한", "image_url"]
            
            df['마감기한'] = pd.to_datetime(df['마감기한'])
            df = df.sort_values(by='마감기한')

            for index, row in df.iterrows():
                days_left = (row['마감기한'] - datetime.now()).days + 1
                d_label = f"D-{days_left}" if days_left > 0 else "마감"
                
                with st.expander(f"[{d_label}] {row['과목']} - {row['마감기한'].strftime('%m/%d')}까지"):
                    st.write(f"**상세 내용:** {row['내용']}")
                    
                    # 이미지 주소 유효성 검사 강화
                    img_path = str(row['image_url']).strip()
                    if img_path.startswith("http"):
                        st.image(img_path, caption="참고 자료", use_container_width=True)
                    else:
                        st.caption("📷 등록된 사진이 없습니다.")
        else:
            st.info("등록된 수행평가가 없습니다.")
    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
# --- 제작자 정보 ---
st.markdown("---")
st.caption("제작자: 30508 김지성 | 본 페이지는 실시간 학급 공유용입니다.")
