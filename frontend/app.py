import streamlit as st
import requests
from datetime import date
import time
import re  # Added for regex pattern matching

API_URL = "http://backend:8000/applications"
TIMEOUT = 10  # seconds

# Constants
STATUS_OPTIONS = ["applied", "interview", "offer", "rejected"]

# Simplified domain regex that handles common TLDs and subdomains
DOMAIN_PATTERN = re.compile(
    r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
)

def is_valid_url(url):
    """
    Validates if a string is a proper URL or domain name.
    - Accepts full URLs with http/https
    - Accepts domain names like 'google.com'
    - Rejects nonsensical input
    """
    if not url or not url.strip():
        return True  # Empty URLs are considered valid (optional field)
    
    url = url.strip().lower()
    
    # If URL already has a protocol, use a more strict validation
    if url.startswith(('http://', 'https://')):
        try:
            # Simple structure validation
            parts = url.split('://', 1)
            if len(parts) != 2 or not parts[1] or '.' not in parts[1]:
                return False
            return True
        except:
            return False
    
    # For domain-only URLs (without protocol), check domain pattern
    else:
        # Add basic validation for domain names
        return bool(DOMAIN_PATTERN.match(url))

def format_url(url):
    """
    Formats the URL to ensure it has a protocol prefix.
    If no protocol is specified, adds https:// as default.
    """
    if not url or not url.strip():
        return None
    
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        return f"https://{url}"
    return url

st.set_page_config(page_title="Job Tracker", layout="wide")
st.title("Job Tracker")
st.header("Track your job applications")

def fetch_jobs():
    try:
        with st.spinner("Loading applications..."):
            resp = requests.get(API_URL, timeout=TIMEOUT)
            resp.raise_for_status()
            return resp.json()
    except requests.exceptions.Timeout:
        st.error("Request timed out. The server might be overloaded or down.")
        return []
    except Exception as e:
        st.error(f"Failed to fetch applications: {e}")
        return []

def handle_api_response(response, success_msg):
    """Generic handler for API responses with consistent error handling"""
    try:
        response.raise_for_status()
        st.success(success_msg)
        return True
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
            try:
                error_detail = e.response.json().get("detail", str(e))
                st.error(f"Request error: {error_detail}")
            except:
                st.error(f"Request error: {str(e)}")
        else:
            st.error(f"Server error: {str(e)}")
        return False
    except requests.exceptions.Timeout:
        st.error("Request timed out. The server might be overloaded or down.")
        return False
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        return False

def add_job(payload):
    try:
        with st.spinner("Adding application..."):
            resp = requests.post(API_URL, json=payload, timeout=TIMEOUT)
        return handle_api_response(resp, "Application added successfully!"), None
    except Exception as e:
        return False, str(e)

def update_job(job_id, payload):
    try:
        with st.spinner("Updating application..."):
            resp = requests.put(f"{API_URL}/{job_id}", json=payload, timeout=TIMEOUT)
        return handle_api_response(resp, "Application updated successfully!"), None
    except Exception as e:
        return False, str(e)

def delete_job(job_id):
    try:
        with st.spinner("Deleting application..."):
            resp = requests.delete(f"{API_URL}/{job_id}", timeout=TIMEOUT)
        return handle_api_response(resp, "Application deleted successfully!"), None
    except Exception as e:
        return False, str(e)

def validate_form(company, position, link=None):
    """Common form validation logic"""
    if not company.strip():
        st.error("Company name is required")
        return False
    elif not position.strip():
        st.error("Position is required")
        return False
    elif link and link.strip():
        if not is_valid_url(link):
            st.error("Invalid URL format. Please enter a valid domain (e.g., google.com) or full URL (e.g., https://google.com)")
            return False
    return True

# --- Add New Job Application Form ---
with st.expander("➕ Add New Application", expanded=True):
    with st.form("add_job_form"):
        cols = st.columns(3)
        company = cols[0].text_input("Company *", max_chars=100)
        position = cols[1].text_input("Position *", max_chars=100)
        status = cols[2].selectbox("Status *", STATUS_OPTIONS, index=0)
        link = st.text_input(
            "Link (optional)", 
            placeholder="google.com or https://google.com",
            help="Enter a domain name or full URL"
        )
        notes = st.text_area("Notes (optional)")
        date_cols = st.columns(2)
        today = date.today()
        applied_date = date_cols[0].date_input("Applied Date", value=today)
        submitted = st.form_submit_button("Add Application")

        if submitted:
            if validate_form(company, position, link):
                payload = {
                    "company": company.strip(),
                    "position": position.strip(),
                    "status": status,
                    "link": format_url(link) if link and link.strip() else None,
                    "notes": notes.strip() if notes and notes.strip() else None,
                    "applied_date": str(applied_date),
                    "updated_date": None
                }
                ok, err = add_job(payload)
                if ok:
                    st.rerun()
                elif err:
                    st.error(f"Failed to add application: {err}")

# --- Filter by Status ---
st.subheader("Applications")
status_filter = st.selectbox("Filter by status", ["all"] + STATUS_OPTIONS, key="status_filter")

try:
    jobs = fetch_jobs()
    if status_filter != "all":
        jobs = [job for job in jobs if job["status"] == status_filter]

    if jobs:
        # Initialize session state for editing and confirmation
        if 'editing_job_id' not in st.session_state:
            st.session_state.editing_job_id = None
        if 'confirm_delete_id' not in st.session_state:
            st.session_state.confirm_delete_id = None

        st.write("Click 'Edit' to update application details, or 'Delete' to remove an application.")
        
        for job in jobs:
            with st.container():
                cols = st.columns([2,2,2,2,2,2,1,1])
                cols[0].markdown(f"**{job['company']}**")
                cols[1].markdown(f"{job['position']}")
                cols[2].markdown(f"Status: `{job['status']}`")
                cols[3].markdown(f"[Link]({job['link']})" if job['link'] else "")
                cols[4].markdown(f"Applied: {job['applied_date'] or '-'}")
                cols[5].markdown(f"Updated: {job['updated_date'] or '-'}")
                
                # Change edit button to set session state
                if cols[6].button("Edit", key=f"edit_{job['id']}"):
                    st.session_state.editing_job_id = job['id']
                    # Clear any delete confirmation
                    st.session_state.confirm_delete_id = None
                    st.rerun()
                
                # Two-step delete with confirmation
                if st.session_state.confirm_delete_id == job['id']:
                    if cols[7].button("Confirm", key=f"confirm_{job['id']}"):
                        ok, err = delete_job(job["id"])
                        if ok:
                            st.session_state.confirm_delete_id = None
                            st.rerun()
                        else:
                            st.error(f"Failed to delete application: {err}")
                else:
                    if cols[7].button("Delete", key=f"del_{job['id']}"):
                        st.session_state.confirm_delete_id = job['id']
                        # Clear any editing state
                        if st.session_state.editing_job_id == job['id']:
                            st.session_state.editing_job_id = None
                        st.rerun()

                # Show job notes if they exist
                if job['notes']:
                    with st.expander("View Notes", expanded=False):
                        st.markdown(job['notes'])

                # Show edit form if this job is being edited
                if st.session_state.editing_job_id == job['id']:
                    with st.form(f"edit_form_{job['id']}"):
                        st.write("Update job application details:")
                        new_company = st.text_input("Company *", value=job["company"], key=f"edit_company_{job['id']}")
                        new_position = st.text_input("Position *", value=job["position"], key=f"edit_position_{job['id']}")
                        new_status = st.selectbox(
                            "Status *",
                            STATUS_OPTIONS,
                            index=STATUS_OPTIONS.index(job["status"]),
                            key=f"edit_status_{job['id']}"
                        )
                        new_link = st.text_input(
                            "Link", 
                            value=job["link"] or "", 
                            key=f"edit_link_{job['id']}",
                            help="Enter a domain name or full URL"
                        )
                        new_notes = st.text_area("Notes", value=job["notes"] or "", key=f"edit_notes_{job['id']}")
                        col1, col2 = st.columns([1, 4])
                        update_submitted = col1.form_submit_button("Save")
                        if col2.form_submit_button("Cancel"):
                            st.session_state.editing_job_id = None
                            st.rerun()

                        if update_submitted:
                            if validate_form(new_company, new_position, new_link):
                                update_payload = {
                                    "company": new_company.strip(),
                                    "position": new_position.strip(),
                                    "status": new_status,
                                    "link": format_url(new_link) if new_link and new_link.strip() else None,
                                    "notes": new_notes.strip() if new_notes and new_notes.strip() else None,
                                    "updated_date": str(date.today())
                                }
                                ok, err = update_job(job["id"], update_payload)
                                if ok:
                                    st.session_state.editing_job_id = None
                                    st.rerun()
                                elif err:
                                    st.error(f"Failed to update application: {err}")
    else:
        st.info("No applications found for this filter.")
except Exception as e:
    st.error(f"An error occurred: {e}")
    st.warning("Please try again or contact support if the problem persists.")

# Add a footer with help information
st.markdown("---")
with st.expander("Help & Tips"):
    st.markdown("""
    ### How to use this app
    
    - **Add** new applications using the form at the top
    - **Filter** applications by status using the dropdown
    - **Edit** applications by clicking the 'Edit' button
    - **Delete** applications by clicking 'Delete' (requires confirmation)
    - **View Notes** by expanding the notes section under each application
    """)
