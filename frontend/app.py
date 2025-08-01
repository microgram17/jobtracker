import streamlit as st
import requests

API_URL = "http://backend:8000/applications"

st.set_page_config(page_title="Job Tracker", layout="wide")
st.title("Job Tracker")
st.header("Track your job applications")

def fetch_jobs():
    try:
        resp = requests.get(API_URL)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"Failed to fetch applications: {e}")
        return []

def add_job(payload):
    try:
        resp = requests.post(API_URL, json=payload)
        resp.raise_for_status()
        return True, None
    except Exception as e:
        return False, str(e)

def update_job(job_id, payload):
    try:
        resp = requests.put(f"{API_URL}/{job_id}", json=payload)
        resp.raise_for_status()
        return True, None
    except Exception as e:
        return False, str(e)

def delete_job(job_id):
    try:
        resp = requests.delete(f"{API_URL}/{job_id}")
        resp.raise_for_status()
        return True, None
    except Exception as e:
        return False, str(e)

# --- Add New Job Application Form ---
with st.expander("➕ Add New Application", expanded=True):
    with st.form("add_job_form"):
        cols = st.columns(3)
        company = cols[0].text_input("Company", max_chars=100)
        position = cols[1].text_input("Position", max_chars=100)
        status = cols[2].selectbox("Status", ["applied", "interview", "offer", "rejected"])
        link = st.text_input("Link (optional)")
        notes = st.text_area("Notes (optional)")
        date_cols = st.columns(2)
        applied_date = date_cols[0].date_input("Applied Date (optional)", value=None)
        submitted = st.form_submit_button("Add Application")

        if submitted:
            payload = {
                "company": company,
                "position": position,
                "status": status,
                "link": link if link else None,
                "notes": notes if notes else None,
                "applied_date": str(applied_date) if applied_date else None,
                "updated_date": None
            }
            ok, err = add_job(payload)
            if ok:
                st.success("Application added!")
                st.experimental_rerun()
            else:
                st.error(f"Error: {err}")

# --- Filter by Status ---
st.subheader("Applications")
status_filter = st.selectbox("Filter by status", ["all", "applied", "interview", "offer", "rejected"], key="status_filter")

jobs = fetch_jobs()
if status_filter != "all":
    jobs = [job for job in jobs if job["status"] == status_filter]

if jobs:
    st.write("Click 'Edit' to update status/notes, or 'Delete' to remove an application.")
    for job in jobs:
        with st.container():
            cols = st.columns([2,2,2,2,2,2,1,1])
            cols[0].markdown(f"**{job['company']}**")
            cols[1].markdown(f"{job['position']}")
            cols[2].markdown(f"Status: `{job['status']}`")
            cols[3].markdown(f"[Link]({job['link']})" if job['link'] else "")
            cols[4].markdown(f"Applied: {job['applied_date'] or '-'}")
            cols[5].markdown(f"Updated: {job['updated_date'] or '-'}")
            edit_btn = cols[6].button("Edit", key=f"edit_{job['id']}")
            del_btn = cols[7].button("Delete", key=f"del_{job['id']}")

            if edit_btn:
                with st.expander(f"Edit Application #{job['id']}", expanded=True):
                    with st.form(f"edit_form_{job['id']}"):
                        new_status = st.selectbox("Status", ["applied", "interview", "offer", "rejected"], index=["applied", "interview", "offer", "rejected"].index(job["status"]))
                        new_notes = st.text_area("Notes", value=job["notes"] or "")
                        submitted = st.form_submit_button("Update")
                        if submitted:
                            payload = {
                                "status": new_status,
                                "notes": new_notes,
                                "updated_date": str(st.session_state.get("edit_date", None)) or None
                            }
                            ok, err = update_job(job["id"], payload)
                            if ok:
                                st.success("Application updated!")
                                st.experimental_rerun()
                            else:
                                st.error(f"Error: {err}")

            if del_btn:
                ok, err = delete_job(job["id"])
                if ok:
                    st.success("Application deleted!")
                    st.experimental_rerun()
                else:
                    st.error(f"Error: {err}")
else:
    st.info("No applications found for this filter.")
