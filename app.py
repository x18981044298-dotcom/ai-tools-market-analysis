# -*- coding: utf-8 -*-
"""
AI工具市场多维度分析报告 - Streamlit交互式仪表盘
基于 There's An AI For That 数据
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from data_processor import AIToolsDataProcessor

# ============================================================================
# 页面配置
# ============================================================================
st.set_page_config(
    page_title="AI工具市场深度分析",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# 自定义CSS样式
# ============================================================================
st.markdown("""
<style>
    /* 主题色彩 */
    :root {
        --primary: #1E3A5F;
        --accent: #F39C12;
        --success: #27AE60;
        --warning: #E74C3C;
    }
    
    /* 隐藏Streamlit默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 标题样式 */
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #1E3A5F 0%, #3D7EAA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 20px 0;
    }
    
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1E3A5F;
        border-left: 4px solid #F39C12;
        padding-left: 15px;
        margin: 30px 0 20px 0;
    }
    
    /* 指标卡片 */
    .metric-card {
        background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        text-align: center;
        border: 1px solid #e2e8f0;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1E3A5F;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #7F8C8D;
        margin-top: 5px;
    }
    
    /* 洞察卡片 */
    .insight-card {
        background: #f0f9ff;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #3D7EAA;
    }
    
    .insight-card.warning {
        background: #fef2f2;
        border-left-color: #E74C3C;
    }
    
    .insight-card.success {
        background: #f0fdf4;
        border-left-color: #27AE60;
    }
    
    .insight-card.gold {
        background: #fffbeb;
        border-left-color: #F39C12;
    }
    
    /* 标签样式 */
    .tag {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 2px;
    }
    
    .tag-blue { background: #dbeafe; color: #1e40af; }
    .tag-green { background: #dcfce7; color: #166534; }
    .tag-yellow { background: #fef3c7; color: #92400e; }
    .tag-red { background: #fee2e2; color: #991b1b; }
    
    /* 表格优化 */
    .dataframe {
        font-size: 0.85rem;
    }
    
    /* 侧边栏 */
    .css-1d391kg {
        background: linear-gradient(180deg, #1E3A5F 0%, #2D5A8A 100%);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# 数据加载
# ============================================================================
# 使用ttl=0强制每次重新加载数据，确保数据处理模块的更新生效
@st.cache_data(ttl=0)
def load_data():
    processor = AIToolsDataProcessor()
    return processor.get_data()

df = load_data()

# ============================================================================
# 侧边栏导航
# ============================================================================
st.sidebar.markdown("## 🤖 AI工具市场分析")
st.sidebar.markdown("---")

analysis_view = st.sidebar.radio(
    "📊 选择分析视角",
    [
        "🏠 执行摘要",
        "🚀 市场结构视角",
        "🧭 用户需求视角", 
        "🔎 趋势机会视角",
        "🪜 产品机会视角",
        "🧱 分类系统视角",
        "🧲 商业化视角",
        "🧬 用户角色视角",
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎛️ 数据筛选")

# 层级筛选
selected_tiers = st.sidebar.multiselect(
    "市场层级",
    options=df['market_tier'].unique().tolist(),
    default=df['market_tier'].unique().tolist()
)

# 用户场景筛选
selected_scenarios = st.sidebar.multiselect(
    "用户场景",
    options=df['user_scenario'].unique().tolist(),
    default=df['user_scenario'].unique().tolist()
)

# 应用筛选
df_filtered = df[
    (df['market_tier'].isin(selected_tiers)) &
    (df['user_scenario'].isin(selected_scenarios))
]

st.sidebar.markdown("---")
st.sidebar.markdown(f"**当前数据:** {len(df_filtered)} 个分类")
st.sidebar.markdown(f"**工具总数:** {df_filtered['tools_count'].sum():,}")

# ============================================================================
# 辅助函数
# ============================================================================
def create_metric_card(value, label, delta=None):
    """创建指标卡片"""
    delta_html = f"<div style='color: {'green' if delta and delta > 0 else 'red'}; font-size: 0.8rem;'>{delta:+.1f}%</div>" if delta else ""
    return f"""
    <div class="metric-card">
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
        {delta_html}
    </div>
    """

def create_insight_card(content, card_type="default"):
    """创建洞察卡片"""
    return f'<div class="insight-card {card_type}">{content}</div>'

# ============================================================================
# 视图1: 执行摘要
# ============================================================================
if analysis_view == "🏠 执行摘要":
    st.markdown('<h1 class="main-title">🤖 AI工具市场深度分析报告</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666;">基于 There\'s An AI For That 数据 | 2025年11月30日</p>', unsafe_allow_html=True)
    
    # KPI指标行
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("📊 分析分类", f"{len(df):,}")
    with col2:
        st.metric("🔧 AI工具总数", f"{df['tools_count'].sum():,}")
    with col3:
        st.metric("📈 头部占比(Top10)", f"{df.head(10)['tools_count'].sum()/df['tools_count'].sum()*100:.1f}%")
    with col4:
        st.metric("🎯 平均工具数", f"{df['tools_count'].mean():.0f}")
    with col5:
        st.metric("📉 中位数", f"{df['tools_count'].median():.0f}")
    
    st.markdown("---")
    
    # 两列布局
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Top 15 分类排行")
        fig = px.bar(
            df.head(15),
            x='tools_count',
            y='category',
            orientation='h',
            color='tools_count',
            color_continuous_scale='Blues',
            text='tools_count'
        )
        fig.update_layout(
            height=500,
            showlegend=False,
            yaxis={'categoryorder': 'total ascending'},
            xaxis_title="AI工具数量",
            yaxis_title="",
            coloraxis_showscale=False
        )
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 工具数量占比")
        # 构建饼图数据 - 计算工具数量占比
        total_tools = df['tools_count'].sum()
        top5 = df.head(5).copy()
        top5['market_share'] = (top5['tools_count'] / total_tools * 100).round(1)
        
        others_count = df['tools_count'].iloc[5:].sum()
        others_share = (others_count / total_tools * 100).round(1)
        
        others = pd.DataFrame({
            'category': ['Others'],
            'tools_count': [others_count],
            'market_share': [others_share]
        })
        pie_data = pd.concat([top5[['category', 'tools_count', 'market_share']], others])
        
        fig = px.pie(
            pie_data,
            values='market_share',
            names='category',
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
        fig.update_layout(height=500)
        fig.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>占比: %{value:.1f}%<br>工具数: ' + pie_data['tools_count'].astype(str) + '<extra></extra>'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # 核心洞察
    st.markdown("### 💡 核心洞察")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(create_insight_card(
            "🔴 <b>红海警示</b><br>Creativity(8,787)、Business(6,508)、Images(2,726) 竞争极其激烈，同质化严重",
            "warning"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_insight_card(
            "🟢 <b>蓝海机会</b><br>Legal(217)、Data analysis(230)、HR(226) 工具少但付费意愿极高",
            "success"
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_insight_card(
            "🟡 <b>增长趋势</b><br>Document chat、Virtual companion、Mental health 受大模型推动快速增长",
            "gold"
        ), unsafe_allow_html=True)

# ============================================================================
# 视图2: 市场结构视角
# ============================================================================
elif analysis_view == "🚀 市场结构视角":
    st.markdown('<h2 class="section-header">🚀 市场结构视角 - Macro Market Structure</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📊 供给密度分析", "📈 赛道分层结构", "🎯 颗粒度分析"])
    
    with tab1:
        st.markdown("#### 1️⃣ 赛道供给饱和度指数")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # 饱和度热力图
            df_saturation = df_filtered.copy()
            df_saturation['saturation_level'] = pd.cut(
                df_saturation['saturation_index'],
                bins=[0, 5, 15, 30, 50, 100],
                labels=['蓝海空白', '蓝海机会', '竞争中等', '红海预警', '超级红海']
            )
            
            fig = px.treemap(
                df_saturation.head(50),
                path=['saturation_level', 'category'],
                values='tools_count',
                color='saturation_index',
                color_continuous_scale='RdYlGn_r',
                title='赛道饱和度树状图 (Top 50)'
            )
            fig.update_layout(height=600)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("##### 🔴 超级红海 (饱和度 > 50%)")
            red_ocean = df_filtered[df_filtered['saturation_index'] > 50][['category', 'tools_count', 'chinese_name']]
            st.dataframe(red_ocean, hide_index=True, use_container_width=True)
            
            st.markdown("##### 🔵 蓝海空白 (饱和度 < 5%)")
            blue_ocean = df_filtered[df_filtered['saturation_index'] < 5].tail(15)[['category', 'tools_count', 'chinese_name']]
            st.dataframe(blue_ocean, hide_index=True, use_container_width=True)
    
    with tab2:
        st.markdown("#### 2️⃣ 市场分层结构分析")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 层级分布
            tier_stats = df_filtered.groupby('market_tier').agg({
                'tools_count': ['count', 'sum', 'mean']
            }).round(0)
            tier_stats.columns = ['分类数量', '工具总数', '平均工具数']
            tier_stats['工具占比%'] = (tier_stats['工具总数'] / tier_stats['工具总数'].sum() * 100).round(1)
            tier_stats = tier_stats.reset_index()
            
            fig = px.sunburst(
                df_filtered,
                path=['market_tier', 'category'],
                values='tools_count',
                color='market_tier',
                color_discrete_map={
                    'Tier 1 头部': '#F39C12',
                    'Tier 2 腰部上': '#1E3A5F',
                    'Tier 3 腰部': '#3D7EAA',
                    'Tier 4 腰部下': '#5DADE2',
                    'Tier 5 尾部': '#AED6F1'
                },
                title='市场层级旭日图'
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("##### 📊 层级统计详情")
            st.dataframe(tier_stats, hide_index=True, use_container_width=True)
            
            # 头部集中度分析
            st.markdown("##### 📈 头部集中度")
            top_n_options = [5, 10, 20, 50]
            concentration = []
            for n in top_n_options:
                share = df_filtered.head(n)['tools_count'].sum() / df_filtered['tools_count'].sum() * 100
                concentration.append({'Top N': f'Top {n}', '工具占比': f'{share:.1f}%'})
            st.dataframe(pd.DataFrame(concentration), hide_index=True, use_container_width=True)
        
        # 累计份额曲线
        st.markdown("##### 📉 帕累托曲线 - 累计工具占比")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(range(1, len(df_filtered)+1)),
            y=df_filtered['cumulative_share'],
            fill='tozeroy',
            name='累计份额',
            line=dict(color='#1E3A5F', width=2)
        ))
        fig.add_hline(y=80, line_dash="dash", line_color="#F39C12", annotation_text="80%线")
        fig.update_layout(
            xaxis_title="分类排名",
            yaxis_title="累计工具占比 (%)",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("#### 3️⃣ 赛道颗粒度分析")
        
        # 颗粒度分布
        granularity_stats = df_filtered.groupby('granularity').agg({
            'tools_count': ['count', 'mean', 'sum']
        }).round(0)
        granularity_stats.columns = ['分类数', '平均工具数', '工具总数']
        granularity_stats = granularity_stats.reset_index()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                granularity_stats,
                x='granularity',
                y='分类数',
                color='平均工具数',
                color_continuous_scale='Blues',
                title='各颗粒度级别的分类数量'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.scatter(
                df_filtered,
                x='tools_count',
                y='rank',
                color='granularity',
                hover_name='category',
                title='颗粒度 vs 工具数量分布',
                log_x=True
            )
            fig.update_layout(height=400, yaxis_title='排名')
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(create_insight_card(
            "💡 <b>颗粒度洞察:</b> 大分类(Creativity, Business)覆盖范围广，工具数量多，竞争激烈；小分类(Wine, Tarot, Wedding)定位精准，工具数量少，可能存在细分机会。",
            "gold"
        ), unsafe_allow_html=True)

# ============================================================================
# 视图3: 用户需求视角
# ============================================================================
elif analysis_view == "🧭 用户需求视角":
    st.markdown('<h2 class="section-header">🧭 用户需求视角 - User & Jobs-to-be-Done</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["👤 用户场景分析", "🎯 用户意图分析", "📊 竞争强度分析"])
    
    with tab1:
        st.markdown("#### 4️⃣ 用户行为领域分类")
        
        # 场景分布
        scenario_stats = df_filtered.groupby('user_scenario').agg({
            'tools_count': ['count', 'sum', 'mean']
        }).round(0)
        scenario_stats.columns = ['分类数', '工具总数', '平均工具数']
        scenario_stats = scenario_stats.sort_values('工具总数', ascending=False).reset_index()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                scenario_stats,
                x='user_scenario',
                y='工具总数',
                color='分类数',
                color_continuous_scale='Blues',
                title='用户场景工具分布'
            )
            fig.update_layout(height=450, xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.pie(
                scenario_stats,
                values='工具总数',
                names='user_scenario',
                title='场景份额分布',
                hole=0.3
            )
            fig.update_layout(height=450)
            st.plotly_chart(fig, use_container_width=True)
        
        # 场景详情表
        st.markdown("##### 📊 各场景详细数据")
        st.dataframe(scenario_stats, hide_index=True, use_container_width=True)
    
    with tab2:
        st.markdown("#### 5️⃣ 用户意图类型分析")
        
        intent_stats = df_filtered.groupby('user_intent').agg({
            'tools_count': ['count', 'sum', 'mean']
        }).round(0)
        intent_stats.columns = ['分类数', '工具总数', '平均工具数']
        intent_stats = intent_stats.sort_values('工具总数', ascending=False).reset_index()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.treemap(
                df_filtered,
                path=['user_intent', 'category'],
                values='tools_count',
                color='tools_count',
                color_continuous_scale='Blues',
                title='用户意图树状图 (按工具数量)'
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # 雷达图 - 只显示工具数量分布
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=intent_stats['工具总数'].head(8) / intent_stats['工具总数'].max() * 100,
                theta=intent_stats['user_intent'].head(8),
                fill='toself',
                name='工具数量占比',
                line_color='#1E3A5F'
            ))
            fig.add_trace(go.Scatterpolar(
                r=intent_stats['分类数'].head(8) / intent_stats['分类数'].max() * 100,
                theta=intent_stats['user_intent'].head(8),
                fill='toself',
                name='分类数量占比',
                line_color='#F39C12'
            ))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                title='意图类型分布雷达图',
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(intent_stats, hide_index=True, use_container_width=True)
    
    with tab3:
        st.markdown("#### 6️⃣ 竞争强度分析")
        
        st.info("💡 **说明**: 竞争强度基于工具数量客观衡量，工具数量越多表示该赛道竞争越激烈。")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### 🔵 低竞争赛道 (工具数量最少)")
            low_competition = df_filtered.nsmallest(15, 'tools_count')[
                ['category', 'chinese_name', 'tools_count', 'rank']
            ]
            st.dataframe(low_competition, hide_index=True, use_container_width=True)
        
        with col2:
            st.markdown("##### 🔴 高竞争赛道 (工具数量最多)")
            high_competition = df_filtered.nlargest(15, 'tools_count')[
                ['category', 'chinese_name', 'tools_count', 'rank']
            ]
            st.dataframe(high_competition, hide_index=True, use_container_width=True)
        
        # 竞争强度分布图
        fig = px.scatter(
            df_filtered,
            x='rank',
            y='tools_count',
            color='market_tier',
            hover_name='category',
            hover_data=['chinese_name'],
            title='赛道竞争分布图 (排名 vs 工具数量)'
        )
        fig.add_hline(y=500, line_dash="dash", line_color="red", annotation_text="高竞争线 (500+)")
        fig.add_hline(y=100, line_dash="dash", line_color="green", annotation_text="低竞争线 (<100)")
        fig.update_layout(height=500, xaxis_title="排名", yaxis_title="工具数量")
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# 视图4: 趋势机会视角
# ============================================================================
elif analysis_view == "🔎 趋势机会视角":
    st.markdown('<h2 class="section-header">🔎 趋势机会视角 - Trend & Opportunity</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🚀 大模型推动赛道", "💢 痛点驱动赛道", "🎯 机会象限分析"])
    
    with tab1:
        st.markdown("#### 7️⃣ 大模型推动的新兴赛道")
        
        llm_categories = df_filtered[df_filtered['llm_driven']]
        non_llm = df_filtered[~df_filtered['llm_driven']]
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("##### 🤖 LLM推动赛道")
            st.dataframe(
                llm_categories[['category', 'chinese_name', 'tools_count', 'rank']],
                hide_index=True,
                use_container_width=True
            )
            
            st.markdown(create_insight_card(
                "💡 这些赛道因 GPT/Claude/Gemini 而诞生或爆发，代表AI原生应用方向",
                "gold"
            ), unsafe_allow_html=True)
        
        with col2:
            # 对比图
            compare_data = pd.DataFrame({
                '类型': ['LLM推动', '传统赛道'],
                '分类数': [len(llm_categories), len(non_llm)],
                '平均工具数': [llm_categories['tools_count'].mean(), non_llm['tools_count'].mean()],
                '工具总数': [llm_categories['tools_count'].sum(), non_llm['tools_count'].sum()]
            })
            
            fig = make_subplots(rows=1, cols=3, subplot_titles=['分类数量', '平均工具数', '工具总数'])
            
            fig.add_trace(go.Bar(x=compare_data['类型'], y=compare_data['分类数'], marker_color=['#F39C12', '#3D7EAA']), row=1, col=1)
            fig.add_trace(go.Bar(x=compare_data['类型'], y=compare_data['平均工具数'], marker_color=['#F39C12', '#3D7EAA']), row=1, col=2)
            fig.add_trace(go.Bar(x=compare_data['类型'], y=compare_data['工具总数'], marker_color=['#F39C12', '#3D7EAA']), row=1, col=3)
            
            fig.update_layout(height=400, showlegend=False, title='LLM推动 vs 传统赛道对比')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("#### 8️⃣ 现实痛点驱动的赛道")
        
        pain_categories = df_filtered[df_filtered['pain_driven']]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### 💢 痛点驱动赛道")
            st.dataframe(
                pain_categories[['category', 'chinese_name', 'tools_count', 'rank']],
                hide_index=True,
                use_container_width=True
            )
        
        with col2:
            fig = px.bar(
                pain_categories,
                x='category',
                y='tools_count',
                color='tools_count',
                color_continuous_scale='Blues',
                title='痛点赛道工具分布'
            )
            fig.update_layout(height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        **痛点来源分析 (基于分类名称推断):**
        - 🎯 **求职压力**: Job interview, Interview preparation, Resume
        - 💔 **情感孤独**: Emotional support, Mental health, Therapy  
        - ⏰ **效率焦虑**: Productivity, Automation
        - 🏥 **健康意识**: Health, Fitness
        """)
    
    with tab3:
        st.markdown("#### 9️⃣ 竞争格局分析")
        
        st.info("💡 **说明**: 竞争格局仅基于工具数量划分，工具数量多表示竞争激烈，不代表商业价值判断。")
        
        quadrant_stats = df_filtered.groupby('competition_quadrant').agg({
            'tools_count': ['count', 'sum', 'mean']
        }).round(0)
        quadrant_stats.columns = ['分类数', '工具总数', '平均工具数']
        quadrant_stats = quadrant_stats.reset_index()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(
                quadrant_stats,
                values='分类数',
                names='competition_quadrant',
                color='competition_quadrant',
                color_discrete_map={
                    '红海赛道 (工具数≥500)': '#E74C3C',
                    '竞争赛道 (200≤工具数<500)': '#F39C12',
                    '机会赛道 (100≤工具数<200)': '#3498DB',
                    '蓝海赛道 (工具数<100)': '#27AE60'
                },
                title='竞争格局分布'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.dataframe(quadrant_stats, hide_index=True, use_container_width=True)
            
            st.markdown("##### 🔵 蓝海赛道 (工具数<100)")
            blue_ocean = df_filtered[df_filtered['competition_quadrant'] == '蓝海赛道 (工具数<100)']
            st.dataframe(
                blue_ocean[['category', 'chinese_name', 'tools_count', 'rank']].head(10),
                hide_index=True,
                use_container_width=True
            )

# ============================================================================
# 视图5: 产品机会视角
# ============================================================================
elif analysis_view == "🪜 产品机会视角":
    st.markdown('<h2 class="section-header">🪜 产品机会视角 - Product Opportunity</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🔴 高竞争赛道", "🔵 低竞争赛道", "🔍 纵深/横切机会"])
    
    with tab1:
        st.markdown("#### 10️⃣ 高竞争赛道 (工具数≥500)")
        
        st.info("💡 **说明**: 高竞争赛道工具数量多，可能存在差异化机会，但具体价值需结合实际市场调研判断。")
        
        high_supply = df_filtered[
            df_filtered['tools_count'] >= 500
        ].sort_values('tools_count', ascending=False)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("##### 🔴 高竞争赛道列表")
            st.dataframe(
                high_supply[['category', 'chinese_name', 'tools_count', 'rank']],
                hide_index=True,
                use_container_width=True
            )
        
        with col2:
            fig = px.bar(
                high_supply,
                x='category',
                y='tools_count',
                color='tools_count',
                color_continuous_scale='Reds',
                title='高竞争赛道工具分布'
            )
            fig.update_layout(height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(create_insight_card(
            "💡 <b>观察:</b> 这些赛道工具数量多，竞争激烈。如需进入，建议寻找<b>细分定位</b>或<b>差异化功能</b>。",
            "gold"
        ), unsafe_allow_html=True)
    
    with tab2:
        st.markdown("#### 11️⃣ 低竞争赛道 (工具数<100)")
        
        st.info("💡 **说明**: 低竞争不等于高价值，需结合实际市场需求判断。工具少可能是需求小或市场未成熟。")
        
        low_supply = df_filtered[
            df_filtered['tools_count'] < 100
        ].sort_values('tools_count', ascending=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("##### 🔵 低竞争赛道列表")
            st.dataframe(
                low_supply[['category', 'chinese_name', 'tools_count', 'rank', 'target_user']],
                hide_index=True,
                use_container_width=True
            )
        
        with col2:
            fig = px.scatter(
                low_supply,
                x='rank',
                y='tools_count',
                color='target_user',
                hover_name='category',
                title='低竞争赛道分布'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(create_insight_card(
            "💡 <b>注意:</b> 这些赛道工具数量少，可能存在机会，但也需要验证市场需求是否真实存在。",
            "success"
        ), unsafe_allow_html=True)
    
    with tab3:
        st.markdown("#### 12️⃣ 纵深与横切机会分析")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### 🔽 可纵深挖掘的赛道")
            deep_dive = {
                'Coding/Software': ['Debugging', 'Code review', 'Testing', 'Deployment', 'Documentation'],
                'Marketing': ['SEO', 'Ads', 'Social media', 'Email marketing', 'Content marketing'],
                'Education': ['K-12', 'Higher Ed', 'Corporate training', 'Language', 'Skills'],
                'Health': ['Mental health', 'Fitness', 'Nutrition', 'Sleep', 'Chronic disease']
            }
            
            for parent, children in deep_dive.items():
                st.markdown(f"**{parent}**")
                st.markdown(f"→ {' | '.join(children)}")
                st.markdown("")
        
        with col2:
            st.markdown("##### ↔️ 可横向切分的赛道")
            horizontal = {
                'Business': ['管理', '战略', '发票', '合同', '提案', '会议'],
                'Marketing': ['SEO', '广告', '文案', '社媒', '落地页', '邮件'],
                'Design': ['Logo', 'UI/UX', '海报', '名片', '包装', '插画'],
                'Personal': ['日程', '习惯', '记账', '健康', '社交', '学习']
            }
            
            for parent, children in horizontal.items():
                st.markdown(f"**{parent}**")
                st.markdown(f"→ {' | '.join(children)}")
                st.markdown("")

# ============================================================================
# 视图6: 分类系统视角
# ============================================================================
elif analysis_view == "🧱 分类系统视角":
    st.markdown('<h2 class="section-header">🧱 分类系统视角 - Taxonomy Insights</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🔄 分类冗余分析", "📏 颗粒度不一致", "🌐 超级领域合并"])
    
    with tab1:
        st.markdown("#### 14️⃣ 分类重叠/冗余分析")
        
        overlap_groups = {
            '文本相关': ['Writing', 'Text', 'Content', 'Stories', 'Short stories', 'Copywriting'],
            '教育相关': ['Education', 'Learning', 'Studying', 'School', 'School subject', 'Teaching'],
            '图像相关': ['Images', 'Image editing', 'Anime image', 'Cartoon image', 'Photo editing', 'Portraits'],
            '职业相关': ['Career', 'Job search', 'Resume', 'Job interview', 'Interview preparation'],
            '健康相关': ['Health', 'Mental health', 'Fitness', 'Nutrition', 'Therapy', 'Meditation'],
        }
        
        overlap_data = []
        for group_name, categories in overlap_groups.items():
            group_df = df_filtered[df_filtered['category'].isin(categories)]
            overlap_data.append({
                '重叠组': group_name,
                '包含分类数': len(group_df),
                '工具总数': group_df['tools_count'].sum(),
                '包含分类': ', '.join(categories)
            })
        
        overlap_df = pd.DataFrame(overlap_data)
        st.dataframe(overlap_df, hide_index=True, use_container_width=True)
        
        st.markdown(create_insight_card(
            "💡 <b>分类优化建议:</b> 当前分类存在明显重叠，建议合并相似分类，减少用户认知负担。例如将Writing/Text/Content合并为「文本创作」。",
            "gold"
        ), unsafe_allow_html=True)
    
    with tab2:
        st.markdown("#### 15️⃣ 分类颗粒度不一致")
        
        granularity_examples = df_filtered.groupby('granularity').apply(
            lambda x: x.nlargest(3, 'tools_count')[['category', 'tools_count']].values.tolist()
        ).to_dict()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### 🔵 颗粒度分布")
            granularity_count = df_filtered['granularity'].value_counts().reset_index()
            granularity_count.columns = ['颗粒度', '分类数']
            
            fig = px.bar(
                granularity_count,
                x='颗粒度',
                y='分类数',
                color='颗粒度',
                color_discrete_sequence=px.colors.sequential.Blues
            )
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("##### 📊 颗粒度对比")
            comparison = df_filtered.groupby('granularity').agg({
                'tools_count': ['mean', 'min', 'max', 'count']
            }).round(0)
            comparison.columns = ['平均工具数', '最少', '最多', '分类数']
            st.dataframe(comparison, use_container_width=True)
    
    with tab3:
        st.markdown("#### 16️⃣ 超级领域合并视图")
        
        super_domain_stats = df_filtered.groupby('super_domain').agg({
            'tools_count': ['count', 'sum', 'mean']
        }).round(0)
        super_domain_stats.columns = ['子分类数', '工具总数', '平均工具数']
        super_domain_stats = super_domain_stats.sort_values('工具总数', ascending=False).reset_index()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.treemap(
                df_filtered,
                path=['super_domain', 'category'],
                values='tools_count',
                color='tools_count',
                color_continuous_scale='Blues',
                title='超级领域树状图 (按工具数量)'
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("##### 📊 超级领域统计")
            st.dataframe(super_domain_stats, hide_index=True, use_container_width=True)

# ============================================================================
# 视图7: 商业化视角
# ============================================================================
elif analysis_view == "🧲 商业化视角":
    st.markdown('<h2 class="section-header">🧲 商业化视角 - Business & Monetization</h2>', unsafe_allow_html=True)
    
    st.warning("⚠️ **重要说明**: 本视角的分析基于分类名称推断目标用户类型，不代表实际付费能力或商业价值。准确的商业化分析需要真实的收入、转化率等数据支撑。")
    
    tab1, tab2, tab3 = st.tabs(["👥 目标用户分析", "📊 商业模式分布", "🎯 变现策略参考"])
    
    with tab1:
        st.markdown("#### 17️⃣ 目标用户类型分析")
        
        st.info("💡 **说明**: 目标用户类型基于分类名称推断，B2B企业类通常付费意愿较高，B2C个人类通常更依赖免费增值模式。")
        
        target_user_stats = df_filtered.groupby('target_user').agg({
            'tools_count': ['count', 'sum', 'mean']
        }).round(0)
        target_user_stats.columns = ['分类数', '工具总数', '平均工具数']
        target_user_stats = target_user_stats.sort_values('工具总数', ascending=False).reset_index()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(
                target_user_stats,
                values='工具总数',
                names='target_user',
                title='目标用户类型分布',
                hole=0.3,
                color_discrete_sequence=['#1E3A5F', '#3D7EAA', '#F39C12']
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.dataframe(target_user_stats, hide_index=True, use_container_width=True)
            
            st.markdown("##### 📋 各类型代表赛道")
            for user_type in ['B2B企业', 'B2B/B2C', 'B2C个人']:
                cats = df_filtered[df_filtered['target_user'] == user_type]['category'].head(5).tolist()
                st.markdown(f"**{user_type}**: {', '.join(cats)}")
    
    with tab2:
        st.markdown("#### 18️⃣ 商业模式分布 (推断)")
        
        st.info("💡 **说明**: 商业模式基于分类特征推断，实际模式可能因产品定位不同而异。")
        
        biz_model_stats = df_filtered.groupby('biz_model').agg({
            'tools_count': ['count', 'sum', 'mean']
        }).round(0)
        biz_model_stats.columns = ['分类数', '工具总数', '平均工具数']
        biz_model_stats = biz_model_stats.sort_values('工具总数', ascending=False).reset_index()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(
                biz_model_stats,
                values='工具总数',
                names='biz_model',
                title='商业模式分布',
                hole=0.3,
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig.update_layout(height=450)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.dataframe(biz_model_stats, hide_index=True, use_container_width=True)
            
            st.markdown("""
            **商业模式说明:**
            - **B2B SaaS**: 企业级订阅，高ARPU
            - **B2B 订阅**: 中小企业营销工具
            - **B2C 订阅**: 个人效率/学习工具
            - **一次性/模板**: 设计资产付费
            - **免费/流量**: 靠广告/流量变现
            - **陪伴订阅**: 情感/社交类订阅
            """)
    
    with tab3:
        st.markdown("#### 19️⃣ 变现策略建议矩阵")
        
        strategy_data = [
            {'赛道类型': 'B2B SaaS', '代表赛道': 'Legal, Data analysis, HR', '建议定价': '$50-500/月', '关键成功因素': '深度集成、数据安全、客户成功'},
            {'赛道类型': 'B2B 订阅', '代表赛道': 'SEO, Marketing, Ads', '建议定价': '$20-100/月', '关键成功因素': '效果可量化、易用性、模板丰富'},
            {'赛道类型': 'B2C 订阅', '代表赛道': 'Learning, Productivity', '建议定价': '$5-30/月', '关键成功因素': '习惯养成、社交属性、免费增值'},
            {'赛道类型': '一次性/模板', '代表赛道': 'Design, Logo, Resume', '建议定价': '$5-50/次', '关键成功因素': '质量、多样性、即时交付'},
            {'赛道类型': '免费/流量', '代表赛道': 'Images, Games, Horoscope', '建议定价': '广告/增值', '关键成功因素': '用户量、使用频次、病毒传播'},
            {'赛道类型': '陪伴订阅', '代表赛道': 'Virtual companion, Dating', '建议定价': '$10-50/月', '关键成功因素': '情感连接、个性化、隐私保护'},
        ]
        
        st.dataframe(pd.DataFrame(strategy_data), hide_index=True, use_container_width=True)

# ============================================================================
# 视图8: 用户角色视角
# ============================================================================
elif analysis_view == "🧬 用户角色视角":
    st.markdown('<h2 class="section-header">🧬 用户角色视角 - Personas</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["👔 工作角色", "🎭 兴趣角色", "💝 情感角色"])
    
    with tab1:
        st.markdown("#### 21️⃣ 工作角色画像")
        
        work_personas = ['产品经理', '人力资源', '招聘专员', '数据分析师', '开发者', 
                        '管理者', '销售', '营销人员', '设计师', '法务', '财务', '教师', '研究员', '客服']
        
        work_df = df_filtered[df_filtered['persona'].isin(work_personas)]
        
        persona_stats = work_df.groupby('persona').agg({
            'tools_count': ['sum', 'mean'],
            'category': 'count'
        }).round(0)
        persona_stats.columns = ['工具总数', '平均工具数', '相关分类数']
        persona_stats = persona_stats.sort_values('工具总数', ascending=False).reset_index()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                persona_stats,
                x='persona',
                y='工具总数',
                color='相关分类数',
                color_continuous_scale='Blues',
                title='工作角色AI工具分布'
            )
            fig.update_layout(height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.dataframe(persona_stats, hide_index=True, use_container_width=True)
    
    with tab2:
        st.markdown("#### 22️⃣ 兴趣角色画像")
        
        interest_personas = ['时尚爱好者', '美食爱好者', '品酒师', '宠物主人', 
                            '旅行者', '游戏玩家', '音乐爱好者', '艺术爱好者', '健身达人']
        
        interest_df = df_filtered[df_filtered['persona'].isin(interest_personas)]
        
        if not interest_df.empty:
            fig = px.treemap(
                interest_df,
                path=['persona', 'category'],
                values='tools_count',
                color='tools_count',
                color_continuous_scale='Purples',
                title='兴趣角色画像分布 (按工具数量)'
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("当前筛选条件下没有兴趣角色相关数据")
    
    with tab3:
        st.markdown("#### 23️⃣ 情感与学习角色")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### 💝 情感需求角色")
            emotional_categories = df_filtered[df_filtered['user_intent'] == '关系陪伴']
            st.dataframe(
                emotional_categories[['category', 'chinese_name', 'tools_count']],
                hide_index=True,
                use_container_width=True
            )
            
            st.markdown(create_insight_card(
                "💡 情感类AI适合做<b>陪伴订阅</b>模式，关键是建立情感连接和个性化体验",
                "gold"
            ), unsafe_allow_html=True)
        
        with col2:
            st.markdown("##### 📚 技能学习角色")
            learning_categories = df_filtered[df_filtered['user_intent'] == '技能学习']
            st.dataframe(
                learning_categories[['category', 'chinese_name', 'tools_count']],
                hide_index=True,
                use_container_width=True
            )
            
            st.markdown(create_insight_card(
                "💡 学习类AI适合做<b>订阅+课程</b>模式，关键是学习效果可量化和习惯养成",
                "success"
            ), unsafe_allow_html=True)

# ============================================================================
# 页脚
# ============================================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.85rem;">
    <p>📊 数据来源: <a href="https://theresanaiforthat.com" target="_blank">There's An AI For That</a> | 更新时间: 2025年11月30日</p>
    <p>🤖 AI工具市场多维度分析报告 | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)

