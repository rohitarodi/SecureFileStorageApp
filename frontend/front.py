import streamlit as st
import requests
import os

# Backend URL
BACKEND_URL = "http://127.0.0.1:5000"  # Change if running backend on a different address

st.title("🔒 Secure File Storage App")

# File Upload Section
st.header("📤 Upload File")
uploaded_file = st.file_uploader("Choose a file to upload", type=None)
if uploaded_file:
    if st.button("Upload File"):
        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
        try:
            response = requests.post(f"{BACKEND_URL}/upload", files=files)
            if response.status_code == 200:
                st.success(f"✅ {uploaded_file.name} uploaded successfully!")
            else:
                error_msg = response.text or "Unknown error"
                st.error(f"❌ Upload failed: {error_msg}")
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Request error: {e}")

# Fetch available files from the server
st.header("📥 Download File")
files_list = []
try:
    file_list_response = requests.get(f"{BACKEND_URL}/list_files")
    if file_list_response.status_code == 200:
        files_list = file_list_response.json().get("files", [])
    else:
        st.error("❌ Failed to fetch file list.")
except requests.exceptions.RequestException as e:
    st.error(f"❌ Request error: {e}")

# Dropdown for file selection
if files_list:
    selected_file = st.selectbox("Select a file to download", files_list)
    if st.button("Download File"):
        try:
            response = requests.get(f"{BACKEND_URL}/download_save", params={"filename": selected_file})
            if response.status_code == 200:
                save_path = os.path.join("downloads", selected_file)
                os.makedirs("downloads", exist_ok=True)
                with open(save_path, "wb") as file:
                    file.write(response.content)
                st.success(f"✅ File downloaded and saved as: {save_path}")
                st.download_button(label="Download File", data=response.content, file_name=selected_file)
            else:
                error_msg = response.text or "File not found"
                st.error(f"❌ Download failed: {error_msg}")
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Request error: {e}")
else:
    st.warning("⚠ No files available for download.")

# Download & Save on Server Section
# st.header("💾 Download & Save File on Server")
# save_filename = st.text_input("Enter filename to download & save on server")
# if st.button("Download & Save File on Server"):
#     if save_filename:
#         try:
#             response = requests.get(f"{BACKEND_URL}/download_save", params={"filename": save_filename})
#             if response.status_code == 200:
#                 json_response = response.json() if response.content else {"message": "File saved successfully!"}
#                 st.success(json_response.get("message", "File saved successfully!"))
#             else:
#                 error_msg = response.text or "Unknown error"
#                 st.error(f"❌ Operation failed: {error_msg}")
#         except requests.exceptions.RequestException as e:
#             st.error(f"❌ Request error: {e}")
#     else:
#         st.warning("⚠ Please enter a filename.")