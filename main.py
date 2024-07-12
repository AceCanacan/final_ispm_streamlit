import streamlit as st
from fpdf import FPDF
import base64
import random

# Define instruction arrays with simplified requirements
common_info = ["Name", "Address", "Birthdate"]
instructions = {
    "LTO Driver's License": ["Upload Birth Certificate", "Upload ID Photo"],
    "DFA Passport": ["Upload Birth Certificate", "Upload Passport Photo", "Upload Old Passport (if renewing)"],
    "NBI Clearance": ["Upload Birth Certificate", "Upload ID Photo"],
    "PSA Birth Certificate": ["Upload ID Photo"]
}

# Function to generate a PDF with requirements
def generate_pdf(requirements, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", size=16)
    pdf.cell(200, 20, txt="Document Requirements", ln=True, align="C")
    pdf.set_font("Arial", size=12)
    for item in requirements:
        pdf.cell(200, 10, txt="- " + item, ln=True)
    pdf.output(filename)
    return filename

# Function to create a download link for the generated PDF
def create_download_link(pdf_file, file_label):
    with open(pdf_file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<a href="data:application/octet-stream;base64,{base64_pdf}" download="{pdf_file}" class="download-button">{file_label}</a>'
    return pdf_display

# Custom CSS for styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
        
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #f0f2f6;
            color: #333;
        }
        .main-title {
            color: #1e88e5;
            text-align: center;
            font-size: 2.5em;
            font-weight: 700;
            margin-bottom: 30px;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }
        .section-title {
            color: #333;
            font-size: 1.8em;
            font-weight: 700;
            margin-top: 30px;
            margin-bottom: 20px;
            border-bottom: 2px solid #1e88e5;
            padding-bottom: 10px;
        }
        .instruction-text {
            font-size: 1.1em;
            color: #555;
            background-color: #fff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .stButton > button {
            background-color: #1e88e5;
            color: white;
            font-weight: 500;
            padding: 10px 20px;
            border-radius: 25px;
            border: none;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #1565c0;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        .success-message {
            color: #4caf50;
            font-size: 1.3em;
            font-weight: 700;
            text-align: center;
            padding: 20px;
            background-color: #e8f5e9;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        .error-message {
            color: #f44336;
            font-size: 1.3em;
            font-weight: 700;
            text-align: center;
            padding: 20px;
            background-color: #ffebee;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        .download-button {
            display: inline-block;
            background-color: #4caf50;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 25px;
            font-weight: 500;
            margin-top: 10px;
            transition: all 0.3s ease;
        }
        .download-button:hover {
            background-color: white;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        .stMultiSelect > div > div {
            background-color: #fff;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Streamlit app
st.markdown("<h1 class='main-title'>Philippine Government Document Processing</h1>", unsafe_allow_html=True)

# Simulate pages with session state
if 'page' not in st.session_state:
    st.session_state.page = 1
if 'statuses' not in st.session_state:
    st.session_state.statuses = {}

if st.session_state.page == 1:
    st.markdown("<h2 class='section-title'>Select Your Documents</h2>", unsafe_allow_html=True)
    docs = ["LTO Driver's License", "DFA Passport", "NBI Clearance", "PSA Birth Certificate"]
    selected_docs = st.multiselect("Choose the documents you need to process:", docs)
    
    st.markdown("""
    <div class='instruction-text'>
        <p><strong>Instructions:</strong></p>
        <ol>
            <li>Select one or more documents from the list above.</li>
            <li>Click 'Next' to proceed to the information input step.</li>
            <li>Make sure you have all necessary documents ready for upload.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Next", key="next1"):
        if selected_docs:
            st.session_state.selected_docs = selected_docs
            st.session_state.page = 2
        else:
            st.markdown("<p class='error-message'>Please select at least one document to process.</p>", unsafe_allow_html=True)

elif st.session_state.page == 2:
    st.markdown("<h2 class='section-title'>Personal Information</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name")
    with col2:
        birthdate = st.date_input("Date of Birth")
    
    address = st.text_area("Complete Address")

    st.markdown("<h2 class='section-title'>Document Requirements</h2>", unsafe_allow_html=True)
    uploaded_files = {}

    for doc in st.session_state.selected_docs:
        st.markdown(f"<h3 class='section-title'>{doc}</h3>", unsafe_allow_html=True)
        for idx, instruction in enumerate(instructions[doc]):
            if "Upload" in instruction:
                key = f"{doc}_{instruction}_{idx}"
                uploaded_files[instruction] = st.file_uploader(instruction, type=["pdf", "jpg", "png"], key=key)
    
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button("Submit Application", key="submit"):
            # Assign reference numbers and statuses
            for doc in st.session_state.selected_docs:
                ref_number = random.randint(100000, 999999)
                st.session_state.statuses[doc] = {"Reference Number": ref_number, "Status": "Submitted"}
            st.session_state.page = 3

elif st.session_state.page == 3:
    st.markdown("<p class='success-message'>Your application has been successfully submitted!</p>", unsafe_allow_html=True)
    
    st.markdown("<h2 class='section-title'>Next Steps</h2>", unsafe_allow_html=True)
    for doc in st.session_state.selected_docs:
        st.markdown(f"<h3 class='section-title'>{doc} Instructions:</h3>", unsafe_allow_html=True)
        if doc == "LTO Driver's License":
            instructions_text = "Please visit your nearest LTO office with your completed form and uploaded documents."
        elif doc == "DFA Passport":
            instructions_text = "Schedule an appointment at your preferred DFA office and bring your completed form and uploaded documents."
        elif doc == "NBI Clearance":
            instructions_text = "Visit the nearest NBI office with your completed form and uploaded documents for processing."
        elif doc == "PSA Birth Certificate":
            instructions_text = "Submit your completed form and uploaded documents to the nearest PSA office or through their online portal."
        
        st.markdown(f"<p class='instruction-text'>{instructions_text}</p>", unsafe_allow_html=True)
    
    st.markdown("<h3 class='section-title'>Download Requirements Checklist</h3>", unsafe_allow_html=True)
    for doc in st.session_state.selected_docs:
        pdf_file = f"{doc}_requirements.pdf"
        generate_pdf(instructions[doc], pdf_file)
        st.markdown(create_download_link(pdf_file, f"Download {doc} Requirements"), unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button("Start New Application", key="new_application"):
            st.session_state.page = 1

    st.markdown("<h3 class='section-title'>Check Application Status</h3>", unsafe_allow_html=True)
    if st.button("Check Status", key="check_status"):
        st.session_state.page = 4

elif st.session_state.page == 4:
    st.markdown("<h2 class='section-title'>Application Status</h2>", unsafe_allow_html=True)
    
    for doc, details in st.session_state.statuses.items():
        st.markdown(f"<h3 class='section-title'>{doc}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p class='instruction-text'>Reference Number: {details['Reference Number']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='instruction-text'>Status: {details['Status']}</p>", unsafe_allow_html=True)

    if st.button("Refresh Status", key="refresh_status"):
        for doc in st.session_state.statuses:
            if st.session_state.statuses[doc]["Status"] == "Submitted":
                st.session_state.statuses[doc]["Status"] = "Processing"
            elif st.session_state.statuses[doc]["Status"] == "Processing":
                st.session_state.statuses[doc]["Status"] = "Ready for Pickup"

    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button("Start New Application", key="new_application_from_status"):
            st.session_state.page = 1
