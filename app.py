import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# 페이지 기본 설정
# =====================================================
st.set_page_config(
    page_title="한국 글로벌 무역 포지션 대시보드",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# 디자인 설정: 이미지와 완전히 동일한 한지/전통 스타일
# =====================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&family=Noto+Serif+KR:wght@400;600;700;900&display=swap');

    :root {
        --hanji: #f0e2c0;
        --hanji-deep: #d9be8a;
        --ink: #2a1f14;
        --brown: #7a4f2a;
        --light-brown: #a8783d;
        --orange: #c76a28;
        --green: #617046;
        --sage: #8a9564;
        --export-bar: #8B5E3C;
        --import-bar: #7A9147;
        --card: rgba(255, 248, 225, 0.82);
        --line: rgba(94, 60, 31, 0.28);
        --sidebar-bg: #e8d5a8;
    }

    html, body, .stApp {
        background-color: #e8d09a !important;
        background-image:
            url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='400'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='400' height='400' filter='url(%23n)' opacity='0.07'/%3E%3C/svg%3E"),
            radial-gradient(ellipse at 5% 5%, rgba(210,158,72,0.35) 0%, transparent 40%),
            radial-gradient(ellipse at 95% 10%, rgba(97,112,70,0.22) 0%, transparent 35%),
            radial-gradient(ellipse at 50% 95%, rgba(122,79,42,0.18) 0%, transparent 40%),
            linear-gradient(160deg, #f2e3ba 0%, #e8d09a 40%, #d8b878 80%, #ccaa62 100%);
        color: var(--ink);
        font-family: 'Gowun Batang', 'Noto Serif KR', 'Malgun Gothic', serif !important;
    }

    /* 한지 노이즈 텍스처 오버레이 */
    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        background-image:
            radial-gradient(rgba(86,55,31,0.07) 1px, transparent 1px),
            radial-gradient(rgba(255,255,255,0.14) 0.8px, transparent 0.8px);
        background-size: 20px 20px, 14px 14px;
        background-position: 0 0, 7px 7px;
        z-index: 0;
    }

    /* 사이드바 */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #e8d5a8 0%, #dfc898 100%) !important;
        border-right: 2px solid rgba(96,61,32,0.30);
        box-shadow: 4px 0 16px rgba(61,38,19,0.12);
    }
    section[data-testid="stSidebar"] * {
        font-family: 'Gowun Batang', 'Noto Serif KR', serif !important;
        color: #2a1f14 !important;
    }
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stMultiSelect label,
    section[data-testid="stSidebar"] p {
        font-weight: 700 !important;
        font-size: 14px !important;
    }

    /* 사이드바 제목 */
    .sidebar-title {
        font-size: 20px;
        font-weight: 900;
        color: #2a1f14;
        margin-bottom: 2px;
        font-family: 'Noto Serif KR', serif;
    }

    /* 메인 타이틀 */
    .main-title {
        font-family: 'Noto Serif KR', 'Gowun Batang', serif;
        font-size: 44px;
        font-weight: 900;
        color: #1e1408;
        letter-spacing: -1px;
        text-align: center;
        margin-top: 6px;
        margin-bottom: 4px;
        text-shadow: 0 1px 0 rgba(255,255,255,0.35);
    }
    .sub-title {
        text-align: center;
        color: #5d3e20;
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 20px;
        font-family: 'Gowun Batang', serif;
    }
    .title-seal {
        float: right;
        font-size: 28px;
        color: #8b2020;
        border: 2px solid #8b2020;
        padding: 4px 8px;
        border-radius: 4px;
        font-family: serif;
    }

    /* 핵심 지표 카드 */
    .metric-card {
        background: rgba(255, 248, 220, 0.88);
        border: 1.5px solid rgba(120, 80, 30, 0.32);
        border-radius: 12px;
        padding: 16px 12px;
        text-align: center;
        box-shadow: 0 4px 14px rgba(73,45,24,0.12), inset 0 0 0 1px rgba(255,255,255,0.22);
        position: relative;
    }
    .metric-icon {
        font-size: 20px;
        margin-bottom: 4px;
        display: block;
    }
    .metric-label {
        color: #5a3e22;
        font-size: 13px;
        font-weight: 700;
        font-family: 'Gowun Batang', serif;
        margin-bottom: 4px;
    }
    .metric-value {
        color: #1e1408;
        font-size: 30px;
        font-weight: 900;
        font-family: 'Noto Serif KR', serif;
        line-height: 1.1;
    }
    .metric-unit {
        font-size: 13px;
        font-weight: 600;
        color: #5a3e22;
    }
    .metric-note {
        color: #7a5b3d;
        font-size: 11px;
        margin-top: 3px;
    }

    /* 섹션 카드 */
    .paper-card {
        background: rgba(255, 249, 228, 0.80);
        border: 1.5px solid rgba(100, 65, 30, 0.25);
        border-radius: 14px;
        padding: 20px 22px;
        box-shadow: 0 6px 22px rgba(77,48,24,0.10);
        margin-bottom: 16px;
    }
    .paper-card h3 {
        font-family: 'Noto Serif KR', serif;
        font-size: 16px;
        font-weight: 700;
        color: #2a1f14;
        margin-bottom: 10px;
        border-bottom: 1px solid rgba(100,65,30,0.20);
        padding-bottom: 6px;
    }
    .paper-card p, .paper-card li {
        font-size: 14px;
        line-height: 1.75;
        color: #3a2a18;
    }
    .paper-card ul {
        padding-left: 18px;
    }

    /* 인사이트 박스 */
    .insight-box {
        background: rgba(245, 235, 200, 0.85);
        border: 1.5px solid rgba(120,80,30,0.28);
        border-radius: 12px;
        padding: 16px 18px;
        color: #2a1f14;
        margin: 10px 0 16px 0;
        font-weight: 600;
        line-height: 1.8;
        font-size: 14px;
        font-family: 'Gowun Batang', serif;
    }
    .insight-box-title {
        font-weight: 900;
        font-size: 15px;
        margin-bottom: 6px;
        color: #1e1408;
    }

    /* 핵심 인사이트 사이드 패널 */
    .insight-side {
        background: rgba(248, 238, 210, 0.88);
        border: 1.5px solid rgba(120,80,30,0.28);
        border-radius: 12px;
        padding: 18px;
        font-size: 14px;
        line-height: 1.8;
        color: #2a1f14;
        font-family: 'Gowun Batang', serif;
        height: 100%;
    }
    .insight-side h4 {
        font-weight: 900;
        font-size: 15px;
        border-bottom: 1px solid rgba(100,65,30,0.22);
        padding-bottom: 6px;
        margin-bottom: 10px;
    }

    /* 섹션 헤더 */
    .section-header {
        font-family: 'Noto Serif KR', serif;
        font-size: 18px;
        font-weight: 900;
        color: #1e1408;
        padding: 10px 0 6px 0;
        border-bottom: 2px solid rgba(100,65,30,0.25);
        margin-bottom: 16px;
    }

    /* 키워드 pill */
    .keyword-pill {
        display: inline-block;
        padding: 5px 13px;
        margin: 4px;
        border-radius: 100px;
        background: rgba(122,79,42,0.12);
        border: 1px solid rgba(122,79,42,0.28);
        color: #2a1f14;
        font-size: 13px;
        font-weight: 700;
        font-family: 'Gowun Batang', serif;
    }

    /* GVC 카드 */
    .gvc-step {
        background: rgba(255,249,228,0.80);
        border: 1px solid rgba(98,63,34,0.22);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .gvc-step h3 {
        font-size: 15px;
        font-weight: 900;
        color: #1e1408;
        margin-bottom: 8px;
    }
    .gvc-step p {
        font-size: 13px;
        color: #3a2a18;
        margin: 4px 0;
        line-height: 1.6;
    }
    .gvc-arrow {
        font-size: 18px;
        color: #7a4f2a;
        margin: 3px 0;
    }

    /* 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: rgba(220,195,145,0.45);
        border-radius: 12px 12px 0 0;
        padding: 6px 6px 0 6px;
        border-bottom: 2px solid rgba(98,63,34,0.22);
    }
    .stTabs [data-baseweb="tab"] {
        background: rgba(245,230,190,0.55);
        border-radius: 10px 10px 0 0;
        color: #3a2a18;
        font-weight: 700;
        font-family: 'Gowun Batang', serif;
        font-size: 14px;
        border: 1px solid rgba(98,63,34,0.18);
        border-bottom: none;
        padding: 8px 16px;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(200,160,90,0.38) !important;
        color: #1e1408 !important;
        border-color: rgba(98,63,34,0.30) !important;
    }

    /* 테이블/데이터프레임 */
    .stDataFrame {
        background: rgba(255,248,222,0.72);
        border-radius: 8px;
    }

    /* 라디오 버튼 */
    .stRadio > div {
        background: rgba(245,230,190,0.55);
        border-radius: 8px;
        padding: 6px;
        gap: 8px;
    }
    .stRadio label {
        font-family: 'Gowun Batang', serif;
        font-weight: 700;
        color: #2a1f14;
        font-size: 14px;
    }

    /* 전체 폰트 */
    h1, h2, h3, h4, h5, .stMarkdown p, label, .stSelectbox, .stMultiSelect {
        font-family: 'Gowun Batang', 'Noto Serif KR', serif !important;
        color: #2a1f14 !important;
    }

    /* 멀티셀렉트 태그: 갈색 배경 + 흰 글자 */
    [data-baseweb="tag"] {
        background-color: #7a4f2a !important;
        border-color: #5c3a1e !important;
        border-radius: 6px !important;
    }
    [data-baseweb="tag"] span {
        color: #ffffff !important;
        font-family: 'Gowun Batang', serif !important;
        font-weight: 700 !important;
    }
    [data-baseweb="tag"] [role="presentation"] svg {
        fill: rgba(255,255,255,0.80) !important;
    }

    /* 구분선 */
    hr {
        border-color: rgba(98,63,34,0.22);
    }

    /* 하단 캡션 */
    .stCaption {
        color: #6a4a2e !important;
        font-size: 12px;
        font-family: 'Gowun Batang', serif;
    }

    /* 산업 테이블 강조행 */
    .industry-highlight {
        background: rgba(180,130,60,0.22);
        border-radius: 6px;
        padding: 2px 6px;
        font-weight: 900;
    }

    /* 비교 결과 패널 */
    .compare-panel {
        background: rgba(248,238,210,0.88);
        border: 1.5px solid rgba(120,80,30,0.28);
        border-radius: 12px;
        padding: 16px 18px;
        margin-bottom: 12px;
        font-size: 14px;
        line-height: 1.75;
        color: #2a1f14;
    }
    .compare-panel h4 {
        font-weight: 900;
        font-size: 14px;
        margin-bottom: 8px;
        color: #1e1408;
    }

    /* 종합 시사점 */
    .summary-box {
        background: rgba(240,225,185,0.90);
        border: 2px solid rgba(130,85,30,0.30);
        border-radius: 14px;
        padding: 18px 22px;
        font-size: 14px;
        line-height: 1.85;
        color: #1e1408;
        font-weight: 600;
    }

    div[data-testid="stMetricValue"],
    div[data-testid="stMetricLabel"] {
        color: #2a1f14 !important;
        font-family: 'Gowun Batang', serif !important;
    }
</style>
""", unsafe_allow_html=True)

# =====================================================
# 데이터
# =====================================================

trade_partners = pd.DataFrame({
    "국가": ["중국", "미국", "베트남", "일본", "대만", "독일", "싱가포르", "인도", "멕시코", "호주"],
    "수출액_십억달러": [136.2, 124.4, 63.8, 56.7, 50.3, 40.1, 36.7, 33.2, 29.6, 21.1],
    "수입액_십억달러": [104.6, 86.4, 41.2, 36.9, 31.7, 31.4, 26.1, 23.4, 19.2, 13.4],
    "공급망연결지수": [18.7, 15.2, 7.3, 10.8, 8.6, 6.1, 5.4, 4.2, 3.1, 3.6],
    "핵심산업의존도": [92, 90, 78, 75, 72, 60, 48, 45, 42, 36],
    "관계해석": [
        "최대 교역국이자 반도체·중간재 공급망의 핵심 축입니다.",
        "첨단기술, 반도체, 자동차, 배터리 시장에서 전략적 중요성이 가장 큽니다.",
        "생산기지 다변화와 전자제품 조립 공급망에서 중요성이 커지고 있습니다.",
        "소재·부품·장비 공급망에서 협력과 리스크 관리가 모두 필요한 국가입니다.",
        "반도체 생태계에서 한국과 긴밀하게 연결된 핵심 파트너입니다.",
        "자동차, 기계, 친환경 산업 분야에서 비교와 협력 가치가 높은 국가입니다.",
        "동남아 물류·중계무역 및 첨단 제조 연결성이 있는 국가입니다.",
        "신흥 소비시장과 생산거점으로서 장기적 중요성이 높아지고 있습니다.",
        "북미 생산거점 및 자동차 공급망에서 연결성이 커지고 있습니다.",
        "자원 수입과 원자재 안정성 측면에서 중요한 파트너입니다."
    ]
})
trade_partners["총교역액_십억달러"] = trade_partners["수출액_십억달러"] + trade_partners["수입액_십억달러"]
trade_partners["무역수지_십억달러"] = trade_partners["수출액_십억달러"] - trade_partners["수입액_십억달러"]
trade_partners["전략점수"] = (
    trade_partners["총교역액_십억달러"] / trade_partners["총교역액_십억달러"].max() * 40
    + trade_partners["공급망연결지수"] / trade_partners["공급망연결지수"].max() * 40
    + trade_partners["핵심산업의존도"] / 100 * 20
).round(1)

trade_timeline = pd.DataFrame({
    "연도": ["2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025", "2026.06"],
    "수출": [573.1, 526.8, 495.4, 573.7, 604.9, 542.2, 512.5, 644.4, 683.6, 632.2, 683.8, 697.4, 608.4],
    "수입": [525.5, 436.5, 406.2, 478.5, 535.2, 503.3, 467.6, 615.1, 731.4, 642.6, 632.0, 631.8, 470.8],
})
trade_timeline["무역수지"] = trade_timeline["수출"] - trade_timeline["수입"]
trade_timeline["총교역액"] = trade_timeline["수출"] + trade_timeline["수입"]

industries = pd.DataFrame({
    "산업": ["반도체", "자동차", "석유제품", "이차전지", "선박", "철강", "디스플레이", "일반기계", "무선통신기기"],
    "수출액_십억달러": [130.0, 88.0, 50.2, 37.9, 27.6, 24.1, 20.6, 20.2, 18.9],
    "공급망_의존도": ["매우 높음", "높음", "중간", "높음", "중간", "중간", "높음", "중간", "높음"],
    "주요_연결국가": [
        "중국 / 대만 / 미국 / 베트남",
        "미국 / 유럽 / 멕시코",
        "중국 / 일본 / ASEAN",
        "미국 / 유럽 / 중국",
        "유럽 / 중동 / 미국",
        "중국 / 일본 / 유럽",
        "중국 / 베트남",
        "미국 / 중국 / 독일",
        "중국 / 베트남 / 미국"
    ],
    "주요기업": [
        "삼성전자, SK하이닉스",
        "현대자동차, 기아",
        "SK에너지, GS칼텍스, S-OIL",
        "LG에너지솔루션, 삼성SDI, SK온",
        "HD현대중공업, 한화오션",
        "POSCO, 현대제철",
        "삼성디스플레이, LG디스플레이",
        "두산에너빌리티, 현대로템",
        "삼성전자"
    ],
    "산업인사이트": [
        "한국 수출의 핵심 산업으로 중국·미국·대만과의 기술·공급망 관계가 매우 중요합니다.",
        "미국과 유럽의 친환경차·관세 정책에 민감하며 북미 공급망 전략이 중요합니다.",
        "에너지 가격과 중국 수요 변화에 영향을 크게 받는 산업입니다.",
        "전기차 전환과 미국·유럽 보조금 정책에 따라 전략적 가치가 커지고 있습니다.",
        "글로벌 선박 수요와 에너지 운송, 방산·해양 전략과 연결됩니다.",
        "중국 공급 과잉과 EU 규제에 대응해야 하는 산업입니다.",
        "중국·베트남 생산 네트워크와 전자제품 수요에 연결되어 있습니다.",
        "제조업 전반의 설비투자와 글로벌 경기 흐름에 영향을 받습니다.",
        "스마트폰·통신장비 수요와 아시아 생산망에 연결됩니다."
    ]
})

base_oecd = pd.DataFrame({
    "국가": ["한국", "독일", "일본", "미국", "네덜란드", "프랑스", "멕시코", "캐나다"],
    "무역의존도": [85, 89, 45, 27, 156, 66, 83, 68],
    "GVC참여도": [55.1, 52, 41, 38, 61, 45, 49, 46],
    "서비스무역비중": [18, 24, 21, 31, 33, 29, 15, 20],
    "FDI연결성": [62, 68, 48, 76, 85, 64, 59, 66],
    "제조업비중": [27, 19, 20, 11, 10, 10, 18, 10]
})
oecd_average = base_oecd[base_oecd["국가"] != "한국"].drop(columns=["국가"]).mean().round(1)
oecd_sample = pd.concat([
    pd.DataFrame([{"국가": "OECD 평균", **oecd_average.to_dict()}]),
    base_oecd
], ignore_index=True)

value_chain_flows = pd.DataFrame({
    "산업": ["반도체", "배터리", "자동차", "디스플레이"],
    "1단계": ["한국: 핵심 부품·메모리 생산", "한국: 셀·소재 기술", "한국: 완성차·부품 생산", "한국: 패널·부품 생산"],
    "2단계": ["중국·베트남: 조립·가공", "베트남·중국: 중간 생산", "미국·멕시코: 판매·현지 생산", "중국·베트남: 세트 조립"],
    "3단계": ["미국·유럽: 최종 소비·AI 수요", "미국·유럽: 전기차 시장", "북미·유럽: 소비시장", "글로벌 IT 기기 시장"],
    "설명": [
        "한국 반도체는 해외 조립과 글로벌 AI·전자제품 수요로 이어집니다.",
        "배터리는 미국·유럽 친환경 정책과 전기차 시장 변화에 민감합니다.",
        "자동차는 북미 시장과 현지 생산 네트워크의 영향이 큽니다.",
        "디스플레이는 아시아 전자제품 생산망과 강하게 연결됩니다."
    ]
})

# =====================================================
# 보조 함수: 이미지와 동일한 색상 스타일
# =====================================================
EXPORT_COLOR = "#8B5E3C"   # 황갈색 (수출)
IMPORT_COLOR = "#7A9147"   # 올리브 초록 (수입)
BAR_COLORS = ["#9B6E4A", "#7A9147", "#B8860B", "#6B8E5E", "#A0785A",
               "#8FAA60", "#C49A5A", "#6A8C5A", "#BC8C5A", "#7A9E52"]
PAPER_BG = "rgba(0,0,0,0)"
PLOT_BG = "rgba(252,244,220,0.45)"
FONT_COLOR = "#2a1f14"
GRID_COLOR = "rgba(80,50,25,0.14)"
LINE_COLOR = "rgba(80,50,25,0.22)"

TICK_FONT = dict(family="Gowun Batang, serif", size=12, color="#111111")

def set_plot_style(fig, height=None):
    layout_kwargs = dict(
        template="plotly_white",
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,
        title="",   # 빈 문자열로 명시해야 Streamlit이 'undefined' 표시 안 함
        font=dict(family="Noto Serif KR, Gowun Batang, serif", color=FONT_COLOR, size=13),
        title_font=dict(size=16, color=FONT_COLOR, family="Noto Serif KR, serif"),
        legend=dict(bgcolor="rgba(255,248,220,0.55)", bordercolor=LINE_COLOR, borderwidth=1,
                    font=dict(family="Gowun Batang, serif", size=12, color="#111111")),
        margin=dict(l=10, r=10, t=10, b=10),
    )
    if height:
        layout_kwargs["height"] = height
    fig.update_layout(**layout_kwargs)
    fig.update_xaxes(gridcolor=GRID_COLOR, linecolor=LINE_COLOR, tickfont=TICK_FONT)
    fig.update_yaxes(gridcolor=GRID_COLOR, linecolor=LINE_COLOR, tickfont=TICK_FONT)
    return fig

def oecd_comment(selected_country):
    korea = oecd_sample[oecd_sample["국가"] == "한국"].iloc[0]
    target = oecd_sample[oecd_sample["국가"] == selected_country].iloc[0]
    if selected_country == "OECD 평균":
        return ("한국은 무역의존도, GVC 참여도, 제조업 비중이 OECD 평균보다 높아 수출 경쟁력과 산업 역량이 강합니다. "
                "다만 서비스 무역 비중과 FDI 연결성은 개선 여지가 있습니다.")
    if selected_country == "미국":
        return ("한국은 미국 대비 GVC 참여도와 제조업 비중에서 우위를 보입니다. "
                "그러나 서비스 무역 비중과 FDI 연결성은 미국과의 격차를 줄여야 합니다.")
    trade_gap = korea["무역의존도"] - target["무역의존도"]
    gvc_gap = korea["GVC참여도"] - target["GVC참여도"]
    service_gap = korea["서비스무역비중"] - target["서비스무역비중"]
    return (f"한국은 {selected_country} 대비 무역의존도 {abs(trade_gap):.0f}p {'높고' if trade_gap>0 else '낮고'}, "
            f"GVC 참여도는 {abs(gvc_gap):.1f}p {'높습니다' if gvc_gap>0 else '낮습니다'}. "
            f"서비스무역비중은 {abs(service_gap):.0f}p {'높은' if service_gap>0 else '낮은'} 수준입니다.")

# =====================================================
# 사이드바
# =====================================================
with st.sidebar:
    st.markdown('<div class="sidebar-title">🌾 대시보드 컨트롤</div>', unsafe_allow_html=True)
    st.markdown('<hr style="border-color:rgba(98,63,34,0.25);margin:8px 0 14px 0"/>', unsafe_allow_html=True)

    st.markdown("**연도 선택**")
    selected_period = st.selectbox("", ["2014 - 2026.06"], index=0, label_visibility="collapsed")

    st.markdown("**지역 선택**")
    selected_region = st.selectbox("", ["전체 선택"], index=0, label_visibility="collapsed")

    st.markdown("**수출 산업 선택**")
    selected_industries = st.multiselect(
        "",
        options=industries["산업"].tolist(),
        default=industries["산업"].tolist(),
        label_visibility="collapsed"
    )

    st.markdown("**OECD 비교 대상 선택**")
    selected_country = st.selectbox(
        "",
        options=["OECD 평균"] + [c for c in oecd_sample["국가"].tolist() if c not in ["한국", "OECD 평균"]],
        label_visibility="collapsed"
    )

    st.markdown("**전략 파트너 선택**")
    selected_partner = st.selectbox(
        "",
        options=trade_partners.sort_values("전략점수", ascending=False)["국가"].tolist(),
        label_visibility="collapsed"
    )

filtered_industries = industries[industries["산업"].isin(selected_industries)].copy()

# =====================================================
# 헤더 타이틀
# =====================================================
st.markdown("""
<div style="text-align:center; padding: 8px 0 4px 0;">
  <span style="font-size:28px;">🌺</span>
</div>
<h1 class="main-title">한국 글로벌 무역 포지션 대시보드</h1>
<p class="sub-title">세계 경제 속 한국의 역할을 데이터로 이해하다</p>
""", unsafe_allow_html=True)

# =====================================================
# 상단 핵심 지표 카드 5개
# =====================================================
latest = trade_timeline.iloc[-1]
korea_gvc = oecd_sample.loc[oecd_sample["국가"] == "한국", "GVC참여도"].iloc[0]

m1, m2, m3, m4, m5 = st.columns(5)
cards = [
    ("🏛", "총 교역액", f"{latest['총교역액']:.1f}", "십억 달러", "(2026.06 기준)"),
    ("📤", "총 수출액", f"{latest['수출']:.1f}", "십억 달러", "(2026.06 기준)"),
    ("📥", "총 수입액", f"{latest['수입']:.1f}", "십억 달러", "(2026.06 기준)"),
    ("⚖️", "무역수지", f"{latest['무역수지']:.1f}", "십억 달러", "(2026.06 기준)"),
    ("🔗", "한국 GVC 참여도", f"{korea_gvc:.1f}", "%", "(2023 기준)"),
]
for col, (icon, label, val, unit, note) in zip([m1, m2, m3, m4, m5], cards):
    with col:
        st.markdown(f"""
        <div class="metric-card">
          <span class="metric-icon">{icon}</span>
          <div class="metric-label">{label}</div>
          <div class="metric-value">{val}<span class="metric-unit"> {unit}</span></div>
          <div class="metric-note">{note}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =====================================================
# 탭 구성
# =====================================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "① 개요",
    "② 무역 타임라인",
    "③ 산업 분석",
    "④ GVC & 공급망",
    "⑤ OECD 비교",
    "⑥ 전략적 파트너 분석"
])

# =====================================================
# 탭 1: 개요
# =====================================================
with tab1:
    col1, col2, col_insight = st.columns([1.0, 1.4, 0.85])

    with col1:
        st.markdown("""
        <div class="paper-card">
          <h3>프로젝트 방향성</h3>
          <p>이 대시보드는 한국이 세계 경제와 국제 공급망 안에서 어떤 위치에 있는지를 시각화합니다.<br>
          교역 규모, 무역 의존도, 글로벌 가치사슬 참여도, 산업 구조를 통해 한국 경제의 현황과 과제를 종합적으로 이해하는 것이 목표입니다.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="paper-card">
          <h3>핵심 질문</h3>
          <ul>
            <li>한국은 어떤 국가와 가장 강하게 연결되어 있는가?</li>
            <li>한국 경제는 세계 무역에 얼마나 의존하고 있는가?</li>
            <li>한국은 글로벌 가치사슬에서 어떤 역할을 하는가?</li>
            <li>한국의 무역 구조는 시간에 따라 어떻게 변화해왔는가?</li>
          </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-header">국가별 한국 무역 규모 (2026.06 누계)</div>', unsafe_allow_html=True)
        df_overview = trade_partners.sort_values("총교역액_십억달러", ascending=False)
        fig_overview = go.Figure()
        fig_overview.add_trace(go.Bar(
            name="수출액 (십억 달러)",
            x=df_overview["국가"],
            y=df_overview["수출액_십억달러"],
            marker_color=EXPORT_COLOR,
            marker_line_color="rgba(60,30,10,0.2)",
            marker_line_width=0.5,
        ))
        fig_overview.add_trace(go.Bar(
            name="수입액 (십억 달러)",
            x=df_overview["국가"],
            y=df_overview["수입액_십억달러"],
            marker_color=IMPORT_COLOR,
            marker_line_color="rgba(40,60,20,0.2)",
            marker_line_width=0.5,
        ))
        fig_overview.update_layout(barmode="group", height=340, margin=dict(l=10, r=10, t=10, b=60))
        fig_overview = set_plot_style(fig_overview)
        # X축 레이블 가로 정렬 (세로 아님), 검은색
        fig_overview.update_xaxes(tickangle=0, tickfont=dict(family="Gowun Batang, serif", size=12, color="#111111"))
        st.plotly_chart(fig_overview, use_container_width=True)
        st.markdown('<p style="font-size:12px;color:#6a4a2e;">※ 2026년은 1~6월 누계 기준 &nbsp;|&nbsp; ※ 출처: 한국무역협회(KITA), 무역통계</p>', unsafe_allow_html=True)

    with col_insight:
        st.markdown("""
        <div class="insight-side">
          <h4>핵심 인사이트</h4>
          <p>한국은 상위 교역국들과 긴밀히 연결되어 있으며,
          특히 중국, 미국, 베트남과의 교역 비중이 높습니다.</p>
          <br>
          <p>수출이 수입을 상회하며 무역수지 흑자를 유지하고 있습니다.</p>
        </div>
        """, unsafe_allow_html=True)

# =====================================================
# 탭 2: 무역 타임라인
# =====================================================
with tab2:
    st.markdown('<div class="section-header">② 무역 타임라인</div>', unsafe_allow_html=True)

    col_ctrl, col_chart = st.columns([0.25, 0.75])
    with col_ctrl:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**차트 선택**")
        chart_option = st.radio("", ["수출 & 수입", "무역수지", "총 교역액"], label_visibility="collapsed")

    with col_chart:
        if chart_option == "수출 & 수입":
            fig_line = go.Figure()
            fig_line.add_trace(go.Scatter(
                x=trade_timeline["연도"], y=trade_timeline["수출"],
                mode="lines+markers", name="수출액",
                line=dict(color=EXPORT_COLOR, width=2.5),
                marker=dict(size=6, color=EXPORT_COLOR)
            ))
            fig_line.add_trace(go.Scatter(
                x=trade_timeline["연도"], y=trade_timeline["수입"],
                mode="lines+markers", name="수입액",
                line=dict(color=IMPORT_COLOR, width=2.5),
                marker=dict(size=6, color=IMPORT_COLOR)
            ))
            fig_line.update_layout(yaxis_title="십억 달러", height=340)
        elif chart_option == "무역수지":
            colors_bar = [EXPORT_COLOR if v >= 0 else "#c0392b" for v in trade_timeline["무역수지"]]
            fig_line = go.Figure(go.Bar(
                x=trade_timeline["연도"], y=trade_timeline["무역수지"],
                marker_color=colors_bar, name="무역수지"
            ))
            fig_line.update_layout(yaxis_title="십억 달러", height=340)
        else:
            fig_line = go.Figure()
            fig_line.add_trace(go.Scatter(
                x=trade_timeline["연도"], y=trade_timeline["총교역액"],
                fill="tozeroy", mode="lines",
                line=dict(color=EXPORT_COLOR, width=2),
                fillcolor="rgba(139,94,60,0.22)", name="총교역액"
            ))
            fig_line.update_layout(yaxis_title="십억 달러", height=340)
        fig_line = set_plot_style(fig_line)
        st.plotly_chart(fig_line, use_container_width=True)

    st.markdown('<p style="font-size:12px;color:#6a4a2e;">※ 2026년은 1~6월 누계 기준 &nbsp;|&nbsp; ※ 출처: 한국무역협회(KITA), 무역통계</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="insight-box">
    2026년 6월 현재 한국 무역은 반도체와 첨단 제조업 회복의 영향을 크게 받고 있습니다.
    수출 중심 경제 구조는 글로벌 경기·미중 갈등·주요국 관세 정책 변화에 민감하므로 공급망 다변화가 필요합니다.
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# 탭 3: 산업 분석
# =====================================================
with tab3:
    st.markdown('<div class="section-header">③ 산업 분석</div>', unsafe_allow_html=True)

    col_tbl, col_ins = st.columns([1.6, 1])
    with col_tbl:
        # 산업 테이블 (이미지와 동일하게 반도체 강조)
        industry_display = filtered_industries[["산업", "수출액_십억달러", "주요기업"]].copy()
        industry_display.columns = ["산업", "수출액\n(십억 달러)", "주요 기업"]
        industry_display = industry_display.sort_values("수출액\n(십억 달러)", ascending=False)

        # HTML 테이블로 직접 렌더링 (반도체 행 강조)
        rows_html = ""
        for i, row in industry_display.iterrows():
            bg = "background:rgba(180,130,60,0.25);" if row["산업"] == "반도체" else ""
            fw = "font-weight:900;" if row["산업"] == "반도체" else ""
            rows_html += f"""
            <tr style="{bg}{fw}">
              <td style="padding:8px 12px;border-bottom:1px solid rgba(120,80,30,0.15);">{row['산업']}</td>
              <td style="padding:8px 12px;border-bottom:1px solid rgba(120,80,30,0.15);text-align:center;">{row['수출액\n(십억 달러)']}</td>
              <td style="padding:8px 12px;border-bottom:1px solid rgba(120,80,30,0.15);">{row['주요 기업']}</td>
            </tr>"""

        st.markdown(f"""
        <div style="background:rgba(255,249,225,0.82);border:1.5px solid rgba(120,80,30,0.25);border-radius:12px;overflow:hidden;">
        <table style="width:100%;border-collapse:collapse;font-family:'Gowun Batang',serif;font-size:14px;color:#2a1f14;">
          <thead>
            <tr style="background:rgba(200,160,90,0.35);">
              <th style="padding:10px 12px;text-align:left;font-weight:900;">산업</th>
              <th style="padding:10px 12px;text-align:center;font-weight:900;">수출액 (십억 달러)</th>
              <th style="padding:10px 12px;text-align:left;font-weight:900;">주요 기업</th>
            </tr>
          </thead>
          <tbody>{rows_html}</tbody>
        </table>
        </div>
        <p style="font-size:12px;color:#6a4a2e;margin-top:6px;">※ 2026년은 1~6월 누계 기준 &nbsp;|&nbsp; ※ 출처: 한국무역협회(KITA), 품목별 수출입 통계</p>
        """, unsafe_allow_html=True)

    with col_ins:
        # 수평 막대 그래프
        fig_industry_bar = go.Figure(go.Bar(
            x=filtered_industries.sort_values("수출액_십억달러")["수출액_십억달러"],
            y=filtered_industries.sort_values("수출액_십억달러")["산업"],
            orientation="h",
            marker_color=[EXPORT_COLOR if s == "반도체" else "#A07850"
                          for s in filtered_industries.sort_values("수출액_십억달러")["산업"]],
            marker_line_color="rgba(60,30,10,0.2)",
            marker_line_width=0.5,
        ))
        fig_industry_bar.update_layout(xaxis_title="수출액 (십억 달러)", height=380)
        fig_industry_bar = set_plot_style(fig_industry_bar)
        st.plotly_chart(fig_industry_bar, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
    반도체는 한국 수출의 핵심이며, 자동차·이차전지·선박은 미국·유럽 시장 및 글로벌 친환경 전환과 연결됩니다.
    산업별 주요 기업을 함께 보면 한국 무역이 단순한 국가 간 거래가 아니라 기업과 공급망을 통해 움직인다는 점을 알 수 있습니다.
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# 탭 4: GVC & 공급망
# =====================================================
with tab4:
    st.markdown('<div class="section-header">④ GVC & 공급망</div>', unsafe_allow_html=True)

    col_gvc_left, col_gvc_right = st.columns([1, 1.3])

    with col_gvc_left:
        st.markdown("""
        <div class="paper-card">
          <h3>글로벌 공급망 구조 이해</h3>
          <div style="display:flex;align-items:flex-start;gap:10px;margin-bottom:12px;">
            <span style="font-size:22px;">⛏️</span>
            <div><b>원자재 공급</b><br><span style="font-size:13px;">한국은 다양한 국가로부터 원자재와 중간재를 수입합니다.</span></div>
          </div>
          <div style="display:flex;align-items:flex-start;gap:10px;margin-bottom:12px;">
            <span style="font-size:22px;">🏭</span>
            <div><b>국내 생산 및 가공</b><br><span style="font-size:13px;">첨단 기술과 제조 역량으로 제품을 생산·가공합니다.</span></div>
          </div>
          <div style="display:flex;align-items:flex-start;gap:10px;">
            <span style="font-size:22px;">🌐</span>
            <div><b>글로벌 시장 수출</b><br><span style="font-size:13px;">완제품을 전 세계로 수출하여 글로벌 가치사슬에 참여합니다.</span></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        for _, row in value_chain_flows.iterrows():
            st.markdown(f"""
            <div class="gvc-step">
              <h3>{row['산업']}</h3>
              <p>▶ {row['1단계']}</p>
              <div class="gvc-arrow">↓</div>
              <p>▶ {row['2단계']}</p>
              <div class="gvc-arrow">↓</div>
              <p>▶ {row['3단계']}</p>
              <p style="color:#5a3e22;font-size:12px;margin-top:6px;">{row['설명']}</p>
            </div>
            """, unsafe_allow_html=True)

    with col_gvc_right:
        st.markdown('<div style="font-weight:900;font-size:15px;margin-bottom:8px;color:#1e1408;">국가별 공급망 연결 규모 (2023)</div>', unsafe_allow_html=True)

        df_supply = trade_partners.sort_values("공급망연결지수", ascending=True)
        fig_supply = go.Figure(go.Bar(
            x=df_supply["공급망연결지수"],
            y=df_supply["국가"],
            orientation="h",
            marker_color=EXPORT_COLOR,
            marker_line_color="rgba(60,30,10,0.2)",
            marker_line_width=0.5,
            text=df_supply["공급망연결지수"].round(1),
            textposition="outside",
            textfont=dict(family="Gowun Batang, serif", size=12, color=FONT_COLOR)
        ))
        fig_supply.update_layout(xaxis_title="연결 규모 지수", height=320)
        fig_supply = set_plot_style(fig_supply)
        st.plotly_chart(fig_supply, use_container_width=True)
        st.markdown('<p style="font-size:12px;color:#6a4a2e;">※ 출처: OECD TiVA (2023)</p>', unsafe_allow_html=True)

# =====================================================
# 탭 5: OECD 비교
# =====================================================
with tab5:
    st.markdown('<div class="section-header">⑤ OECD 비교</div>', unsafe_allow_html=True)

    col_radar, col_bar, col_result = st.columns([1.1, 1, 0.9])
    categories = ["무역의존도", "GVC참여도", "서비스무역비중", "FDI연결성", "제조업비중"]

    comparison_df = oecd_sample[oecd_sample["국가"].isin(["한국", selected_country])]

    with col_radar:
        st.markdown(f'<div style="font-weight:900;font-size:14px;margin-bottom:6px;">한국 vs OECD 평균 (2023)</div>', unsafe_allow_html=True)
        fig_radar = go.Figure()
        radar_colors = [EXPORT_COLOR, IMPORT_COLOR]
        for i, (_, row) in enumerate(comparison_df.iterrows()):
            fig_radar.add_trace(go.Scatterpolar(
                r=[row[c] for c in categories],
                theta=["무역의존도", "제조업비중", "GVC참여도", "서비스무역비중", "FDI연결성"],
                fill="toself",
                name=row["국가"],
                line=dict(color=radar_colors[i % 2], width=2),
                fillcolor=f"rgba({','.join(['139,94,60' if i==0 else '122,145,71'])},0.20)"
            ))
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100],
                                tickfont=dict(family="Gowun Batang, serif", size=10, color="#111111"),
                                gridcolor=GRID_COLOR),
                angularaxis=dict(tickfont=dict(family="Gowun Batang, serif", size=11, color="#111111"),
                                 gridcolor=GRID_COLOR)
            ),
            title="",
            showlegend=True,
            paper_bgcolor=PAPER_BG,
            plot_bgcolor=PLOT_BG,
            font=dict(family="Noto Serif KR, Gowun Batang, serif", color="#111111"),
            legend=dict(bgcolor="rgba(255,248,220,0.55)", bordercolor=LINE_COLOR, borderwidth=1,
                        font=dict(family="Gowun Batang, serif", size=12, color="#111111")),
            height=320,
            margin=dict(l=30, r=30, t=10, b=20),
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    with col_bar:
        fig_oecd_bar = go.Figure(go.Bar(
            x=oecd_sample.sort_values("무역의존도")["무역의존도"],
            y=oecd_sample.sort_values("무역의존도")["국가"],
            orientation="h",
            marker_color=[EXPORT_COLOR if c == "한국" else "#A07850"
                          for c in oecd_sample.sort_values("무역의존도")["국가"]],
            marker_line_color="rgba(60,30,10,0.2)",
            marker_line_width=0.5,
        ))
        fig_oecd_bar.update_layout(xaxis_title="무역의존도", height=320)
        fig_oecd_bar = set_plot_style(fig_oecd_bar)
        st.plotly_chart(fig_oecd_bar, use_container_width=True)
        st.markdown('<p style="font-size:12px;color:#6a4a2e;">※ 출처: OECD (2023)</p>', unsafe_allow_html=True)

    with col_result:
        st.markdown(f"""
        <div class="compare-panel">
          <h4>비교 분석 결과</h4>
          <div style="background:rgba(200,160,80,0.15);border-radius:8px;padding:10px;margin-bottom:8px;">
            <b>OECD 평균 대비 한국</b><br>
            <span style="font-size:13px;">한국은 무역의존도, GVC 참여도, 제조업 비중이 OECD 평균보다 높아 수출 경쟁력과 산업 역량이 강합니다. 다만 서비스 무역 비중과 FDI 연결성은 개선 여지가 있습니다.</span>
          </div>
          <div style="background:rgba(200,160,80,0.10);border-radius:8px;padding:10px;">
            <b>선택 국가 대비 한국 ({selected_country})</b><br>
            <span style="font-size:13px;">{oecd_comment(selected_country)}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.dataframe(oecd_sample, use_container_width=True, hide_index=True)

# =====================================================
# 탭 6: 전략적 파트너 분석
# =====================================================
with tab6:
    st.markdown('<div class="section-header">⑥ 전략적 파트너 분석</div>', unsafe_allow_html=True)

    # partner_flags를 columns 밖에서 정의해야 col_sum에서도 참조 가능
    partner_flags = {"미국": "🇺🇸", "중국": "🇨🇳", "베트남": "🇻🇳", "일본": "🇯🇵",
                     "대만": "🏳️", "독일": "🇩🇪", "싱가포르": "🇸🇬",
                     "인도": "🇮🇳", "멕시코": "🇲🇽", "호주": "🇦🇺"}

    col_bar6, col_detail, col_sum = st.columns([1.1, 1, 0.85])

    with col_bar6:
        st.markdown('<div style="font-weight:900;font-size:14px;margin-bottom:6px;">전략적 파트너 중요도 (종합 점수)</div>', unsafe_allow_html=True)
        df_sorted = trade_partners.sort_values("전략점수", ascending=True)
        fig_partner = go.Figure(go.Bar(
            x=df_sorted["전략점수"],
            y=df_sorted["국가"],
            orientation="h",
            marker_color=[IMPORT_COLOR if c == selected_partner else "#A07850"
                          for c in df_sorted["국가"]],
            marker_line_color="rgba(60,30,10,0.2)",
            marker_line_width=0.5,
            text=df_sorted["전략점수"].round(1),
            textposition="outside",
            textfont=dict(family="Gowun Batang, serif", size=11, color=FONT_COLOR)
        ))
        fig_partner.update_layout(xaxis_title="종합 점수", height=360)
        fig_partner = set_plot_style(fig_partner)
        st.plotly_chart(fig_partner, use_container_width=True)
        st.markdown('<p style="font-size:12px;color:#6a4a2e;">※ 종합 점수 = 교역 규모(40%) + 수출(30%) + 수입(30%)</p>', unsafe_allow_html=True)

    with col_detail:
        partner_meanings = {
            "미국": ["최대 수출 시장이자 첨단 기술·서비스 협력의 핵심 파트너", "반도체, 배터리, 자동차 등 전략 산업 협력 강화 필요"],
            "중국": ["최대 교역국으로 공급망 압력과 리스크 관리가 필수", "첨단팹, 디지털 전환 분야 협력 확대 기회"],
            "베트남": ["생산 거점 및 수출 시장으로서 중요성 지속 증가", "공급망 다변화 전략의 핵심 파트너"],
            "일본": ["핵심 소재·부품 공급 파트너", "첨단 제조업 및 기술 협력 강화 필요"],
        }
        st.markdown('<div style="font-weight:900;font-size:14px;margin-bottom:8px;">주요 파트너별 전략적 의미</div>', unsafe_allow_html=True)
        for country, meanings in list(partner_meanings.items()):
            flag = partner_flags.get(country, "🌐")
            st.markdown(f"""
            <div style="background:rgba(255,249,225,0.80);border:1.5px solid rgba(120,80,30,0.22);
                        border-radius:10px;padding:12px;margin-bottom:10px;">
              <b style="font-size:15px;">{flag} {country}</b><br>
              {"<br>".join([f'<span style="font-size:13px;color:#3a2a18;">• {m}</span>' for m in meanings])}
            </div>
            """, unsafe_allow_html=True)

    with col_sum:
        partner_detail = trade_partners[trade_partners["국가"] == selected_partner].iloc[0]
        st.markdown(f"""
        <div class="summary-box">
          <b style="font-size:15px;">종합 시사점</b><br><br>
          한국은 주요 교역국들과의 전략적 협력을 지속적으로 강화해야 합니다.<br><br>
          특히 첨단 산업 협력, 공급망 안정화, 신시장 개척을 통해 글로벌 경쟁력을 높여야 합니다.
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="paper-card">
          <h3>{partner_flags.get(selected_partner,'🌐')} {selected_partner} 상세</h3>
          <p><b>총교역액:</b> ${partner_detail['총교역액_십억달러']:.1f}B</p>
          <p><b>공급망 연결 지수:</b> {partner_detail['공급망연결지수']:.1f}</p>
          <p><b>전략 점수:</b> {partner_detail['전략점수']}</p>
          <p style="margin-top:8px;font-size:13px;">{partner_detail['관계해석']}</p>
        </div>
        """, unsafe_allow_html=True)

    st.dataframe(
        trade_partners[["국가", "수출액_십억달러", "수입액_십억달러", "총교역액_십억달러",
                         "공급망연결지수", "핵심산업의존도", "전략점수", "관계해석"
                         ]].sort_values("전략점수", ascending=False),
        use_container_width=True,
        hide_index=True
    )

# =====================================================
# 푸터
# =====================================================
st.markdown("---")
st.caption("출처: 한국무역협회(KITA), 산업통상자원부 수출입 동향, 관세청 무역통계, OECD TiVA, World Bank")
st.caption("제작 도구: Python, Streamlit, Pandas, Plotly")
