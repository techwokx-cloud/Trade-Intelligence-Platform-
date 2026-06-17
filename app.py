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
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'uploaded_documents' not in st.session_state:
    st.session_state.uploaded_documents = []

# Bloomberg-style Custom CSS
st.markdown("""
<style>
    /* Bloomberg Dark Theme */
    .main {
        background-color: #0a0a0a;
        color: #e0e0e0;
    }
    .stApp {
        background-color: #0a0a0a;
        color: #e0e0e0;
    }
    
    /* Global Text Colors */
    body, p, span, div, label, input, textarea, select {
        color: #e0e0e0 !important;
    }
    
    /* Streamlit Native Elements */
    .stMarkdown, .stMarkdown p, .stMarkdown span {
        color: #e0e0e0 !important;
    }
    
    .stText, .stTextInput label, .stSelectbox label, .stMultiSelect label {
        color: #e0e0e0 !important;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    /* Metric Labels */
    .stMetric label {
        color: #b0b0b0 !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #ffffff !important;
    }
    
    .stMetric [data-testid="stMetricDelta"] {
        color: #00ff88 !important;
    }
    
    /* Buttons */
    .stButton button {
        color: #ffffff !important;
        background-color: #0f62fe;
        border: none;
    }
    
    .stButton button:hover {
        background-color: #0353e9;
    }
    
    /* File Uploader */
    .stFileUploader label {
        color: #e0e0e0 !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        color: #e0e0e0 !important;
        background-color: #1a1a1a;
    }
    
    .streamlit-expanderContent {
        background-color: #1a1a1a;
        color: #e0e0e0 !important;
    }
    
    /* Dataframe */
    .stDataFrame {
        color: #e0e0e0 !important;
    }
    
    /* Info/Warning/Error boxes */
    .stAlert {
        color: #000000 !important;
    }
    
    /* Sidebar */
    .css-1d391kg, [data-testid="stSidebar"] {
        background-color: #0f0f0f;
        color: #e0e0e0 !important;
    }
    
    [data-testid="stSidebar"] label {
        color: #e0e0e0 !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #e0e0e0 !important;
    }
    
    /* Tooltips and Help Text */
    .stTooltipIcon {
        color: #00d4ff !important;
    }
    
    [data-testid="stTooltipHoverTarget"] {
        color: #e0e0e0 !important;
    }
    
    .stTooltipContent {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
        border: 1px solid #00d4ff;
    }
    
    /* Dropdown and Select Options */
    .stSelectbox div[data-baseweb="select"] {
        background-color: #1a1a1a !important;
    }
    
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #1a1a1a !important;
        color: #e0e0e0 !important;
    }
    
    [data-baseweb="popover"] {
        background-color: #1a1a1a !important;
    }
    
    [role="option"] {
        background-color: #1a1a1a !important;
        color: #e0e0e0 !important;
    }
    
    [role="option"]:hover {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
    }
    
    [aria-selected="true"] {
        background-color: #0f62fe !important;
        color: #ffffff !important;
    }
    
    /* Multi-select */
    .stMultiSelect div[data-baseweb="select"] {
        background-color: #1a1a1a !important;
    }
    
    .stMultiSelect span {
        color: #e0e0e0 !important;
    }
    
    [data-baseweb="tag"] {
        background-color: #0f62fe !important;
        color: #ffffff !important;
    }
    
    /* File Uploader Text */
    .stFileUploader section {
        color: #e0e0e0 !important;
    }
    
    .stFileUploader small {
        color: #e0e0e0 !important;
    }
    
    .stFileUploader [data-testid="stFileUploaderDropzoneInstructions"] {
        color: #e0e0e0 !important;
    }
    
    .stFileUploader [data-testid="stFileUploaderDropzoneInstructions"] small {
        color: #e0e0e0 !important;
    }
    
    .stFileUploader div {
        color: #e0e0e0 !important;
    }
    
    .stFileUploader span {
        color: #e0e0e0 !important;
    }
    
    /* Button Help Text */
    button[title] {
        color: #ffffff !important;
    }
    
    /* Expander Header */
    [data-testid="stExpander"] summary {
        background-color: #1a1a1a !important;
        color: #e0e0e0 !important;
    }
    
    [data-testid="stExpander"] summary:hover {
        background-color: #2d2d2d !important;
    }
    
    /* Text in expander */
    [data-testid="stExpander"] div {
        color: #e0e0e0 !important;
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
    
    .port-card * {
        color: #e0e0e0 !important;
    }
    
    .port-name {
        color: #00ff88 !important;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    .port-stat {
        color: #b0b0b0 !important;
        font-size: 0.9rem;
    }
    
    /* Ticker Style */
    .ticker {
        background-color: #1a1a1a;
        padding: 0.5rem;
        border-radius: 4px;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
    }
    
    .ticker strong {
        color: #ffffff !important;
    }
    
    .ticker * {
        color: #e0e0e0 !important;
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
    
    # Commodity icons mapping
    commodity_icons = {
        "Coffee": "☕",
        "Cocoa": "🍫",
        "Gold": "🥇",
        "Oil": "🛢️",
        "Cotton": "🧵"
    }
    
    cols = st.columns(5)
    for idx, (commodity, info) in enumerate(data["commodity_prices"].items()):
        with cols[idx]:
            # Get commodity icon
            icon = commodity_icons.get(commodity, "📦")
            
            # Determine color based on change direction
            if info["change"] >= 0:
                change_color = "#00ff88"  # Green for positive
                change_symbol = "▲"
            else:
                change_color = "#ff3366"  # Red for negative
                change_symbol = "▼"
            
            st.markdown(f"""
            <div class="ticker">
                <strong>{icon} {commodity}</strong><br/>
                ${info['price']:.2f}<br/>
                <span style="color: {change_color};">{change_symbol} {abs(info['change']):.1f}%</span>
            </div>
            """, unsafe_allow_html=True)


def render_user_role_selection():
    """Render user role selection"""
    st.markdown("### 👤 User Profile")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        role = st.selectbox(
            "Select Your Role",
            ["Importer", "Exporter", "Government Agency", "Customs Broker", "Freight Forwarder"],
            index=0 if st.session_state.user_role is None else ["Importer", "Exporter", "Government Agency", "Customs Broker", "Freight Forwarder"].index(st.session_state.user_role) if st.session_state.user_role in ["Importer", "Exporter", "Government Agency", "Customs Broker", "Freight Forwarder"] else 0,
            key="user_role_select"
        )
        
        if role != st.session_state.user_role:
            st.session_state.user_role = role
            st.rerun()
    
    with col2:
        role_descriptions = {
            "Importer": "📥 Verify import documentation, check compliance, calculate duties",
            "Exporter": "📤 Validate export permits, ensure origin compliance, track shipments",
            "Government Agency": "🏛️ Monitor trade flows, enforce regulations, audit declarations",
            "Customs Broker": "🤝 Process customs clearance, file declarations, advise clients",
            "Freight Forwarder": "🚚 Coordinate logistics, manage documentation, track cargo"
        }
        st.info(f"**{role}:** {role_descriptions[role]}")


def render_document_upload():
    """Render document upload section"""
    st.markdown("### 📄 Document Verification Center")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("**Upload Trade Documents for AI-Powered Verification**")
        
        uploaded_files = st.file_uploader(
            "Choose files",
            type=['pdf', 'jpg', 'jpeg', 'png', 'xlsx', 'csv', 'docx'],
            accept_multiple_files=True,
            help="Supported: Commercial Invoice, Bill of Lading, Packing List, Certificate of Origin, Import/Export License",
            label_visibility="collapsed"
        )
        
        if uploaded_files:
            for file in uploaded_files:
                if file not in [doc['file'] for doc in st.session_state.uploaded_documents]:
                    # Simulate document analysis
                    file_bytes = file.read()
                    is_blank = len(file_bytes) < 1000  # Simple check for blank/small files
                    
                    doc_info = {
                        'file': file,
                        'name': file.name,
                        'size': file.size,
                        'type': file.type,
                        'uploaded_at': datetime.utcnow(),
                        'status': 'uploaded',
                        'verification_score': None,
                        'verification_stage': None,
                        'progress': 0,
                        'is_blank': is_blank,
                        'analysis': None,
                        'issues': [],
                        'extracted_fields': {}
                    }
                    st.session_state.uploaded_documents.append(doc_info)
                    
                    # Reset file pointer
                    file.seek(0)
            
            st.success(f"✅ {len(uploaded_files)} document(s) uploaded successfully!")
    
    with col2:
        st.markdown("**Document Types:**")
        st.markdown("""
        - 📋 Commercial Invoice
        - 🚢 Bill of Lading
        - 📦 Packing List
        - 🎫 Certificate of Origin
        - 📜 Import/Export License
        - 🛃 Customs Declaration
        """)
    
    # Display uploaded documents
    if st.session_state.uploaded_documents:
        st.markdown("---")
        st.markdown("#### 📚 Uploaded Documents")
        
        for idx, doc in enumerate(st.session_state.uploaded_documents):
            # Document header
            col_header1, col_header2, col_header3 = st.columns([4, 2, 1])
            
            with col_header1:
                st.markdown(f"<span style='color: #ffffff; font-size: 1.1rem; font-weight: 600;'>📄 {doc['name']}</span>", unsafe_allow_html=True)
            
            with col_header2:
                size_kb = doc['size'] / 1024
                st.markdown(f"<span style='color: #b0b0b0; font-size: 0.95rem;'>📦 {size_kb:.1f} KB</span>", unsafe_allow_html=True)
            
            with col_header3:
                if st.button("🗑️", key=f"delete_{idx}", help="Delete document"):
                    st.session_state.uploaded_documents.pop(idx)
                    st.rerun()
            
            # Verification section
            if doc['status'] == 'uploaded':
                if st.button(f"🔍 Start Verification", key=f"verify_{idx}", type="primary", use_container_width=True):
                    doc['status'] = 'verifying'
                    doc['progress'] = 0
                    doc['verification_stage'] = 'Initializing...'
                    st.rerun()
            
            elif doc['status'] == 'verifying':
                # Progressive verification stages
                stages = [
                    (20, "📤 Uploading to AI engine..."),
                    (40, "🔍 Extracting document data..."),
                    (60, "🎯 Checking compliance rules..."),
                    (80, "⚖️ Validating against framework..."),
                    (100, "✅ Generating compliance report...")
                ]
                
                current_progress = doc['progress']
                
                # Find current stage
                for progress, stage_text in stages:
                    if current_progress < progress:
                        doc['verification_stage'] = stage_text
                        doc['progress'] = min(current_progress + 20, progress)
                        break
                
                # Display progress
                st.markdown(f"<div style='color: #00d4ff; font-size: 0.9rem; margin: 0.5rem 0;'>{doc['verification_stage']}</div>", unsafe_allow_html=True)
                progress_bar = st.progress(doc['progress'] / 100)
                st.markdown(f"<div style='text-align: right; color: #b0b0b0; font-size: 0.85rem;'>{doc['progress']}% Complete</div>", unsafe_allow_html=True)
                
                # Complete verification
                if doc['progress'] >= 100:
                    time.sleep(0.5)  # Brief pause before showing result
                    doc['status'] = 'verified'
                    
                    # Simulate document analysis
                    if doc['is_blank']:
                        doc['verification_score'] = np.random.randint(0, 30)
                        doc['issues'] = [
                            "❌ Document appears to be blank or incomplete",
                            "❌ No readable content detected",
                            "❌ Missing required fields"
                        ]
                        doc['extracted_fields'] = {}
                        doc['analysis'] = "Document is blank or contains insufficient data for verification."
                    else:
                        doc['verification_score'] = np.random.randint(75, 100)
                        # Simulate extracted fields
                        doc['extracted_fields'] = {
                            'Document Type': 'Commercial Invoice',
                            'Invoice Number': f'INV-{np.random.randint(1000, 9999)}',
                            'Date': datetime.utcnow().strftime('%Y-%m-%d'),
                            'Exporter': 'ABC Trading Co.',
                            'Importer': 'XYZ Imports Ltd.',
                            'Total Value': f'${np.random.randint(10000, 99999):,}',
                            'Currency': 'USD',
                            'HS Code': f'{np.random.randint(1000, 9999)}.{np.random.randint(10, 99)}',
                            'Country of Origin': np.random.choice(['Kenya', 'Ghana', 'Nigeria', 'South Africa'])
                        }
                        
                        # Simulate issues based on score
                        if doc['verification_score'] < 90:
                            doc['issues'] = [
                                "⚠️ HS code classification needs verification",
                                "⚠️ Certificate of origin not attached",
                                "ℹ️ Consider adding insurance details"
                            ]
                        else:
                            doc['issues'] = [
                                "✅ All required fields present",
                                "✅ Document format compliant",
                                "✅ Data validation passed"
                            ]
                        
                        doc['analysis'] = f"Document successfully analyzed. {len(doc['extracted_fields'])} fields extracted."
                    
                    doc['verification_stage'] = 'Completed'
                    st.rerun()
                else:
                    time.sleep(0.8)  # Simulate processing time
                    st.rerun()
            
            elif doc['status'] == 'verified':
                score = doc['verification_score']
                
                # Color coding based on score
                if score >= 90:
                    color = "#00ff88"
                    status_icon = "✅"
                    status_text = "Excellent"
                elif score >= 75:
                    color = "#ffaa00"
                    status_icon = "⚠️"
                    status_text = "Good"
                else:
                    color = "#ff3366"
                    status_icon = "❌"
                    status_text = "Needs Review"
                
                # Display result summary
                col_result1, col_result2 = st.columns([3, 1])
                
                with col_result1:
                    analysis_text = doc.get('analysis', 'Verified against trade regulations')
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
                                padding: 1rem; border-radius: 6px; border-left: 4px solid {color};'>
                        <div style='color: {color}; font-size: 1.2rem; font-weight: 600;'>
                            {status_icon} {score}% Compliant - {status_text}
                        </div>
                        <div style='color: #b0b0b0; font-size: 0.85rem; margin-top: 0.3rem;'>
                            {analysis_text}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_result2:
                    if st.button("🔄 Re-verify", key=f"reverify_{idx}"):
                        doc['status'] = 'uploaded'
                        doc['progress'] = 0
                        doc['verification_score'] = None
                        doc['analysis'] = None
                        doc['issues'] = []
                        doc['extracted_fields'] = {}
                        st.rerun()
                
                # Detailed analysis in expander
                with st.expander("📋 View Detailed Analysis", expanded=False):
                    # Check for blank document (with safety check)
                    if doc.get('is_blank', False):
                        st.error("⚠️ **Blank Document Detected**")
                        st.markdown("""
                        This document appears to be blank or contains insufficient data. Please ensure:
                        - The document is not empty
                        - The file is not corrupted
                        - All required fields are filled
                        - The document is in a readable format
                        """)
                    
                    # Extracted Fields (with safety check)
                    extracted_fields = doc.get('extracted_fields', {})
                    if extracted_fields:
                        st.markdown("### 📊 Extracted Information")
                        
                        col_field1, col_field2 = st.columns(2)
                        
                        fields_list = list(extracted_fields.items())
                        mid_point = len(fields_list) // 2
                        
                        with col_field1:
                            for key, value in fields_list[:mid_point]:
                                st.markdown(f"**{key}:** {value}")
                        
                        with col_field2:
                            for key, value in fields_list[mid_point:]:
                                st.markdown(f"**{key}:** {value}")
                    
                    # Issues and Recommendations (with safety check)
                    issues = doc.get('issues', [])
                    if issues:
                        st.markdown("### 🔍 Findings & Recommendations")
                        for issue in issues:
                            if "❌" in issue:
                                st.error(issue)
                            elif "⚠️" in issue:
                                st.warning(issue)
                            elif "ℹ️" in issue:
                                st.info(issue)
                            else:
                                st.success(issue)
                    
                    # Compliance Details
                    st.markdown("### ⚖️ Compliance Check")
                    st.markdown(f"**Framework:** {st.session_state.user_role or 'General Trade'} Regulations")
                    st.markdown(f"**Verification Date:** {doc['uploaded_at'].strftime('%Y-%m-%d %H:%M:%S')} UTC")
                    st.markdown(f"**Document Size:** {doc['size'] / 1024:.1f} KB")
                    st.markdown(f"**File Type:** {doc['type']}")
            
            st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)


def render_workflow_execution_panel():
    """Render interactive workflow execution panel"""
    st.markdown("""
    <div class="workflow-panel">
        <div class="workflow-title">🚀 Workflow Execution Control</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Add help/info section
    with st.expander("ℹ️ What is a Workflow? (Click to learn more)", expanded=False):
        st.markdown("""
        <div style='color: #e0e0e0; line-height: 1.8;'>
        
        ### 📖 Understanding Workflows
        
        A **Workflow** is an automated process that analyzes trade documents and transactions using AI agents.
        Think of it as a digital assistant that checks your trade compliance automatically.
        
        ### 🔍 Workflow Components Explained:
        
        **1. Workflow ID (e.g., wf-001, wf-002)**
        - **What it is:** A unique identifier for each analysis task
        - **Why it matters:** Helps you track and reference specific analyses
        - **Example:** "wf-001" = Your first workflow execution
        
        **2. Trade Framework (e.g., AfCFTA, WTO, USMCA)**
        - **What it is:** The international trade agreement rules to check against
        - **Why it matters:** Different regions have different trade rules
        - **Examples:**
          - **AfCFTA:** African Continental Free Trade Area rules
          - **WTO:** World Trade Organization standards
          - **USMCA:** US-Mexico-Canada trade agreement
        
        **3. Execution Mode**
        - **Sequential:** Checks one thing at a time (slower but thorough)
        - **Parallel:** Checks multiple things simultaneously (faster)
        - **Conditional:** Smart checking based on document type
        
        **4. Status Indicators**
        - ⚡ **RUNNING** (Blue): Analysis in progress
        - ✅ **COMPLETED** (Green): Analysis finished successfully
        - ❌ **FAILED** (Red): Analysis encountered an error
        
        ### 💡 How to Use:
        1. Select your trade framework
        2. Choose execution mode
        3. Pick data source (documents, ports, etc.)
        4. Click "🚀 Execute Workflow"
        5. Watch the progress in "Recent Workflows" below
        
        ### 📊 What Happens During a Workflow:
        - AI agents analyze your documents
        - Compliance rules are checked
        - Risk assessment is performed
        - Detailed report is generated
        - Results appear in 10-15 seconds
        
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
    
    # Show active workflows with detailed descriptions
    if st.session_state.workflows:
        st.markdown("#### 📋 Recent Workflow Executions")
        st.markdown("<p style='color: #b0b0b0; font-size: 0.9rem; margin-bottom: 1rem;'>Track your AI-powered trade compliance analyses below</p>", unsafe_allow_html=True)
        
        for wf in st.session_state.workflows[:5]:
            status_color = "#00ff88" if wf["status"] == "completed" else "#00d4ff" if wf["status"] == "running" else "#ff3366"
            status_icon = "✅" if wf["status"] == "completed" else "⚡" if wf["status"] == "running" else "❌"
            
            # Create descriptive status text
            if wf["status"] == "completed":
                status_desc = "Analysis Complete"
            elif wf["status"] == "running":
                status_desc = "Analyzing..."
            else:
                status_desc = "Failed"
            
            # Framework descriptions
            framework_desc = {
                "AfCFTA": "African Continental Free Trade Area",
                "WTO": "World Trade Organization",
                "USMCA": "US-Mexico-Canada Agreement",
                "EU Customs": "European Union Customs",
                "ASEAN": "Association of Southeast Asian Nations",
                "GCC": "Gulf Cooperation Council"
            }
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1a1a1a 0%, #252525 100%);
                        padding: 1rem; border-radius: 6px; margin: 0.5rem 0;
                        border-left: 4px solid {status_color}; color: #e0e0e0;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <div style="font-size: 1.1rem; font-weight: 600;">
                        {status_icon} Workflow {wf['id'].upper()}
                    </div>
                    <div style="color: {status_color}; font-weight: 600; font-size: 0.95rem;">
                        {status_desc}
                    </div>
                </div>
                <div style="color: #b0b0b0; font-size: 0.9rem; line-height: 1.6;">
                    <strong style="color: #00d4ff;">Framework:</strong> {wf['framework']} ({framework_desc.get(wf['framework'], wf['framework'])})<br/>
                    <strong style="color: #00d4ff;">Mode:</strong> {wf['mode']} Processing<br/>
                    <strong style="color: #00d4ff;">Data Source:</strong> {wf['source']}<br/>
                    <strong style="color: #00d4ff;">Started:</strong> {wf['timestamp'].strftime('%Y-%m-%d %H:%M:%S')} UTC
                </div>
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
        st.markdown('<div class="about-card">', unsafe_allow_html=True)
        st.markdown('<div class="about-title">Trade Intelligence Platform v2.0.0</div>', unsafe_allow_html=True)
        st.markdown('<div class="about-text">', unsafe_allow_html=True)
        
        st.write("**AI-powered multi-agent system** for cross-border trade compliance, risk analysis, and executive decision support.")
        
        st.write("**Supported Trade Frameworks:**")
        st.markdown("""
        - **AfCFTA** (African Continental Free Trade Area)
        - **WTO** (World Trade Organization)
        - **USMCA** (United States-Mexico-Canada Agreement)
        - **EU** Customs Union
        - **ASEAN** (Association of Southeast Asian Nations)
        - **GCC** (Gulf Cooperation Council)
        """)
        
        st.markdown('</div></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="about-card">', unsafe_allow_html=True)
        st.markdown('<div class="about-title">Technology Stack</div>', unsafe_allow_html=True)
        st.markdown('<div class="about-text">', unsafe_allow_html=True)
        
        st.write("**Powered by:**")
        st.markdown("""
        - 🤖 **IBM watsonx.ai**
        - 💎 **IBM Granite Models**
        - 🐍 **IBM Watson Python SDK**
        - 📊 **Bright Data API**
        - ⚡ **Streamlit Framework**
        """)
        
        st.markdown('<p style="text-align: center; color: #ff6b00; font-weight: 600; margin-top: 1rem;">Built for IBM AI Builders Challenge</p>', unsafe_allow_html=True)
        
        st.markdown('</div></div>', unsafe_allow_html=True)


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
    
    # User Role Selection
    render_user_role_selection()
    
    st.markdown("---")
    
    # Document Upload Section
    render_document_upload()
    
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
