import streamlit as st
import redis
import os
from datetime import datetime

st.set_page_config(
    page_title="Container Orchestration Demo",
    page_icon="🐳",
    layout="wide"
)

redis_host = os.getenv('REDIS_HOST', 'redis')
redis_port = int(os.getenv('REDIS_PORT', 6379))

try:
    r = redis.Redis(
        host=redis_host,
        port=redis_port,
        decode_responses=True,
        socket_connect_timeout=5
    )
    r.ping()
    redis_available = True
except:
    redis_available = False

st.title("🐳 Container Orchestration Demo")
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Redis Host", redis_host)

with col2:
    st.metric("Redis Port", redis_port)

with col3:
    status = "🟢 Connected" if redis_available else "🔴 Disconnected"
    st.metric("Redis Status", status)

st.markdown("---")

if redis_available:
    
    page_views = r.incr('page_views')
    
    st.subheader("📊 Page View Counter")
    st.markdown(f"### This page has been viewed **{page_views}** times")
    
    st.markdown("---")
    
    st.subheader("🔧 Interactive Demo")
    
    user_input = st.text_input("Enter a message to cache:", key="message_input")
    
    if st.button("Cache Message"):
        if user_input:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            r.rpush('messages', f"{timestamp}: {user_input}")
            st.success(f"Message cached: {user_input}")
        else:
            st.warning("Please enter a message first")
    
    if st.button("Show All Cached Messages"):
        messages = r.lrange('messages', 0, -1)
        if messages:
            st.write("**Cached Messages:**")
            for idx, msg in enumerate(reversed(messages), 1):
                st.text(f"{idx}. {msg}")
        else:
            st.info("No messages cached yet")
    
    if st.button("Clear All Messages"):
        r.delete('messages')
        st.success("All messages cleared!")
    
    st.markdown("---")
    
    st.subheader("💾 Redis Statistics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        all_keys = r.keys('*')
        st.metric("Total Keys in Redis", len(all_keys))
        
        if all_keys:
            st.write("**Keys:**")
            for key in all_keys:
                key_type = r.type(key)
                st.text(f"- {key} ({key_type})")
    
    with col2:
        message_count = r.llen('messages')
        st.metric("Cached Messages", message_count)
        
        info = r.info('server')
        st.write(f"**Redis Version:** {info.get('redis_version', 'N/A')}")
        st.write(f"**Uptime (seconds):** {info.get('uptime_in_seconds', 'N/A')}")

else:
    st.error("❌ Cannot connect to Redis")
    st.info(f"Attempting to connect to: {redis_host}:{redis_port}")
    st.markdown("""
    **Troubleshooting:**
    - Ensure Redis service is running
    - Check Redis host and port configuration
    - Verify network connectivity between containers
    """)

st.markdown("---")
st.caption("Container Orchestration Demo | Streamlit + Redis")
