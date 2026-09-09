import streamlit as st
import pandas as pd
import os
import base64

# 1. 페이지 설정
st.set_page_config(page_title="동국제약 맞춤형 제품 단가표", layout="wide")

# 2. 인쇄용 CSS 설정 (표 외의 버튼이나 메뉴는 인쇄 시 숨김)
st.markdown("""
    <style>
    @media print {
        header, footer, .stDeployButton, .no-print { display: none !important; }
        .stApp { background-color: white !important; }
        .print-table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 13pt; }
        .print-table th, .print-table td { border: 1px solid #ccc; padding: 12px; text-align: center; vertical-align: middle; }
        .print-table th { background-color: #f4f4f4 !important; -webkit-print-color-adjust: exact; }
        .product-img { max-height: 80px; object-fit: contain; }
    }
    .print-table { width: 100%; border-collapse: collapse; background: white; margin-bottom: 20px;}
    .print-table th, .print-table td { border: 1px solid #eee; padding: 15px; text-align: center; vertical-align: middle; }
    .print-table th { background-color: #f8f9fa; font-weight: bold; color: #333; }
    .product-img { max-height: 90px; object-fit: contain; border-radius: 8px;}
    </style>
""", unsafe_allow_html=True)

st.title("📄 약국 맞춤형 제품 단가 안내서")
st.markdown("<p class='no-print' style='color:#666;'>원장님께 제안할 제품을 선택한 후 인쇄 버튼을 누르시면 맞춤형 단가표가 출력됩니다.</p>", unsafe_allow_html=True)

# 3. 로컬 이미지를 HTML에서 띄우기 위한 Base64 변환 함수
def get_image_base64(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return f"data:image/png;base64,{base64.b64encode(img_file.read()).decode()}"
    else:
        # 이미지가 없을 경우 빈 공간 처리 또는 동국제약 기본 로고(선택사항)
        return "https://via.placeholder.com/150?text=No+Image" 

# 4. 실제 CSV 데이터 파싱 함수 (주문_템플릿.csv)
@st.cache_data
def load_real_data():
    try:
        # 헤더(첫 줄)가 없거나 섞여있을 수 있으므로 header=None으로 안전하게 읽어옵니다.
        df = pd.read_csv("주문_템플릿.csv", header=None, dtype=str)
        products = []
        
        for row in range(len(df)):
            prod = str(df.iloc[row, 0]).strip()
            
            # 빈칸이거나 안내 문구(제품명 등)는 건너뜁니다.
            if prod == 'nan' or not prod or "제품명" in prod or "종류" in prod or "에키나포스" in prod:
                continue
                
            unit = str(df.iloc[row, 1]).strip()
            if unit == 'nan' or not unit: 
                unit = "EA"
            
            factory_price_raw = str(df.iloc[row, 2]).strip()
            if factory_price_raw == 'nan': 
                factory_price_raw = "-"
                
            selling_price = str(df.iloc[row, 3]).strip()
            if selling_price == 'nan': 
                selling_price = "-"
            
            # 괄호 '(' 를 기준으로 출하가와 할인조건을 분리하여 표에서 예쁘게 보여줍니다.
            base_price = factory_price_raw
            discount_range = "-"
            if '(' in factory_price_raw:
                parts = factory_price_raw.split('(')
                base_price = parts[0].strip()
                discount_range = "(" + parts[1]
                
            products.append({
                "제품명": prod,
                "주문단위": unit,
                "출하가": base_price,
                "구간단가": discount_range,
                "판매가": selling_price,
                "이미지경로": f"images/{prod}.png" 
            })
        return pd.DataFrame(products)
    except Exception as e:
        st.error(f"데이터를 불러오는 데 실패했습니다: {e}")
        return pd.DataFrame()

df = load_real_data()

# 5. 제품 선택기 (158개 제품 전체 로드됨)
st.markdown("<div class='no-print'>", unsafe_allow_html=True)
if not df.empty:
    selected_products = st.multiselect(
        "🗂️ 안내서에 포함할 제품을 검색하고 선택하세요:",
        options=df["제품명"].tolist()
    )

    if selected_products:
        st.components.v1.html(
            '''
            <button onclick="window.parent.print()" style="padding:15px; background-color:#e31837; color:white; border:none; border-radius:8px; cursor:pointer; font-size:18px; font-weight:bold; width:100%; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                🖨️ 현재 선택된 맞춤 단가표 인쇄하기
            </button>
            ''',
            height=70
        )
st.markdown("</div>", unsafe_allow_html=True)
st.divider()

# 6. 인쇄용 깔끔한 HTML 표 렌더링
if not df.empty and selected_products:
    filtered_df = df[df["제품명"].isin(selected_products)]
    
    table_html = "<table class='print-table'>"
    table_html += "<thead><tr><th>제품 이미지</th><th>제품명</th><th>주문단위</th><th>기본 출하가(천원)</th><th>할인 구간단가</th><th>권장 판매가(천원)</th></tr></thead><tbody>"
    
    for _, row in filtered_df.iterrows():
        img_base64 = get_image_base64(row['이미지경로'])
        
        table_html += "<tr>"
        table_html += f"<td><img src='{img_base64}' class='product-img'></td>"
        table_html += f"<td style='font-weight:bold; font-size:1.1em;'>{row['제품명']}</td>"
        table_html += f"<td>{row['주문단위']}</td>"
        table_html += f"<td>{row['출하가']}</td>"
        
        # 구간단가가 있으면 붉은색으로 강조
        color = "#e31837" if row['구간단가'] != "-" else "#333"
        table_html += f"<td style='color:{color}; font-weight:bold;'>{row['구간단가']}</td>"
        table_html += f"<td>{row['판매가']}</td>"
        table_html += "</tr>"
        
    table_html += "</tbody></table>"
    st.markdown(table_html, unsafe_allow_html=True)
else:
    st.info("👆 위에서 제품을 선택하시면 출력용 표가 생성됩니다.")
