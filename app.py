import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="3-5 반을 위한 30508 김지성의 수행알리미", layout="wide")

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
    st.subheader("📌 수행평가 목록")
    try:
        # 1. 데이터 불러오기 및 날짜 변환
        df = pd.read_csv(READ_URL)
        if not df.empty:
            df['마감기한'] = pd.to_datetime(df['마감기한'])
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

            # 2. 데이터 분리 (진행 중 vs 마감됨)
            # 오늘 이후인 것들은 마감 기한이 임박한 순(오름차순) 정렬
            active_df = df[df['마감기한'] >= today].sort_values(by='마감기한')
            # 오늘 이전인 것들은 최신 마감 순(내림차순) 정렬
            expired_df = df[df['마감기한'] < today].sort_values(by='마감기한', ascending=False)

            # 3. 진행 중인 수행평가 표시
            st.markdown("#### 🏃‍♂️ 진행 중인 수행평가")
            if not active_df.empty:
                for index, row in active_df.iterrows():
                    days_left = (row['마감기한'] - today).days
                    d_label = f"D-{days_left}" if days_left > 0 else "D-Day"
                    
                    with st.expander(f"[{d_label}] {row['과목']} - {row['마감기한'].strftime('%m/%d')}까지"):
                        st.write(f"**상세 내용:** {row['내용']}")
                        if pd.notna(row.get('image_url')) and str(row['image_url']).startswith("http"):
                            st.image(row['image_url'], width=400)
            else:
                st.info("현재 진행 중인 수행평가가 없습니다. 여유를 즐기세요!")

            # 4. 마감된 수행평가 표시 (구분선 추가)
            if not expired_df.empty:
                st.write("---")
                with st.expander("✅ 마감된 수행평가 보기 (클릭)", expanded=False):
                    for index, row in expired_df.iterrows():
                        st.write(f"~~[{row['마감기한'].strftime('%m/%d')}] {row['과목']}~~")
                        st.caption(f"내용: {row['내용']}")
        else:
            st.write("등록된 내용이 없습니다.")
    except Exception as e:
        st.error(f"데이터 로드 중 오류 발생: {e}")
# --- 제작자 정보 ---
st.markdown("---")
st.caption("제작자: 30508 김지성 | 본 페이지는 실시간 학급 공유용입니다.")
