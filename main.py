
import streamlit as st
import os
from database import create_table, add_cv, get_all_cvs, clear_database, update_cv_analysis, save_job_description, get_job_description, get_unanalyzed_cvs, save_analysis_result
from analyzer import analyze_cv
from PyPDF2 import PdfReader
from utils import parse_json_result, navigate_to_page

# --- App Setup ---
st.set_page_config(
    page_title="CV Analyzer",
    page_icon="📄",
    layout="wide"
)

# Initialize session state
if "current_page" not in st.session_state:
    st.session_state.current_page = "main"
if "selected_cv" not in st.session_state:
    st.session_state.selected_cv = None

# --- Navigation Logic ---
if st.session_state.current_page == "cv_details":
    from pages.cv_analysis_details import show_cv_details
    show_cv_details()
    st.stop()

elif st.session_state.current_page == "all_analyses":
    from pages.all_analyses import show_all_analyses
    show_all_analyses()
    st.stop()

# --- Main Page ---
st.title("📄 CV Analyzer")
create_table()

# --- Job Description Input ---
st.header("Job Description")
job_description = st.text_area("Enter the job description here:", value=get_job_description(), height=200)
if st.button("Save Job Description"):
    save_job_description(job_description)
    st.success("Job description saved!")

# --- File Uploader ---
st.header("Upload CVs")
uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)

if uploaded_files:
    cv_dir = "CV"
    if not os.path.exists(cv_dir):
        os.makedirs(cv_dir)

    for uploaded_file in uploaded_files:
        file_path = os.path.join(cv_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        add_cv(uploaded_file.name, file_path)

    st.success("Files uploaded successfully!")
    st.rerun()

# --- Analysis Button ---
st.header("Analyze CVs")
if st.button("Analyze Unanalyzed CVs"):
    if not job_description:
        st.warning("Please enter a job description before analyzing CVs.")
    else:
        unanalyzed_cvs = get_unanalyzed_cvs()
        if unanalyzed_cvs:
            st.info(f"Analyzing {len(unanalyzed_cvs)} unanalyzed CVs...")
            progress_bar = st.progress(0)
            successful_analyses = 0
            
            for i, (cv_name, cv_path) in enumerate(unanalyzed_cvs):
                try:
                    # Extract text from PDF
                    reader = PdfReader(cv_path)
                    cv_text = ""
                    for page in reader.pages:
                        cv_text += page.extract_text() + "\n"

                    # Analyze CV using Gemini API
                    analysis_result = analyze_cv(cv_text, job_description)

                    # Parse JSON result using utility function
                    analysis_data = parse_json_result(analysis_result)
                    
                    if analysis_data:
                        # Extract name and email for basic CV table
                        full_name = analysis_data.get("nombre_candidato", "N/A")
                        email = analysis_data.get("email", "N/A")
                        
                        # Save complete analysis to database
                        save_analysis_result(cv_name, analysis_data)
                        
                        # Update basic CV info
                        update_cv_analysis(cv_name, full_name, email)
                        
                        successful_analyses += 1
                        
                except Exception as e:
                    st.error(f"Error analyzing {cv_name}: {e}")
                    
                progress_bar.progress((i + 1) / len(unanalyzed_cvs))
            
            st.success(f"Analysis complete! Successfully analyzed {successful_analyses} out of {len(unanalyzed_cvs)} CVs.")
            st.rerun()
        else:
            st.info("No unanalyzed CVs found.")

# --- Display CVs ---
st.header("List of CVs")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Refresh List"):
        st.rerun()
with col2:
    if st.button("Clear Database"):
        clear_database()
        st.success("Database cleared!")
        st.rerun()

cv_list = get_all_cvs()

# Display the list of CVs as a table with action buttons
if cv_list:
    st.subheader("CV List")
    
    for name, analyzed, full_name, email in cv_list:
        col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 2])
        
        with col1:
            st.write(f"**{name}**")
        
        with col2:
            st.write("✅ Analyzed" if analyzed else "❌ Not Analyzed")
        
        with col3:
            st.write(full_name if full_name else "N/A")
        
        with col4:
            st.write(email if email else "N/A")
        
        with col5:
            if analyzed:
                if st.button(f"View Analysis", key=f"view_{name}"):
                    st.session_state.selected_cv = name
                    navigate_to_page("cv_details")
            else:
                st.write("Not available")
        
        st.divider()
else:
    st.write("No CVs found in the database.")

# --- Navigation to other pages ---
st.divider()
st.subheader("📊 Additional Views")

col1, col2 = st.columns(2)
with col1:
    if st.button("📊 View All Analyses"):
        navigate_to_page("all_analyses")

with col2:
    if st.button("📄 View CV Details"):
        navigate_to_page("cv_details")

