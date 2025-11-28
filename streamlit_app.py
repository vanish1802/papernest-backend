import streamlit as st
import requests
from datetime import datetime

# Configuration
API_URL = "https://papernest-api.onrender.com"

# Page config
st.set_page_config(
    page_title="PaperNest",
    page_icon="📚",
    layout="wide"
)

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "username" not in st.session_state:
    st.session_state.username = None

# Sidebar - Authentication
with st.sidebar:
    st.title("🔐 Authentication")
    
    if not st.session_state.session_id:
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            st.subheader("Login")
            login_username = st.text_input("Username", key="login_user")
            login_password = st.text_input("Password", type="password", key="login_pass")
            
            if st.button("Login", type="primary"):
                try:
                    resp = requests.post(
                        f"{API_URL}/auth/login",
                        json={"username": login_username, "password": login_password}
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        st.session_state.session_id = data["session_id"]
                        st.session_state.username = login_username
                        st.success("✅ Logged in successfully!")
                        st.rerun()
                    else:
                        st.error(f"❌ Login failed: {resp.json().get('detail', 'Unknown error')}")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        
        with tab2:
            st.subheader("Register")
            reg_email = st.text_input("Email", key="reg_email")
            reg_username = st.text_input("Username", key="reg_user")
            reg_password = st.text_input("Password", type="password", key="reg_pass")
            
            if st.button("Register", type="primary"):
                try:
                    resp = requests.post(
                        f"{API_URL}/auth/register",
                        json={
                            "email": reg_email,
                            "username": reg_username,
                            "password": reg_password
                        }
                    )
                    if resp.status_code == 201:
                        st.success("✅ Registered! Please login.")
                    else:
                        st.error(f"❌ Registration failed: {resp.json().get('detail', 'Unknown error')}")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    else:
        st.success(f"👤 Logged in as: **{st.session_state.username}**")
        if st.button("Logout", type="secondary"):
            st.session_state.session_id = None
            st.session_state.username = None
            st.rerun()

# Main app
st.title("📚 PaperNest - Research Paper Manager")

if not st.session_state.session_id:
    st.info("👈 Please login or register to continue")
    st.stop()

# Headers for authenticated requests
headers = {"X-Session-ID": st.session_state.session_id}

# Create tabs
tab1, tab2 = st.tabs(["📄 My Papers", "➕ Add New Paper"])

# Tab 1: View Papers
with tab1:
    st.header("My Research Papers")
    
    try:
        resp = requests.get(f"{API_URL}/papers/", headers=headers)
        if resp.status_code == 200:
            papers = resp.json()
            
            if not papers:
                st.info("No papers yet. Add your first paper in the 'Add New Paper' tab!")
            else:
                # Filter options
                col1, col2, col3 = st.columns(3)
                with col1:
                    status_filter = st.selectbox(
                        "Filter by Status",
                        ["All", "TO_READ", "READING", "COMPLETED"]
                    )
                with col2:
                    priority_filter = st.selectbox(
                        "Filter by Priority",
                        ["All", "LOW", "MEDIUM", "HIGH"]
                    )
                with col3:
                    st.write(f"**Total Papers:** {len(papers)}")
                
                # Apply filters
                filtered_papers = papers
                if status_filter != "All":
                    filtered_papers = [p for p in filtered_papers if p["status"] == status_filter]
                if priority_filter != "All":
                    filtered_papers = [p for p in filtered_papers if p["priority"] == priority_filter]
                
                st.write(f"Showing {len(filtered_papers)} papers")
                st.divider()
                
                # Display papers
                for paper in filtered_papers:
                    with st.expander(f"📄 {paper['title']}", expanded=False):
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.write(f"**Authors:** {paper['authors']}")
                            st.write(f"**Status:** {paper['status']}")
                            st.write(f"**Priority:** {paper['priority']}")
                            if paper.get('categories'):
                                st.write(f"**Categories:** {paper['categories']}")
                            st.write(f"**Created:** {paper['created_at'][:10]}")
                            
                            if paper.get('paper_text'):
                                st.write("**Paper Text:**")
                                st.text_area("", paper['paper_text'], height=100, key=f"text_{paper['id']}", disabled=True)
                            
                            if paper.get('summary'):
                                st.success("**AI Summary:**")
                                st.write(paper['summary'])
                            else:
                                if st.button("🤖 Generate AI Summary", key=f"summarize_{paper['id']}"):
                                    with st.spinner("Generating summary... (10-15 sec first time)"):
                                        try:
                                            resp = requests.post(
                                                f"{API_URL}/papers/{paper['id']}/summarize",
                                                headers=headers
                                            )
                                            if resp.status_code == 200:
                                                st.success("✅ Summary generated!")
                                                st.rerun()
                                            else:
                                                st.error(f"Failed: {resp.json().get('detail')}")
                                        except Exception as e:
                                            st.error(f"Error: {str(e)}")
                        
                        with col2:
                            if st.button("🗑️ Delete", key=f"delete_{paper['id']}", type="secondary"):
                                try:
                                    resp = requests.delete(
                                        f"{API_URL}/papers/{paper['id']}",
                                        headers=headers
                                    )
                                    if resp.status_code == 204:
                                        st.success("✅ Deleted!")
                                        st.rerun()
                                    else:
                                        st.error("Failed to delete")
                                except Exception as e:
                                    st.error(f"Error: {str(e)}")
        else:
            st.error(f"Failed to fetch papers: {resp.status_code}")
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Tab 2: Add New Paper
with tab2:
    st.header("Add New Research Paper")
    
    with st.form("add_paper_form"):
        title = st.text_input("Title *", placeholder="e.g., Diabetic Retinopathy Detection using Deep Learning")
        authors = st.text_input("Authors *", placeholder="e.g., Vanish et al.")
        
        col1, col2 = st.columns(2)
        with col1:
            status = st.selectbox("Status", ["TO_READ", "READING", "COMPLETED"])
        with col2:
            priority = st.selectbox("Priority", ["LOW", "MEDIUM", "HIGH"])
        
        categories = st.text_input("Categories (optional)", placeholder="e.g., Deep Learning, Computer Vision")
        paper_text = st.text_area(
            "Paper Text (for AI summarization)",
            height=200,
            placeholder="Paste the paper content here for AI summarization..."
        )
        
        submitted = st.form_submit_button("➕ Add Paper", type="primary")
        
        if submitted:
            if not title or not authors:
                st.error("❌ Title and Authors are required!")
            else:
                try:
                    resp = requests.post(
                        f"{API_URL}/papers/",
                        headers=headers,
                        json={
                            "title": title,
                            "authors": authors,
                            "status": status,
                            "priority": priority,
                            "categories": categories if categories else None,
                            "paper_text": paper_text if paper_text else None
                        }
                    )
                    if resp.status_code == 201:
                        st.success("✅ Paper added successfully!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(f"❌ Failed: {resp.json().get('detail', 'Unknown error')}")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# Footer
st.divider()
st.caption("Built with FastAPI + Streamlit | PaperNest © 2025")

