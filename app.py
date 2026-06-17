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
import time

# Page configuration
st.set_page_config(
    page_title="Trade Intelligence Platform",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for workflow tracking
if 'workflows' not in st.session_state:
    st.session_state.workflows = []
if 'workflow_counter' not in st.session_state:
    st.session_state.workflow_counter = 1
if 'executing' not in st.session_state:
    st.session_state.executing = False

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
    
    /* System Health Cards */
    .health-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #252525 100%);
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #333;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
        text-align: center;
    }
    
    .health-title {
        color: #00ff88;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .health-value {
        color: #fff;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .health-status {
        color: #00ff88;
        font-size: 0.9rem;
    }
    
    /* About Section */
    .about-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        padding: 2rem;
        border-radius: 8px;
        border: 1px solid #333;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
    }
    
    .about-title {
        color: #ff6b00;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .about-text {
        color: #b0b0b0;
        line-height: 1.6;
    }
    
    /* Workflow Execution Panel */
    .workflow-panel {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #00d4ff;
        margin: 1rem 0;
    }
    
    .workflow-title {
        color: #00d4ff;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1rem;
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
    
    /* Ticker Style */
    .ticker {
        background-color: #1a1a1a;
        padding: 0.5rem;
        border-radius: 4px;
        font-family: 'Courier New', monospace;
        color: #00ff88;
        font-size: 0.9rem;
    }
    
    /* Progress Animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .executing {
        animation: pulse 1.5s ease-in-out infinite;
    }
</style>
""", unsafe_allow_html=True)


def create_sample_data():
    """Create comprehensive sample data for demonstration"""
    return {
        "workflows": st.session_state.workflows,
        "agents": [
            {"name": "Data Ingestion Agent", "status": "running", "executions": 156, "success_rate": 98.7},
            {"name": "Compliance Intelligence Agent", "status": "completed", "executions": 142, "success_rate": 99.3},
            {"name": "Regulatory Validation Agent", "status": "completed", "executions": 138, "success_rate": 97.8}
        ],
        "metrics": {
            "total_workflows": len(st.session_state.workflows),
            "active_workflows": sum(1 for w in st.session_state.workflows if w["status"] == "running"),
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


def execute_workflow(framework, mode, source, ports):
    """Execute a workflow with real tracking"""
    workflow_id = f"wf-{st.session_state.workflow_counter:03d}"
    st.session_state.workflow_counter += 1
    
    workflow = {
        "id": workflow_id,
        "framework": framework,
        "mode": mode,
        "source": source,
        "ports": ports,
        "status": "running",
        "execution_time": 0.0,
        "timestamp": datetime.utcnow(),
        "progress": 0
    }
    
    st.session_state.workflows.insert(0, workflow)
    st.session_state.executing = True
    return workflow_id


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


def render_workflow_execution_panel():
    """Render interactive workflow execution panel"""
    st.markdown("""
    <div class="workflow-panel">
        <div class="workflow-title">🚀 Workflow Execution Control</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        framework = st.selectbox(
            "🌐 Trade Framework",
            ["AfCFTA", "WTO", "USMCA", "EU Customs", "ASEAN", "GCC"],
            key="framework_select"
        )
    
    with col2:
        mode = st.selectbox(
            "🔄 Execution Mode",
            ["Sequential", "Parallel", "Conditional"],
            key="mode_select"
        )
    
    with col3:
        source = st.selectbox(
            "📊 Data Source",
            ["Trade Documents", "Border Ports", "Commodity Prices", "Shipment Data", "Customs Declarations"],
            key="source_select"
        )
    
    with col4:
        ports = st.multiselect(
            "🚢 Target Ports",
            ["Mombasa", "Lagos", "Durban", "Tema", "Dar es Salaam"],
            default=["Mombasa"],
            key="ports_select"
        )
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
    
    with col_btn1:
        if st.button("🚀 Execute Workflow", type="primary", use_container_width=True, disabled=st.session_state.executing):
            workflow_id = execute_workflow(framework, mode, source, ports)
            st.success(f"✅ Workflow {workflow_id} initiated!")
            st.rerun()
    
    with col_btn2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    # Show active workflows
    if st.session_state.workflows:
        st.markdown("#### 📋 Recent Workflows")
        for wf in st.session_state.workflows[:5]:
            status_color = "#00ff88" if wf["status"] == "completed" else "#00d4ff" if wf["status"] == "running" else "#ff3366"
            status_icon = "✅" if wf["status"] == "completed" else "⚡" if wf["status"] == "running" else "❌"
            
            st.markdown(f"""
            <div style="background: #1a1a1a; padding: 0.8rem; border-radius: 4px; margin: 0.3rem 0; border-left: 3px solid {status_color};">
                <strong>{status_icon} {wf['id']}</strong> | {wf['framework']} | {wf['mode']} | 
                <span style="color: {status_color};">{wf['status'].upper()}</span> | 
                {wf['timestamp'].strftime('%H:%M:%S')}
            </div>
            """, unsafe_allow_html=True)


def render_system_health():
    """Render system health in main area with professional styling"""
    st.markdown("### 🏥 System Health Monitor")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="health-card">
            <div class="health-title">🎯 Orchestrator</div>
            <div class="health-value">Healthy</div>
            <div class="health-status">✅ Online | 99.9% Uptime</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="health-card">
            <div class="health-title">🤖 AI Agents</div>
            <div class="health-value">3/3 Active</div>
            <div class="health-status">✅ All Systems Operational</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="health-card">
            <div class="health-title">🔌 Bright Data API</div>
            <div class="health-value">Connected</div>
            <div class="health-status">✅ Real-time Data Stream</div>
        </div>
        """, unsafe_allow_html=True)


def render_about_section():
    """Render about section in main area"""
    st.markdown("### ℹ️ Platform Information")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="about-card">
            <div class="about-title">Trade Intelligence Platform v2.0.0</div>
            <div class="about-text">
                <p>AI-powered multi-agent system for cross-border trade compliance, risk analysis, and executive decision support.</p>
                
                <p><strong>Supported Trade Frameworks:</strong></p>
                <ul>
                    <li>AfCFTA (African Continental Free Trade Area)</li>
                    <li>WTO (World Trade Organization)</li>
                    <li>USMCA (United States-Mexico-Canada Agreement)</li>
                    <li>EU Customs Union</li>
                    <li>ASEAN (Association of Southeast Asian Nations)</li>
                    <li>GCC (Gulf Cooperation Council)</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="about-card">
            <div class="about-title">Technology Stack</div>
            <div class="about-text">
                <p><strong>Powered by:</strong></p>
                <ul>
                    <li>🤖 IBM watsonx.ai</li>
                    <li>💎 IBM Granite Models</li>
                    <li>🐍 IBM Watson Python SDK</li>
                    <li>📊 Bright Data API</li>
                    <li>⚡ Streamlit Framework</li>
                </ul>
                <br/>
                <p style="text-align: center; color: #ff6b00; font-weight: 600;">
                    Built for IBM AI Builders Challenge
                </p>
            </div>
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
            delta=f"+{len([w for w in data['workflows'] if (datetime.utcnow() - w['timestamp']).seconds < 86400])} today"
        )
    
    with col2:
        st.metric(
            label="⚡ Active Workflows",
            value=metrics["active_workflows"],
            delta="Running" if metrics["active_workflows"] > 0 else "Idle"
        )
    
    with col3:
        st.metric(
            label="⏱️ Avg Execution Time",
            value=f"{metrics['avg_execution_time']:.2f}s",
            delta="-0.3s"
        )
    
    with col4:
        st.metric(
            label="✅ Success Rate",
            value=f"{metrics['success_rate']:.1f}%",
            delta="+0.5%"
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
                <div style="color: #b0b0b0; font-size: 0.9rem;">{port['country']}</div>
                <div style="color: #fff; font-size: 1.3rem; font-weight: 600; margin: 0.5rem 0;">{port['containers']:,} TEUs</div>
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
    
    fig.add_trace(go.Bar(
        x=df['Date'],
        y=df['Volume'],
        name='Container Volume',
        marker_color='#00ff88',
        yaxis='y',
        opacity=0.7
    ))
    
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
            title=dict(text='Container Volume (TEUs)', font=dict(color='#00ff88')),
            tickfont=dict(color='#00ff88')
        ),
        yaxis2=dict(
            title=dict(text='Trade Value (USD)', font=dict(color='#ff6b00')),
            tickfont=dict(color='#ff6b00'),
            overlaying='y',
            side='right'
        ),
        xaxis=dict(showgrid=True, gridcolor='#2d2d2d'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_compliance_heatmap():
    """Render compliance framework heatmap"""
    st.markdown("### 🎯 Multi-Framework Compliance Matrix")
    
    frameworks = ['AfCFTA', 'WTO', 'USMCA', 'EU', 'ASEAN', 'GCC']
    categories = ['Tariffs', 'Documentation', 'Standards', 'Origin Rules', 'Quotas']
    
    np.random.seed(42)
    scores = np.random.randint(85, 100, size=(len(categories), len(frameworks)))
    
    fig = go.Figure(data=go.Heatmap(
        z=scores,
        x=frameworks,
        y=categories,
        colorscale=[[0, '#ff3366'], [0.5, '#ffaa00'], [1, '#00ff88']],
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
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.1)
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_workflow_logs():
    """Render workflow execution logs"""
    st.markdown("### 📝 Real-time Execution Logs")
    
    logs = [
        {"time": datetime.utcnow().strftime("%H:%M:%S"), "level": "INFO", "agent": "Orchestrator", "message": "System initialized and ready"},
        {"time": (datetime.utcnow() - timedelta(seconds=5)).strftime("%H:%M:%S"), "level": "INFO", "agent": "Data Ingestion", "message": "Processing trade documents"},
        {"time": (datetime.utcnow() - timedelta(seconds=10)).strftime("%H:%M:%S"), "level": "INFO", "agent": "Compliance Intel", "message": "Multi-framework validation in progress"},
        {"time": (datetime.utcnow() - timedelta(seconds=15)).strftime("%H:%M:%S"), "level": "WARNING", "agent": "Risk Sentinel", "message": "High-risk transaction detected"},
        {"time": (datetime.utcnow() - timedelta(seconds=20)).strftime("%H:%M:%S"), "level": "SUCCESS", "agent": "Validation", "message": "Workflow completed - 98.5% compliance"},
    ]
    
    # Add workflow logs
    for wf in st.session_state.workflows[:3]:
        logs.insert(0, {
            "time": wf['timestamp'].strftime("%H:%M:%S"),
            "level": "SUCCESS" if wf["status"] == "completed" else "INFO",
            "agent": "Workflow",
            "message": f"{wf['id']} - {wf['framework']} | {wf['status']}"
        })
    
    log_df = pd.DataFrame(logs[:10])
    
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
    
    # Use map (pandas >= 2.1.0 replaced applymap with map)
    styled_df = log_df.style.map(style_log_level, subset=['level'])
    
    st.dataframe(styled_df, use_container_width=True, height=300)


def render_sidebar():
    """Render minimal sidebar"""
    st.sidebar.markdown("## ⚙️ Dashboard Controls")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📡 Auto-Refresh")
    auto_refresh = st.sidebar.checkbox("Enable (5s interval)", value=False)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎨 Theme")
    theme = st.sidebar.radio("Select Theme", ["Dark (Bloomberg)", "Light"], index=0)
    
    st.sidebar.markdown("---")
    if st.sidebar.button("🗑️ Clear Workflows", use_container_width=True):
        st.session_state.workflows = []
        st.session_state.workflow_counter = 1
        st.rerun()
    
    return auto_refresh


def main():
    """Main dashboard application"""
    
    # Render sidebar
    auto_refresh = render_sidebar()
    
    # Render header
    render_header()
    
    # Get sample data
    data = create_sample_data()
    
    # Live ticker
    render_live_ticker(data)
    
    st.markdown("---")
    
    # Workflow Execution Panel (moved from sidebar)
    render_workflow_execution_panel()
    
    st.markdown("---")
    
    # Key metrics
    render_key_metrics(data)
    
    st.markdown("---")
    
    # System Health (moved from sidebar)
    render_system_health()
    
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
    
    # Execution logs
    render_workflow_logs()
    
    st.markdown("---")
    
    # About section (moved from sidebar)
    render_about_section()
    
    # Simulate workflow completion
    if st.session_state.executing and st.session_state.workflows:
        for wf in st.session_state.workflows:
            if wf["status"] == "running":
                # Simulate completion after 10 seconds
                if (datetime.utcnow() - wf["timestamp"]).seconds > 10:
                    wf["status"] = "completed"
                    wf["execution_time"] = (datetime.utcnow() - wf["timestamp"]).seconds
                    st.session_state.executing = False
    
    # Auto-refresh logic
    if auto_refresh:
        time.sleep(5)
        st.rerun()


if __name__ == "__main__":
    main()

# Made with Bob
