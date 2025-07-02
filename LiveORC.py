import streamlit as st
import requests
import json

API_BASE = "http://localhost:8000/api"

st.session_state.token = "dummy-token"
headers = {"Authorization": f"Bearer {st.session_state.token}"}

st.title("🌊 LiveOpenRiverCam Control Panel")

mode = st.sidebar.radio("Navigation", [
    "🏠 Home",
    "📍 Sites & Cameras",
    "📹 Upload Video",
    "⚙️ Configuration",
    "📊 Results"
])

if mode == "🏠 Home":
    st.markdown("""
    Welcome to LiveOpenRiverCam Streamlit front-end.
    Use the sidebar to navigate through the main steps:
    - Add sites & cameras  
    - Upload videos for processing  
    - Configure water levels, recipes, camera settings  
    - View processing results
    """)

if mode == "📍 Sites & Cameras":
    st.subheader("Sites")
    r = requests.get(f"{API_BASE}/sites/")
    if r.ok:
        sites = r.json()
        for s in sites:
            st.write(f"• **{s['name']}** — {s['description']}")
    else:
        st.error("Failed to fetch sites.")

    st.markdown("---")
    st.markdown("### Add New Site")
    new_site = st.text_input("Site Name")
    new_desc = st.text_area("Description")
    if st.button("Create Site"):
        j = {"name": new_site, "description": new_desc}
        r = requests.post(f"{API_BASE}/sites/", json=j)
        if r.ok:
            st.success("Site created.")
            st.experimental_rerun()
        else:
            st.error("Error creating site.")

    st.markdown("### Camera Configuration")
    r = requests.get(f"{API_BASE}/cameras/")
    if r.ok:
        st.write(r.json())
    uploaded = st.file_uploader("Upload camera config (JSON)", type=["json"])
    if uploaded:
        data = json.load(uploaded)
        r = requests.post(f"{API_BASE}/cameras/", json=data)
        if r.ok:
            st.success("Camera config uploaded.")
        else:
            st.error("Upload failed.")

if mode == "📹 Upload Video":
    st.subheader("Upload Video for Processing")
    site_id = st.number_input("Site ID", min_value=0, step=1)
    cam_id = st.number_input("Camera ID", min_value=0, step=1)
    video = st.file_uploader("Select mp4 video", type=["mp4", "mov", "avi"])
    if video and st.button("Upload & Process"):
        files = {"file": (video.name, video, video.type)}
        r = requests.post(
            f"{API_BASE}/sites/{site_id}/cameras/{cam_id}/upload/",
            files=files
        )
        if r.ok:
            st.success("Uploaded! Processing started.")
        else:
            st.error("Upload failed.")

if mode == "⚙️ Configuration":
    st.subheader("Water Level Configuration")
    wl_fmt = st.text_input("Water level filename format", value="wlevel_{%Y%m%d}.txt")
    datetime_fmt = st.text_input("Datetime format", value="%Y%m%d_%H%M%S")
    if st.button("Update Format"):
        payload = {"settings": {"water_level_fmt": wl_fmt, "water_level_datetimefmt": datetime_fmt}}
        r = requests.patch(f"{API_BASE}/config/", json=payload)
        if r.ok:
            st.success("Updated!")
        else:
            st.error("Failed to update.")

    st.markdown("---")
    st.subheader("Recipes")
    recipe = st.file_uploader("Upload recipe config (JSON)", type="json")
    if recipe and st.button("Upload Recipe"):
        cfg = json.load(recipe)
        r = requests.post(f"{API_BASE}/recipes/", json=cfg)
        if r.ok:
            st.success("Recipe uploaded.")
        else:
            st.error("Upload failed.")

if mode == "📊 Results":
    st.subheader("Processing Results")
    r = requests.get(f"{API_BASE}/results/")
    if r.ok:
        results = r.json()
        for res in results:
            st.markdown(f"**Video**: {res['video_name']} – Status: {res['status']}")
            if res.get("result_url"):
                st.markdown(f"- [Download result data]({res['result_url']})")
            if res.get("plot_url"):
                st.image(res["plot_url"], caption="Result plot")
    else:
        st.error("Could not fetch results.")