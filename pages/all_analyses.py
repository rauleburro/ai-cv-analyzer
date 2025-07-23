import streamlit as st
from database import get_all_analysis_results
from utils import display_analysis_summary, handle_no_data_message, back_to_main, navigate_to_page, get_score_color, get_score_level

def show_all_analyses():
    """Function to show all CV analyses page"""
    st.title("📊 All CV Analyses")

    # --- Get all analysis results ---
    analysis_results = get_all_analysis_results()

    if not analysis_results:
        handle_no_data_message("No analysis results found. Please analyze some CVs first.")
        return

    # --- Filters ---
    st.subheader("🔍 Filters")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        # Filter by candidate name
        all_names = list(set([result["nombre_candidato"] for result in analysis_results if result["nombre_candidato"] != "N/A"]))
        selected_name = st.selectbox(
            "Filter by Candidate Name:",
            ["All"] + all_names,
            index=0
        )

    with col2:
        # Filter by position
        all_positions = list(set([result["puesto_solicitado"] for result in analysis_results if result["puesto_solicitado"] != "N/A"]))
        selected_position = st.selectbox(
            "Filter by Position:",
            ["All"] + all_positions,
            index=0
        )

    with col3:
        # Filter by score range
        score_range = st.selectbox(
            "Filter by Score:",
            ["All Scores", "8.0-10.0 (Excellent)", "6.0-7.9 (Good)", "4.0-5.9 (Moderate)", "0.0-3.9 (Low)"],
            index=0
        )

    with col4:
        # Search functionality
        search_term = st.text_input("Search in analysis content:", placeholder="Enter keywords...")

    # --- Apply filters ---
    filtered_results = analysis_results

    if selected_name != "All":
        filtered_results = [r for r in filtered_results if r["nombre_candidato"] == selected_name]

    if selected_position != "All":
        filtered_results = [r for r in filtered_results if r["puesto_solicitado"] == selected_position]

    if score_range != "All Scores":
        if score_range == "8.0-10.0 (Excellent)":
            filtered_results = [r for r in filtered_results if r.get("score_fit", 0.0) >= 8.0]
        elif score_range == "6.0-7.9 (Good)":
            filtered_results = [r for r in filtered_results if 6.0 <= r.get("score_fit", 0.0) < 8.0]
        elif score_range == "4.0-5.9 (Moderate)":
            filtered_results = [r for r in filtered_results if 4.0 <= r.get("score_fit", 0.0) < 6.0]
        elif score_range == "0.0-3.9 (Low)":
            filtered_results = [r for r in filtered_results if r.get("score_fit", 0.0) < 4.0]

    if search_term:
        search_term_lower = search_term.lower()
        filtered_results = [r for r in filtered_results if 
                           search_term_lower in r["nombre_candidato"].lower() or
                           search_term_lower in r["resumen_idoneidad"].lower() or
                           any(search_term_lower in skill.lower() for skill in r["habilidades_coincidentes"]) or
                           any(search_term_lower in exp.lower() for exp in r["experiencia_coincidente"])]

    # --- Display results ---
    st.subheader(f"📋 Analysis Results ({len(filtered_results)} found)")

    if filtered_results:
        # Sort by score (highest first)
        filtered_results.sort(key=lambda x: x.get("score_fit", 0.0), reverse=True)
        
        # Create expandable sections for each analysis
        for i, result in enumerate(filtered_results):
            score = result.get("score_fit", 0.0)
            color = get_score_color(score)
            level = get_score_level(score)
            
            with st.expander(f"{color} {result['cv_name']} - {result['nombre_candidato']} (Score: {score:.1f}/10.0)", expanded=False):
                # Quick score overview
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Fit Score", f"{score:.1f}/10.0", f"{level}")
                with col2:
                    st.metric("Experience", result.get("nivel_experiencia", "N/A"))
                with col3:
                    st.metric("Recommendation", result.get("recomendacion", "N/A"))
                
                # Display analysis summary using utility function
                display_analysis_summary(result)
                
                # Action buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"View Full Analysis", key=f"view_full_{i}"):
                        st.session_state.selected_cv = result["cv_name"]
                        navigate_to_page("cv_details")
                
                with col2:
                    if st.button(f"Download Analysis", key=f"download_{i}"):
                        # TODO: Implement download functionality
                        st.info("Download functionality coming soon!")

    else:
        st.info("No results match the selected filters.")

    # --- Summary Statistics ---
    st.divider()
    st.subheader("📈 Summary Statistics")

    if analysis_results:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_analyses = len(analysis_results)
            st.metric("Total Analyses", total_analyses)
        
        with col2:
            unique_candidates = len(set([r["nombre_candidato"] for r in analysis_results if r["nombre_candidato"] != "N/A"]))
            st.metric("Unique Candidates", unique_candidates)
        
        with col3:
            avg_score = sum(r.get("score_fit", 0.0) for r in analysis_results) / len(analysis_results)
            st.metric("Avg Fit Score", f"{avg_score:.1f}/10.0")
        
        with col4:
            high_scores = len([r for r in analysis_results if r.get("score_fit", 0.0) >= 7.0])
            st.metric("High Scores (≥7.0)", high_scores)
        
        # Score distribution
        st.subheader("📊 Score Distribution")
        score_ranges = {
            "8.0-10.0 (Excellent)": len([r for r in analysis_results if r.get("score_fit", 0.0) >= 8.0]),
            "6.0-7.9 (Good)": len([r for r in analysis_results if 6.0 <= r.get("score_fit", 0.0) < 8.0]),
            "4.0-5.9 (Moderate)": len([r for r in analysis_results if 4.0 <= r.get("score_fit", 0.0) < 6.0]),
            "0.0-3.9 (Low)": len([r for r in analysis_results if r.get("score_fit", 0.0) < 4.0])
        }
        
        col1, col2, col3, col4 = st.columns(4)
        for i, (range_name, count) in enumerate(score_ranges.items()):
            with [col1, col2, col3, col4][i]:
                st.metric(range_name, count)

    # --- Navigation ---
    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        if st.button("← Back to Main Page"):
            back_to_main()

    with col2:
        if st.button("📊 View Individual Analysis"):
            navigate_to_page("cv_details")

# For direct execution as a page
if __name__ == "__main__":
    st.set_page_config(
        page_title="All CV Analyses",
        page_icon="📊",
        layout="wide"
    )
    show_all_analyses() 