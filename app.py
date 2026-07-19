"""
HireSense AI - AI Resume Analyzer & Smart Recruitment Platform
Main Application File
"""

import streamlit as st
import os
import sys
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Load local, untracked credentials and configuration before initializing clients.
load_dotenv(project_root / ".env")

# Page configuration
st.set_page_config(
    page_title="HireSense AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS and JavaScript
def load_custom_styles():
    """Load custom CSS styles."""
    css_path = project_root / "css" / "styles.css"
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def load_custom_scripts():
    """Load custom JavaScript."""
    js_path = project_root / "assets" / "animations.js"
    if js_path.exists():
        with open(js_path) as f:
            st.markdown(f"<script>{f.read()}</script>", unsafe_allow_html=True)

# Load styles and scripts
load_custom_styles()
load_custom_scripts()

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'language' not in st.session_state:
    st.session_state.language = 'english'
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None
if 'hr_candidates' not in st.session_state:
    st.session_state.hr_candidates = []

# Navigation
def navigate_to(page):
    """Navigate to specified page."""
    st.session_state.page = page
    st.rerun()

# Landing Page
def show_landing_page():
    """Display premium landing page with animations."""
    # Aurora background
    st.markdown("""
    <div class="aurora-background"></div>
    """, unsafe_allow_html=True)
    
    # Hero Section - HireSense at top with minimal margin
    st.markdown("""
    <div class="hero" style="min-height: 5vh; padding: 5px 0; margin-top: 0; margin-bottom: 0;">
        <div class="hero-content" style="text-align: center;">
            <h1 class="hero-title gradient-text" style="font-size: 40px; margin-bottom: 2px; animation: titlePulse 3s infinite;">HireSense AI</h1>
            <p class="hero-subtitle" style="font-size: 13px; margin-bottom: 1px;">AI Resume Analyzer & Smart Recruitment Platform</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quote Section - minimal margin
    st.markdown("""
    <div style="text-align: center; margin: 5px 0; padding: 5px;">
        <p style="font-size: 15px; color: var(--accent-primary); font-style: italic; font-weight: 500;">
            "Transform Your Resume, Transform Your Career"
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Premium Glass Cards - Smaller, clickable, no buttons
    col1, col2 = st.columns(2, gap="medium")
    
    with col1:
        # Clickable card using HTML
        st.markdown("""
        <div class="premium-glass-card card-3d glow-effect animated-card clickable-card" 
             style="padding: 16px; text-align: center; min-height: 200px; cursor: pointer;">
            <div class="card-3d-inner">
                <div style="font-size: 48px; margin-bottom: 8px; animation: iconJump 3s infinite;">👨</div>
                <h2 style="margin-bottom: 12px; font-size: 24px;">Candidate</h2>
                <ul style="text-align: left; color: var(--text-secondary); margin-bottom: 16px; line-height: 1.8; font-size: 14px;">
                    <li>✨ Analyze Resume</li>
                    <li>📈 Resume Improvement</li>
                    <li>🎯 ATS Optimization</li>
                    <li>❓ Interview Questions</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Candidate", key="candidate_btn", use_container_width=True):
            navigate_to('candidate')
    
    with col2:
        st.markdown("""
        <div class="premium-glass-card card-3d glow-effect animated-card clickable-card" 
             style="padding: 16px; text-align: center; min-height: 200px; cursor: pointer; animation-delay: 1.5s;">
            <div class="card-3d-inner">
                <div style="font-size: 48px; margin-bottom: 8px; animation: iconJump 3s infinite; animation-delay: 1.5s;">🏢</div>
                <h2 style="margin-bottom: 12px; font-size: 24px;">HR Recruiter</h2>
                <ul style="text-align: left; color: var(--text-secondary); margin-bottom: 16px; line-height: 1.8; font-size: 14px;">
                    <li>📊 Bulk Resume Screening</li>
                    <li>🏆 Candidate Ranking</li>
                    <li>🎯 Skill Matrix</li>
                    <li>📋 Hiring Dashboard</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("HR Recruiter", key="hr_btn", use_container_width=True):
            navigate_to('recruiter')
    
    # Add custom animations and Netflix theme
    st.markdown("""
    <style>
    @keyframes titlePulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    @keyframes iconJump {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-8px); }
    }
    
    @keyframes cardColorChange {
        0% { border-color: #E50914; }
        33% { border-color: #E50914; }
        66% { border-color: #E50914; }
        100% { border-color: #E50914; }
    }
    
    @keyframes cardZoom {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    @keyframes redLineFlow {
        0% { width: 0%; left: 0; }
        50% { width: 100%; left: 0; }
        100% { width: 0%; left: 100%; }
    }
    
    .animated-card {
        animation: cardColorChange 3s infinite, cardZoom 3s infinite;
    }
    
    .clickable-card:hover {
        transform: scale(1.05);
        box-shadow: 0 0 20px rgba(229, 9, 20, 0.5);
    }
    
    /* Hide Streamlit buttons completely */
    button[data-testid="candidate_btn"], button[data-testid="hr_btn"] {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        width: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        opacity: 0 !important;
        position: fixed !important;
        top: -9999px !important;
        left: -9999px !important;
    }
    
    /* Animated red line between title and quote */
    .hero-content::after {
        content: '';
        display: block;
        width: 0%;
        height: 3px;
        background: linear-gradient(90deg, transparent, #E50914, transparent);
        animation: redLineFlow 3s infinite;
        margin: 8px auto 0;
    }
    
    /* Netflix Theme Colors */
    :root {
        --netflix-bg: #141414;
        --netflix-red: #E50914;
        --netflix-card-bg: #1F1F1F;
        --netflix-card-secondary: #2B2B2B;
        --netflix-text-primary: #FFFFFF;
        --netflix-text-secondary: #B3B3B3;
        --netflix-text-muted: #808080;
        --netflix-border: #333333;
        --netflix-hover: #2D2D2D;
    }
    
    body {
        background-color: var(--netflix-bg) !important;
    }
    
    .stApp {
        background-color: var(--netflix-bg) !important;
    }
    
    .premium-glass-card {
        background-color: var(--netflix-card-bg) !important;
        border: 1px solid var(--netflix-border) !important;
    }
    
    .gradient-text {
        background: linear-gradient(135deg, #E50914, #ff6b6b) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Footer - reduced margin
    st.markdown("""
    <div style="text-align: center; margin-top: 8px; color: var(--netflix-text-muted); font-size: 11px;">
        <p>Built with ❤️ using AI-Powered Resume Analysis</p>
    </div>
    """, unsafe_allow_html=True)

# Candidate Module
def show_candidate_module():
    """Display candidate analysis module."""
    st.markdown("""
    <div class="aurora-background"></div>
    """, unsafe_allow_html=True)
    
    # Header
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; margin: 48px 0;">
            <h1 class="gradient-text">Candidate Analysis</h1>
            <p style="color: var(--text-secondary);">Upload your resume and get AI-powered insights</p>
        </div>
        """, unsafe_allow_html=True)
    
    # File upload
    st.markdown("<br>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Upload Your Resume",
        type=['pdf', 'docx', 'png', 'jpg', 'jpeg'],
        label_visibility="collapsed"
    )
    
    # Job description input
    col1, col2 = st.columns(2)
    with col1:
        job_role = st.text_input("Job Role (Optional)", placeholder="e.g., Software Engineer")
    with col2:
        job_description = st.text_area(
            "Job Description (Optional)",
            placeholder="Paste the job description here...",
            height=100
        )
    
    # Certificate upload
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Certificates (Optional)")
    certificate_files = st.file_uploader(
        "Upload Certificates",
        type=['pdf', 'png', 'jpg', 'jpeg'],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )
    
    # Analyze button
    st.markdown("<br>", unsafe_allow_html=True)
    analyze_col1, analyze_col2, analyze_col3 = st.columns([1, 1, 1])
    with analyze_col2:
        if st.button("Analyze Resume", use_container_width=True, type="primary"):
            if uploaded_file:
                with st.spinner("🧠 Analyzing your resume..."):
                    # Import analysis modules
                    from utils.document_extractor import DocumentExtractor
                    from core.ai.llm_factory import LLMFactory
                    from utils.certificate_analyzer import CertificateAnalyzer
                    from utils.translator import Translator
                    
                    # Initialize clients
                    document_extractor = DocumentExtractor()
                    llm_client = LLMFactory.create()
                    certificate_analyzer = CertificateAnalyzer(llm_client)
                    translator = Translator(llm_client)
                    
                    # Save uploaded file
                    upload_dir = project_root / "uploads"
                    upload_dir.mkdir(exist_ok=True)
                    
                    file_path = upload_dir / uploaded_file.name
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Extract text
                    with st.spinner("✓ Extracting Text..."):
                        resume_text = document_extractor.extract_text(str(file_path))
                    
                    # Analyze resume
                    with st.spinner("✓ AI Analysis in Progress..."):
                        analysis_result = llm_client.analyze_resume(
                            resume_text,
                            job_description if job_description else None,
                            job_role if job_role else None
                        )
                    
                    # Debug: Show analysis result status
                    if not analysis_result.success:
                        st.error(f"Analysis failed: {analysis_result.error}")
                        st.session_state.analysis_result = {
                            'resume_analysis': {},
                            'resume_text': resume_text,
                            'job_role': job_role,
                            'job_description': job_description,
                            'certificates': [],
                            'language': st.session_state.language,
                            'error': analysis_result.error
                        }
                    else:
                        # Analyze certificates if provided
                        certificate_results = []
                        if certificate_files:
                            with st.spinner("✓ Analyzing Certificates..."):
                                for cert_file in certificate_files:
                                    cert_path = upload_dir / cert_file.name
                                    with open(cert_path, "wb") as f:
                                        f.write(cert_file.getbuffer())
                                    
                                    try:
                                        cert_result = certificate_analyzer.analyze_certificate(
                                            certificate_file=str(cert_path),
                                            resume_text=resume_text,
                                            target_role=job_role if job_role else None
                                        )
                                        certificate_results.append(cert_result)
                                    except Exception as cert_error:
                                        st.warning(f"Certificate analysis failed: {str(cert_error)}")
                        
                        # Store results
                        st.session_state.analysis_result = {
                            'resume_analysis': analysis_result.data if analysis_result.data else {},
                            'resume_text': resume_text,
                            'job_role': job_role,
                            'job_description': job_description,
                            'certificates': certificate_results,
                            'language': st.session_state.language
                        }
                        
                        st.success("✓ Analysis Complete!")
                        st.rerun()
            else:
                st.error("Please upload a resume file")
    
    # Display results
    if st.session_state.analysis_result:
        display_candidate_results()
    
    # Back button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Back to Home", use_container_width=False):
        navigate_to('home')

def display_candidate_results():
    """Display candidate analysis results with new comprehensive sections."""
    result = st.session_state.analysis_result
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="glass-card" style="padding: 32px; margin-bottom: 24px;">
        <h2 class="gradient-text">Resume Analysis Results</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Check for errors
    if 'error' in result:
        st.error(f"Analysis Error: {result['error']}")
        st.info("The analysis encountered an error. Please try again or check your API key.")
        return
    
    # Get analysis data
    analysis = result.get('resume_analysis', {})
    
    # Check if analysis has expected data
    if not analysis or not isinstance(analysis, dict):
        st.warning("Analysis returned empty data. This might be due to API issues.")
        st.json(result)  # Show raw data for debugging
        return
    
    # Score cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        score = analysis.get('overall_score', 0)
        score_color = "green" if score >= 80 else "yellow" if score >= 60 else "red"
        st.markdown(f"""
        <div class="score-card">
            <div class="score-value">{score}</div>
            <div class="score-label">Overall Score</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        ats_score = analysis.get('ats_score', 0)
        st.markdown(f"""
        <div class="score-card">
            <div class="score-value">{ats_score}</div>
            <div class="score-label">ATS Score</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        grammar_score = analysis.get('grammar_score', 0)
        st.markdown(f"""
        <div class="score-card">
            <div class="score-value">{grammar_score}</div>
            <div class="score-label">Grammar</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        communication_score = analysis.get('communication_score', 0)
        st.markdown(f"""
        <div class="score-card">
            <div class="score-value">{communication_score}</div>
            <div class="score-label">Communication</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
        "📊 Summary", "💪 Strengths", "⚠️ Weaknesses", "🚀 Improvements", 
        "📚 Missing Skills", "📋 Missing Sections", "🎯 ATS Analysis", 
        "✍️ Rewrite Suggestions", "❓ Interview Questions"
    ])
    
    # Tab 1: Summary / Recruiter Verdict
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        
        if 'recruiter_verdict' in analysis:
            verdict = analysis['recruiter_verdict']
            
            # Hire Confidence
            hire_confidence = verdict.get('hire_confidence', 0)
            confidence_color = "green" if hire_confidence >= 80 else "yellow" if hire_confidence >= 60 else "red"
            
            st.markdown(f"""
            <div class="glass-card" style="padding: 24px;">
                <h3>🎯 Final Recruiter Verdict</h3>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="glass-card" style="padding: 20px; text-align: center;">
                    <h4 style="color: var(--text-secondary); margin-bottom: 8px;">Hire Confidence</h4>
                    <div style="font-size: 48px; font-weight: bold; color: var(--accent-primary);">{hire_confidence}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                readiness = verdict.get('resume_readiness', 'N/A')
                readiness_color = "green" if readiness == "Excellent" or readiness == "Ready" else "yellow" if readiness == "Needs Work" else "red"
                st.markdown(f"""
                <div class="glass-card" style="padding: 20px; text-align: center;">
                    <h4 style="color: var(--text-secondary); margin-bottom: 8px;">Resume Readiness</h4>
                    <div style="font-size: 32px; font-weight: bold; color: var(--accent-primary);">{readiness}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Recommendation
            st.markdown(f"""
            <div class="glass-card" style="padding: 20px;">
                <h4 style="color: var(--accent-primary); margin-bottom: 12px;">Recommendation</h4>
                <p style="font-size: 18px;">{verdict.get('overall_recommendation', 'No recommendation available')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # One-line summary
            st.markdown(f"""
            <div class="glass-card" style="padding: 20px;">
                <h4 style="color: var(--accent-primary); margin-bottom: 12px;">Summary</h4>
                <p style="font-style: italic;">"{verdict.get('one_line_summary', 'No summary available')}"</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Critical Improvements
            critical_improvements = verdict.get('critical_improvements', [])
            if critical_improvements:
                st.markdown("""
                <div class="glass-card" style="padding: 24px;">
                    <h3>🔥 Critical Improvements Before Applying</h3>
                </div>
                """, unsafe_allow_html=True)
                
                for improvement in critical_improvements:
                    st.markdown(f"""
                    <div class="glass-card" style="padding: 16px; margin-top: 12px; border-left: 4px solid var(--accent-primary);">
                        <p>• {improvement}</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Tab 2: Strengths
    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="glass-card" style="padding: 24px; margin-bottom: 20px;">
            <h3 style="color: #E50914; font-size: 24px; margin-bottom: 8px;">💪 Resume Strengths</h3>
            <p style="color: #B3B3B3; font-size: 14px;">Key strengths that make your resume stand out</p>
        </div>
        """, unsafe_allow_html=True)
        
        strengths = analysis.get('strengths', [])
        if strengths:
            for i, strength in enumerate(strengths, 1):
                st.markdown(f"""
                <div class="glass-card" style="padding: 20px; margin-bottom: 16px; border-left: 4px solid #E50914; background: linear-gradient(135deg, #1F1F1F, #2B2B2B);">
                    <div style="display: flex; align-items: center; margin-bottom: 12px;">
                        <div style="background: #E50914; color: white; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 12px;">{i}</div>
                        <h4 style="color: #FFFFFF; font-size: 18px; margin: 0;">{strength.get('title', 'Strength')}</h4>
                    </div>
                    <div style="margin-left: 44px;">
                        <p style="color: #00ff88; font-weight: 600; margin-bottom: 6px; font-size: 14px;">✅ Why it is good:</p>
                        <p style="color: #B3B3B3; margin-bottom: 12px; line-height: 1.6;">{strength.get('why_good', 'N/A')}</p>
                        <p style="color: #00ff88; font-weight: 600; margin-bottom: 6px; font-size: 14px;">🎯 Recruiter Impact:</p>
                        <p style="color: #B3B3B3; line-height: 1.6;">{strength.get('recruiter_impact', 'N/A')}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No strengths identified.")
    
    # Tab 3: Weaknesses
    with tab3:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="glass-card" style="padding: 24px; margin-bottom: 20px;">
            <h3 style="color: #E50914; font-size: 24px; margin-bottom: 8px;">⚠️ Resume Weaknesses</h3>
            <p style="color: #B3B3B3; font-size: 14px;">Areas that need improvement to boost your resume</p>
        </div>
        """, unsafe_allow_html=True)
        
        weaknesses = analysis.get('weaknesses', [])
        if weaknesses:
            for i, weakness in enumerate(weaknesses, 1):
                ats_impact = weakness.get('ats_impact', 'Medium')
                ats_color = "#ff6b6b" if ats_impact == "High" else "#ffd93d" if ats_impact == "Medium" else "#6bcb77"
                
                st.markdown(f"""
                <div class="glass-card" style="padding: 20px; margin-bottom: 16px; border-left: 4px solid #ff6b6b; background: linear-gradient(135deg, #1F1F1F, #2B2B2B);">
                    <div style="display: flex; align-items: center; margin-bottom: 12px;">
                        <div style="background: #ff6b6b; color: white; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 12px;">{i}</div>
                        <h4 style="color: #FFFFFF; font-size: 18px; margin: 0;">{weakness.get('title', 'Weakness')}</h4>
                    </div>
                    <div style="margin-left: 44px;">
                        <p style="color: #ff6b6b; font-weight: 600; margin-bottom: 6px; font-size: 14px;">❌ Why this is hurting:</p>
                        <p style="color: #B3B3B3; margin-bottom: 12px; line-height: 1.6;">{weakness.get('why_hurting', 'N/A')}</p>
                        <p style="color: #ff6b6b; font-weight: 600; margin-bottom: 6px; font-size: 14px;">📊 ATS Impact: <span style="color: {ats_color};">{ats_impact}</span></p>
                        <p style="color: #ff6b6b; font-weight: 600; margin-bottom: 6px; font-size: 14px;">👥 Recruiter Impact:</p>
                        <p style="color: #B3B3B3; line-height: 1.6;">{weakness.get('recruiter_impact', 'N/A')}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No weaknesses identified. Great job!")
    
    # Tab 4: Improvement Suggestions
    with tab4:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="glass-card" style="padding: 24px; margin-bottom: 20px;">
            <h3 style="color: #E50914; font-size: 24px; margin-bottom: 8px;">🚀 Improvement Suggestions</h3>
            <p style="color: #B3B3B3; font-size: 14px;">Actionable steps to enhance your resume</p>
        </div>
        """, unsafe_allow_html=True)
        
        suggestions = analysis.get('improvement_suggestions', [])
        if suggestions:
            for i, suggestion in enumerate(suggestions, 1):
                st.markdown(f"""
                <div class="glass-card" style="padding: 20px; margin-bottom: 16px; border-left: 4px solid #ffd93d; background: linear-gradient(135deg, #1F1F1F, #2B2B2B);">
                    <div style="display: flex; align-items: center; margin-bottom: 12px;">
                        <div style="background: #ffd93d; color: #141414; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 12px;">{i}</div>
                        <h4 style="color: #FFFFFF; font-size: 18px; margin: 0;">{suggestion.get('suggestion', 'Suggestion')}</h4>
                    </div>
                    <div style="margin-left: 44px;">
                        <p style="color: #ffd93d; font-weight: 600; margin-bottom: 6px; font-size: 14px;">💡 Suggestion:</p>
                        <p style="color: #B3B3B3; margin-bottom: 12px; line-height: 1.6;">{suggestion.get('suggestion', 'N/A')}</p>
                        <p style="color: #ffd93d; font-weight: 600; margin-bottom: 6px; font-size: 14px;">🛠 How to implement:</p>
                        <p style="color: #B3B3B3; margin-bottom: 12px; line-height: 1.6;">{suggestion.get('how_to_implement', 'N/A')}</p>
                        <p style="color: #ffd93d; font-weight: 600; margin-bottom: 6px; font-size: 14px;">⭐ Expected Impact:</p>
                        <p style="color: #B3B3B3; line-height: 1.6;">{suggestion.get('expected_impact', 'N/A')}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No improvement suggestions at this time.")
    
    # Tab 5: Missing Skills
    with tab5:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="glass-card" style="padding: 24px; margin-bottom: 20px;">
            <h3 style="color: #E50914; font-size: 24px; margin-bottom: 8px;">📚 Missing Skills</h3>
            <p style="color: #B3B3B3; font-size: 14px;">Skills that could strengthen your resume</p>
        </div>
        """, unsafe_allow_html=True)
        
        missing_skills = analysis.get('missing_skills', [])
        if missing_skills:
            for i, skill in enumerate(missing_skills, 1):
                importance = skill.get('importance', 'Medium')
                importance_color = "#ff6b6b" if importance == "High" else "#ffd93d" if importance == "Medium" else "#6bcb77"
                
                st.markdown(f"""
                <div class="glass-card" style="padding: 20px; margin-bottom: 16px; border-left: 4px solid {importance_color}; background: linear-gradient(135deg, #1F1F1F, #2B2B2B);">
                    <div style="display: flex; align-items: center; margin-bottom: 12px;">
                        <div style="background: {importance_color}; color: #141414; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 12px;">{i}</div>
                        <h4 style="color: #FFFFFF; font-size: 18px; margin: 0;">{skill.get('skill', 'Skill')}</h4>
                        <span style="background: {importance_color}; color: #141414; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 600; margin-left: auto;">{importance}</span>
                    </div>
                    <div style="margin-left: 44px;">
                        <p style="color: {importance_color}; font-weight: 600; margin-bottom: 6px; font-size: 14px;">❓ Reason:</p>
                        <p style="color: #B3B3B3; margin-bottom: 12px; line-height: 1.6;">{skill.get('reason', 'N/A')}</p>
                        <p style="color: {importance_color}; font-weight: 600; margin-bottom: 6px; font-size: 14px;">📖 Learning Resources:</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                resources = skill.get('learning_resources', [])
                if resources:
                    for resource in resources:
                        st.markdown(f"""
                        <div style="padding: 12px; margin-left: 60px; margin-bottom: 8px; border-left: 2px solid #E50914; background: #2B2B2B;">
                            <p style="color: #B3B3B3; margin: 0;">• {resource}</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("<p style='color: #808080; margin-left: 60px;'>No specific resources provided.</p>", unsafe_allow_html=True)
        else:
            st.info("No missing skills identified. Excellent!")
    
    # Tab 6: Missing Resume Sections
    with tab6:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="glass-card" style="padding: 24px;">
            <h3>📋 Missing Resume Sections</h3>
        </div>
        """, unsafe_allow_html=True)
        
        missing_sections = analysis.get('missing_resume_sections', [])
        if missing_sections:
            for i, section in enumerate(missing_sections, 1):
                with st.expander(f"{i}. {section.get('section', 'Section')}", expanded=True):
                    st.markdown(f"""
                    <div style="padding: 12px;">
                        <p style="color: var(--accent-primary); font-weight: 600; margin-bottom: 8px;">❓ Why it matters:</p>
                        <p style="margin-bottom: 12px;">{section.get('why_matters', 'N/A')}</p>
                        
                        <p style="color: var(--accent-primary); font-weight: 600; margin-bottom: 8px;">✍️ How to write it:</p>
                        <p>{section.get('how_to_write', 'N/A')}</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.success("All important resume sections are present!")
    
    # Tab 7: ATS Analysis
    with tab7:
        st.markdown("<br>", unsafe_allow_html=True)
        
        if 'ats_analysis' in analysis:
            ats = analysis['ats_analysis']
            
            st.markdown("""
            <div class="glass-card" style="padding: 24px;">
                <h3>🎯 ATS Optimization Analysis</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # ATS Compatibility
            compatibility = ats.get('ats_compatibility', 'Medium')
            compat_color = "green" if compatibility == "High" else "yellow" if compatibility == "Medium" else "red"
            
            st.markdown(f"""
            <div class="glass-card" style="padding: 20px; text-align: center;">
                <h4 style="color: var(--text-secondary); margin-bottom: 8px;">ATS Compatibility</h4>
                <div style="font-size: 36px; font-weight: bold; color: var(--{compat_color});">{compatibility}</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Keyword Density
            density = ats.get('keyword_density', 'N/A')
            st.markdown(f"""
            <div class="glass-card" style="padding: 20px;">
                <h4 style="color: var(--accent-primary); margin-bottom: 8px;">Keyword Density</h4>
                <p style="font-size: 24px; font-weight: bold;">{density}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Matched Keywords
            matched = ats.get('matched_keywords', [])
            if matched:
                st.markdown("""
                <div class="glass-card" style="padding: 24px;">
                    <h4 style="color: var(--accent-primary);">✅ Matched Keywords</h4>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    for keyword in matched[:len(matched)//2]:
                        st.markdown(f"""
                        <div style="padding: 8px; margin-top: 8px; background: rgba(0, 255, 128, 0.1); border-radius: 8px;">
                            <p>✓ {keyword}</p>
                        </div>
                        """, unsafe_allow_html=True)
                with col2:
                    for keyword in matched[len(matched)//2:]:
                        st.markdown(f"""
                        <div style="padding: 8px; margin-top: 8px; background: rgba(0, 255, 128, 0.1); border-radius: 8px;">
                            <p>✓ {keyword}</p>
                        </div>
                        """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Missing Keywords
            missing = ats.get('missing_keywords', [])
            if missing:
                st.markdown("""
                <div class="glass-card" style="padding: 24px;">
                    <h4 style="color: var(--accent-primary);">❌ Missing Keywords</h4>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    for keyword in missing[:len(missing)//2]:
                        st.markdown(f"""
                        <div style="padding: 8px; margin-top: 8px; background: rgba(255, 128, 0, 0.1); border-radius: 8px;">
                            <p>• {keyword}</p>
                        </div>
                        """, unsafe_allow_html=True)
                with col2:
                    for keyword in missing[len(missing)//2:]:
                        st.markdown(f"""
                        <div style="padding: 8px; margin-top: 8px; background: rgba(255, 128, 0, 0.1); border-radius: 8px;">
                            <p>• {keyword}</p>
                        </div>
                        """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Formatting Issues
            issues = ats.get('formatting_issues', [])
            if issues:
                st.markdown("""
                <div class="glass-card" style="padding: 24px;">
                    <h4 style="color: var(--accent-primary);">⚠️ Formatting Issues</h4>
                </div>
                """, unsafe_allow_html=True)
                
                for issue in issues:
                    st.markdown(f"""
                    <div style="padding: 12px; margin-top: 12px; border-left: 4px solid var(--accent-secondary);">
                        <p>• {issue}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Action Plan
            action_plan = ats.get('action_plan', [])
            if action_plan:
                st.markdown("""
                <div class="glass-card" style="padding: 24px;">
                    <h4 style="color: var(--accent-primary);">📋 ATS Action Plan</h4>
                </div>
                """, unsafe_allow_html=True)
                
                for i, action in enumerate(action_plan, 1):
                    st.markdown(f"""
                    <div style="padding: 12px; margin-top: 12px;">
                        <p><strong>{i}.</strong> {action}</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No ATS analysis data available.")
    
    # Tab 8: Rewrite Suggestions
    with tab8:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="glass-card" style="padding: 24px;">
            <h3>✍️ Resume Rewrite Suggestions</h3>
        </div>
        """, unsafe_allow_html=True)
        
        rewrites = analysis.get('rewrite_suggestions', [])
        if rewrites:
            for i, rewrite in enumerate(rewrites, 1):
                with st.expander(f"{i}. Rewrite Suggestion", expanded=True):
                    st.markdown(f"""
                    <div style="padding: 12px;">
                        <p style="color: var(--accent-primary); font-weight: 600; margin-bottom: 8px;">❌ Current:</p>
                        <div style="padding: 12px; background: rgba(255, 128, 0, 0.1); border-radius: 8px; margin-bottom: 16px;">
                            <p style="color: var(--text-secondary);">{rewrite.get('current_text', 'N/A')}</p>
                        </div>
                        
                        <p style="color: var(--accent-primary); font-weight: 600; margin-bottom: 8px;">✅ Suggested:</p>
                        <div style="padding: 12px; background: rgba(0, 255, 128, 0.1); border-radius: 8px; margin-bottom: 16px;">
                            <p style="color: var(--text-primary);">{rewrite.get('suggested_text', 'N/A')}</p>
                        </div>
                        
                        <p style="color: var(--accent-primary); font-weight: 600; margin-bottom: 8px;">💡 Why this is better:</p>
                        <p>{rewrite.get('reason', 'N/A')}</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No rewrite suggestions at this time.")
    
    # Tab 9: Interview Questions
    with tab9:
        st.markdown("<br>", unsafe_allow_html=True)
        
        if 'interview_questions' in analysis:
            questions = analysis['interview_questions']
            
            st.markdown("""
            <div class="glass-card" style="padding: 24px;">
                <h3>❓ Interview Questions</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Technical Questions
            tech_questions = questions.get('technical_questions', [])
            if tech_questions:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("""
                <div class="glass-card" style="padding: 24px;">
                    <h4 style="color: var(--accent-primary);">💻 Technical Questions</h4>
                </div>
                """, unsafe_allow_html=True)
                
                for i, q in enumerate(tech_questions, 1):
                    difficulty = q.get('difficulty', 'Medium')
                    diff_color = "red" if difficulty == "Hard" else "yellow" if difficulty == "Medium" else "green"
                    
                    with st.expander(f"{i}. {q.get('question', 'Question')} - {difficulty}", expanded=False):
                        st.markdown(f"""
                        <div style="padding: 12px;">
                            <p style="color: var(--accent-primary); font-weight: 600; margin-bottom: 8px;">❓ Why interviewer asks this:</p>
                            <p style="margin-bottom: 12px;">{q.get('why_asked', 'N/A')}</p>
                            
                            <p style="color: var(--accent-primary); font-weight: 600; margin-bottom: 8px;">✅ Ideal answer should contain:</p>
                            <p style="margin-bottom: 12px;">{q.get('ideal_answer', 'N/A')}</p>
                            
                            <p style="color: var(--accent-primary); font-weight: 600; margin-bottom: 8px;">📊 Difficulty: <span style="color: var(--{diff_color});">{difficulty}</span></p>
                        </div>
                        """, unsafe_allow_html=True)
            
            # Behavioral Questions
            behav_questions = questions.get('behavioral_questions', [])
            if behav_questions:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("""
                <div class="glass-card" style="padding: 24px;">
                    <h4 style="color: var(--accent-primary);">🎭 Behavioral Questions</h4>
                </div>
                """, unsafe_allow_html=True)
                
                for i, q in enumerate(behav_questions, 1):
                    difficulty = q.get('difficulty', 'Medium')
                    diff_color = "red" if difficulty == "Hard" else "yellow" if difficulty == "Medium" else "green"
                    
                    with st.expander(f"{i}. {q.get('question', 'Question')} - {difficulty}", expanded=False):
                        st.markdown(f"""
                        <div style="padding: 12px;">
                            <p style="color: var(--accent-primary); font-weight: 600; margin-bottom: 8px;">❓ Why interviewer asks this:</p>
                            <p style="margin-bottom: 12px;">{q.get('why_asked', 'N/A')}</p>
                            
                            <p style="color: var(--accent-primary); font-weight: 600; margin-bottom: 8px;">✅ Ideal answer should contain:</p>
                            <p style="margin-bottom: 12px;">{q.get('ideal_answer', 'N/A')}</p>
                            
                            <p style="color: var(--accent-primary); font-weight: 600; margin-bottom: 8px;">📊 Difficulty: <span style="color: var(--{diff_color});">{difficulty}</span></p>
                        </div>
                        """, unsafe_allow_html=True)
            
            # HR Questions
            hr_questions = questions.get('hr_questions', [])
            if hr_questions:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("""
                <div class="glass-card" style="padding: 24px;">
                    <h4 style="color: var(--accent-primary);">👔 HR Questions</h4>
                </div>
                """, unsafe_allow_html=True)
                
                for i, q in enumerate(hr_questions, 1):
                    difficulty = q.get('difficulty', 'Medium')
                    diff_color = "red" if difficulty == "Hard" else "yellow" if difficulty == "Medium" else "green"
                    
                    with st.expander(f"{i}. {q.get('question', 'Question')} - {difficulty}", expanded=False):
                        st.markdown(f"""
                        <div style="padding: 12px;">
                            <p style="color: var(--accent-primary); font-weight: 600; margin-bottom: 8px;">❓ Why interviewer asks this:</p>
                            <p style="margin-bottom: 12px;">{q.get('why_asked', 'N/A')}</p>
                            
                            <p style="color: var(--accent-primary); font-weight: 600; margin-bottom: 8px;">✅ Ideal answer should contain:</p>
                            <p style="margin-bottom: 12px;">{q.get('ideal_answer', 'N/A')}</p>
                            
                            <p style="color: var(--accent-primary); font-weight: 600; margin-bottom: 8px;">📊 Difficulty: <span style="color: var(--{diff_color});">{difficulty}</span></p>
                        </div>
                        """, unsafe_allow_html=True)
            
            # Coding Questions
            coding_questions = questions.get('coding_questions', [])
            if coding_questions:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("""
                <div class="glass-card" style="padding: 24px;">
                    <h4 style="color: var(--accent-primary);">⌨️ Coding Questions</h4>
                </div>
                """, unsafe_allow_html=True)
                
                for i, q in enumerate(coding_questions, 1):
                    difficulty = q.get('difficulty', 'Medium')
                    diff_color = "red" if difficulty == "Hard" else "yellow" if difficulty == "Medium" else "green"
                    
                    with st.expander(f"{i}. {q.get('question', 'Question')} - {difficulty}", expanded=False):
                        st.markdown(f"""
                        <div style="padding: 12px;">
                            <p style="color: var(--accent-primary); font-weight: 600; margin-bottom: 8px;">❓ Why interviewer asks this:</p>
                            <p style="margin-bottom: 12px;">{q.get('why_asked', 'N/A')}</p>
                            
                            <p style="color: var(--accent-primary); font-weight: 600; margin-bottom: 8px;">✅ Ideal answer should contain:</p>
                            <p style="margin-bottom: 12px;">{q.get('ideal_answer', 'N/A')}</p>
                            
                            <p style="color: var(--accent-primary); font-weight: 600; margin-bottom: 8px;">📊 Difficulty: <span style="color: var(--{diff_color});">{difficulty}</span></p>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.info("No interview questions data available.")
    
    # Action buttons at the bottom
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📄 Export Report (PDF)", use_container_width=True):
            st.info("PDF export feature - will generate comprehensive report")
    
    with col2:
        if st.button("🔄 Re-analyze", use_container_width=True):
            st.session_state.analysis_result = None
            st.rerun()

# HR Recruiter Module
def show_recruiter_module():
    """Display HR recruiter module."""
    st.markdown("""
    <div class="aurora-background"></div>
    """, unsafe_allow_html=True)
    
    # Header
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; margin: 48px 0;">
            <h1 class="gradient-text">HR Recruiter Dashboard</h1>
            <p style="color: var(--text-secondary);">Bulk resume screening and candidate ranking</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Job description input
    st.markdown("<br>", unsafe_allow_html=True)
    job_description = st.text_area(
        "Job Description",
        placeholder="Paste the job description here...",
        height=150
    )
    
    # File upload for multiple resumes
    st.markdown("<br>", unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "Upload Resumes (Multiple)",
        type=['pdf', 'docx', 'png', 'jpg', 'jpeg'],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )
    
    # Analyze button
    st.markdown("<br>", unsafe_allow_html=True)
    analyze_col1, analyze_col2, analyze_col3 = st.columns([1, 1, 1])
    with analyze_col2:
        if st.button("Analyze Candidates", use_container_width=True, type="primary"):
            if uploaded_files and job_description:
                with st.spinner("🧠 Analyzing candidates..."):
                    # Import analysis modules
                    from utils.document_extractor import DocumentExtractor
                    from core.ai.llm_factory import LLMFactory
                    
                    # Initialize clients
                    document_extractor = DocumentExtractor()
                    llm_client = LLMFactory.create()
                    
                    # Save uploaded files
                    upload_dir = project_root / "uploads"
                    upload_dir.mkdir(exist_ok=True)
                    
                    candidates = []
                    
                    for uploaded_file in uploaded_files:
                        file_path = upload_dir / uploaded_file.name
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        # Extract text
                        resume_text = document_extractor.extract_text(str(file_path))
                        
                        # Analyze resume
                        analysis_result = llm_client.analyze_resume(
                            resume_text,
                            job_description
                        )
                        
                        candidates.append({
                            'name': uploaded_file.name,
                            'resume_text': resume_text,
                            'analysis': analysis_result.data if analysis_result.success else {}
                        })
                    
                    # Store candidates
                    st.session_state.hr_candidates = candidates
                    st.session_state.job_description = job_description
                    
                    st.success(f"✓ Analyzed {len(candidates)} candidates!")
                    st.rerun()
            else:
                st.error("Please upload resumes and provide job description")
    
    # Display candidate results
    if st.session_state.hr_candidates:
        display_hr_results()
    
    # Back button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Back to Home", use_container_width=False):
        navigate_to('home')

def display_hr_results():
    """Display HR analysis results with graphs."""
    candidates = st.session_state.hr_candidates
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Metrics
    total_candidates = len(candidates)
    strong_matches = sum(1 for c in candidates if c['analysis'].get('overall_score', 0) >= 70)
    avg_score = sum(c['analysis'].get('overall_score', 0) for c in candidates) / total_candidates if total_candidates > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_candidates}</div>
            <div class="metric-label">Total Candidates</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{strong_matches}</div>
            <div class="metric-label">Strong Matches</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{avg_score:.1f}</div>
            <div class="metric-label">Average Score</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        rejected = total_candidates - strong_matches
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{rejected}</div>
            <div class="metric-label">Rejected</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts Section
    st.markdown("""
    <div class="glass-card" style="padding: 24px;">
        <h3>📊 Candidate Analytics</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Sort candidates by score
    sorted_candidates = sorted(
        candidates,
        key=lambda x: x['analysis'].get('overall_score', 0),
        reverse=True
    )
    
    # Prepare data for charts
    candidate_names = [c['name'][:20] for c in sorted_candidates]
    overall_scores = [c['analysis'].get('overall_score', 0) for c in sorted_candidates]
    ats_scores = [c['analysis'].get('ats_score', 0) for c in sorted_candidates]
    grammar_scores = [c['analysis'].get('grammar_score', 0) for c in sorted_candidates]
    
    # Bar Chart - Candidate Scores Comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<br>", unsafe_allow_html=True)
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=candidate_names,
            y=overall_scores,
            name='Overall Score',
            marker_color='#00d4ff'
        ))
        fig_bar.add_trace(go.Bar(
            x=candidate_names,
            y=ats_scores,
            name='ATS Score',
            marker_color='#00ff88'
        ))
        fig_bar.update_layout(
            title='Candidate Scores Comparison',
            xaxis_title='Candidates',
            yaxis_title='Score',
            barmode='group',
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ffffff'),
            xaxis=dict(tickangle=-45)
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        # Pie Chart - Candidate Distribution
        fig_pie = go.Figure(data=[go.Pie(
            labels=['Strong Matches', 'Rejected'],
            values=[strong_matches, rejected],
            hole=.4,
            marker=dict(colors=['#00ff88', '#ff6b6b'])
        )])
        fig_pie.update_layout(
            title='Candidate Distribution',
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ffffff')
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Line Chart - Score Trends
    st.markdown("<br>", unsafe_allow_html=True)
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=list(range(1, len(sorted_candidates) + 1)),
        y=overall_scores,
        mode='lines+markers',
        name='Overall Score',
        line=dict(color='#00d4ff', width=3),
        marker=dict(size=8)
    ))
    fig_line.add_trace(go.Scatter(
        x=list(range(1, len(sorted_candidates) + 1)),
        y=ats_scores,
        mode='lines+markers',
        name='ATS Score',
        line=dict(color='#00ff88', width=3),
        marker=dict(size=8)
    ))
    fig_line.update_layout(
        title='Score Trends by Ranking',
        xaxis_title='Candidate Rank',
        yaxis_title='Score',
        height=350,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff')
    )
    st.plotly_chart(fig_line, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Candidate table
    st.markdown("""
    <div class="glass-card" style="padding: 24px;">
        <h3>📋 Detailed Candidate Ranking</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Display candidates
    for i, candidate in enumerate(sorted_candidates):
        analysis = candidate['analysis']
        score = analysis.get('overall_score', 0)
        ats_score = analysis.get('ats_score', 0)
        
        # Determine status
        if score >= 80:
            status = "Strong Match"
            status_class = "success"
        elif score >= 60:
            status = "Potential Match"
            status_class = "warning"
        else:
            status = "Rejected"
            status_class = "error"
        
        st.markdown(f"""
        <div class="glass-card" style="padding: 20px; margin-top: 12px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4>#{i + 1} {candidate['name']}</h4>
                    <p style="color: var(--text-secondary); margin-top: 8px;">
                        Overall Score: {score} | ATS Score: {ats_score}
                    </p>
                </div>
                <span class="status-badge {status_class}">{status}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Export options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Export to PDF", use_container_width=True):
            st.info("PDF export feature - would generate PDF report")
    
    with col2:
        if st.button("📊 Export to Excel", use_container_width=True):
            # Export to Excel
            import pandas as pd
            from io import BytesIO
            
            # Prepare data
            export_data = []
            for candidate in sorted_candidates:
                export_data.append({
                    'Name': candidate['name'],
                    'Overall Score': candidate['analysis'].get('overall_score', 0),
                    'ATS Score': candidate['analysis'].get('ats_score', 0),
                    'Grammar Score': candidate['analysis'].get('grammar_score', 0),
                    'Communication Score': candidate['analysis'].get('communication_score', 0),
                })
            
            df = pd.DataFrame(export_data)
            
            # Create Excel file
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Candidates')
            
            st.download_button(
                label="Download Excel",
                data=output.getvalue(),
                file_name="candidates_analysis.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    
    with col3:
        if st.button("📋 Export to CSV", use_container_width=True):
            # Export to CSV
            import pandas as pd
            from io import StringIO
            
            # Prepare data
            export_data = []
            for candidate in sorted_candidates:
                export_data.append({
                    'Name': candidate['name'],
                    'Overall Score': candidate['analysis'].get('overall_score', 0),
                    'ATS Score': candidate['analysis'].get('ats_score', 0),
                    'Grammar Score': candidate['analysis'].get('grammar_score', 0),
                    'Communication Score': candidate['analysis'].get('communication_score', 0),
                })
            
            df = pd.DataFrame(export_data)
            csv = df.to_csv(index=False)
            
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="candidates_analysis.csv",
                mime="text/csv"
            )

# Main application logic
def main():
    """Main application entry point."""
    # Route to appropriate page
    if st.session_state.page == 'home':
        show_landing_page()
    elif st.session_state.page == 'candidate':
        show_candidate_module()
    elif st.session_state.page == 'recruiter':
        show_recruiter_module()

if __name__ == "__main__":
    main()
