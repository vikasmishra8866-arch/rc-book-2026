import streamlit as st
from PIL import Image
import io

# Page setup
st.set_page_config(page_title="RC Detail Modifier", layout="wide")

# Custom CSS for UI and 6.4pt text
# 6.4pt is approximately 8.53 pixels
st.markdown(
    """
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .rc-box {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    /* 6.4pt Font Styling */
    .target-text {
        font-size: 8.53px !important;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
        color: #000;
        margin: 2px 0;
        text-transform: uppercase;
    }
    .label-style {
        font-size: 14px;
        font-weight: 600;
        color: #333;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📄 RC Modification System")
st.write("Apni purani RC upload karein aur naye details enter karke preview check karein.")

# Layout: Two Columns
col_input, col_preview = st.columns([1, 1])

with col_input:
    st.markdown('<div class="rc-box">', unsafe_allow_html=True)
    st.subheader("1. Upload Old RC")
    uploaded_file = st.file_uploader("Choose Image/PDF", type=["jpg", "png", "jpeg", "pdf"])
    
    st.divider()
    
    st.subheader("2. Enter New Details")
    # Input Boxes
    reg_no = st.text_input("Registration Number", placeholder="e.g. GJ05CV6327")
    reg_date = st.text_input("Registration Date", placeholder="DD-MMM-YYYY")
    fitness_to = st.text_input("Fitness Up To", placeholder="DD-MMM-YYYY")
    chassis_no = st.text_input("Chassis Number", placeholder="17 Digit Number")
    
    st.markdown('</div>', unsafe_allow_html=True)

with col_preview:
    st.subheader("3. Live Output (6.4pt Size)")
    
    if uploaded_file:
        # File preview
        if uploaded_file.type != "application/pdf":
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Original RC", use_container_width=True)
        else:
            st.info("PDF Uploaded: Preview available after processing.")
    
    if reg_no or reg_date or fitness_to or chassis_no:
        st.markdown('<div class="rc-box">', unsafe_allow_html=True)
        st.write("**Modified Data Preview:**")
        
        # This div simulates the small text area on an RC
        preview_html = f"""
        <div style="border: 2px solid #333; padding: 10px; background: #fffde7; min-height: 100px;">
            <p class="target-text">REGN NO: {reg_no if reg_no else '________'}</p>
            <p class="target-text">REGN DATE: {reg_date if reg_date else '________'}</p>
            <p class="target-text">FITNESS UP TO: {fitness_to if fitness_to else '________'}</p>
            <p class="target-text">CHASSIS NO: {chassis_no if chassis_no else '________'}</p>
        </div>
        """
        st.markdown(preview_html, unsafe_allow_html=True)
        st.caption("Upar dikhaya gaya text exact 6.4pt font size par set hai.")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("Niche details fill karein preview dekhne ke liye.")

# Action Buttons
if st.sidebar.button("Save & Process"):
    if reg_no and chassis_no:
        st.sidebar.success("Data Saved Successfully!")
    else:
        st.sidebar.error("Main fields fill karna zaroori hai.")

st.sidebar.info("Note: Agle update mein hum in details ko seedha image ke upar overlay karenge.")
