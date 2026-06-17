"""
Trade Intelligence Platform - Bloomberg-Style Dashboard
Executive UI for monitoring multi-agent AI system execution
Supports multiple international trade frameworks
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from typing import Dict, Any, List

# Page configuration
st.set_page_config(
    page_title="Trade Intelligence Platform",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Bloomberg-style Custom CSS
st.markdown("""
<style>
    /* Bloomberg Dark Theme */
    .main {
        background-color: #0a0a0a;
    }
    .stApp {
        background-color: #0a0a0a;
    }
    
    /* Header Styling */
    .bloomberg-header {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #ff6b00;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #ff6b00;
        font-family: 'Helvetica Neue', sans-serif;
        letter-spacing: -0.5px;
    }
    
    .subtitle {
        color: #b0b0b0;
        font-size: 0.95rem;
        margin-top: 0.3rem;
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #252525 100%);
        padding: 1.2rem;
        border-radius: 8px;
        border: 1px solid #333;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
        transition: transform 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: #ff6b00;
    }
    
    /* Status Indicators */
    .status-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 4px;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .status-active {
        background-color: #00ff88;
        color: #000;
    }
    
    .status-warning {
        background-color: #ffaa00;
        color: #000;
    }
    
    .status-error {
        background-color: #ff3366;
        color: #fff;
    }
    
    /* Data Tables */
    .dataframe {
        background-color: #1a1a1a !important;
        color: #e0e0e0 !important;
        border: 1px solid #333 !important;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background-color: #0f0f0f;
    }
    
    /* Port Info Cards */
    .port-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        padding: 1rem;
        border-radius: 6px;
        border-left: 3px solid #00ff88;
        margin: 0.5rem 0;
    }
    
    .port-name {
        color: #00ff88;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    .port-stat {
        color: #b0b0b0;
        font-size: 0.9rem;
    }
    
    /* Ticker Style */
    .ticker {
        background-color: #1a1a1a;
        padding: 0.5rem;
        border-radius: 4px;
        font-family: 'Courier New', monospace;
        color: #00ff88;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)


def create_sample_data():
    """Create comprehensive sample data for demonstration"""
    return {
        "workflows": [
            {"id": "wf-001", "status": "completed", "execution_time": 2.34, "timestamp": datetime.utcnow() - timedelta(minutes=5)},
            {"id": "wf-002", "status": "completed", "execution_time": 1.89, "timestamp": datetime.utcnow() - timedelta(minutes=3)},
            {"id": "wf-003", "status": "running", "execution_time": 0.0, "timestamp": datetime.utcnow()}
        ],
        "agents": [
            {"name": "Data Ingestion Agent", "status": "running", "executions": 156, "success_rate": 98.7},
            {"name": "Compliance Intelligence Agent", "status": "completed", "executions": 142, "success_rate": 99.3},
            {"name": "Regulatory Validation Agent", "status": "completed", "executions": 138, "success_rate": 97.8}
        ],
        "metrics": {
            "total_workflows": 156,
            "active_workflows": 3,
            "avg_execution_time": 2.1,
            "success_rate": 98.6
        },
        "ports": [
            {"name": "Port of Mombasa", "country": "Kenya", "containers": 12450, "change": 5.2, "status": "active"},
            {"name": "Port of Lagos", "country": "Nigeria", "containers": 8920, "change": -2.1, "status": "active"},
            {"name": "Port of Durban", "country": "South Africa", "containers": 15680, "change": 3.8, "status": "active"},
            {"name": "Port of Tema", "country": "Ghana", "containers": 6340, "change": 1.5, "status": "active"},
            {"name": "Port of Dar es Salaam", "country": "Tanzania", "containers": 5120, "change": 4.2, "status": "active"}
        ],
        "trade_volume": pd.DataFrame({
            'Date': pd.date_range(start=datetime.utcnow() - timedelta(days=30), end=datetime.utcnow(), freq='D'),
            'Volume': np.random.randint(8000, 15000, 31),
            'Value_USD': np.random.randint(50000000, 120000000, 31)
        }),
        "commodity_prices": {
            "Coffee": {"price": 245.50, "change": 2.3},
            "Cocoa": {"price": 3420.00, "change": -1.2},
            "Gold": {"price": 1950.25, "change": 0.8},
            "Oil": {"price": 82.40, "change": 1.5},
            "Cotton": {"price": 89.30, "change": -0.5}
        }
    }


def render_header():
    """Render Bloomberg-style header"""
    st.markdown("""
    <div class="bloomberg-header">
        <div class="main-title">🌍 TRADE INTELLIGENCE PLATFORM</div>
        <div class="subtitle">Real-time Cross-Border Trade Compliance & Risk Analysis | Powered by IBM watsonx.ai</div>
    </div>
    """, unsafe_allow_html=True)


def render_live_ticker(data: Dict[str, Any]):
    """Render live commodity ticker"""
    st.markdown("### 📊 Live Market Data")
    
    cols = st.columns(5)
    for idx, (commodity, info) in enumerate(data["commodity_prices"].items()):
        with cols[idx]:
            change_color = "#00ff88" if info["change"] >= 0 else "#ff3366"
            change_symbol = "▲" if info["change"] >= 0 else "▼"
            st.markdown(f"""
            <div class="ticker">
                <strong>{commodity}</strong><br/>
                ${info['price']:.2f}<br/>
                <span style="color: {change_color};">{change_symbol} {abs(info['change']):.1f}%</span>
            </div>
            """, unsafe_allow_html=True)


def render_key_metrics(data: Dict[str, Any]):
    """Render key performance metrics"""
    metrics = data["metrics"]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📦 Total Workflows",
            value=f"{metrics['total_workflows']:,}",
            delta="+12 today",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            label="⚡ Active Workflows",
            value=metrics["active_workflows"],
            delta="Running",
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            label="⏱️ Avg Execution Time",
            value=f"{metrics['avg_execution_time']:.2f}s",
            delta="-0.3s",
            delta_color="inverse"
        )
    
    with col4:
        st.metric(
            label="✅ Success Rate",
            value=f"{metrics['success_rate']:.1f}%",
            delta="+0.5%",
            delta_color="normal"
        )


def render_port_information(data: Dict[str, Any]):
    """Render port activity information"""
    st.markdown("### 🚢 Major Port Activity")
    
    cols = st.columns(5)
    for idx, port in enumerate(data["ports"]):
        with cols[idx]:
            change_color = "#00ff88" if port["change"] >= 0 else "#ff3366"
            change_symbol = "▲" if port["change"] >= 0 else "▼"
            st.markdown(f"""
            <div class="port-card">
                <div class="port-name">{port['name']}</div>
                <div class="port-stat">{port['country']}</div>
                <div class="port-stat"><strong>{port['containers']:,}</strong> TEUs</div>
                <div style="color: {change_color}; font-weight: 600;">
                    {change_symbol} {abs(port['change']):.1f}%
                </div>
            </div>
            """, unsafe_allow_html=True)


def render_trade_volume_chart(data: Dict[str, Any]):
    """Render trade volume over time"""
    st.markdown("### 📈 Trade Volume Trends (30 Days)")
    
    df = data["trade_volume"]
    
    fig = go.Figure()
    
    # Volume bars
    fig.add_trace(go.Bar(
        x=df['Date'],
        y=df['Volume'],
        name='Container Volume',
        marker_color='#00ff88',
        yaxis='y',
        opacity=0.7
    ))
    
    # Value line
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Value_USD'],
        name='Trade Value (USD)',
        line=dict(color='#ff6b00', width=3),
        yaxis='y2'
    ))
    
    fig.update_layout(
        plot_bgcolor='#0a0a0a',
        paper_bgcolor='#1a1a1a',
        font=dict(color='#e0e0e0'),
        height=400,
        hovermode='x unified',
        yaxis=dict(
            title='Container Volume (TEUs)',
            titlefont=dict(color='#00ff88'),
            tickfont=dict(color='#00ff88')
        ),
        yaxis2=dict(
            title='Trade Value (USD)',
            titlefont=dict(color='#ff6b00'),
            tickfont=dict(color='#ff6b00'),
            overlaying='y',
            side='right'
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor='#2d2d2d'
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_compliance_heatmap():
    """Render compliance framework heatmap"""
    st.markdown("### 🎯 Multi-Framework Compliance Matrix")
    
    frameworks = ['AfCFTA', 'WTO', 'USMCA', 'EU', 'ASEAN', 'GCC']
    categories = ['Tariffs', 'Documentation', 'Standards', 'Origin Rules', 'Quotas']
    
    # Generate sample compliance scores
    np.random.seed(42)
    scores = np.random.randint(85, 100, size=(len(categories), len(frameworks)))
    
    fig = go.Figure(data=go.Heatmap(
        z=scores,
        x=frameworks,
        y=categories,
        colorscale=[
            [0, '#ff3366'],
            [0.5, '#ffaa00'],
            [1, '#00ff88']
        ],
        text=scores,
        texttemplate='%{text}%',
        textfont={"size": 12, "color": "#000"},
        hovertemplate='Framework: %{x}<br>Category: %{y}<br>Compliance: %{z}%<extra></extra>'
    ))
    
    fig.update_layout(
        plot_bgcolor='#0a0a0a',
        paper_bgcolor='#1a1a1a',
        font=dict(color='#e0e0e0'),
        height=350,
        xaxis=dict(side='top')
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_risk_distribution():
    """Render risk level distribution"""
    st.markdown("### ⚠️ Risk Assessment Distribution")
    
    risk_data = pd.DataFrame({
        'Risk Level': ['Low', 'Medium', 'High', 'Critical'],
        'Count': [145, 78, 23, 4],
        'Color': ['#00ff88', '#ffaa00', '#ff6b00', '#ff3366']
    })
    
    fig = go.Figure(data=[go.Pie(
        labels=risk_data['Risk Level'],
        values=risk_data['Count'],
        hole=0.4,
        marker=dict(colors=risk_data['Color']),
        textinfo='label+percent',
        textfont=dict(size=14, color='#fff')
    )])
    
    fig.update_layout(
        plot_bgcolor='#0a0a0a',
        paper_bgcolor='#1a1a1a',
        font=dict(color='#e0e0e0'),
        height=350,
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_agent_performance():
    """Render agent performance metrics"""
    st.markdown("### 🤖 Agent Performance Analytics")
    
    agents = ['Data Ingestion', 'Compliance Intel', 'Risk Sentinel', 'Validation']
    metrics_data = {
        'Response Time (ms)': [120, 340, 280, 190],
        'Success Rate (%)': [98.7, 99.3, 97.8, 98.9],
        'Throughput (req/s)': [450, 320, 380, 410]
    }
    
    fig = go.Figure()
    
    colors = ['#00ff88', '#ff6b00', '#00d4ff']
    for idx, (metric, values) in enumerate(metrics_data.items()):
        fig.add_trace(go.Bar(
            name=metric,
            x=agents,
            y=values,
            marker_color=colors[idx],
            text=values,
            textposition='auto',
        ))
    
    fig.update_layout(
        plot_bgcolor='#0a0a0a',
        paper_bgcolor='#1a1a1a',
        font=dict(color='#e0e0e0'),
        height=350,
        barmode='group',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#2d2d2d'),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_execution_timeline(data: Dict[str, Any]):
    """Render workflow execution timeline"""
    st.markdown("### ⏰ Workflow Execution Timeline")
    
    workflows = data["workflows"]
    df = pd.DataFrame([
        {
            "Workflow": wf["id"],
            "Status": wf["status"],
            "Time": wf["timestamp"],
            "Duration": wf["execution_time"]
        }
        for wf in workflows
    ])
    
    fig = px.scatter(
        df,
        x="Time",
        y="Workflow",
        color="Status",
        size="Duration",
        hover_data=["Duration"],
        color_discrete_map={
            "completed": "#00ff88",
            "running": "#00d4ff",
            "failed": "#ff3366"
        }
    )
    
    fig.update_layout(
        plot_bgcolor='#0a0a0a',
        paper_bgcolor='#1a1a1a',
        font=dict(color='#e0e0e0'),
        height=300,
        showlegend=True,
        xaxis=dict(showgrid=True, gridcolor='#2d2d2d'),
        yaxis=dict(showgrid=True, gridcolor='#2d2d2d')
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_data_flow_sankey():
    """Render data flow visualization"""
    st.markdown("### 🔄 Data Flow Architecture")
    
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="#2d2d2d", width=0.5),
            label=["Bright Data API", "Data Ingestion", "Compliance Check", "Risk Analysis", 
                   "Validation", "Executive Dashboard", "Alert System"],
            color=["#ff6b00", "#00ff88", "#00d4ff", "#ffaa00", "#00ff88", "#ff6b00", "#ff3366"]
        ),
        link=dict(
            source=[0, 1, 1, 2, 2, 3, 4, 4],
            target=[1, 2, 3, 4, 5, 4, 5, 6],
            value=[100, 60, 40, 60, 30, 40, 70, 20],
            color=["rgba(255, 107, 0, 0.3)", "rgba(0, 255, 136, 0.3)", "rgba(0, 212, 255, 0.3)",
                   "rgba(255, 170, 0, 0.3)", "rgba(0, 255, 136, 0.3)", "rgba(255, 170, 0, 0.3)",
                   "rgba(0, 255, 136, 0.3)", "rgba(255, 51, 102, 0.3)"]
        )
    )])
    
    fig.update_layout(
        plot_bgcolor='#0a0a0a',
        paper_bgcolor='#1a1a1a',
        font=dict(size=12, color='#e0e0e0'),
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_system_health():
    """Render system health metrics"""
    st.markdown("### 🏥 System Health Monitor")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="🎯 Orchestrator",
            value="Healthy",
            delta="✅ Online",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            label="🤖 Agents",
            value="3/3 Active",
            delta="✅ All Running",
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            label="🔌 Bright Data API",
            value="Connected",
            delta="✅ 99.9% Uptime",
            delta_color="normal"
        )


def render_workflow_logs():
    """Render workflow execution logs"""
    st.markdown("### 📝 Real-time Execution Logs")
    
    logs = [
        {"time": "21:25:34", "level": "INFO", "agent": "Orchestrator", "message": "Workflow wf-003 initiated"},
        {"time": "21:25:35", "level": "INFO", "agent": "Data Ingestion", "message": "Processing 1,245 trade documents"},
        {"time": "21:25:36", "level": "INFO", "agent": "Compliance Intel", "message": "Multi-framework validation in progress"},
        {"time": "21:25:37", "level": "WARNING", "agent": "Risk Sentinel", "message": "High-risk transaction detected - flagged for review"},
        {"time": "21:25:38", "level": "SUCCESS", "agent": "Validation", "message": "Workflow wf-003 completed - 98.5% compliance"},
    ]
    
    log_df = pd.DataFrame(logs)
    
    def style_log_level(val):
        if val == "ERROR":
            return 'background-color: #ff3366; color: #fff'
        elif val == "SUCCESS":
            return 'background-color: #00ff88; color: #000'
        elif val == "WARNING":
            return 'background-color: #ffaa00; color: #000'
        elif val == "INFO":
            return 'background-color: #00d4ff; color: #000'
        return ''
    
    styled_df = log_df.style.map(style_log_level, subset=['level'])
    
    st.dataframe(styled_df, use_container_width=True, height=250)


def render_sidebar():
    """Render sidebar controls"""
    st.sidebar.markdown("## ⚙️ Control Panel")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🌐 Trade Framework")
    framework = st.sidebar.selectbox(
        "Select Framework",
        ["AfCFTA", "WTO", "USMCA", "EU Customs", "ASEAN", "GCC"],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("### 🔄 Execution Mode")
    workflow_type = st.sidebar.selectbox(
        "Select Mode",
        ["Sequential", "Parallel", "Conditional"],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("### 📊 Data Source")
    data_source = st.sidebar.selectbox(
        "Select Source",
        ["Trade Documents", "Border Ports", "Commodity Prices", "Shipment Data", "Customs Declarations"],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("### 🚢 Port Selection")
    port = st.sidebar.multiselect(
        "Select Ports",
        ["Port of Mombasa", "Port of Lagos", "Port of Durban", "Port of Tema", "Port of Dar es Salaam"],
        default=["Port of Mombasa"],
        label_visibility="collapsed"
    )
    
    if st.sidebar.button("🚀 Execute Workflow", type="primary", use_container_width=True):
        st.sidebar.success("✅ Workflow initiated successfully!")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📡 Auto-Refresh")
    auto_refresh = st.sidebar.checkbox("Enable (5s interval)", value=False)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.8rem;'>
        <strong>Trade Intelligence Platform v2.0.0</strong><br/>
        Powered by IBM watsonx.ai<br/>
        Built for IBM AI Builders Challenge
    </div>
    """, unsafe_allow_html=True)
    
    return auto_refresh


def main():
    """Main dashboard application"""
    
    # Render sidebar and get auto-refresh setting
    auto_refresh = render_sidebar()
    
    # Render header
    render_header()
    
    # Get sample data
    data = create_sample_data()
    
    # Live ticker
    render_live_ticker(data)
    
    st.markdown("---")
    
    # Key metrics
    render_key_metrics(data)
    
    st.markdown("---")
    
    # Port information
    render_port_information(data)
    
    st.markdown("---")
    
    # Trade volume chart
    render_trade_volume_chart(data)
    
    st.markdown("---")
    
    # Two column layout for charts
    col1, col2 = st.columns(2)
    
    with col1:
        render_compliance_heatmap()
    
    with col2:
        render_risk_distribution()
    
    st.markdown("---")
    
    # Agent performance and timeline
    col3, col4 = st.columns(2)
    
    with col3:
        render_agent_performance()
    
    with col4:
        render_execution_timeline(data)
    
    st.markdown("---")
    
    # Data flow visualization
    render_data_flow_sankey()
    
    st.markdown("---")
    
    # System health
    render_system_health()
    
    st.markdown("---")
    
    # Execution logs
    render_workflow_logs()
    
    # Auto-refresh logic
    if auto_refresh:
        import time
        time.sleep(5)
        st.rerun()


if __name__ == "__main__":
    main()

# Made with Bob
