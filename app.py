import streamlit as st
import requests
import io

# Set Page Config
st.set_page_config(page_title="Multilingual OCR Assistant", page_icon="📄")

st.title("📄 Multilingual OCR to Word")
st.markdown("""
Upload up to **20 images** (any language). 
The system will automatically detect the text and combine it into a single **.docx** file.
""")

# 1. File Uploader
uploaded_files = st.file_uploader(
    "Choose images...", 
    type=["jpg", "jpeg", "png"], 
    accept_multiple_files=True
)

# 2. Validation for the 20-file limit
if uploaded_files:
    if len(uploaded_files) > 20:
        st.error("Please upload a maximum of 20 files.")
    else:
        st.info(f"Selected {len(uploaded_files)} files.")
        
        # Optional: Show a small gallery of uploaded images
        with st.expander("Preview Uploaded Images"):
            cols = st.columns(4)
            for idx, file in enumerate(uploaded_files):
                cols[idx % 4].image(file, width='stretch')

        # 3. Process Button
        if st.button("Extract Text & Generate DOCX"):
            with st.spinner("Processing OCR... This may take a moment for multiple files."):
                try:
                    # Prepare files for the API request
                    # We convert Streamlit UploadedFile objects to the format 'requests' expects
                    files = [
                        ("files", (file.name, file.getvalue(), file.type)) 
                        for file in uploaded_files
                    ]

                    # Call your FastAPI endpoint
                    # Replace with your actual deployed URL if not local
                    response = requests.post(
                        "http://localhost:8000/ocr/upload-multiple/", 
                        files=files
                    )

                    if response.status_code == 200:
                        st.success("Extraction Complete!")
                        
                        # 4. Download Button
                        st.download_button(
                            label="📥 Download Combined Word Document",
                            data=response.content,
                            file_name="extracted_text.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                    else:
                        st.error(f"Error from API: {response.text}")

                except Exception as e:
                    st.error(f"Connection Error: {e}")

### 2. How to Run Your System

# To see this in action, you need both the backend and the frontend running simultaneously:

# 1.  **Start the FastAPI Backend:**
#     ```bash
#     uvicorn main:app --reload
#     ```
# 2.  **Start the Streamlit Frontend:**
#     ```bash
#     streamlit run app.py
#     ```