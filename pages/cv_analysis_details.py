import streamlit as st
from database import get_analysis_result, get_all_cvs
from utils import display_analysis_metrics, display_analysis_details, show_navigation_buttons, handle_no_data_message, back_to_main, get_score_color, get_score_level

def show_cv_details():
    """Function to show CV analysis details page"""
    st.title("📊 CV Analysis Details")

    # --- CV Selection ---
    cv_list = get_all_cvs()
    analyzed_cvs = [(name, full_name) for name, analyzed, full_name, email in cv_list if analyzed]

    if not analyzed_cvs:
        handle_no_data_message("No analyzed CVs found. Please analyze some CVs first.")
        return

    # Get selected CV from session state or URL params
    selected_cv = st.session_state.get("selected_cv", None)

    if not selected_cv:
        # Show CV selection dropdown
        st.subheader("Select a CV to view analysis details:")
        
        cv_options = {f"{name} ({full_name})" if full_name != "N/A" else name: name 
                      for name, full_name in analyzed_cvs}
        
        selected_option = st.selectbox(
            "Choose a CV:",
            options=list(cv_options.keys()),
            index=0
        )
        
        selected_cv = cv_options[selected_option]

    # --- Display Analysis ---
    if selected_cv:
        analysis_result = get_analysis_result(selected_cv)
        
        if analysis_result:
            # Header with CV name
            st.subheader(f"📄 Analysis for: {selected_cv}")
            
            # Display metrics using utility function
            display_analysis_metrics(analysis_result)
            
            # Special score visualization
            score = analysis_result.get("score_fit", 0.0)
            color = get_score_color(score)
            level = get_score_level(score)
            
            st.divider()
            st.subheader(f"{color} Fit Score Analysis")
            
            # Progress bar for score
            col1, col2 = st.columns([3, 1])
            with col1:
                st.progress(score / 10.0)
            with col2:
                st.metric("Score", f"{score:.1f}/10.0", f"{level}")
            
            # Score interpretation
            if score >= 8.0:
                st.success("🎉 **Excellent Fit:** This candidate is highly qualified and would be an excellent addition to the team.")
            elif score >= 6.0:
                st.info("✅ **Good Fit:** This candidate meets most requirements and would be a good fit for the position.")
            elif score >= 4.0:
                st.warning("⚠️ **Moderate Fit:** This candidate has potential but may need additional training or support.")
            elif score >= 2.0:
                st.error("❌ **Poor Fit:** This candidate may not be suitable for the position without significant training.")
            else:
                st.error("🚫 **Not Suitable:** This candidate does not meet the basic requirements for the position.")
            
            st.divider()
            
            # Display detailed analysis using utility function
            display_analysis_details(analysis_result)
            
            # Navigation buttons using utility function
            st.divider()
            show_navigation_buttons()
                    
        else:
            st.error(f"No analysis found for {selected_cv}")
            if st.button("← Back to Main Page"):
                back_to_main()
    else:
        st.info("Please select a CV to view its analysis details.")
        if st.button("← Back to Main Page"):
            back_to_main()

# For direct execution as a page
if __name__ == "__main__":
    st.set_page_config(
        page_title="CV Analysis Details",
        page_icon="📊",
        layout="wide"
    )
    show_cv_details() 