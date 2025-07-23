import streamlit as st
from database import get_analysis_result
import json

def navigate_to_page(page_name):
    """Centralized navigation function"""
    st.session_state.current_page = page_name
    st.rerun()

def back_to_main():
    """Navigate back to main page"""
    navigate_to_page("main")

def show_back_button():
    """Show back button with consistent styling"""
    if st.button("← Back to Main Page"):
        back_to_main()

def show_navigation_buttons():
    """Show consistent navigation buttons"""
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("← Back to Main Page"):
            back_to_main()
    
    with col2:
        if st.button("🔄 Select Different CV"):
            if "selected_cv" in st.session_state:
                del st.session_state.selected_cv
            st.rerun()
    
    with col3:
        if st.button("📊 View All Analyses"):
            navigate_to_page("all_analyses")

def get_score_color(score):
    """Get color based on score"""
    if score >= 8.0:
        return "🟢"  # Green
    elif score >= 6.0:
        return "🟡"  # Yellow
    elif score >= 4.0:
        return "🟠"  # Orange
    else:
        return "🔴"  # Red

def get_score_level(score):
    """Get score level description"""
    if score >= 8.0:
        return "Excelente"
    elif score >= 6.0:
        return "Bueno"
    elif score >= 4.0:
        return "Moderado"
    elif score >= 2.0:
        return "Bajo"
    else:
        return "Muy Bajo"

def display_analysis_metrics(analysis_result):
    """Display analysis metrics in a consistent format"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Candidate Name", 
            analysis_result["nombre_candidato"],
            help="Full name extracted from CV"
        )
    
    with col2:
        st.metric(
            "Email", 
            analysis_result["email"],
            help="Email address from CV"
        )
    
    with col3:
        st.metric(
            "Position", 
            analysis_result["puesto_solicitado"],
            help="Target position"
        )
    
    with col4:
        st.metric(
            "Analysis Date", 
            analysis_result["analysis_date"][:10] if analysis_result["analysis_date"] else "N/A",
            help="Date when analysis was performed"
        )
    
    # Score section with visual indicators
    st.divider()
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        score = analysis_result.get("score_fit", 0.0)
        color = get_score_color(score)
        level = get_score_level(score)
        st.metric(
            f"{color} Fit Score", 
            f"{score:.1f}/10.0",
            f"({level})",
            help="Score from 0.0 to 10.0 indicating how well the candidate fits the position"
        )
    
    with col2:
        st.metric(
            "Experience Level", 
            analysis_result.get("nivel_experiencia", "N/A"),
            help="Junior, Mid, Senior level"
        )
    
    with col3:
        st.metric(
            "Experience Time", 
            analysis_result.get("tiempo_experiencia", "N/A"),
            help="Years of relevant experience"
        )
    
    with col4:
        st.metric(
            "Recommendation", 
            analysis_result.get("recomendacion", "N/A"),
            help="HR recommendation for the candidate"
        )

def display_analysis_details(analysis_result):
    """Display detailed analysis sections"""
    col1, col2 = st.columns(2)
    
    with col1:
        # Matching Skills
        st.subheader("🎯 Matching Skills")
        if analysis_result["habilidades_coincidentes"]:
            for i, skill in enumerate(analysis_result["habilidades_coincidentes"], 1):
                st.write(f"{i}. {skill}")
        else:
            st.info("No matching skills identified.")
        
        st.divider()
        
        # Matching Experience
        st.subheader("💼 Matching Experience")
        if analysis_result["experiencia_coincidente"]:
            for i, exp in enumerate(analysis_result["experiencia_coincidente"], 1):
                st.write(f"{i}. {exp}")
        else:
            st.info("No matching experience identified.")
        
        st.divider()
        
        # Strengths
        st.subheader("💪 Strengths")
        if analysis_result.get("fortalezas"):
            for i, strength in enumerate(analysis_result["fortalezas"], 1):
                st.write(f"{i}. {strength}")
        else:
            st.info("No specific strengths identified.")
    
    with col2:
        # Areas for Improvement
        st.subheader("📈 Areas for Improvement")
        if analysis_result["puntos_de_mejora"]:
            for i, area in enumerate(analysis_result["puntos_de_mejora"], 1):
                st.write(f"{i}. {area}")
        else:
            st.info("No specific areas for improvement identified.")
        
        st.divider()
        
        # Risks
        st.subheader("⚠️ Risks")
        if analysis_result.get("riesgos"):
            for i, risk in enumerate(analysis_result["riesgos"], 1):
                st.write(f"{i}. {risk}")
        else:
            st.info("No specific risks identified.")
        
        st.divider()
        
        # Suitability Summary
        st.subheader("📋 Suitability Summary")
        st.write(analysis_result["resumen_idoneidad"])

def display_analysis_summary(result):
    """Display analysis summary for list views"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Email:** {result['email']}")
        st.write(f"**Position:** {result['puesto_solicitado']}")
        st.write(f"**Analysis Date:** {result['analysis_date'][:10] if result['analysis_date'] else 'N/A'}")
        
        # Score display
        score = result.get("score_fit", 0.0)
        color = get_score_color(score)
        level = get_score_level(score)
        st.write(f"**{color} Fit Score:** {score:.1f}/10.0 ({level})")
        
        # Experience info
        st.write(f"**Experience Level:** {result.get('nivel_experiencia', 'N/A')}")
        st.write(f"**Experience Time:** {result.get('tiempo_experiencia', 'N/A')}")
        st.write(f"**Recommendation:** {result.get('recomendacion', 'N/A')}")
        
        # Matching Skills
        st.write("**🎯 Matching Skills:**")
        if result["habilidades_coincidentes"]:
            for skill in result["habilidades_coincidentes"]:
                st.write(f"• {skill}")
        else:
            st.write("No matching skills identified.")
        
        # Matching Experience
        st.write("**💼 Matching Experience:**")
        if result["experiencia_coincidente"]:
            for exp in result["experiencia_coincidente"]:
                st.write(f"• {exp}")
        else:
            st.write("No matching experience identified.")
    
    with col2:
        # Areas for Improvement
        st.write("**📈 Areas for Improvement:**")
        if result["puntos_de_mejora"]:
            for area in result["puntos_de_mejora"]:
                st.write(f"• {area}")
        else:
            st.write("No specific areas for improvement identified.")
        
        st.divider()
        
        # Strengths
        st.write("**💪 Strengths:**")
        if result.get("fortalezas"):
            for strength in result["fortalezas"]:
                st.write(f"• {strength}")
        else:
            st.write("No specific strengths identified.")
        
        st.divider()
        
        # Risks
        st.write("**⚠️ Risks:**")
        if result.get("riesgos"):
            for risk in result["riesgos"]:
                st.write(f"• {risk}")
        else:
            st.write("No specific risks identified.")
        
        st.divider()
        
        # Suitability Summary
        st.write("**📋 Suitability Summary:**")
        st.write(result["resumen_idoneidad"])

def handle_no_data_message(message, show_back=True):
    """Handle no data scenarios consistently"""
    st.warning(message)
    if show_back:
        show_back_button()
    return False

def parse_json_result(analysis_result):
    """Parse JSON result from analyzer with error handling"""
    try:
        # Clean the result to extract JSON
        result_text = analysis_result.strip()
        if result_text.startswith("```json"):
            result_text = result_text[7:]
        if result_text.endswith("```"):
            result_text = result_text[:-3]
        
        return json.loads(result_text)
    except json.JSONDecodeError as json_error:
        st.error(f"Error parsing JSON result: {json_error}")
        st.write("Raw result:", analysis_result)
        return None 