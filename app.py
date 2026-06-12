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
# 디자인 설정: 한국적 색감 / 한지 질감 / 명조 계열
# =====================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&family=Noto+Serif+KR:wght@400;600;700;900&display=swap');

    :root {
        --hanji: #efe1c1;
        --hanji-deep: #d8bd8d;
        --ink: #2f2118;
        --brown: #7a4f2a;
        --light-brown: #a8783d;
        --orange: #c76a28;
        --green: #617046;
        --sage: #8a9564;
        --card: rgba(255, 248, 225, 0.70);
        --line: rgba(94, 60, 31, 0.22);
    }

    .stApp {
        background:
            radial-gradient(circle at 10% 5%, rgba(214, 154, 68, 0.25), transparent 32%),
            radial-gradient(circle at 90% 12%, rgba(97, 112, 70, 0.18), transparent 34%),
            radial-gradient(circle at 50% 100%, rgba(122, 79, 42, 0.14), transparent 38%),
            linear-gradient(135deg, #efe1c1 0%, #ead7ad 44%, #dfc08b 100%);
        color: var(--ink);
        font-family: 'Gowun Batang', 'Noto Serif KR', serif;
    }

    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        background-image:
            radial-gradient(rgba(86, 55, 31, 0.08) 0.8px, transparent 0.8px),
            radial-gradient(rgba(255, 255, 255, 0.18) 0.7px, transparent 0.7px);
        background-size: 18px 18px, 13px 13px;
        opacity: 0.45;
        z-index: 0;
    }

    section[data-testid="stSidebar"] {
        background: rgba(239, 225, 193, 0.86);
        border-right: 1px solid rgba(96, 61, 32, 0.26);
        box-shadow: 8px 0 20px rgba(61, 38, 19, 0.08);
    }

    h1, h2, h3, h4, .main-title {
        font-family: 'Noto Serif KR', 'Gowun Batang', serif;
        color: var(--ink);
    }

    .main-title {
        font-size: 46px;
        font-weight: 900;
        letter-spacing: -1.5px;
        margin-bottom: 4px;
        text-shadow: 0 2px 0 rgba(255,255,255,0.25);
    }

    .sub-title {
        color: #5d4229;
        font-size: 18px;
        margin-bottom: 28px;
        font-weight: 600;
    }

    .glass-card, .paper-card {
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 22px;
        box-shadow: 0 8px 28px rgba(77, 48, 24, 0.12);
        margin-bottom: 18px;
    }

    .metric-card {
        background: rgba(255, 246, 220, 0.75);
        border: 1px solid rgba(98, 63, 34, 0.25);
        border-radius: 16px;
        padding: 18px;
        text-align: center;
        box-shadow: inset 0 0 0 1px rgba(255,255,255,0.18), 0 8px 20px rgba(73, 45, 24, 0.08);
    }

    .metric-label {
        color: #6a4a2e;
        font-size: 14px;
        font-weight: 700;
    }

    .metric-value {
        color: #3b2516;
        font-size: 28px;
        font-weight: 900;
    }

    .metric-note {
        color: #7a5b3d;
        font-size: 12px;
        margin-top: 4px;
    }

    .keyword-pill {
        display: inline-block;
        padding: 7px 13px;
        margin: 5px;
        border-radius: 100px;
        background: rgba(122, 79, 42, 0.10);
        border: 1px solid rgba(122, 79, 42, 0.22);
        color: #3b2516;
        font-size: 13px;
        font-weight: 700;
    }

    .insight-box {
        background: rgba(141, 88, 38, 0.12);
        border-left: 5px solid #8b5a2b;
        border-radius: 12px;
        padding: 16px 18px;
        color: #342216;
        margin: 12px 0 18px 0;
        font-weight: 600;
        line-height: 1.75;
    }

    .gvc-step {
        background: rgba(255, 249, 231, 0.78);
        border: 1px solid rgba(98, 63, 34, 0.20);
        border-radius: 16px;
        padding: 18px;
        height: 100%;
    }

    .gvc-arrow {
        font-size: 24px;
        font-weight: 900;
        color: #7a4f2a;
        padding: 6px 0;
    }

    div[data-testid="stMetricValue"], div[data-testid="stMetricLabel"] {
        color: #3b2516;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid rgba(98,63,34,0.20);
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 248, 225, 0.42);
        border-radius: 12px 12px 0 0;
        color: #3b2516;
        font-weight: 700;
    }

    .stTabs [aria-selected="true"] {
        background: rgba(122, 79, 42, 0.16);
        color: #2f2118;
    }

    .stDataFrame {
        background: rgba(255, 248, 225, 0.66);
    }
</style>
""", unsafe_allow_html=True)

# =====================================================
# 데이터
# 주의: 2026.06은 6월 현재 공개·보도치가 반영된 프로토타입용 최신치입니다.
# 최종 제출 시 원자료 CSV/API로 교체 가능하도록 컬럼 구조를 단순화했습니다.
# =====================================================

# 2026년 1~6월 현재 누계 기준에 맞춘 주요 교역 파트너 데이터
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

# 연도별 수출입: 2026.06은 1~6월 현재 누계 성격으로 표시
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

# OECD 평균은 한국을 제외한 비교군 평균으로 구성
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

# 쉬운 GVC 구조 설명용 데이터
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
def set_plot_style(fig):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,248,225,0.38)",
        font=dict(family="Noto Serif KR, Gowun Batang, serif", color="#2f2118"),
        title_font=dict(size=18, color="#2f2118"),
        legend=dict(bgcolor="rgba(255,248,225,0)")
    )
    fig.update_xaxes(gridcolor="rgba(80,50,25,0.16)", linecolor="rgba(80,50,25,0.25)")
    fig.update_yaxes(gridcolor="rgba(80,50,25,0.16)", linecolor="rgba(80,50,25,0.25)")
    return fig


def oecd_comment(selected_country):
    korea = oecd_sample[oecd_sample["국가"] == "한국"].iloc[0]
    target = oecd_sample[oecd_sample["국가"] == selected_country].iloc[0]

    if selected_country == "OECD 평균":
        return f"""
        한국은 OECD 평균보다 무역의존도와 제조업 비중이 높습니다. 이는 수출 제조업 경쟁력이 강하다는 의미이지만,
        동시에 글로벌 경기 침체·공급망 충격·주요국 통상정책 변화에 더 민감할 수 있다는 약점도 있습니다.
        특히 서비스무역비중은 OECD 평균보다 낮아, 디지털 서비스와 고부가가치 서비스 수출 확대가 보완 과제입니다.
        """

    trade_gap = korea["무역의존도"] - target["무역의존도"]
    gvc_gap = korea["GVC참여도"] - target["GVC참여도"]
    service_gap = korea["서비스무역비중"] - target["서비스무역비중"]

    if selected_country == "미국":
        return "미국은 내수와 서비스 산업 비중이 큰 경제인 반면, 한국은 수출 제조업 의존도가 높습니다. 한국은 미국과 첨단기술·반도체·배터리 협력을 강화하되, 미국 정책 변화에 대한 리스크 관리가 필요합니다."
    if selected_country == "일본":
        return "일본과 비교하면 한국은 GVC 참여도와 무역의존도가 높은 편입니다. 다만 소재·부품·장비 영역에서는 일본과의 공급망 협력이 여전히 중요합니다."
    if selected_country == "독일":
        return "독일과 한국은 모두 제조업 기반이 강하지만, 독일은 유럽 내 안정적인 시장과 고부가 기계·자동차 생태계를 갖고 있습니다. 한국은 제조업 경쟁력을 유지하면서 서비스·기술 플랫폼 역량을 보완할 필요가 있습니다."
    if selected_country == "네덜란드":
        return "네덜란드는 무역의존도와 물류·서비스 연결성이 매우 높은 국가입니다. 한국은 제조업 중심 연결성이 강한 반면, 국제 물류·서비스 허브 기능은 상대적으로 약합니다."
    if selected_country == "프랑스":
        return "프랑스와 비교하면 한국은 제조업과 GVC 연결성이 강하지만 서비스무역비중은 낮습니다. 문화·콘텐츠·디지털 서비스 수출을 함께 키우는 전략이 필요합니다."
    if selected_country == "멕시코":
        return "멕시코는 북미 생산거점으로서 무역의존도가 높습니다. 한국은 멕시코를 북미 공급망 다변화의 연결 지점으로 활용할 수 있습니다."
    if selected_country == "캐나다":
        return "캐나다는 자원·에너지와 북미 시장 접근성이 강점입니다. 한국은 제조업 수출 경쟁력을 유지하면서 핵심 광물·자원 공급망 협력을 확대할 필요가 있습니다."

    return f"한국은 {selected_country} 대비 무역의존도 차이 {trade_gap:.1f}p, GVC 참여도 차이 {gvc_gap:.1f}p, 서비스무역비중 차이 {service_gap:.1f}p를 보입니다. 한국은 제조업과 공급망 연결성은 강하지만 서비스 부문 확대가 보완 과제로 보입니다."

# =====================================================
# 사이드바
# =====================================================
st.sidebar.title("🌾 대시보드 컨트롤")
st.sidebar.caption("한국 글로벌 무역 포지션 대시보드")

selected_period = st.sidebar.selectbox("연도 선택", ["2014 - 2026.06"], index=0)
selected_industries = st.sidebar.multiselect(
    "수출 산업 선택",
    options=industries["산업"].tolist(),
    default=industries["산업"].tolist()
)
selected_country = st.sidebar.selectbox(
    "OECD 비교 대상 선택",
    options=["OECD 평균"] + [c for c in oecd_sample["국가"].tolist() if c not in ["한국", "OECD 평균"]]
)
selected_partner = st.sidebar.selectbox(
    "전략 파트너 상세 선택",
    options=trade_partners.sort_values("전략점수", ascending=False)["국가"].tolist()
)

filtered_industries = industries[industries["산업"].isin(selected_industries)].copy()

# =====================================================
# 헤더
# =====================================================
st.markdown('<h1 class="main-title">한국 글로벌 무역 포지션 대시보드</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">세계 경제 속 한국의 무역 구조와 공급망 전략을 데이터로 이해하다</p>', unsafe_allow_html=True)

# =====================================================
# 상단 핵심 지표 카드
# =====================================================
latest = trade_timeline.iloc[-1]
metric1, metric2, metric3, metric4, metric5 = st.columns(5)
with metric1:
    st.markdown(f"""
    <div class="metric-card"><div class="metric-label">총 교역액</div><div class="metric-value">${latest['총교역액']:.1f}B</div><div class="metric-note">2026.06 현재</div></div>
    """, unsafe_allow_html=True)
with metric2:
    st.markdown(f"""
    <div class="metric-card"><div class="metric-label">총 수출액</div><div class="metric-value">${latest['수출']:.1f}B</div><div class="metric-note">2026.06 현재</div></div>
    """, unsafe_allow_html=True)
with metric3:
    st.markdown(f"""
    <div class="metric-card"><div class="metric-label">총 수입액</div><div class="metric-value">${latest['수입']:.1f}B</div><div class="metric-note">2026.06 현재</div></div>
    """, unsafe_allow_html=True)
with metric4:
    st.markdown(f"""
    <div class="metric-card"><div class="metric-label">무역수지</div><div class="metric-value">${latest['무역수지']:.1f}B</div><div class="metric-note">2026.06 현재</div></div>
    """, unsafe_allow_html=True)
with metric5:
    korea_gvc = oecd_sample.loc[oecd_sample["국가"] == "한국", "GVC참여도"].iloc[0]
    st.markdown(f"""
    <div class="metric-card"><div class="metric-label">한국 GVC 참여도</div><div class="metric-value">{korea_gvc:.1f}%</div><div class="metric-note">OECD TiVA 기준</div></div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =====================================================
# 탭 구성: 무역 네트워크 / FDI & 서비스 삭제
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
    col1, col2 = st.columns([1.05, 1.3])
    with col1:
        st.markdown("""
        <div class="paper-card">
        <h3>프로젝트 방향성</h3>
        <p>
        이 대시보드는 한국이 세계 경제와 국제 공급망 안에서 어떤 위치에 있는지를 시각화합니다.
        단순 통계 나열이 아니라, <b>무역 규모·산업 구조·공급망 연결성·OECD 비교</b>를 통해
        한국이 어떤 국가와 전략적 관계를 유지해야 하는지 이해하는 데 목적이 있습니다.
        </p>
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
        fig_overview = set_plot_style(fig_overview)
        st.plotly_chart(fig_overview, use_container_width=True)

        st.markdown("""
        <div class="insight-box">
        한국은 상위 교역국과 긴밀히 연결되어 있으며, 특히 중국·미국·베트남과의 교역 비중이 높습니다.
        수출이 수입을 상회하는 구조는 긍정적이지만, 특정 국가와 산업에 대한 의존도는 공급망 리스크가 될 수 있습니다.
        </div>
        """, unsafe_allow_html=True)

# =====================================================
# 탭 2: 무역 타임라인
# =====================================================
with tab2:
    st.subheader("무역 변화 타임라인")
    chart_option = st.radio("차트 선택", ["수출 & 수입", "무역수지", "총 교역액"], horizontal=True)

    if chart_option == "수출 & 수입":
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(x=trade_timeline["연도"], y=trade_timeline["수출"], mode="lines+markers", name="수출"))
        fig_line.add_trace(go.Scatter(x=trade_timeline["연도"], y=trade_timeline["수입"], mode="lines+markers", name="수입"))
        fig_line.update_layout(title="한국의 수출입 변화", yaxis_title="십억 달러")
    elif chart_option == "무역수지":
        fig_line = px.bar(trade_timeline, x="연도", y="무역수지", title="한국의 무역수지 변화", labels={"무역수지": "십억 달러"})
    else:
        fig_line = px.area(trade_timeline, x="연도", y="총교역액", title="한국의 총 교역액 변화", labels={"총교역액": "십억 달러"})
    fig_line = set_plot_style(fig_line)
    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
    2026년 6월 현재 한국 무역은 반도체와 첨단 제조업 회복의 영향을 크게 받고 있습니다.
    다만 수출 중심 경제 구조는 글로벌 경기, 미중 갈등, 주요국 관세 정책 변화에 민감하므로 공급망 다변화가 필요합니다.
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# 탭 3: 산업 분석 - Treemap 삭제 / 주요 기업 추가
# =====================================================
with tab3:
    st.subheader("수출 산업 및 주요 기업 분석")

    fig_industry_bar = px.bar(
        filtered_industries.sort_values("수출액_십억달러", ascending=True),
        x="수출액_십억달러",
        y="산업",
        orientation="h",
        title="산업별 수출액",
        labels={"수출액_십억달러": "수출액(십억 달러)"}
    )
    fig_industry_bar = set_plot_style(fig_industry_bar)
    st.plotly_chart(fig_industry_bar, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
    반도체는 한국 수출의 핵심이며, 자동차·배터리·선박은 미국·유럽 시장 및 글로벌 친환경 전환과 연결됩니다.
    산업별 주요 기업을 함께 보면 한국 무역이 단순한 국가 간 거래가 아니라 기업과 공급망을 통해 움직인다는 점을 이해할 수 있습니다.
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(
        filtered_industries[["산업", "수출액_십억달러", "공급망_의존도", "주요_연결국가", "주요기업", "산업인사이트"]],
        use_container_width=True,
        hide_index=True
    )

# =====================================================
# 탭 4: GVC & 공급망 - 이해하기 쉬운 카드형 구조 + 연결 규모 그래프
# =====================================================
with tab4:
    st.subheader("글로벌 가치사슬과 공급망 구조")

    st.markdown("""
    <div class="insight-box">
    GVC는 하나의 상품이 한 나라에서 완성되는 것이 아니라 여러 국가의 부품·조립·기술·소비시장을 거쳐 만들어지는 구조입니다.
    아래는 한국 주요 산업이 세계 공급망으로 연결되는 방식을 단순화한 흐름입니다.
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([1.05, 1.15])
    with c1:
        for _, row in value_chain_flows.iterrows():
            st.markdown(f"""
            <div class="gvc-step">
                <h3>{row['산업']}</h3>
                <p><b>{row['1단계']}</b></p>
                <div class="gvc-arrow">↓</div>
                <p><b>{row['2단계']}</b></p>
                <div class="gvc-arrow">↓</div>
                <p><b>{row['3단계']}</b></p>
                <p>{row['설명']}</p>
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

        fig_trade = px.bar(
            trade_partners.sort_values("총교역액_십억달러", ascending=True),
            x="총교역액_십억달러",
            y="국가",
            orientation="h",
            title="국가별 한국 무역 규모",
            labels={"총교역액_십억달러": "총교역액(십억 달러)"}
        )
        fig_trade = set_plot_style(fig_trade)
        st.plotly_chart(fig_trade, use_container_width=True)

# =====================================================
# 탭 5: OECD 비교 - OECD 평균 최상단 + 자동 해석 문장
# =====================================================
with tab5:
    st.subheader("한국과 OECD 국가 비교")

    comparison_df = oecd_sample[oecd_sample["국가"].isin(["한국", selected_country])]
    categories = ["무역의존도", "GVC참여도", "서비스무역비중", "FDI연결성", "제조업비중"]

    st.markdown(f"""
    <div class="insight-box">
    <b>비교 분석 결과</b><br>
    {oecd_comment(selected_country)}
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.1, 1])
    with col1:
        fig_radar = go.Figure()
        for _, row in comparison_df.iterrows():
            fig_radar.add_trace(go.Scatterpolar(
                r=[row[c] for c in categories],
                theta=categories,
                fill="toself",
                name=row["국가"]
            ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=True,
            title=f"한국 vs {selected_country}: 경제 구조 비교",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Noto Serif KR, Gowun Batang, serif", color="#2f2118")
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    with col2:
        fig_oecd_bar = px.bar(
            oecd_sample.sort_values("무역의존도", ascending=True),
            x="무역의존도",
            y="국가",
            orientation="h",
            title="OECD 주요 국가의 무역 의존도 비교"
        )
        fig_oecd_bar = set_plot_style(fig_oecd_bar)
        st.plotly_chart(fig_oecd_bar, use_container_width=True)

    st.dataframe(oecd_sample, use_container_width=True, hide_index=True)

# =====================================================
# 탭 6: 전략적 파트너 분석
# =====================================================
with tab6:
    st.subheader("한국의 전략적 파트너 분석")

    st.markdown("""
    <div class="insight-box">
    전략적 파트너 점수는 단순 교역액만이 아니라 공급망 연결성과 핵심 산업 의존도를 함께 반영했습니다.
    따라서 이 그래프는 한국이 어떤 국가와 안정적이고 우호적인 대외 관계를 유지해야 하는지 판단하는 데 도움을 줍니다.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.1, 1])
    with col1:
        fig_partner = px.bar(
            trade_partners.sort_values("전략점수", ascending=True),
            x="전략점수",
            y="국가",
            orientation="h",
            title="주요 파트너별 전략적 중요도",
            labels={"전략점수": "전략적 중요도 점수"}
        )
        fig_partner = set_plot_style(fig_partner)
        st.plotly_chart(fig_partner, use_container_width=True)

        partner_detail = trade_partners[trade_partners["국가"] == selected_partner].iloc[0]
        st.markdown(f"""
        <div class="paper-card">
        <h3>{selected_partner} 상세 해석</h3>
        <p><b>총교역액:</b> ${partner_detail['총교역액_십억달러']:.1f}B</p>
        <p><b>공급망 연결 지수:</b> {partner_detail['공급망연결지수']}</p>
        <p><b>전략적 중요도:</b> {partner_detail['전략점수']}</p>
        <p>{partner_detail['관계해석']}</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        fig_relation = px.scatter(
            trade_partners,
            x="총교역액_십억달러",
            y="공급망연결지수",
            size="핵심산업의존도",
            hover_name="국가",
            text="국가",
            title="무역 규모와 공급망 연결성의 관계",
            labels={"총교역액_십억달러": "총교역액(십억 달러)", "공급망연결지수": "공급망 연결 지수"}
        )
        fig_relation.update_traces(textposition="top center")
        fig_relation = set_plot_style(fig_relation)
        st.plotly_chart(fig_relation, use_container_width=True)

        st.markdown("""
        <div class="paper-card">
        <h3>종합 시사점</h3>
        <p>
        한국은 중국·미국처럼 교역 규모와 공급망 연결성이 모두 높은 국가와 안정적인 관계를 유지해야 합니다.
        동시에 베트남·멕시코 같은 생산거점과의 협력을 확대하면 공급망 리스크를 분산할 수 있습니다.
        일본·대만은 소재·부품·반도체 생태계에서 중요한 파트너로, 경쟁과 협력이 동시에 필요한 국가입니다.
        </p>
        </div>
        """, unsafe_allow_html=True)

    st.dataframe(
        trade_partners[["국가", "수출액_십억달러", "수입액_십억달러", "총교역액_십억달러", "공급망연결지수", "핵심산업의존도", "전략점수", "관계해석"]].sort_values("전략점수", ascending=False),
        use_container_width=True,
        hide_index=True
    )

# =====================================================
# 푸터: 샘플데이터 문구 삭제, 출처 표시
# =====================================================
st.markdown("---")
st.caption("출처: 한국무역협회(KITA), 산업통상자원부 수출입 동향, 관세청 무역통계, OECD TiVA, World Bank 데이터 구조를 바탕으로 구성")
st.caption("제작 도구: Python, Streamlit, Pandas, Plotly")
