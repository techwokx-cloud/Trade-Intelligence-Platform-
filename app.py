"""
Trade Intelligence Platform - Streamlit Dashboard
Executive UI for monitoring multi-agent AI system execution
Supports multiple international trade frameworks
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
import asyncio
from typing import Dict, Any, List

# Page configuration
st.set_page_config(
    page_title="Trade Intelligence Platform",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #0f62fe;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f4f4f4;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #0f62fe;
    }
    .agent-status {
        padding: 0.5rem;
        border-radius: 0.25rem;
        margin: 0.5rem 0;
    }
    .status-running {
        background-color: #d0e2ff;
        border-left: 4px solid #0f62fe;
    }
    .status-completed {
        background-color: #defbe6;
        border-left: 4px solid #24a148;
    }
    .status-failed {
        background-color: #ffd7d9;
        border-left: 4px solid #da1e28;
    }
</style>
""", unsafe_allow_html=True)


def create_sample_data():
    """Create sample data for demonstration"""
    return {
        "workflows": [
            {
                "id": "wf-001",
                "status": "completed",
                "execution_time": 2.34,
                "timestamp": datetime.utcnow() - timedelta(minutes=5)
            },
            {
                "id": "wf-002",
                "status": "completed",
                "execution_time": 1.89,
                "timestamp": datetime.utcnow() - timedelta(minutes=3)
            },
            {
                "id": "wf-003",
                "status": "running",
                "execution_time": 0.0,
                "timestamp": datetime.utcnow()
            }
        ],
        "agents": [
            {
                "name": "Data Ingestion Agent",
                "status": "running",
                "executions": 156,
                "success_rate": 98.7
            },
            {
                "name": "Compliance Intelligence Agent",
                "status": "completed",
                "executions": 142,
                "success_rate": 99.3
            },
            {
                "name": "Regulatory Validation Agent",
                "status": "completed",
                "executions": 138,
                "success_rate": 97.8
            }
        ],
        "metrics": {
            "total_workflows": 156,
            "active_workflows": 3,
            "avg_execution_time": 2.1,
            "success_rate": 98.6
        }
    }


def render_header():
    """Render dashboard header"""
    st.markdown('<div class="main-header">🌍 Trade Intelligence Platform</div>',
                unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666; font-size: 1.1rem;">AI-Powered Cross-Border Trade Compliance & Risk Analysis</p>',
                unsafe_allow_html=True)
    st.markdown("---")


def render_metrics(data: Dict[str, Any]):
    """Render key metrics"""
    metrics = data["metrics"]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Workflows",
            value=metrics["total_workflows"],
            delta="+12 today"
        )
    
    with col2:
        st.metric(
            label="Active Workflows",
            value=metrics["active_workflows"],
            delta="Running"
        )
    
    with col3:
        st.metric(
            label="Avg Execution Time",
            value=f"{metrics['avg_execution_time']:.2f}s",
            delta="-0.3s"
        )
    
    with col4:
        st.metric(
            label="Success Rate",
            value=f"{metrics['success_rate']:.1f}%",
            delta="+0.5%"
        )


def render_agent_status(data: Dict[str, Any]):
    """Render agent status cards"""
    st.subheader("🤖 Agent Status")
    
    cols = st.columns(3)
    
    for idx, agent in enumerate(data["agents"]):
        with cols[idx]:
            status_class = f"status-{agent['status']}"
            
            st.markdown(f"""
            <div class="agent-status {status_class}">
                <h4>{agent['name']}</h4>
                <p><strong>Status:</strong> {agent['status'].upper()}</p>
                <p><strong>Executions:</strong> {agent['executions']}</p>
                <p><strong>Success Rate:</strong> {agent['success_rate']:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)


def render_execution_timeline(data: Dict[str, Any]):
    """Render execution timeline chart"""
    st.subheader("📊 Execution Timeline")
    
    workflows = data["workflows"]
    
    # Create timeline data
    df = pd.DataFrame([
        {
            "Workflow": wf["id"],
            "Status": wf["status"],
            "Time": wf["timestamp"],
            "Duration": wf["execution_time"]
        }
        for wf in workflows
    ])
    
    # Create timeline chart
    fig = px.scatter(
        df,
        x="Time",
        y="Workflow",
        color="Status",
        size="Duration",
        hover_data=["Duration"],
        color_discrete_map={
            "completed": "#24a148",
            "running": "#0f62fe",
            "failed": "#da1e28"
        }
    )
    
    fig.update_layout(
        height=300,
        showlegend=True,
        xaxis_title="Timestamp",
        yaxis_title="Workflow ID"
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_performance_chart():
    """Render performance metrics chart"""
    st.subheader("⚡ Performance Metrics")
    
    # Sample performance data
    times = pd.date_range(start=datetime.utcnow() - timedelta(hours=1), 
                          end=datetime.utcnow(), 
                          freq='5min')
    
    df = pd.DataFrame({
        'Time': times,
        'Execution Time (s)': [2.1, 1.9, 2.3, 2.0, 1.8, 2.2, 2.1, 1.9, 2.0, 2.1, 1.8, 2.0, 2.1],
        'Success Rate (%)': [98, 99, 97, 98, 99, 98, 99, 98, 99, 98, 99, 98, 99]
    })
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['Time'],
        y=df['Execution Time (s)'],
        name='Execution Time',
        line=dict(color='#0f62fe', width=2)
    ))
    
    fig.update_layout(
        height=300,
        xaxis_title="Time",
        yaxis_title="Execution Time (seconds)",
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_workflow_logs():
    """Render workflow execution logs"""
    st.subheader("📝 Execution Logs")
    
    logs = [
        {"time": "21:25:34", "level": "INFO", "message": "Workflow wf-003 started"},
        {"time": "21:25:35", "level": "INFO", "message": "Data Ingestion Agent processing trade documents"},
        {"time": "21:25:36", "level": "INFO", "message": "Compliance Intelligence Agent checking multi-framework compliance"},
        {"time": "21:25:37", "level": "INFO", "message": "Regulatory Validation Agent assessing transaction risk"},
        {"time": "21:25:38", "level": "SUCCESS", "message": "Workflow wf-003 completed successfully"},
    ]
    
    log_df = pd.DataFrame(logs)
    
    # Style logs based on level
    def style_log_level(val):
        if val == "ERROR":
            return 'background-color: #ffd7d9'
        elif val == "SUCCESS":
            return 'background-color: #defbe6'
        elif val == "WARNING":
            return 'background-color: #fff1d0'
        return ''
    
    # Use map (pandas >= 2.1.0 replaced applymap with map)
    styled_df = log_df.style.map(style_log_level, subset=['level'])
    
    st.dataframe(styled_df, use_container_width=True, height=200)


def render_system_health():
    """Render system health metrics in main area"""
    st.subheader("🏥 System Health")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Orchestrator",
            value="Healthy",
            delta="✅ Online"
        )
    
    with col2:
        st.metric(
            label="Agents",
            value="3/3 Active",
            delta="✅ All Running"
        )
    
    with col3:
        st.metric(
            label="Bright Data",
            value="Connected",
            delta="✅ API Ready"
        )


def render_about():
    """Render about section in main area"""
    st.subheader("ℹ️ About")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **Trade Intelligence Platform v2.0.0**
        
        AI-powered multi-agent system for cross-border trade compliance, risk analysis, and executive decision support.
        
        **Supported Frameworks:**
        - AfCFTA, WTO, USMCA, EU, ASEAN, GCC
        """)
    
    with col2:
        st.markdown("""
        **Powered by:**
        - IBM watsonx.ai
        - IBM Granite Models
        - IBM Watson Python SDK
        
        **Built for IBM AI Builders Challenge**
        """)


def render_sidebar():
    """Render sidebar controls"""
    st.sidebar.title("⚙️ Controls")
    
    st.sidebar.subheader("Workflow Execution")
    
    framework = st.sidebar.selectbox(
        "Trade Framework",
        ["AfCFTA", "WTO", "USMCA", "EU Customs", "ASEAN", "GCC"]
    )
    
    workflow_type = st.sidebar.selectbox(
        "Execution Mode",
        ["Sequential", "Parallel", "Conditional"]
    )
    
    data_source = st.sidebar.selectbox(
        "Data Source",
        ["Trade Documents", "Border Ports", "Commodity Prices", "Shipment Data"]
    )
    
    if st.sidebar.button("🚀 Execute Workflow", type="primary"):
        st.sidebar.success("Workflow initiated!")


def main():
    """Main dashboard application"""
    
    # Render sidebar
    render_sidebar()
    
    # Render header
    render_header()
    
    # Get sample data
    data = create_sample_data()
    
    # Render metrics
    render_metrics(data)
    
    st.markdown("---")
    
    # Render system health
    render_system_health()
    
    st.markdown("---")
    
    # Render agent status
    render_agent_status(data)
    
    st.markdown("---")
    
    # Create two columns for charts
    col1, col2 = st.columns(2)
    
    with col1:
        render_execution_timeline(data)
    
    with col2:
        render_performance_chart()
    
    st.markdown("---")
    
    # Render logs
    render_workflow_logs()
    
    st.markdown("---")
    
    # Render about section
    render_about()
    
    # Auto-refresh
    st.sidebar.markdown("---")
    auto_refresh = st.sidebar.checkbox("Auto-refresh (5s)", value=False)
    
    if auto_refresh:
        import time
        time.sleep(5)
        st.rerun()


if __name__ == "__main__":
    main()

# Made with Bob