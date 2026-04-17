import streamlit as st
from PIL import Image

# Page Configuration
st.set_page_config(page_title="RC Modifier Tool", layout="centered")

# Custom CSS for Font Size 6.4pt and styling
# 6.4pt is roughly 8.5px
st.markdown(
    """
    <style>
    .custom-text {
        font-size: 8.5px !important;
        font-family: 'Arial', sans-serif;
        line-height: 1.2;
    }
    .stTextInput label {
        font-size: 14px !important;
        font-weight: bold;
    }
    .upload-section {
        border: 2px dashed #4CAF50;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📄 RC Modification Portal")
st.write("Apni purani RC upload karein aur niche naye details enter karein.")

# 1. RC Upload Section
st.markdown('<div class="upload-section">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload Your Old RC (Image/PDF)", type=["jpg", "jpeg", "png", "pdf"])
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file is not None:
    st.success("File Upload Ho Gayi Hai!")
    if uploaded_file.type != "application/pdf":
        img = Image.open(uploaded_file)
        st.image(img, caption="Uploaded RC Preview", use_container_width=True)

st.divider()

# 2. Input Fields Section (The Boxes)
st.subheader("New RC Details (Modify Here)")

col1, col2 = st.columns(2)

with col1:
    reg_no = st.text_input("1. Registration No", placeholder="e.g. GJ05CV6327")
    reg_date = st.text_input("2. Reg Date", placeholder="DD-MMM-YYYY")

with col2:
    fitness_date = st.text_input("3. Fitness Up To", placeholder="DD-MMM-YYYY")
    chassis_no = st.text_input("4. Chassis Number", placeholder="Enter 17 digit number")

# 3. Output Preview with 6.4pt font size
if st.button("Generate Preview"):
    if reg_no and reg_date and fitness_date and chassis_no:
        st.info("Niche aapka modified data 6.4pt size me dikh raha hai:")
        
        # Displaying data in a box with exact font size constraint
        preview_html = f"""
        <div style="border: 1px solid #ccc; padding: 15px; border-radius: 5px; background-color: #f9f9f9;">
            <p class="custom-text"><strong>REGN NO:</strong> {reg_no.upper()}</p>
            <p class="custom-text"><strong>REGN DATE:</strong> {reg_date}</p>
            <p class="custom-text"><strong>FITNESS VALID UPTO:</strong> {fitness_date}</p>
            <p class="custom-text"><strong>CHASSIS NO:</strong> {chassis_no.upper()}</p>
        </div>
        """
        st.markdown(preview_html, unsafe_allow_html=True)
    else:
        st.warning("Kripya saare boxes fill karein.")

# Footer info
st.markdown("---")
st.caption("Developed for RC Modification Testing - GitHub + Streamlit")
