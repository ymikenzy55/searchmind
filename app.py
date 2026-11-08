import streamlit as st
from main import create_agent, query_agent, get_conversation_history, clear_conversation_history, get_total_messages
import uuid
from datetime import datetime

st.set_page_config(
    page_title="SearchMind - AI Research Assistant",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
        background: linear-gradient(120deg, #6366f1 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .sub-header {
        font-size: 1.1rem;
        text-align: center;
        margin-bottom: 2rem;
        opacity: 0.7;
    }
    
    .icon {
        margin-right: 8px;
        opacity: 0.8;
    }
    
    .feature-item {
        padding: 0.5rem 0;
        display: flex;
        align-items: center;
    }
    
    .stChatMessage {
        padding: 1rem;
        border-radius: 12px;
    }
    
    .stButton button {
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    hr {
        margin: 1.5rem 0;
        opacity: 0.3;
    }
    
    .metric-card {
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        background: rgba(99, 102, 241, 0.1);
        border: 1px solid rgba(99, 102, 241, 0.2);
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.7;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 1.5rem;
        font-weight: 600;
        color: #6366f1;
    }
    
    @media (prefers-color-scheme: dark) {
        .main-header {
            background: linear-gradient(120deg, #818cf8 0%, #a78bfa 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .metric-card {
            background: rgba(129, 140, 248, 0.1);
            border: 1px solid rgba(129, 140, 248, 0.2);
        }
        
        .metric-value {
            color: #818cf8;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Initialize agent
if "agent" not in st.session_state:
    with st.spinner("Initializing SearchMind..."):
        st.session_state.agent = create_agent()

# Initialize session ID (unique for each chat)
if "session_id" not in st.session_state:
    st.session_state.session_id = "default"

# Get current session history
conversation_history = get_conversation_history(session_id=st.session_state.session_id, limit=100)

# Header
st.markdown('<div class="main-header"><i class="fa-solid fa-magnifying-glass-chart" style="margin-right: 12px;"></i>SearchMind</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Your intelligent research companion with permanent memory</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### <i class='fa-solid fa-circle-info icon'></i>What is SearchMind?", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-item">
        <i class="fa-solid fa-magnifying-glass icon"></i>
        <strong>Real-time Web Search</strong>
    </div>
    <p style="margin-left: 28px; font-size: 0.9rem; opacity: 0.8;">Access current information</p>
    
    <div class="feature-item">
        <i class="fa-solid fa-brain icon"></i>
        <strong>Intelligent Reasoning</strong>
    </div>
    <p style="margin-left: 28px; font-size: 0.9rem; opacity: 0.8;">Analyzes and synthesizes</p>
    
    <div class="feature-item">
        <i class="fa-solid fa-database icon"></i>
        <strong>Permanent Memory</strong>
    </div>
    <p style="margin-left: 28px; font-size: 0.9rem; opacity: 0.8;">Remembers conversations</p>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # New Chat Button
    col1, col2 = st.columns(2)
    with col1:
        if st.button("New Chat", key="new_chat", use_container_width=True, type="primary"):
            # Generate new session ID
            st.session_state.session_id = str(uuid.uuid4())[:8]
            st.success("New chat started!")
            st.rerun()
    
    with col2:
        if st.button("View All", key="view_all", use_container_width=True):
            st.session_state.session_id = "default"
            st.info("Viewing all conversations")
            st.rerun()
    
    st.divider()
    
    st.markdown("### <i class='fa-solid fa-bullseye icon'></i>Quick Questions", unsafe_allow_html=True)
    examples = [
        "My name is John",
        "What's my name?",
        "Who created you?",
        "Latest in AI"
    ]
    
    for example in examples:
        if st.button(example, key=f"ex_{example}", use_container_width=True):
            st.session_state.current_question = example
    
    st.divider()
    
    # Clear options
    st.markdown("### <i class='fa-solid fa-trash icon'></i>Clear Options", unsafe_allow_html=True)
    
    if st.button("Clear This Chat", key="clear_current", use_container_width=True, type="secondary"):
        clear_conversation_history(session_id=st.session_state.session_id)
        st.success("Current chat cleared!")
        st.rerun()
    
    if st.button("Clear All Chats", key="clear_all", use_container_width=True, type="secondary"):
        clear_conversation_history(session_id="default")
        st.success("All chats cleared!")
        st.rerun()
    
    st.divider()
    
    st.markdown("""
    <div style="text-align: center; opacity: 0.6; font-size: 0.85rem;">
        <i class="fa-solid fa-circle-half-stroke"></i> Light & Dark mode
    </div>
    """, unsafe_allow_html=True)
    
    # Show current session info
    if st.session_state.session_id != "default":
        st.caption(f"Chat ID: {st.session_state.session_id}")
    else:
        st.caption("Viewing: All conversations")

# Main chat interface
st.markdown("### <i class='fa-solid fa-message icon'></i>Chat", unsafe_allow_html=True)

# Display chat messages
for message in conversation_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle example question from sidebar
if "current_question" in st.session_state:
    question = st.session_state.current_question
    del st.session_state.current_question
    
    with st.chat_message("user"):
        st.markdown(question)
    
    with st.chat_message("assistant"):
        with st.spinner("SearchMind is analyzing..."):
            response = query_agent(st.session_state.agent, question, session_id=st.session_state.session_id)
        st.markdown(response)
    
    st.rerun()

# Chat input
if prompt := st.chat_input("Ask SearchMind anything..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("SearchMind is analyzing..."):
            response = query_agent(st.session_state.agent, prompt, session_id=st.session_state.session_id)
        st.markdown(response)
    
    st.rerun()

# Footer stats
st.divider()
col1, col2, col3 = st.columns(3)

current_chat_messages = len(conversation_history)
total_all_messages = get_total_messages(session_id="default")

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label"><i class="fa-solid fa-comment"></i> This Chat</div>
        <div class="metric-value">{current_chat_messages}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label"><i class="fa-solid fa-database"></i> All Chats</div>
        <div class="metric-value">{total_all_messages}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label"><i class="fa-solid fa-bolt"></i> Status</div>
        <div class="metric-value">Active</div>
    </div>
    """, unsafe_allow_html=True)
