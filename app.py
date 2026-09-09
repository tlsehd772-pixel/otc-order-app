import streamlit as st
import pandas as pd

# 페이지 기본 설정
st.set_page_config(page_title="스마트 발주/견적 정리 시스템", layout="wide")

st.title("📦 스마트 발주/견적 정리 시스템")

# 1. 데이터 로드 (실제 환경에서는 캐싱을 사용하여 속도 최적화)
@st.cache_data
def load_data():
    # 예시 데이터 (실제로는 pd.read_csv("주문_템플릿.csv") 후 전처리 로직 적용)
    return pd.DataFrame([
        {"제품명": "인사돌 정(100T)", "주문단위": "EA", "출하가": "28", "할인구간": "-", "판매가": "32"},
        {"제품명": "마데카솔케어 6g", "주문단위": "10.0", "출하가": "4.2", "할인구간": "4(30~)", "판매가": "5.5"},
        {"제품명": "위스콘 더블액션", "주문단위": "20", "출하가": "1.54", "할인구간": "(~80)/1.4(100~)", "판매가": "3.0"},
        {"제품명": "사라펜 플라스타", "주문단위": "50.0", "출하가": "5.2", "할인구간": "4.7(100~)", "판매가": "10(3)"}
    ])

df = load_data()

# 세션 상태 초기화 (선택된 제품 목록 저장)
if 'cart' not in st.session_state:
    st.session_state.cart = []

col1, col2 = st.columns([1, 1])

# 왼쪽: 제품 카탈로그
with col1:
    st.header("제품 카탈로그")
    for index, row in df.iterrows():
        with st.container():
            st.write(f"**{row['제품명']}** (단위: {row['주문단위']} / 출하가: {row['출하가']}천원)")
            if st.button(f"추가하기", key=f"add_{index}"):
                st.session_state.cart.append(row.to_dict())
                st.rerun()
            st.divider()

# 오른쪽: 견적서 및 인쇄 영역
with col2:
    st.header("선택된 제품 요약")
    
    if st.session_state.cart:
        cart_df = pd.DataFrame(st.session_state.cart)
        st.dataframe(cart_df, hide_index=True, use_container_width=True)
        
        if st.button("초기화"):
            st.session_state.cart = []
            st.rerun()
            
        # 브라우저 기본 인쇄 기능 호출을 위한 자바스크립트 버튼
        components_html = """
        <button onclick="window.print()" style="padding:10px; background-color:#28a745; color:white; border:none; border-radius:5px; cursor:pointer;">
            🖨️ 인쇄하기
        </button>
        """
        st.components.v1.html(components_html, height=50)
    else:
        st.info("선택된 제품이 없습니다.")