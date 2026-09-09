import streamlit as st
import pandas as pd

# 1. 페이지 설정 (넓게 쓰기)
st.set_page_config(page_title="맞춤형 제품 단가표", layout="wide")

# 2. 🖨️ 인쇄 최적화를 위한 마법의 CSS 코드
# 웹에서 보이는 버튼이나 메뉴를 '인쇄' 시에는 모두 숨기고, 깔끔한 표만 나오게 만듭니다.
st.markdown("""
    <style>
    @media print {
        /* 스트림릿 기본 메뉴, 사이드바, 여백 등 인쇄 시 숨기기 */
        header, footer, .stDeployButton, .no-print { display: none !important; }
        .stApp { background-color: white !important; }
        
        /* 인쇄될 표 스타일 */
        .print-table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 13pt; }
        .print-table th, .print-table td { border: 1px solid #ccc; padding: 12px; text-align: center; }
        .print-table th { background-color: #f4f4f4 !important; -webkit-print-color-adjust: exact; }
        .product-img { max-height: 80px; object-fit: contain; }
    }
    
    /* 평상시 웹 화면에서의 표 스타일 */
    .print-table { width: 100%; border-collapse: collapse; background: white; }
    .print-table th, .print-table td { border: 1px solid #eee; padding: 15px; text-align: center; vertical-align: middle; }
    .print-table th { background-color: #f8f9fa; font-weight: bold; color: #333; }
    .product-img { max-height: 90px; object-fit: contain; }
    </style>
""", unsafe_allow_html=True)

st.title("📄 맞춤형 제품 단가 안내서")
st.markdown("<p class='no-print' style='color:#666;'>안내가 필요한 제품을 선택하신 후 인쇄 버튼을 누르시면, 선택한 항목만 깔끔하게 출력됩니다.</p>", unsafe_allow_html=True)

# 3. 데이터 준비 (현재는 임시 이미지 링크 사용, 추후 실제 제품 이미지 주소로 변경)
data = [
    {"제품명": "인사돌 정(100T)", "이미지": "https://via.placeholder.com/150?text=Insadol", "주문단위": "EA", "출하가": "28,000", "구간단가": "-", "판매가": "32,000"},
    {"제품명": "마데카솔케어 6g", "이미지": "https://via.placeholder.com/150?text=Madecasol", "주문단위": "10.0", "출하가": "4,200", "구간단가": "4,000 (30개~)", "판매가": "5,500"},
    {"제품명": "위스콘 더블액션", "이미지": "https://via.placeholder.com/150?text=Wiscon", "주문단위": "20", "출하가": "1,540", "구간단가": "1,400 (100개~)", "판매가": "3,000"},
    {"제품명": "사라펜 플라스타", "이미지": "https://via.placeholder.com/150?text=Sarapen", "주문단위": "50.0", "출하가": "5,200", "구간단가": "4,700 (100개~)", "판매가": "10,000 (3개)"},
    {"제품명": "판시딜 캡슐(180C)", "이미지": "https://via.placeholder.com/150?text=Pancidil", "주문단위": "EA", "출하가": "45,000", "구간단가": "43,000 (50개~)", "판매가": "50,000"}
]
df = pd.DataFrame(data)

# 4. 인쇄할 제품 선택 (스트림릿의 멀티셀렉트 기능 활용)
st.markdown("<div class='no-print'>", unsafe_allow_html=True)
selected_products = st.multiselect(
    "🗂️ 안내서에 포함할 제품을 선택하세요:",
    options=df["제품명"].tolist(),
    default=["인사돌 정(100T)", "마데카솔케어 6g"] # 처음에 기본으로 선택되어 있을 항목
)

# 자바스크립트를 이용한 인쇄 버튼 생성 (화면에서는 보이고, 인쇄물에서는 안 보이게 처리)
if selected_products:
    st.components.v1.html(
        '''
        <button onclick="window.parent.print()" style="padding:12px 24px; background-color:#28a745; color:white; border:none; border-radius:5px; cursor:pointer; font-size:16px; font-weight:bold; width:100%;">
            🖨️ 현재 선택된 목록 인쇄하기
        </button>
        ''',
        height=60
    )
st.markdown("</div>", unsafe_allow_html=True)
st.divider()

# 5. 선택된 제품만 모아서 깔끔한 HTML 표로 렌더링
if selected_products:
    # 선택된 제품만 필터링
    filtered_df = df[df["제품명"].isin(selected_products)]
    
    # 표 그리기 시작
    table_html = "<table class='print-table'>"
    table_html += "<thead><tr><th>제품 이미지</th><th>제품명</th><th>주문단위</th><th>기본 출하가</th><th>할인 구간단가</th><th>권장 판매가</th></tr></thead><tbody>"
    
    # 데이터 채워넣기
    for _, row in filtered_df.iterrows():
        table_html += "<tr>"
        table_html += f"<td><img src='{row['이미지']}' class='product-img'></td>"
        table_html += f"<td style='font-weight:bold; font-size:1.1em;'>{row['제품명']}</td>"
        table_html += f"<td>{row['주문단위']}</td>"
        table_html += f"<td>{row['출하가']}원</td>"
        # 할인 구간이 있을 경우 붉은색으로 눈에 띄게 강조
        color = "#e31837" if row['구간단가'] != "-" else "#333"
        table_html += f"<td style='color:{color}; font-weight:bold;'>{row['구간단가']}</td>"
        table_html += f"<td>{row['판매가']}원</td>"
        table_html += "</tr>"
        
    table_html += "</tbody></table>"
    
    # 스트림릿 화면에 HTML 표 출력
    st.markdown(table_html, unsafe_allow_html=True)
else:
    st.info("제품을 선택하시면 표가 생성됩니다.")
