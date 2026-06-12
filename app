import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# 페이지 기본 설정
# =====================================================
st.set_page_config(
    page_title="한국 글로벌 무역 포지션 대시보드",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CSS 디자인 설정
# =====================================================
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at top left, #10284f 0%, #07111f 35%, #020617 100%);
        color: #e5eefc;
    }

    section[data-testid="stSidebar"] {
        background: rgba(5, 15, 30, 0.92);
        border-right: 1px solid rgba(100, 180, 255, 0.25);
    }

    .main-title {
        font-size: 44px;
        font-weight: 800;
        background: linear-gradient(90deg, #7dd3fc, #60a5fa, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }

    .sub-title {
        color: #b8c7e0;
        font-size: 18px;
        margin-bottom: 28px;
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(125, 211, 252, 0.18);
        border-radius: 20px;
        padding: 22px;
        box-shadow: 0 8px 28px rgba(0, 0, 0, 0.22);
        backdrop-filter: blur(10px);
        margin-bottom: 18px;
    }

    .metric-card {
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.2), rgba(79, 70, 229, 0.18));
        border: 1px solid rgba(125, 211, 252, 0.25);
        border-radius: 18px;
        padding: 18px;
        text-align: center;
    }

    .metric-label {
        color: #b8c7e0;
        font-size: 14px;
    }

    .metric-value {
        color: #ffffff;
        font-size: 28px;
        font-weight: 800;
    }

    .keyword-pill {
        display: inline-block;
        padding: 7px 13px;
        margin: 5px;
        border-radius: 100px;
        background: rgba(56, 189, 248, 0.15);
        border: 1px solid rgba(125, 211, 252, 0.3);
        color: #dbeafe;
        font-size: 13px;
    }

    .flow-box {
        background: rgba(15, 23, 42, 0.76);
        border: 1px solid rgba(125, 211, 252, 0.22);
        border-radius: 18px;
        padding: 18px;
        text-align: center;
        min-height: 210px;
        margin-bottom: 18px;
    }

    .flow-title {
        font-size: 20px;
        font-weight: 800;
        color: #bfdbfe;
        margin-bottom: 12px;
    }

    .flow-step {
        background: rgba(56, 189, 248, 0.12);
        border: 1px solid rgba(125, 211, 252, 0.25);
        border-radius: 14px;
        padding: 10px;
        margin: 8px 0;
        color: #e0f2fe;
    }

    .arrow {
        color: #93c5fd;
        font-size: 24px;
        font-weight: 800;
        margin: 2px 0;
    }

    .insight {
        background: rgba(14, 165, 233, 0.10);
        border-left: 4px solid #38bdf8;
        border-radius: 12px;
        padding: 16px;
        margin: 14px 0;
        color: #dbeafe;
    }

    .warning-insight {
        background: rgba(251, 146, 60, 0.10);
        border-left: 4px solid #fb923c;
        border-radius: 12px;
        padding: 16px;
        margin: 14px 0;
        color: #ffedd5;
    }
</style>
""", unsafe_allow_html=True)

# =====================================================
# 샘플 데이터
# 실제 제출 전에는 OECD, World Bank, KITA, UN Comtrade 데이터로 교체 가능
# =====================================================

trade_partners = pd.DataFrame({
    "국가": ["중국", "미국", "베트남", "일본", "대만", "독일", "싱가포르", "인도", "멕시코", "호주"],
    "영문국가명": ["China", "United States", "Vietnam", "Japan", "Taiwan", "Germany", "Singapore", "India", "Mexico", "Australia"],
    "수출액_십억달러": [124.8, 115.7, 53.5, 29.0, 28.4, 11.2, 18.7, 18.0, 12.3, 17.8],
    "수입액_십억달러": [142.9, 71.3, 26.7, 47.6, 23.1, 23.7, 12.4, 8.9, 7.1, 33.2],
    "지역": ["아시아", "북미", "아시아", "아시아", "아시아", "유럽", "아시아", "아시아", "북미", "오세아니아"],
    "공급망연결강도": [95, 90, 78, 74, 70, 55, 48, 42, 38, 36],
    "핵심산업의존도": [95, 92, 75, 84, 78, 58, 45, 38, 42, 35],
    "전략적_의미": [
        "최대 교역국이자 반도체·중간재 공급망에서 매우 중요한 국가입니다.",
        "첨단기술, 반도체, 자동차, 배터리 시장에서 핵심적인 전략 파트너입니다.",
        "한국 기업의 생산 거점 다변화와 전자제품 조립 공급망에서 중요성이 커지고 있습니다.",
        "소재·부품·장비 분야에서 한국 제조업과 깊게 연결된 국가입니다.",
        "반도체 생산 생태계에서 한국과 경쟁·협력 관계를 동시에 갖는 국가입니다.",
        "자동차, 기계, 제조업 표준 측면에서 비교 가치가 높은 유럽 핵심 국가입니다.",
        "동남아 물류·금융 허브로서 아시아 공급망 연결에 중요한 역할을 합니다.",
        "신흥시장 소비 수요와 생산 다변화 측면에서 잠재력이 큰 국가입니다.",
        "북미 생산기지와 자동차 공급망 측면에서 중요성이 커지는 국가입니다.",
        "원자재 수입과 에너지·자원 공급 안정성 측면에서 중요한 국가입니다."
    ]
})
trade_partners["총교역액_십억달러"] = trade_partners["수출액_십억달러"] + trade_partners["수입액_십억달러"]
trade_partners["무역수지_십억달러"] = trade_partners["수출액_십억달러"] - trade_partners["수입액_십억달러"]

trade_timeline = pd.DataFrame({
    "연도": list(range(2014, 2025)),
    "수출": [573, 527, 495, 573, 605, 542, 512, 644, 683, 632, 683],
    "수입": [526, 436, 406, 478, 535, 503, 467, 615, 731, 642, 632],
})
trade_timeline["무역수지"] = trade_timeline["수출"] - trade_timeline["수입"]
trade_timeline["총교역액"] = trade_timeline["수출"] + trade_timeline["수입"]

industries = pd.DataFrame({
    "산업": ["반도체", "자동차", "석유화학", "배터리", "조선", "철강", "디스플레이", "기계", "IT 기기"],
    "수출액": [129, 71, 54, 38, 22, 31, 20, 53, 46],
    "공급망_의존도": ["높음", "중간", "중간", "높음", "중간", "중간", "높음", "중간", "높음"],
    "주요_연결국가": ["중국 / 대만 / 미국", "미국 / 유럽", "중국 / ASEAN", "미국 / 유럽 / 중국", "유럽 / 중동", "중국 / 일본", "중국 / 베트남", "미국 / 중국", "중국 / 베트남"],
    "주요기업": [
        "삼성전자, SK하이닉스",
        "현대자동차, 기아",
        "LG화학, 롯데케미칼, 한화솔루션",
        "LG에너지솔루션, 삼성SDI, SK온",
        "HD현대중공업, 한화오션, 삼성중공업",
        "POSCO, 현대제철",
        "삼성디스플레이, LG디스플레이",
        "두산에너빌리티, 현대두산인프라코어, 한화에어로스페이스",
        "삼성전자, LG전자"
    ],
    "산업_인사이트": [
        "한국 수출에서 가장 큰 비중을 차지하며 중국·미국·대만과의 공급망 관계가 매우 중요합니다.",
        "미국과 유럽 시장의 정책 변화에 민감하며, 전기차 전환에 따라 배터리 산업과 연결성이 커지고 있습니다.",
        "중국과 아세안 제조업 경기의 영향을 크게 받는 중간재 중심 산업입니다.",
        "친환경 전환과 전기차 확산으로 전략적 중요성이 빠르게 높아지는 산업입니다.",
        "유럽·중동 발주 시장과 에너지 운송 수요에 영향을 받는 고부가 제조업입니다.",
        "자동차·조선·기계 등 제조업 전반의 기초 소재 역할을 합니다.",
        "중국·베트남 전자제품 생산망과 연결되며, 반도체 산업과 함께 IT 공급망의 핵심입니다.",
        "제조업 자동화와 설비 투자 흐름에 영향을 받는 산업입니다.",
        "글로벌 소비재 시장과 전자제품 생산 네트워크에 직접 연결됩니다."
    ]
})

oecd_sample = pd.DataFrame({
    "국가": ["한국", "독일", "일본", "미국", "네덜란드", "프랑스", "멕시코", "캐나다"],
    "무역의존도": [85, 89, 45, 27, 156, 66, 83, 68],
    "GVC참여도": [56, 52, 41, 38, 61, 45, 49, 46],
    "서비스무역비중": [18, 24, 21, 31, 33, 29, 15, 20],
    "FDI연결성": [62, 68, 48, 76, 85, 64, 59, 66],
    "제조업비중": [27, 19, 20, 11, 10, 10, 18, 10]
})

# OECD 평균은 한국을 제외한 비교 국가 기준으로 계산
oecd_average = pd.DataFrame({
    "국가": ["OECD 평균"],
    "무역의존도": [oecd_sample[oecd_sample["국가"] != "한국"]["무역의존도"].mean()],
    "GVC참여도": [oecd_sample[oecd_sample["국가"] != "한국"]["GVC참여도"].mean()],
    "서비스무역비중": [oecd_sample[oecd_sample["국가"] != "한국"]["서비스무역비중"].mean()],
    "FDI연결성": [oecd_sample[oecd_sample["국가"] != "한국"]["FDI연결성"].mean()],
    "제조업비중": [oecd_sample[oecd_sample["국가"] != "한국"]["제조업비중"].mean()]
})
oecd_compare = pd.concat([oecd_average, oecd_sample], ignore_index=True)

value_chain_cases = pd.DataFrame({
    "산업": ["반도체", "배터리", "자동차", "디스플레이"],
    "1단계": ["한국: 핵심 반도체 생산", "한국: 배터리 셀·소재 생산", "한국: 완성차·부품 생산", "한국: 디스플레이 패널 생산"],
    "2단계": ["중국·베트남: 조립 및 중간 생산", "베트남·중국: 중간 생산 및 조립", "미국·멕시코: 현지 생산·판매", "중국·베트남: 전자제품 조립"],
    "3단계": ["미국·유럽: 최종 소비시장", "미국·유럽: 전기차 시장", "북미·유럽: 최종 소비시장", "글로벌 IT 기기 시장"],
    "핵심국가": ["중국, 미국, 대만, 베트남", "미국, 유럽, 중국, 베트남", "미국, 멕시코, 유럽", "중국, 베트남, 미국"],
    "설명": [
        "한국의 반도체는 해외 조립 과정을 거쳐 글로벌 소비시장으로 이동합니다.",
        "배터리는 전기차 산업과 연결되며 미국·유럽 시장의 정책 변화에 민감합니다.",
        "자동차는 최종 소비시장과 현지 생산기지의 영향을 동시에 받습니다.",
        "디스플레이는 전자제품 조립 공급망과 강하게 연결됩니다."
    ]
})

# =====================================================
# 보조 함수
# =====================================================
def make_dark_layout(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e5eefc")
    )
    return fig

def normalize(series):
    max_value = series.max()
    if max_value == 0:
        return series
    return series / max_value * 100

def get_oecd_comment(selected_country, korea_row, selected_row):
    if selected_country == "OECD 평균":
        return f"""
        <div class="warning-insight">
        <b>OECD 평균 대비 한국의 아쉬운 점</b><br>
        한국은 OECD 평균보다 무역의존도와 제조업 비중이 높은 구조입니다. 이는 수출 경쟁력의 강점이지만,
        동시에 글로벌 경기 침체, 공급망 충격, 특정 산업 부진에 더 크게 영향을 받을 수 있다는 약점이 있습니다.
        또한 서비스무역비중은 OECD 평균보다 낮아, 제조업 중심 구조를 보완할 고부가 서비스 산업 확대가 필요합니다.
        </div>
        """

    trade_gap = korea_row["무역의존도"] - selected_row["무역의존도"]
    gvc_gap = korea_row["GVC참여도"] - selected_row["GVC참여도"]
    service_gap = korea_row["서비스무역비중"] - selected_row["서비스무역비중"]
    mfg_gap = korea_row["제조업비중"] - selected_row["제조업비중"]

    comments = []
    if trade_gap > 0:
        comments.append(f"한국은 {selected_country}보다 무역의존도가 높아 대외 경기 변화에 더 민감합니다.")
    else:
        comments.append(f"한국은 {selected_country}보다 무역의존도가 낮지만, 산업별 특정 국가 의존도는 여전히 관리가 필요합니다.")

    if gvc_gap > 0:
        comments.append(f"GVC 참여도는 한국이 더 높아 글로벌 공급망 안에서 더 깊게 연결되어 있습니다.")
    else:
        comments.append(f"GVC 참여도는 {selected_country}가 더 높아, 한국은 공급망 내 부가가치 확대 전략이 필요합니다.")

    if service_gap < 0:
        comments.append(f"서비스무역비중은 한국이 낮아 디지털 서비스·콘텐츠·금융 등 고부가 서비스 분야 강화가 필요합니다.")
    else:
        comments.append(f"서비스무역비중은 한국이 더 높거나 비슷해 제조업 외 영역의 성장 가능성을 보여줍니다.")

    if mfg_gap > 0:
        comments.append(f"제조업 비중은 한국이 높아 제조 경쟁력은 강하지만 특정 산업 경기 변동에 취약할 수 있습니다.")
    else:
        comments.append(f"제조업 비중은 {selected_country}가 높거나 비슷해, 한국은 산업 구조 다변화가 중요합니다.")

    return f"""
    <div class="insight">
    <b>{selected_country}와 비교한 해석</b><br>
    {' '.join(comments)}
    </div>
    """

def get_partner_level(score):
    if score >= 85:
        return "매우 높음"
    elif score >= 70:
        return "높음"
    elif score >= 50:
        return "중간"
    return "낮음"

# 전략 점수 계산
partner_analysis = trade_partners.copy()
partner_analysis["무역규모점수"] = normalize(partner_analysis["총교역액_십억달러"])
partner_analysis["전략점수"] = (
    partner_analysis["무역규모점수"] * 0.4 +
    partner_analysis["공급망연결강도"] * 0.4 +
    partner_analysis["핵심산업의존도"] * 0.2
).round(1)
partner_analysis["전략중요도"] = partner_analysis["전략점수"].apply(get_partner_level)

# =====================================================
# 사이드바
# =====================================================
st.sidebar.title("🌐 대시보드 컨트롤")
st.sidebar.caption("한국 글로벌 무역 포지션 대시보드")

selected_year = st.sidebar.slider("연도 선택", 2014, 2024, 2024)
selected_region = st.sidebar.multiselect(
    "지역 선택",
    options=trade_partners["지역"].unique(),
    default=list(trade_partners["지역"].unique())
)
selected_industries = st.sidebar.multiselect(
    "수출 산업 선택",
    options=industries["산업"].tolist(),
    default=industries["산업"].tolist()[:5]
)
selected_country = st.sidebar.selectbox(
    "OECD 비교 국가 선택",
    options=["OECD 평균"] + [c for c in oecd_sample["국가"] if c != "한국"]
)
selected_partner = st.sidebar.selectbox(
    "전략 파트너 상세 보기",
    options=partner_analysis.sort_values("전략점수", ascending=False)["국가"].tolist()
)

filtered_trade = trade_partners[trade_partners["지역"].isin(selected_region)]
filtered_industries = industries[industries["산업"].isin(selected_industries)].copy()

# =====================================================
# 헤더
# =====================================================
st.markdown('<h1 class="main-title">한국 글로벌 무역 포지션 대시보드</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">한국이 세계 경제와 글로벌 공급망 속에서 어떤 국가와 연결되어 있는지 분석하는 인터랙티브 웹사이트</p>', unsafe_allow_html=True)

# =====================================================
# 상단 핵심 지표 카드
# =====================================================
metric1, metric2, metric3, metric4 = st.columns(4)

with metric1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">총 교역액</div>
        <div class="metric-value">${filtered_trade['총교역액_십억달러'].sum():.1f}B</div>
    </div>
    """, unsafe_allow_html=True)
with metric2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">총 수출액</div>
        <div class="metric-value">${filtered_trade['수출액_십억달러'].sum():.1f}B</div>
    </div>
    """, unsafe_allow_html=True)
with metric3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">총 수입액</div>
        <div class="metric-value">${filtered_trade['수입액_십억달러'].sum():.1f}B</div>
    </div>
    """, unsafe_allow_html=True)
with metric4:
    korea_gvc = oecd_sample.loc[oecd_sample["국가"] == "한국", "GVC참여도"].iloc[0]
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">한국 GVC 참여도</div>
        <div class="metric-value">{korea_gvc}%</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =====================================================
# 탭 구성
# 무역 네트워크 / FDI & 서비스 탭 삭제 반영
# =====================================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📌 개요",
    "📈 무역 타임라인",
    "🏭 산업 분석",
    "🔗 GVC & 공급망",
    "🌍 OECD 비교",
    "🤝 전략적 파트너"
])

# =====================================================
# 탭 1: 개요
# =====================================================
with tab1:
    col1, col2 = st.columns([1.15, 1])

    with col1:
        st.markdown("""
        <div class="glass-card">
        <h3>프로젝트 방향성</h3>
        <p>
        이 대시보드는 한국이 세계 경제와 국제 공급망 안에서 어떤 위치에 있는지를 시각화합니다.
        단순히 수출입 통계를 보여주는 것이 아니라, 한국이 어떤 국가와 얼마나 연결되어 있는지,
        어떤 산업을 중심으로 글로벌 가치사슬에 참여하는지, 그리고 어떤 국가와 전략적으로 좋은 관계를 유지해야 하는지를 분석합니다.
        </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="glass-card">
        <h3>핵심 질문</h3>
        <ul>
            <li>한국은 어떤 국가들과 가장 강하게 경제적으로 연결되어 있는가?</li>
            <li>한국 경제는 세계 무역과 공급망에 얼마나 의존하고 있는가?</li>
            <li>한국은 OECD 국가들과 비교했을 때 어떤 강점과 약점이 있는가?</li>
            <li>한국은 앞으로 어떤 국가와 전략적으로 좋은 관계를 유지해야 하는가?</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='glass-card'><h3>핵심 키워드</h3>", unsafe_allow_html=True)
        keywords = [
            "글로벌 무역", "한국 경제", "GVC", "OECD 평균 비교",
            "공급망", "전략적 파트너", "산업 구조", "데이터 시각화"
        ]
        keyword_html = "".join([f"<span class='keyword-pill'>{k}</span>" for k in keywords])
        st.markdown(keyword_html + "</div>", unsafe_allow_html=True)

        fig_overview = px.bar(
            trade_partners.sort_values("총교역액_십억달러", ascending=True),
            x="총교역액_십억달러",
            y="국가",
            orientation="h",
            title="한국의 주요 교역국",
            labels={"총교역액_십억달러": "총 교역액, 십억 달러", "국가": "국가"}
        )
        make_dark_layout(fig_overview)
        st.plotly_chart(fig_overview, use_container_width=True)

# =====================================================
# 탭 2: 무역 타임라인
# =====================================================
with tab2:
    st.subheader("무역 변화 타임라인")

    chart_option = st.radio("보고 싶은 차트 선택", ["수출 & 수입", "무역수지", "총 교역액"], horizontal=True)

    if chart_option == "수출 & 수입":
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(x=trade_timeline["연도"], y=trade_timeline["수출"], mode="lines+markers", name="수출"))
        fig_line.add_trace(go.Scatter(x=trade_timeline["연도"], y=trade_timeline["수입"], mode="lines+markers", name="수입"))
        fig_line.update_layout(title="한국의 수출입 변화", yaxis_title="십억 달러")
    elif chart_option == "무역수지":
        fig_line = px.bar(trade_timeline, x="연도", y="무역수지", title="한국의 무역수지 변화")
        fig_line.update_layout(yaxis_title="십억 달러")
    else:
        fig_line = px.area(trade_timeline, x="연도", y="총교역액", title="한국의 총 교역액 변화")
        fig_line.update_layout(yaxis_title="십억 달러")

    make_dark_layout(fig_line)
    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("""
    <div class="glass-card">
    <h3>경제 이벤트 해석</h3>
    <p><b>코로나19:</b> 글로벌 수요 감소와 물류 차질이 한국 수출 산업에 영향을 주었습니다.</p>
    <p><b>반도체 호황:</b> 한국의 수출 성과는 반도체 경기 사이클에 크게 좌우됩니다.</p>
    <p><b>미중 무역 갈등:</b> 한국은 두 거대 경제권 사이에 위치해 공급망 불확실성에 영향을 받습니다.</p>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# 탭 3: 산업 분석
# Treemap 삭제 / 가로 그래프와 주요 기업 추가
# =====================================================
with tab3:
    st.subheader("수출 산업 및 주요 기업 분석")

    col1, col2 = st.columns([1.1, 1])

    with col1:
        fig_industry_bar = px.bar(
            filtered_industries.sort_values("수출액", ascending=True),
            x="수출액",
            y="산업",
            orientation="h",
            title="산업별 수출액",
            labels={"수출액": "수출액, 십억 달러", "산업": "산업"}
        )
        make_dark_layout(fig_industry_bar)
        st.plotly_chart(fig_industry_bar, use_container_width=True)

    with col2:
        st.markdown("""
        <div class="glass-card">
        <h3>산업 분석 방향</h3>
        <p>
        이 탭은 산업별 수출 비중을 단순 이미지가 아니라 가로 막대그래프로 비교합니다.
        또한 각 산업을 대표하는 주요 기업과 공급망 연결 국가를 함께 제시하여,
        한국 수출 산업이 실제로 어떤 기업과 국가 관계를 중심으로 움직이는지 이해할 수 있도록 구성했습니다.
        </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 산업별 주요 기업 및 공급망 정보")
    st.dataframe(
        filtered_industries[["산업", "수출액", "주요기업", "주요_연결국가", "공급망_의존도"]],
        use_container_width=True,
        hide_index=True
    )

    selected_industry_for_comment = st.selectbox(
        "산업별 해석 보기",
        options=filtered_industries["산업"].tolist()
    )
    industry_comment = filtered_industries[filtered_industries["산업"] == selected_industry_for_comment]["산업_인사이트"].iloc[0]
    st.markdown(f"""
    <div class="insight">
    <b>{selected_industry_for_comment} 산업 인사이트</b><br>
    {industry_comment}
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# 탭 4: GVC & 공급망
# Sankey 대신 이해하기 쉬운 카드형 구조 + 국가별 연결 규모 그래프
# =====================================================
with tab4:
    st.subheader("글로벌 가치사슬과 공급망 구조")

    st.markdown("""
    <div class="glass-card">
    <h3>GVC를 쉽게 이해하기</h3>
    <p>
    글로벌 가치사슬(GVC)은 하나의 제품이 한 국가에서만 완성되는 것이 아니라,
    여러 국가의 생산·조립·소비 단계를 거쳐 만들어지는 구조를 의미합니다.
    아래 카드는 한국의 주요 산업이 어떤 국가들과 연결되는지 단순한 흐름으로 보여줍니다.
    </p>
    </div>
    """, unsafe_allow_html=True)

    flow_cols = st.columns(4)
    for i, row in value_chain_cases.iterrows():
        with flow_cols[i % 4]:
            st.markdown(f"""
            <div class="flow-box">
                <div class="flow-title">{row['산업']}</div>
                <div class="flow-step">{row['1단계']}</div>
                <div class="arrow">↓</div>
                <div class="flow-step">{row['2단계']}</div>
                <div class="arrow">↓</div>
                <div class="flow-step">{row['3단계']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("### 국가별 공급망 연결 규모")
    fig_supply = px.bar(
        partner_analysis.sort_values("공급망연결강도", ascending=True),
        x="공급망연결강도",
        y="국가",
        orientation="h",
        title="국가별 공급망 연결 강도",
        labels={"공급망연결강도": "공급망 연결 강도", "국가": "국가"}
    )
    make_dark_layout(fig_supply)
    st.plotly_chart(fig_supply, use_container_width=True)

    st.markdown("### 국가별 무역 규모")
    fig_trade_scale = px.bar(
        partner_analysis.sort_values("총교역액_십억달러", ascending=True),
        x="총교역액_십억달러",
        y="국가",
        orientation="h",
        title="한국과 주요 국가의 총 교역액",
        labels={"총교역액_십억달러": "총 교역액, 십억 달러", "국가": "국가"}
    )
    make_dark_layout(fig_trade_scale)
    st.plotly_chart(fig_trade_scale, use_container_width=True)

    top_supply_country = partner_analysis.sort_values("공급망연결강도", ascending=False).iloc[0]
    top_trade_country = partner_analysis.sort_values("총교역액_십억달러", ascending=False).iloc[0]

    st.markdown(f"""
    <div class="insight">
    <b>공급망 해석</b><br>
    공급망 연결 강도가 가장 높은 국가는 <b>{top_supply_country['국가']}</b>입니다.
    총 교역액 기준으로 가장 큰 국가는 <b>{top_trade_country['국가']}</b>입니다.
    즉, 한국은 단순히 많이 거래하는 국가뿐 아니라 핵심 산업 공급망에서 연결 강도가 높은 국가와도 안정적인 관계를 유지해야 합니다.
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# 탭 5: OECD 비교
# OECD 평균 추가 + 자동 해석 문장
# =====================================================
with tab5:
    st.subheader("한국과 OECD 국가 비교")

    korea_row = oecd_sample[oecd_sample["국가"] == "한국"].iloc[0]
    selected_row = oecd_compare[oecd_compare["국가"] == selected_country].iloc[0]

    comparison_df = pd.DataFrame([korea_row, selected_row])

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
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        title=f"한국 vs {selected_country}: 경제 구조 비교"
    )
    make_dark_layout(fig_radar)
    st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown(get_oecd_comment(selected_country, korea_row, selected_row), unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        fig_oecd_trade = px.bar(
            oecd_compare.sort_values("무역의존도", ascending=True),
            x="무역의존도",
            y="국가",
            orientation="h",
            title="OECD 비교: 무역 의존도",
            labels={"무역의존도": "무역 의존도", "국가": "국가"}
        )
        make_dark_layout(fig_oecd_trade)
        st.plotly_chart(fig_oecd_trade, use_container_width=True)

    with col2:
        fig_oecd_service = px.bar(
            oecd_compare.sort_values("서비스무역비중", ascending=True),
            x="서비스무역비중",
            y="국가",
            orientation="h",
            title="OECD 비교: 서비스 무역 비중",
            labels={"서비스무역비중": "서비스 무역 비중", "국가": "국가"}
        )
        make_dark_layout(fig_oecd_service)
        st.plotly_chart(fig_oecd_service, use_container_width=True)

# =====================================================
# 탭 6: 전략적 파트너 분석
# 국가별 무역 규모 + 공급망 연결 규모 + 종합 전략점수
# =====================================================
with tab6:
    st.subheader("한국의 전략적 파트너 분석")

    st.markdown("""
    <div class="glass-card">
    <h3>왜 전략적 파트너 분석이 필요한가?</h3>
    <p>
    한국은 무역 의존도가 높은 국가이기 때문에 단순히 수출입 규모만 보는 것보다,
    공급망 연결성, 핵심 산업 의존도, 총 교역 규모를 함께 고려해야 합니다.
    이 분석은 한국이 어떤 국가와 대외적으로 안정적인 관계를 유지해야 하는지 판단하는 데 도움을 줍니다.
    </p>
    <p><b>전략점수 계산 방식:</b> 무역 규모 40% + 공급망 연결성 40% + 핵심 산업 의존도 20%</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        fig_strategy = px.bar(
            partner_analysis.sort_values("전략점수", ascending=True),
            x="전략점수",
            y="국가",
            orientation="h",
            title="국가별 전략적 중요도 점수",
            labels={"전략점수": "전략점수", "국가": "국가"}
        )
        make_dark_layout(fig_strategy)
        st.plotly_chart(fig_strategy, use_container_width=True)

    with col2:
        fig_trade_partner = px.bar(
            partner_analysis.sort_values("총교역액_십억달러", ascending=True),
            x="총교역액_십억달러",
            y="국가",
            orientation="h",
            title="국가별 한국 무역 규모",
            labels={"총교역액_십억달러": "총 교역액, 십억 달러", "국가": "국가"}
        )
        make_dark_layout(fig_trade_partner)
        st.plotly_chart(fig_trade_partner, use_container_width=True)

    fig_supply_partner = px.bar(
        partner_analysis.sort_values("공급망연결강도", ascending=True),
        x="공급망연결강도",
        y="국가",
        orientation="h",
        title="국가별 가치사슬 연결 규모",
        labels={"공급망연결강도": "가치사슬 연결 강도", "국가": "국가"}
    )
    make_dark_layout(fig_supply_partner)
    st.plotly_chart(fig_supply_partner, use_container_width=True)

    st.markdown("### 국가별 상세 해석")
    selected_partner_row = partner_analysis[partner_analysis["국가"] == selected_partner].iloc[0]

    st.markdown(f"""
    <div class="insight">
    <b>{selected_partner}의 전략적 의미</b><br>
    전략점수는 <b>{selected_partner_row['전략점수']}</b>점이며, 전략 중요도는 <b>{selected_partner_row['전략중요도']}</b>입니다.
    총 교역액은 <b>${selected_partner_row['총교역액_십억달러']:.1f}B</b>,
    공급망 연결 강도는 <b>{selected_partner_row['공급망연결강도']}</b>,
    핵심 산업 의존도는 <b>{selected_partner_row['핵심산업의존도']}</b>입니다.
    <br><br>
    {selected_partner_row['전략적_의미']}
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(
        partner_analysis[["국가", "총교역액_십억달러", "공급망연결강도", "핵심산업의존도", "전략점수", "전략중요도", "전략적_의미"]]
        .sort_values("전략점수", ascending=False),
        use_container_width=True,
        hide_index=True
    )

# =====================================================
# 푸터
# =====================================================
st.markdown("---")
st.caption("데이터 안내: 현재 버전은 프로토타입용 샘플 데이터를 사용합니다. 최종 제출 시 OECD, World Bank, KITA, UN Comtrade 등의 실제 데이터로 교체할 수 있습니다.")
st.caption("제작 도구: Python, Streamlit, Pandas, Plotly")
