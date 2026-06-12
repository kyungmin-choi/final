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
# 한지/민화풍 디자인 설정
# =====================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&family=Nanum+Myeongjo:wght@400;700;800&family=Song+Myung&display=swap');

    :root {
        --paper: #efe0bd;
        --paper2: #e6cf9f;
        --ink: #2f2116;
        --brown: #7b4b27;
        --brown2: #9b6a36;
        --deep: #4b2f1b;
        --green: #607141;
        --sage: #87935f;
        --ochre: #b9873a;
        --orange: #c66b2b;
        --card: rgba(255, 247, 221, 0.74);
        --line: rgba(84, 52, 25, 0.26);
    }

    .stApp {
        background:
            radial-gradient(circle at 12% 8%, rgba(194, 125, 46, 0.22), transparent 28%),
            radial-gradient(circle at 88% 18%, rgba(96, 113, 65, 0.16), transparent 31%),
            radial-gradient(circle at 22% 84%, rgba(92, 61, 31, 0.13), transparent 32%),
            linear-gradient(135deg, #f0dfb8 0%, #ead2a2 46%, #dfbd83 100%);
        color: var(--ink);
        font-family: 'Gowun Batang', 'Nanum Myeongjo', serif;
    }

    /* 한지 질감 */
    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        z-index: 0;
        pointer-events: none;
        background-image:
            radial-gradient(rgba(56, 35, 18, 0.08) 0.7px, transparent 0.8px),
            radial-gradient(rgba(255, 255, 255, 0.16) 0.8px, transparent 0.9px),
            linear-gradient(45deg, rgba(80, 50, 23, 0.04) 25%, transparent 25%, transparent 75%, rgba(80, 50, 23, 0.04) 75%),
            linear-gradient(-45deg, rgba(255,255,255,0.05) 25%, transparent 25%, transparent 75%, rgba(255,255,255,0.05) 75%);
        background-size: 17px 17px, 11px 11px, 42px 42px, 42px 42px;
        opacity: 0.78;
    }

    .block-container {
        position: relative;
        z-index: 1;
        padding-top: 2.1rem;
        padding-bottom: 3rem;
    }

    section[data-testid="stSidebar"] {
        background: rgba(236, 216, 174, 0.88);
        border-right: 1px solid rgba(75, 47, 27, 0.28);
        box-shadow: 8px 0 28px rgba(56, 36, 18, 0.10);
    }

    section[data-testid="stSidebar"] * {
        font-family: 'Gowun Batang', 'Nanum Myeongjo', serif;
        color: var(--ink);
    }

    h1, h2, h3, h4, .main-title {
        font-family: 'Song Myung', 'Nanum Myeongjo', serif;
        color: var(--ink);
    }

    .main-title {
        font-size: 52px;
        font-weight: 400;
        letter-spacing: -0.5px;
        margin-bottom: 4px;
        text-align: center;
        color: #2d1b10;
        text-shadow: 0 2px 0 rgba(255,255,255,0.18);
    }

    .sub-title {
        text-align: center;
        color: #4f3521;
        font-size: 18px;
        margin-bottom: 26px;
        font-weight: 700;
    }

    .paper-card {
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 22px;
        box-shadow: inset 0 0 0 1px rgba(255,255,255,0.20), 0 8px 28px rgba(79, 48, 22, 0.10);
        margin-bottom: 18px;
        position: relative;
    }

    .paper-card::after {
        content: "";
        position: absolute;
        inset: 8px;
        border: 1px solid rgba(93, 61, 32, 0.08);
        border-radius: 12px;
        pointer-events: none;
    }

    .metric-card {
        background: rgba(255, 246, 219, 0.78);
        border: 1px solid rgba(86, 55, 30, 0.25);
        border-radius: 14px;
        padding: 17px 12px;
        text-align: center;
        box-shadow: inset 0 0 0 1px rgba(255,255,255,0.22), 0 8px 20px rgba(73, 45, 24, 0.08);
        min-height: 122px;
    }

    .metric-label {
        color: #5f4028;
        font-size: 14px;
        font-weight: 800;
    }

    .metric-value {
        color: #3a2214;
        font-size: 29px;
        font-weight: 900;
        font-family: 'Nanum Myeongjo', serif;
        margin-top: 8px;
    }

    .metric-unit {
        color: #3a2214;
        font-size: 13px;
        font-weight: 700;
        margin-top: 3px;
    }

    .metric-note {
        color: #78583a;
        font-size: 12px;
        margin-top: 5px;
    }

    .keyword-pill {
        display: inline-block;
        padding: 7px 13px;
        margin: 5px;
        border-radius: 100px;
        background: rgba(123, 75, 39, 0.10);
        border: 1px solid rgba(123, 75, 39, 0.22);
        color: #3b2516;
        font-size: 13px;
        font-weight: 800;
    }

    .insight-box {
        background: rgba(126, 82, 43, 0.11);
        border-left: 5px solid #7b4b27;
        border-radius: 12px;
        padding: 15px 18px;
        color: #342216;
        margin: 12px 0 18px 0;
        font-weight: 700;
        line-height: 1.8;
    }

    .gvc-card {
        background: rgba(255, 249, 231, 0.80);
        border: 1px solid rgba(98, 63, 34, 0.22);
        border-radius: 14px;
        padding: 18px;
        margin-bottom: 14px;
        box-shadow: 0 5px 16px rgba(62, 38, 18, 0.08);
    }

    .gvc-title {
        font-family: 'Song Myung', 'Nanum Myeongjo', serif;
        font-size: 24px;
        color: #2f2116;
        margin-bottom: 8px;
    }

    .gvc-flow {
        font-weight: 800;
        color: #52321d;
        line-height: 1.9;
    }

    .gvc-desc {
        color: #5c432e;
        font-size: 14px;
        line-height: 1.7;
        margin-top: 8px;
    }

    .partner-card {
        background: rgba(255, 247, 221, 0.78);
        border: 1px solid rgba(86, 55, 30, 0.22);
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 12px;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 5px;
        border-bottom: 1px solid rgba(98,63,34,0.26);
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 248, 225, 0.46);
        border-radius: 12px 12px 0 0;
        color: #3b2516;
        font-weight: 900;
        font-family: 'Gowun Batang', 'Nanum Myeongjo', serif;
    }

    .stTabs [aria-selected="true"] {
        background: rgba(123, 75, 39, 0.18);
        color: #2f2118;
    }

    div[data-testid="stDataFrame"] {
        background: rgba(255, 248, 225, 0.60);
    }

    .source-note {
        color: #694c33;
        font-size: 12px;
        line-height: 1.7;
        margin-top: 8px;
    }
</style>
""", unsafe_allow_html=True)

# =====================================================
# 데이터
# 2026.06은 현재 공개된 2026년 6월 초 통계와 2026년 상반기 흐름을 반영한 대시보드용 값입니다.
# =====================================================
trade_partners = pd.DataFrame({
    "국가": ["중국", "미국", "베트남", "일본", "대만", "독일", "싱가포르", "인도", "멕시코", "호주"],
    "수출액_십억달러": [136.2, 124.4, 63.8, 56.7, 50.3, 40.1, 36.7, 33.2, 29.6, 21.1],
    "수입액_십억달러": [104.6, 86.4, 41.2, 36.9, 31.7, 31.4, 26.1, 23.4, 19.2, 13.4],
    "공급망연결지수": [94, 88, 76, 70, 68, 54, 48, 44, 41, 35],
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
    + trade_partners["공급망연결지수"] / 100 * 40
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
    "산업": ["반도체", "자동차", "석유제품", "배터리", "선박", "철강", "디스플레이", "일반기계", "무선통신기기"],
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
        "HD현대중공업, 한화오션, 삼성중공업",
        "POSCO, 현대제철",
        "삼성디스플레이, LG디스플레이",
        "두산에너빌리티, 현대모비스",
        "삼성전자, LG전자"
    ],
    "산업인사이트": [
        "한국 수출의 핵심 산업으로 중국·미국·대만과의 기술·공급망 관계가 중요합니다.",
        "미국과 유럽의 친환경차·관세 정책에 민감하며 북미 공급망 전략이 중요합니다.",
        "에너지 가격과 중국 수요 변화에 영향을 크게 받습니다.",
        "전기차 전환과 미국·유럽 보조금 정책에 따라 전략적 가치가 커지고 있습니다.",
        "글로벌 선박 수요와 에너지 운송, 방산·해양 전략과 연결됩니다.",
        "중국 공급 과잉과 EU 규제에 대응해야 합니다.",
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
# 보조 함수
# =====================================================
BROWN = "#7b4b27"
BROWN2 = "#9b6a36"
GREEN = "#607141"
SAGE = "#87935f"
OCHRE = "#b9873a"
ORANGE = "#c66b2b"
INK = "#2f2116"
PAPER_PLOT = "rgba(255,248,225,0.46)"
COLORWAY = [BROWN, GREEN, OCHRE, ORANGE, SAGE, BROWN2]


def set_plot_style(fig):
    fig.update_layout(
        template="plotly_white",
        colorway=COLORWAY,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=PAPER_PLOT,
        font=dict(family="Gowun Batang, Nanum Myeongjo, serif", color=INK, size=13),
        title_font=dict(size=18, color=INK, family="Song Myung, Nanum Myeongjo, serif"),
        legend=dict(bgcolor="rgba(255,248,225,0)", font=dict(color=INK)),
        margin=dict(l=40, r=30, t=70, b=45)
    )
    fig.update_xaxes(gridcolor="rgba(80,50,25,0.16)", linecolor="rgba(80,50,25,0.28)", tickfont=dict(color=INK))
    fig.update_yaxes(gridcolor="rgba(80,50,25,0.16)", linecolor="rgba(80,50,25,0.28)", tickfont=dict(color=INK))
    for i, trace in enumerate(fig.data):
        color = COLORWAY[i % len(COLORWAY)]
        if hasattr(trace, "marker"):
            trace.marker.color = color
        if hasattr(trace, "line"):
            trace.line.color = color
            trace.line.width = 3
    return fig


def oecd_comment(selected_country):
    korea = oecd_sample[oecd_sample["국가"] == "한국"].iloc[0]
    target = oecd_sample[oecd_sample["국가"] == selected_country].iloc[0]
    if selected_country == "OECD 평균":
        return "한국은 OECD 평균보다 무역의존도와 제조업 비중이 높습니다. 이는 수출 제조업 경쟁력이 강하다는 의미이지만, 글로벌 경기 침체·공급망 충격·통상정책 변화에 더 민감하다는 약점도 있습니다. 특히 서비스무역비중은 낮아 디지털 서비스와 고부가가치 서비스 수출 확대가 필요합니다."
    comments = {
        "미국": "미국은 내수와 서비스 산업 비중이 큰 경제인 반면, 한국은 수출 제조업 의존도가 높습니다. 한국은 미국과 첨단기술·반도체·배터리 협력을 강화하되, 미국 정책 변화에 대한 리스크 관리가 필요합니다.",
        "일본": "일본과 비교하면 한국은 GVC 참여도와 무역의존도가 높은 편입니다. 다만 소재·부품·장비 영역에서는 일본과의 공급망 협력이 여전히 중요합니다.",
        "독일": "독일과 한국은 모두 제조업 기반이 강하지만, 독일은 유럽 내 안정적인 시장과 고부가 기계·자동차 생태계를 갖고 있습니다. 한국은 제조업 경쟁력을 유지하면서 서비스·기술 플랫폼 역량을 보완할 필요가 있습니다.",
        "네덜란드": "네덜란드는 무역의존도와 물류·서비스 연결성이 매우 높은 국가입니다. 한국은 제조업 중심 연결성이 강한 반면, 국제 물류·서비스 허브 기능은 상대적으로 약합니다.",
        "프랑스": "프랑스와 비교하면 한국은 제조업과 GVC 연결성이 강하지만 서비스무역비중은 낮습니다. 문화·콘텐츠·디지털 서비스 수출을 함께 키우는 전략이 필요합니다.",
        "멕시코": "멕시코는 북미 생산거점으로서 무역의존도가 높습니다. 한국은 멕시코를 북미 공급망 다변화의 연결 지점으로 활용할 수 있습니다.",
        "캐나다": "캐나다는 자원·에너지와 북미 시장 접근성이 강점입니다. 한국은 제조업 수출 경쟁력을 유지하면서 핵심 광물·자원 공급망 협력을 확대할 필요가 있습니다."
    }
    if selected_country in comments:
        return comments[selected_country]
    return f"한국은 {selected_country} 대비 무역의존도 차이 {korea['무역의존도'] - target['무역의존도']:.1f}p, GVC 참여도 차이 {korea['GVC참여도'] - target['GVC참여도']:.1f}p를 보입니다. 제조업과 공급망 연결성은 강하지만 서비스 부문 확대가 보완 과제입니다."

# =====================================================
# 사이드바
# =====================================================
st.sidebar.title("🌾 대시보드 컨트롤")
st.sidebar.caption("한국 글로벌 무역 포지션 대시보드")
st.sidebar.selectbox("연도 선택", ["2014 - 2026.06"], index=0)
st.sidebar.selectbox("지역 선택", ["전체 선택", "아시아", "북미", "유럽", "오세아니아"], index=0)
selected_country = st.sidebar.selectbox(
    "OECD 비교 대상 선택",
    options=["OECD 평균"] + [c for c in oecd_sample["국가"].tolist() if c not in ["한국", "OECD 평균"]]
)
selected_partner = st.sidebar.selectbox(
    "전략 파트너 상세 선택",
    options=trade_partners.sort_values("전략점수", ascending=False)["국가"].tolist()
)

# =====================================================
# 헤더
# =====================================================
st.markdown('<h1 class="main-title">한국 글로벌 무역 포지션 대시보드</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">세계 경제 속 한국의 역할을 데이터로 이해하다</p>', unsafe_allow_html=True)

latest = trade_timeline.iloc[-1]
metric1, metric2, metric3, metric4, metric5 = st.columns(5)
with metric1:
    st.markdown(f'<div class="metric-card"><div class="metric-label">총 교역액</div><div class="metric-value">{latest["총교역액"]:.1f}</div><div class="metric-unit">십억 달러</div><div class="metric-note">2026.06 현재</div></div>', unsafe_allow_html=True)
with metric2:
    st.markdown(f'<div class="metric-card"><div class="metric-label">총 수출액</div><div class="metric-value">{latest["수출"]:.1f}</div><div class="metric-unit">십억 달러</div><div class="metric-note">2026.06 현재</div></div>', unsafe_allow_html=True)
with metric3:
    st.markdown(f'<div class="metric-card"><div class="metric-label">총 수입액</div><div class="metric-value">{latest["수입"]:.1f}</div><div class="metric-unit">십억 달러</div><div class="metric-note">2026.06 현재</div></div>', unsafe_allow_html=True)
with metric4:
    st.markdown(f'<div class="metric-card"><div class="metric-label">무역수지</div><div class="metric-value">{latest["무역수지"]:.1f}</div><div class="metric-unit">십억 달러</div><div class="metric-note">2026.06 현재</div></div>', unsafe_allow_html=True)
with metric5:
    korea_gvc = oecd_sample.loc[oecd_sample["국가"] == "한국", "GVC참여도"].iloc[0]
    st.markdown(f'<div class="metric-card"><div class="metric-label">한국 GVC 참여도</div><div class="metric-value">{korea_gvc:.1f}%</div><div class="metric-unit">OECD TiVA</div><div class="metric-note">2023 기준</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "① 개요",
    "② 무역 타임라인",
    "③ 산업 분석",
    "④ GVC & 공급망",
    "⑤ OECD 비교",
    "⑥ 전략적 파트너 분석"
])

# =====================================================
# ① 개요
# =====================================================
with tab1:
    col1, col2 = st.columns([1.0, 1.55])
    with col1:
        st.markdown("""
        <div class="paper-card">
        <h3>프로젝트 방향성</h3>
        <p>이 대시보드는 한국이 세계 경제와 국제 공급망 안에서 어떤 위치에 있는지를 시각화합니다. 단순 통계 나열이 아니라 <b>무역 규모·산업 구조·공급망 연결성·OECD 비교</b>를 통해 한국이 어떤 국가와 전략적 관계를 유지해야 하는지 이해하는 데 목적이 있습니다.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="paper-card">
        <h3>핵심 질문</h3>
        <ul>
            <li>한국은 어떤 국가와 가장 강하게 연결되어 있는가?</li>
            <li>어떤 산업이 한국 수출과 공급망의 중심인가?</li>
            <li>OECD 국가와 비교했을 때 한국의 약점은 무엇인가?</li>
            <li>한국은 어떤 국가와 좋은 대외 관계를 유지해야 하는가?</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div class='paper-card'><h3>핵심 키워드</h3>", unsafe_allow_html=True)
        keywords = ["글로벌 무역", "한국 경제", "GVC", "OECD 비교", "공급망", "무역 의존도", "전략적 파트너"]
        st.markdown("".join([f"<span class='keyword-pill'>{k}</span>" for k in keywords]) + "</div>", unsafe_allow_html=True)

    with col2:
        fig_overview = px.bar(
            trade_partners.sort_values("총교역액_십억달러", ascending=False),
            x="국가",
            y=["수출액_십억달러", "수입액_십억달러"],
            barmode="group",
            title="국가별 한국 무역 규모 (2026.06 현재)",
            labels={"value": "십억 달러", "variable": "구분"}
        )
        fig_overview.data[0].name = "수출액"
        fig_overview.data[1].name = "수입액"
        fig_overview = set_plot_style(fig_overview)
        st.plotly_chart(fig_overview, use_container_width=True)
        st.markdown('<div class="source-note">※ 출처: 한국무역협회(KITA)·관세청 무역통계 흐름을 바탕으로 대시보드용 재구성</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="insight-box">한국은 상위 교역국과 긴밀히 연결되어 있으며, 특히 중국·미국·베트남과의 교역 비중이 높습니다. 수출이 수입을 상회하는 구조는 긍정적이지만, 특정 국가와 산업에 대한 의존도는 공급망 리스크가 될 수 있습니다.</div>
        """, unsafe_allow_html=True)

# =====================================================
# ② 무역 타임라인
# =====================================================
with tab2:
    st.subheader("무역 변화 타임라인")
    chart_option = st.radio("차트 선택", ["수출 & 수입", "무역수지", "총 교역액"], horizontal=True)
    if chart_option == "수출 & 수입":
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(x=trade_timeline["연도"], y=trade_timeline["수출"], mode="lines+markers", name="수출액"))
        fig_line.add_trace(go.Scatter(x=trade_timeline["연도"], y=trade_timeline["수입"], mode="lines+markers", name="수입액"))
        fig_line.update_layout(title="한국의 수출입 변화", yaxis_title="십억 달러")
    elif chart_option == "무역수지":
        fig_line = px.bar(trade_timeline, x="연도", y="무역수지", title="한국의 무역수지 변화", labels={"무역수지": "십억 달러"})
    else:
        fig_line = px.area(trade_timeline, x="연도", y="총교역액", title="한국의 총 교역액 변화", labels={"총교역액": "십억 달러"})
    fig_line = set_plot_style(fig_line)
    st.plotly_chart(fig_line, use_container_width=True)
    st.markdown('<div class="source-note">※ 2026.06은 6월 현재 흐름을 반영한 누계형 표시입니다.</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="insight-box">2026년 6월 현재 한국 무역은 반도체와 첨단 제조업 회복의 영향을 크게 받고 있습니다. 다만 수출 중심 경제 구조는 글로벌 경기, 미중 갈등, 주요국 관세 정책 변화에 민감하므로 공급망 다변화가 필요합니다.</div>
    """, unsafe_allow_html=True)

# =====================================================
# ③ 산업 분석: 선택 기능 없음 / 그래프 + 기업 표
# =====================================================
with tab3:
    st.subheader("수출 산업 및 주요 기업 분석")
    fig_industry_bar = px.bar(
        industries.sort_values("수출액_십억달러", ascending=True),
        x="수출액_십억달러",
        y="산업",
        orientation="h",
        title="산업별 수출액",
        labels={"수출액_십억달러": "수출액(십억 달러)"}
    )
    fig_industry_bar = set_plot_style(fig_industry_bar)
    st.plotly_chart(fig_industry_bar, use_container_width=True)
    st.markdown("""
    <div class="insight-box">반도체는 한국 수출의 핵심이며, 자동차·배터리·선박은 미국·유럽 시장 및 글로벌 친환경 전환과 연결됩니다. 산업별 주요 기업을 함께 보면 한국 무역이 단순한 국가 간 거래가 아니라 기업과 공급망을 통해 움직인다는 점을 이해할 수 있습니다.</div>
    """, unsafe_allow_html=True)
    st.dataframe(
        industries[["산업", "수출액_십억달러", "공급망_의존도", "주요_연결국가", "주요기업", "산업인사이트"]],
        use_container_width=True,
        hide_index=True
    )

# =====================================================
# ④ GVC & 공급망
# =====================================================
with tab4:
    st.subheader("글로벌 가치사슬과 공급망 구조")
    st.markdown("""
    <div class="insight-box">GVC는 하나의 상품이 한 나라에서 완성되는 것이 아니라 여러 국가의 부품·조립·기술·소비시장을 거쳐 만들어지는 구조입니다. 아래는 한국 주요 산업이 세계 공급망으로 연결되는 방식을 단순화한 흐름입니다.</div>
    """, unsafe_allow_html=True)
    c1, c2 = st.columns([1.05, 1.15])
    with c1:
        for _, row in value_chain_flows.iterrows():
            st.markdown(f"""
            <div class="gvc-card">
                <div class="gvc-title">{row['산업']}</div>
                <div class="gvc-flow">{row['1단계']}<br>↓<br>{row['2단계']}<br>↓<br>{row['3단계']}</div>
                <div class="gvc-desc">{row['설명']}</div>
            </div>
            """, unsafe_allow_html=True)
    with c2:
        fig_supply = px.bar(
            trade_partners.sort_values("공급망연결지수", ascending=True),
            x="공급망연결지수",
            y="국가",
            orientation="h",
            title="국가별 공급망 연결 규모",
            labels={"공급망연결지수": "공급망 연결 지수"}
        )
        fig_supply = set_plot_style(fig_supply)
        st.plotly_chart(fig_supply, use_container_width=True)
        st.markdown('<div class="source-note">※ 공급망 연결 지수는 GVC 참여, 핵심 산업 연결성, 중간재 흐름을 종합한 설명용 지표입니다.</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="insight-box">중국과 미국은 한국 공급망의 양대 축입니다. 중국은 중간재·조립 네트워크, 미국은 첨단기술·최종소비시장 측면에서 중요성이 큽니다.</div>
        """, unsafe_allow_html=True)

# =====================================================
# ⑤ OECD 비교
# =====================================================
with tab5:
    st.subheader("한국과 OECD 비교")
    comparison_df = oecd_sample[oecd_sample["국가"].isin(["한국", selected_country])]
    categories = ["무역의존도", "GVC참여도", "서비스무역비중", "FDI연결성", "제조업비중"]
    fig_radar = go.Figure()
    for _, row in comparison_df.iterrows():
        fig_radar.add_trace(go.Scatterpolar(
            r=[row[c] for c in categories],
            theta=categories,
            fill="toself",
            name=row["국가"]
        ))
    fig_radar.update_layout(
        polar=dict(
            bgcolor="rgba(255,248,225,0.35)",
            radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(80,50,25,0.18)"),
            angularaxis=dict(gridcolor="rgba(80,50,25,0.18)")
        ),
        showlegend=True,
        title=f"한국 vs {selected_country}: 경제 구조 비교",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Gowun Batang, Nanum Myeongjo, serif", color=INK),
        colorway=COLORWAY
    )
    for i, trace in enumerate(fig_radar.data):
        trace.line.color = COLORWAY[i % len(COLORWAY)]
    st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown(f'<div class="insight-box">{oecd_comment(selected_country)}</div>', unsafe_allow_html=True)

    fig_oecd_bar = px.bar(
        oecd_sample.sort_values("무역의존도", ascending=False),
        x="국가",
        y="무역의존도",
        title="OECD 주요 국가의 무역 의존도 비교",
        labels={"무역의존도": "무역의존도"}
    )
    fig_oecd_bar = set_plot_style(fig_oecd_bar)
    st.plotly_chart(fig_oecd_bar, use_container_width=True)

# =====================================================
# ⑥ 전략적 파트너 분석
# =====================================================
with tab6:
    st.subheader("한국의 전략적 파트너 분석")
    col1, col2 = st.columns([1.1, 1.1])
    with col1:
        fig_partner = px.bar(
            trade_partners.sort_values("전략점수", ascending=True),
            x="전략점수",
            y="국가",
            orientation="h",
            title="전략적 파트너 중요도",
            labels={"전략점수": "종합 점수"}
        )
        fig_partner = set_plot_style(fig_partner)
        st.plotly_chart(fig_partner, use_container_width=True)
        st.markdown('<div class="source-note">※ 종합 점수 = 교역 규모 40% + 공급망 연결 40% + 핵심 산업 의존도 20%</div>', unsafe_allow_html=True)
    with col2:
        fig_trade = px.bar(
            trade_partners.sort_values("총교역액_십억달러", ascending=True),
            x="총교역액_십억달러",
            y="국가",
            orientation="h",
            title="국가별 한국 무역 규모",
            labels={"총교역액_십억달러": "총 교역액(십억 달러)"}
        )
        fig_trade = set_plot_style(fig_trade)
        st.plotly_chart(fig_trade, use_container_width=True)

    selected_info = trade_partners[trade_partners["국가"] == selected_partner].iloc[0]
    st.markdown(f"""
    <div class="partner-card">
        <h3>{selected_partner}와의 전략적 의미</h3>
        <p><b>총 교역액:</b> {selected_info['총교역액_십억달러']:.1f}십억 달러</p>
        <p><b>공급망 연결 지수:</b> {selected_info['공급망연결지수']}</p>
        <p><b>전략 점수:</b> {selected_info['전략점수']}</p>
        <p>{selected_info['관계해석']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">한국은 주요 교역국과의 전략적 협력을 지속적으로 강화해야 합니다. 특히 첨단 산업 협력, 공급망 안정화, 신시장 개척을 통해 글로벌 경쟁력을 높이는 것이 중요합니다.</div>
    """, unsafe_allow_html=True)

# =====================================================
# 푸터
# =====================================================
st.markdown("---")
st.caption("출처: 한국무역협회(KITA), 관세청 무역통계, OECD TiVA 자료 흐름을 바탕으로 대시보드형 시각화에 맞게 재구성")
st.caption("제작 도구: Python, Streamlit, Pandas, Plotly")
