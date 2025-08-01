import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import json
import os
from datetime import datetime
import base64
from extractor.parse_resume import get_resume_text
from extractor.ai_extractor import extract_resume_data
from utils.report_generator import generate_pdf_report
from utils.linkedin_scraper import fetch_linkedin_profile_data

# Page configuration
st.set_page_config(
    page_title="AI Resume Analyzer Pro",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
    }
    .skill-tag {
        background: #e3f2fd;
        color: #1976d2;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.25rem;
        display: inline-block;
        font-size: 0.9rem;
    }
    .section-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .upload-area {
        border: 2px dashed #667eea;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background: #f8f9fa;
    }
    .stProgress > div > div > div > div {
        background-color: #667eea;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'resume_data' not in st.session_state:
    st.session_state.resume_data = None
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []

def main():
    # Sidebar navigation
    with st.sidebar:
        st.markdown("## 🚀 AI Resume Analyzer Pro")
        selected = option_menu(
            menu_title=None,
            options=["📄 Resume Analysis", "📊 Analytics Dashboard", "📈 Skills Analysis", "📋 Report Generator", "🤖 AI Suggestions", "🔗 LinkedIn Analyzer", "⚙️ Settings"],
            icons=["file-earmark-text", "graph-up", "bar-chart", "file-earmark-pdf", "robot", "linkedin", "gear"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "#667eea", "font-size": "18px"},
                "nav-link": {
                    "color": "#333",
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#667eea",
                },
                "nav-link-selected": {"background-color": "#667eea", "color": "white"},
            }
        )
    
    # Main content based on selection
    if selected == "📄 Resume Analysis":
        resume_analysis_page()
    elif selected == "📊 Analytics Dashboard":
        analytics_dashboard_page()
    elif selected == "📈 Skills Analysis":
        skills_analysis_page()
    elif selected == "📋 Report Generator":
        report_generator_page()
    elif selected == "🤖 AI Suggestions":
        ai_suggestions_page()
    elif selected == "🔗 LinkedIn Analyzer":
        linkedin_analyzer_page()
    elif selected == "⚙️ Settings":
        settings_page()

def resume_analysis_page():
    st.markdown('<div class="main-header"><h1>📄 AI-Powered Resume Analyzer Pro</h1><p>Advanced resume parsing and analysis with AI insights</p></div>', unsafe_allow_html=True)
    
    # File upload section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📁 Upload Resume")
        uploaded_file = st.file_uploader(
            "Choose a resume file",
            type=["pdf", "docx", "txt"],
            help="Supported formats: PDF, DOCX, TXT"
        )
    
    with col2:
        st.markdown("### 📝 Quick Analysis")
        if st.button("🔍 Analyze Sample Resume", type="secondary"):
            # Load sample data for demonstration
            sample_data = {
                "Name": "John Doe",
                "Email": "john.doe@email.com",
                "Phone": "+1-555-0123",
                "Education": [
                    {"Degree": "Bachelor of Science", "Field": "Computer Science", "University": "Tech University", "Year": "2023", "CGPA": "3.8"}
                ],
                "Skills": ["Python", "Machine Learning", "Data Analysis", "SQL", "JavaScript"],
                "Projects": [
                    {"Name": "AI Chatbot", "Description": "Built an intelligent chatbot using Python and NLP", "Technologies": ["Python", "NLTK", "Flask"]},
                    {"Name": "E-commerce Platform", "Description": "Full-stack web application", "Technologies": ["React", "Node.js", "MongoDB"]}
                ],
                "Certifications": ["AWS Certified Developer", "Google Cloud Professional"],
                "Internships / Work experience": [
                    {"Company": "Tech Corp", "Position": "Software Engineer Intern", "Duration": "6 months", "Description": "Developed web applications"}
                ],
                "Domain of expertise": "Software Development"
            }
            st.session_state.resume_data = sample_data
            st.session_state.analysis_history.append({
                "timestamp": datetime.now(),
                "name": sample_data["Name"],
                "filename": "Sample Resume"
            })
            st.success("Sample resume analyzed successfully!")

    if uploaded_file:
        with st.spinner("🔄 Processing your resume..."):
            try:
                # Extract text from resume
                resume_text = get_resume_text(uploaded_file)

                # Progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text("Extracting text from resume...")
                progress_bar.progress(25)
                
                status_text.text("Analyzing with AI...")
                progress_bar.progress(50)
                
                # Extract data using AI
                raw_json = extract_resume_data(resume_text)
                data = json.loads(raw_json)

                progress_bar.progress(75)
                status_text.text("Processing results...")
                
                # Store in session state
                st.session_state.resume_data = data
                st.session_state.analysis_history.append({
                    "timestamp": datetime.now(),
                    "name": data.get("Name", "Unknown"),
                    "filename": uploaded_file.name
                })
                
                progress_bar.progress(100)
                status_text.text("Analysis complete!")
                
                st.success("✅ Resume analyzed successfully!")
                
            except Exception as e:
                st.error(f"❌ Error analyzing resume: {str(e)}")
    
        # Display results if data exists
        if st.session_state.resume_data:
            display_resume_results(st.session_state.resume_data)
        
        # Comparison feature
        st.markdown("## 🔄 Compare with Previous Analysis")
        if len(st.session_state.analysis_history) > 1:
            st.write("Compare current analysis with previous ones:")
            
            # Get previous analyses
            previous_analyses = st.session_state.analysis_history[:-1]  # Exclude current
            if previous_analyses:
                selected_previous = st.selectbox(
                    "Select previous analysis to compare:",
                    [f"{analysis['name']} ({analysis['timestamp'].strftime('%Y-%m-%d %H:%M')})" for analysis in previous_analyses]
                )
                
                if st.button("🔍 Compare Skills"):
                    # This would compare skills between current and selected analysis
                    st.info("Comparison feature coming soon! This will show skills evolution over time.")
        else:
            st.info("📊 No previous analyses available for comparison. Analyze more resumes to enable this feature.")

def display_resume_results(data):
    st.markdown("## 📋 Analysis Results")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>👤 Name</h3>
            <p style="font-size: 1.2rem; font-weight: bold;">{data.get('Name', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📧 Email</h3>
            <p style="font-size: 1.2rem; font-weight: bold;">{data.get('Email', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📞 Phone</h3>
            <p style="font-size: 1.2rem; font-weight: bold;">{data.get('Phone', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        skills_count = len(data.get('Skills', [])) if isinstance(data.get('Skills'), list) else 0
        st.markdown(f"""
        <div class="metric-card">
            <h3>🛠️ Skills</h3>
            <p style="font-size: 1.2rem; font-weight: bold;">{skills_count}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Detailed sections
    col1, col2 = st.columns(2)
    
    with col1:
        # Education
        if data.get('Education'):
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.subheader("🎓 Education")
            if isinstance(data['Education'], list):
                for edu in data['Education']:
                    if isinstance(edu, dict):
                        st.write(f"**{edu.get('Degree', 'N/A')}** in {edu.get('Field', 'N/A')}")
                        st.write(f"*{edu.get('University', 'N/A')}* - {edu.get('Year', 'N/A')}")
                        if edu.get('CGPA'):
                            st.write(f"CGPA: {edu.get('CGPA')}")
                    else:
                        st.write(f"• {edu}")
                    st.write("---")
            else:
                st.write(data['Education'])
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Skills
        if data.get('Skills'):
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.subheader("🛠️ Skills")
            skills = data['Skills']
            if isinstance(skills, list):
                for skill in skills:
                    st.markdown(f'<span class="skill-tag">{skill}</span>', unsafe_allow_html=True)
            else:
                st.write(skills)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Work Experience
        if data.get('Internships / Work experience'):
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.subheader("💼 Work Experience")
            experience = data['Internships / Work experience']
            if isinstance(experience, list):
                for exp in experience:
                    if isinstance(exp, dict):
                        st.write(f"**{exp.get('Position', 'N/A')}** at {exp.get('Company', 'N/A')}")
                        st.write(f"*{exp.get('Duration', 'N/A')}*")
                        if exp.get('Description'):
                            st.write(exp.get('Description'))
                    else:
                        st.write(f"• {exp}")
                    st.write("---")
            else:
                st.write(experience)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Projects
        if data.get('Projects'):
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.subheader("🚀 Projects")
            projects = data['Projects']
            if isinstance(projects, list):
                for project in projects:
                    if isinstance(project, dict):
                        st.write(f"**{project.get('Name', 'N/A')}**")
                        if project.get('Description'):
                            st.write(project.get('Description'))
                        if project.get('Technologies'):
                            techs = project.get('Technologies')
                            if isinstance(techs, list):
                                for tech in techs:
                                    st.markdown(f'<span class="skill-tag">{tech}</span>', unsafe_allow_html=True)
                    else:
                        st.write(f"• {project}")
                    st.write("---")
            else:
                st.write(projects)
            st.markdown('</div>', unsafe_allow_html=True)

def analytics_dashboard_page():
    st.markdown('<div class="main-header"><h1>📊 Analytics Dashboard</h1><p>Comprehensive insights and statistics</p></div>', unsafe_allow_html=True)
    
    if not st.session_state.analysis_history:
        st.info("📊 No analysis data available. Please analyze a resume first.")
        return
    
    # Convert history to DataFrame
    df = pd.DataFrame(st.session_state.analysis_history)
    df['date'] = pd.to_datetime(df['timestamp']).dt.date
    
    # Analytics overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_analyses = len(df)
        st.metric("Total Analyses", total_analyses)
    
    with col2:
        unique_names = df['name'].nunique()
        st.metric("Unique Candidates", unique_names)
    
    with col3:
        recent_analyses = len(df[df['date'] == df['date'].max()])
        st.metric("Today's Analyses", recent_analyses)
    
    with col4:
        avg_per_day = len(df) / max(1, (df['date'].max() - df['date'].min()).days)
        st.metric("Avg/Day", f"{avg_per_day:.1f}")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Analysis Timeline")
        daily_counts = df.groupby('date').size().reset_index(name='count')
        fig = px.line(daily_counts, x='date', y='count', 
                     title="Daily Analysis Count",
                     labels={'date': 'Date', 'count': 'Number of Analyses'})
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("👥 Top Candidates")
        candidate_counts = df['name'].value_counts().head(10)
        fig = px.bar(x=candidate_counts.values, y=candidate_counts.index,
                    orientation='h',
                    title="Most Analyzed Candidates",
                    labels={'x': 'Number of Analyses', 'y': 'Candidate Name'})
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent activity
    st.subheader("🕒 Recent Activity")
    recent_df = df.sort_values('timestamp', ascending=False).head(10)
    for _, row in recent_df.iterrows():
        st.write(f"**{row['name']}** - {row['filename']} ({row['timestamp'].strftime('%Y-%m-%d %H:%M')})")
    
    # Export data
    st.subheader("📤 Export Data")
    csv_data = df.to_csv(index=False)
    st.download_button(
        label="📥 Download Analytics Data (CSV)",
        data=csv_data,
        file_name="resume_analytics.csv",
        mime="text/csv"
    )

def skills_analysis_page():
    st.markdown('<div class="main-header"><h1>📈 Skills Analysis</h1><p>Deep dive into skills and competencies</p></div>', unsafe_allow_html=True)
    
    if not st.session_state.resume_data:
        st.info("📈 No resume data available. Please analyze a resume first.")
        return
    
    data = st.session_state.resume_data
    
    # Skills visualization
    if data.get('Skills'):
        skills = data['Skills']
        if isinstance(skills, list):
            st.subheader("🛠️ Skills Distribution")
            
            # Create skills frequency chart
            skills_freq = {skill: 1 for skill in skills}
            
            fig = px.pie(
                values=list(skills_freq.values()),
                names=list(skills_freq.keys()),
                title="Skills Overview"
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            # Skills gap analysis
            st.subheader("🎯 Skills Gap Analysis")
            
            job_requirements = {
                "Software Engineer": ["Python", "JavaScript", "SQL", "Git", "Docker"],
                "Data Scientist": ["Python", "Machine Learning", "SQL", "Pandas", "NumPy"],
                "Frontend Developer": ["JavaScript", "React", "HTML", "CSS", "Git"],
                "DevOps Engineer": ["Docker", "Kubernetes", "AWS", "Jenkins", "Linux"]
            }
            
            selected_job = st.selectbox("Select job role for comparison:", list(job_requirements.keys()))
            
            if selected_job:
                candidate_skills = set(skill.lower() for skill in skills)
                required_skills = set(skill.lower() for skill in job_requirements[selected_job])
                
                matched_skills = candidate_skills.intersection(required_skills)
                missing_skills = required_skills - candidate_skills
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown('<div class="section-card">', unsafe_allow_html=True)
                    st.subheader("✅ Matched Skills")
                    for skill in matched_skills:
                        st.markdown(f'<span class="skill-tag" style="background: #e8f5e8; color: #2e7d32;">{skill.title()}</span>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown('<div class="section-card">', unsafe_allow_html=True)
                    st.subheader("❌ Missing Skills")
                    for skill in missing_skills:
                        st.markdown(f'<span class="skill-tag" style="background: #ffebee; color: #c62828;">{skill.title()}</span>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Match percentage
                match_percentage = len(matched_skills) / len(required_skills) * 100
                st.metric("Match Percentage", f"{match_percentage:.1f}%")
                
                # Skills recommendations
                if missing_skills:
                    st.subheader("💡 Skills Recommendations")
                    st.write("Consider learning these skills to improve your profile:")
                    for skill in list(missing_skills)[:3]:  # Show top 3 missing skills
                        st.write(f"• **{skill.title()}** - Essential for {selected_job} roles")
                
                # Skills radar chart
                if matched_skills or missing_skills:
                    st.subheader("📊 Skills Radar Chart")
                    
                    # Create radar chart data
                    categories = list(required_skills)
                    values = [1 if skill in matched_skills else 0 for skill in categories]
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatterpolar(
                        r=values,
                        theta=categories,
                        fill='toself',
                        name='Your Skills',
                        line_color='#667eea'
                    ))
                    
                    fig.update_layout(
                        polar=dict(
                            radialaxis=dict(
                                visible=True,
                                range=[0, 1]
                            )),
                        showlegend=True,
                        title="Skills Coverage Radar Chart"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)

def report_generator_page():
    st.markdown('<div class="main-header"><h1>📋 Report Generator</h1><p>Generate comprehensive reports and insights</p></div>', unsafe_allow_html=True)
    
    if not st.session_state.resume_data:
        st.info("📋 No resume data available. Please analyze a resume first.")
        return
    
    data = st.session_state.resume_data
    
    # Report options
    st.subheader("📄 Report Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        report_type = st.selectbox(
            "Report Type",
            ["Comprehensive Analysis", "Skills Summary", "Career Overview", "Custom Report"]
        )
        
        include_charts = st.checkbox("Include Charts & Visualizations", value=True)
        include_recommendations = st.checkbox("Include AI Recommendations", value=True)
    
    with col2:
        report_format = st.selectbox("Format", ["PDF", "HTML", "JSON"])
        
        if report_format == "PDF":
            include_cover_page = st.checkbox("Include Cover Page", value=True)
            include_table_of_contents = st.checkbox("Include Table of Contents", value=True)
    
    # Generate report
    if st.button("🚀 Generate Report", type="primary"):
        with st.spinner("Generating report..."):
            try:
                if report_format == "PDF":
                    filename = f"{data.get('Name', 'resume')}_{report_type.lower().replace(' ', '_')}_report.pdf"
                    filepath = generate_pdf_report(data, filename)
                    
                    with open(filepath, "rb") as f:
                        st.download_button(
                            label="📥 Download PDF Report",
                            data=f.read(),
                            file_name=filename,
                            mime="application/pdf"
                        )
                
                elif report_format == "HTML":
                    # Generate HTML report
                    html_content = generate_html_report(data, report_type, include_charts, include_recommendations)
                    filename = f"{data.get('Name', 'resume')}_{report_type.lower().replace(' ', '_')}_report.html"
                    
                    st.download_button(
                        label="📥 Download HTML Report",
                        data=html_content,
                        file_name=filename,
                        mime="text/html"
                    )
                
                elif report_format == "JSON":
                    # Generate JSON report
                    json_content = json.dumps(data, indent=2)
                    filename = f"{data.get('Name', 'resume')}_{report_type.lower().replace(' ', '_')}_report.json"
                    
                    st.download_button(
                        label="📥 Download JSON Report",
                        data=json_content,
                        file_name=filename,
                        mime="application/json"
                    )
                
                st.success("✅ Report generated successfully!")
                
            except Exception as e:
                st.error(f"❌ Error generating report: {str(e)}")

def generate_html_report(data, report_type, include_charts, include_recommendations):
    # This would generate a comprehensive HTML report
    # For now, return a simple HTML structure
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{report_type} - {data.get('Name', 'Resume')}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            h1 {{ color: #667eea; }}
            .section {{ margin: 20px 0; }}
            .skill-tag {{ background: #e3f2fd; color: #1976d2; padding: 5px 10px; border-radius: 15px; margin: 2px; display: inline-block; }}
        </style>
    </head>
    <body>
        <h1>{report_type}</h1>
        <div class="section">
            <h2>Candidate Information</h2>
            <p><strong>Name:</strong> {data.get('Name', 'N/A')}</p>
            <p><strong>Email:</strong> {data.get('Email', 'N/A')}</p>
            <p><strong>Phone:</strong> {data.get('Phone', 'N/A')}</p>
        </div>
    </body>
    </html>
    """
    return html

def settings_page():
    st.markdown('<div class="main-header"><h1>⚙️ Settings</h1><p>Configure your analysis preferences</p></div>', unsafe_allow_html=True)
    
    st.subheader("🔧 Analysis Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**AI Model Settings**")
        model_type = st.selectbox("AI Model", ["GPT-4", "GPT-3.5-turbo"], index=0)
        temperature = st.slider("Creativity Level", 0.0, 1.0, 0.0, 0.1)
        
        st.write("**File Processing**")
        max_file_size = st.number_input("Max File Size (MB)", 1, 50, 10)
        supported_formats = st.multiselect(
            "Supported Formats",
            ["PDF", "DOCX", "TXT", "RTF"],
            default=["PDF", "DOCX", "TXT"]
        )
    
    with col2:
        st.write("**Report Settings**")
        default_report_format = st.selectbox("Default Report Format", ["PDF", "HTML", "JSON"])
        auto_generate_charts = st.checkbox("Auto-generate Charts", value=True)
        
        st.write("**Data Management**")
        auto_save_history = st.checkbox("Auto-save Analysis History", value=True)
        clear_history = st.button("🗑️ Clear Analysis History", type="secondary")
        
        if clear_history:
            st.session_state.analysis_history = []
            st.success("Analysis history cleared!")
    
    st.subheader("🎨 UI Preferences")
    
    theme = st.selectbox("Theme", ["Light", "Dark", "Auto"])
    language = st.selectbox("Language", ["English", "Spanish", "French", "German"])
    
    if st.button("💾 Save Settings", type="primary"):
        st.success("Settings saved successfully!")

def ai_suggestions_page():
    st.markdown('<div class="main-header"><h1>🤖 AI Resume Suggestions</h1><p>Get AI-powered recommendations to improve your resume</p></div>', unsafe_allow_html=True)
    
    if not st.session_state.resume_data:
        st.info("🤖 No resume data available. Please analyze a resume first.")
        return
    
    data = st.session_state.resume_data
    
    st.subheader("💡 AI Recommendations")
    
    # Resume improvement suggestions
    suggestions = []
    
    # Check for missing sections
    if not data.get('Skills'):
        suggestions.append("🔧 **Add a Skills section** - Highlight your technical and soft skills")
    
    if not data.get('Projects'):
        suggestions.append("🚀 **Include Projects** - Showcase your practical experience and achievements")
    
    if not data.get('Certifications'):
        suggestions.append("🏆 **Add Certifications** - Demonstrate your commitment to continuous learning")
    
    # Check for content quality
    if data.get('Skills'):
        skills_count = len(data['Skills']) if isinstance(data['Skills'], list) else 0
        if skills_count < 5:
            suggestions.append("📈 **Expand Skills** - Consider adding more relevant skills to make your profile stronger")
    
    if data.get('Internships / Work experience'):
        exp_count = len(data['Internships / Work experience']) if isinstance(data['Internships / Work experience'], list) else 0
        if exp_count < 2:
            suggestions.append("💼 **Add More Experience** - Include internships, volunteer work, or freelance projects")
    
    # Display suggestions
    if suggestions:
        for suggestion in suggestions:
            st.info(suggestion)
    else:
        st.success("🎉 Your resume looks comprehensive! Great job!")
    
    # Skills enhancement suggestions
    if data.get('Skills'):
        st.subheader("🛠️ Skills Enhancement")
        
        # Popular skills in tech
        trending_skills = {
            "Programming": ["Python", "JavaScript", "Java", "C++", "Go", "Rust"],
            "Web Development": ["React", "Angular", "Vue.js", "Node.js", "Django", "Flask"],
            "Data Science": ["Machine Learning", "Deep Learning", "Data Analysis", "Pandas", "NumPy", "TensorFlow"],
            "Cloud & DevOps": ["AWS", "Azure", "GCP", "Docker", "Kubernetes", "Jenkins"],
            "Databases": ["SQL", "MongoDB", "PostgreSQL", "Redis", "Oracle"]
        }
        
        candidate_skills = set(skill.lower() for skill in data['Skills']) if isinstance(data['Skills'], list) else set()
        
        for category, skills in trending_skills.items():
            missing_in_category = [skill for skill in skills if skill.lower() not in candidate_skills]
            if missing_in_category:
                st.write(f"**{category}:** Consider adding: {', '.join(missing_in_category[:3])}")
    
    # Resume format suggestions
    st.subheader("📝 Format & Structure")
    
    format_suggestions = [
        "✅ Use bullet points for better readability",
        "✅ Quantify achievements with numbers and percentages",
        "✅ Use action verbs to start bullet points",
        "✅ Keep consistent formatting throughout",
        "✅ Include relevant keywords for ATS systems",
        "✅ Limit resume to 1-2 pages",
        "✅ Use professional fonts (Arial, Calibri, Times New Roman)"
    ]
    
    for suggestion in format_suggestions:
        st.write(suggestion)

def fetch_linkedin_data(linkedin_url):
    """
    Fetch LinkedIn profile data from URL using the LinkedIn scraper
    """
    try:
        # Use the LinkedIn scraper to fetch data
        profile_data = fetch_linkedin_profile_data(linkedin_url)
        return profile_data
    except Exception as e:
        st.error(f"Error fetching LinkedIn data: {str(e)}")
        return None

def linkedin_analyzer_page():
    st.markdown('<div class="main-header"><h1>🔗 LinkedIn Profile Analyzer</h1><p>Analyze and compare your LinkedIn profile with your resume</p></div>', unsafe_allow_html=True)
    
    # Initialize session state for LinkedIn data
    if 'linkedin_data' not in st.session_state:
        st.session_state.linkedin_data = None
    
    st.subheader("📥 Import LinkedIn Profile")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔗 LinkedIn URL Input")
        st.write("Enter your LinkedIn profile URL to automatically fetch data:")
        
        with st.form("linkedin_url_form"):
            linkedin_url = st.text_input("LinkedIn Profile URL", placeholder="https://www.linkedin.com/in/username")
            
            if st.form_submit_button("🔍 Fetch & Analyze LinkedIn Profile"):
                if linkedin_url:
                    # Validate URL format
                    if not linkedin_url.startswith(('https://www.linkedin.com/in/', 'https://linkedin.com/in/')):
                        st.error("❌ Please enter a valid LinkedIn profile URL (e.g., https://www.linkedin.com/in/username)")
                        return
                    
                    # Progress tracking
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    status_text.text("Validating LinkedIn URL...")
                    progress_bar.progress(25)
                    
                    status_text.text("Fetching profile data...")
                    progress_bar.progress(50)
                    
                    try:
                        # Fetch LinkedIn data
                        linkedin_data = fetch_linkedin_data(linkedin_url)
                        
                        progress_bar.progress(75)
                        status_text.text("Processing profile data...")
                        
                        if linkedin_data:
                            st.session_state.linkedin_data = linkedin_data
                            
                            progress_bar.progress(100)
                            status_text.text("Analysis complete!")
                            
                            st.success("✅ LinkedIn profile fetched and analyzed successfully!")
                            
                            # Show extracted username
                            if 'Username' in linkedin_data:
                                st.info(f"📋 Extracted username: {linkedin_data['Username']}")
                        else:
                            st.error("❌ Could not fetch LinkedIn data. Please check the URL or try manual input.")
                    except Exception as e:
                        st.error(f"❌ Error fetching LinkedIn data: {str(e)}")
                        st.info("💡 Try using the manual input option below or check if the profile is public.")
                else:
                    st.error("Please provide a LinkedIn profile URL.")
        
        st.markdown("---")
        st.markdown("### 📝 Manual Input (Alternative)")
        st.write("Or enter your LinkedIn profile information manually:")
        
        with st.form("linkedin_manual_form"):
            linkedin_name = st.text_input("Full Name")
            linkedin_headline = st.text_input("Headline")
            linkedin_location = st.text_input("Location")
            linkedin_industry = st.text_input("Industry")
            linkedin_summary = st.text_area("Summary", height=150)
            linkedin_experience = st.text_area("Experience (paste your experience section)", height=200)
            linkedin_education = st.text_area("Education", height=150)
            linkedin_skills = st.text_area("Skills (comma-separated)", height=100)
            
            if st.form_submit_button("🔍 Analyze Manual Input"):
                if linkedin_name and linkedin_headline:
                    # Process LinkedIn data
                    linkedin_data = {
                        "Name": linkedin_name,
                        "Headline": linkedin_headline,
                        "Location": linkedin_location,
                        "Industry": linkedin_industry,
                        "Summary": linkedin_summary,
                        "Experience": linkedin_experience,
                        "Education": linkedin_education,
                        "Skills": [skill.strip() for skill in linkedin_skills.split(",") if skill.strip()] if linkedin_skills else []
                    }
                    
                    st.session_state.linkedin_data = linkedin_data
                    st.success("✅ LinkedIn profile analyzed successfully!")
                else:
                    st.error("Please provide at least your name and headline.")
    
    with col2:
        st.markdown("### 📄 Sample LinkedIn Profile")
        if st.button("🔍 Load Sample LinkedIn Profile", type="secondary"):
            sample_linkedin = {
                "Name": "John Doe",
                "Headline": "Software Engineer | Full Stack Developer | AI Enthusiast",
                "Location": "San Francisco, CA",
                "Industry": "Technology",
                "Summary": "Passionate software engineer with 3+ years of experience in full-stack development. Specialized in Python, React, and machine learning. Always eager to learn new technologies and solve complex problems.",
                "Experience": "Software Engineer at Tech Corp (2022-Present)\n- Developed web applications using React and Node.js\n- Implemented machine learning models for data analysis\n- Led a team of 3 developers for a major project\n\nSoftware Engineer Intern at Startup Inc (2021-2022)\n- Built REST APIs using Python and Flask\n- Worked on database optimization and performance tuning",
                "Education": "Bachelor of Science in Computer Science\nTech University (2018-2022)\nGPA: 3.8/4.0",
                "Skills": ["Python", "JavaScript", "React", "Node.js", "Machine Learning", "SQL", "Git", "Docker", "AWS", "Agile"]
            }
            
            st.session_state.linkedin_data = sample_linkedin
            st.success("Sample LinkedIn profile loaded successfully!")
    
    # Display LinkedIn analysis if data exists
    if st.session_state.linkedin_data:
        display_linkedin_analysis(st.session_state.linkedin_data)
        
        # Compare with resume if both exist
        if st.session_state.resume_data:
            st.markdown("## 🔄 Profile Comparison")
            compare_profiles(st.session_state.resume_data, st.session_state.linkedin_data)

def display_linkedin_analysis(linkedin_data):
    st.markdown("## 📊 LinkedIn Profile Analysis")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>👤 Name</h3>
            <p style="font-size: 1.2rem; font-weight: bold;">{linkedin_data.get('Name', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>💼 Headline</h3>
            <p style="font-size: 1rem; font-weight: bold;">{linkedin_data.get('Headline', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📍 Location</h3>
            <p style="font-size: 1.2rem; font-weight: bold;">{linkedin_data.get('Location', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        skills_count = len(linkedin_data.get('Skills', []))
        st.markdown(f"""
        <div class="metric-card">
            <h3>🛠️ Skills</h3>
            <p style="font-size: 1.2rem; font-weight: bold;">{skills_count}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Show profile URL if available
    if linkedin_data.get('Profile_URL'):
        st.markdown(f"""
        <div class="section-card">
            <h4>🔗 Profile URL</h4>
            <p><a href="{linkedin_data['Profile_URL']}" target="_blank">{linkedin_data['Profile_URL']}</a></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Detailed sections
    col1, col2 = st.columns(2)
    
    with col1:
        # Summary
        if linkedin_data.get('Summary'):
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.subheader("📝 Summary")
            st.write(linkedin_data['Summary'])
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Skills
        if linkedin_data.get('Skills'):
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.subheader("🛠️ Skills")
            for skill in linkedin_data['Skills']:
                st.markdown(f'<span class="skill-tag">{skill}</span>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Experience
        if linkedin_data.get('Experience'):
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.subheader("💼 Experience")
            st.write(linkedin_data['Experience'])
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Education
        if linkedin_data.get('Education'):
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.subheader("🎓 Education")
            st.write(linkedin_data['Education'])
            st.markdown('</div>', unsafe_allow_html=True)

def compare_profiles(resume_data, linkedin_data):
    st.subheader("📊 Profile Comparison Analysis")
    
    # Name consistency
    st.markdown("### 👤 Name Consistency")
    resume_name = resume_data.get('Name', '').lower()
    linkedin_name = linkedin_data.get('Name', '').lower()
    
    if resume_name == linkedin_name:
        st.success("✅ Names match perfectly!")
    elif resume_name in linkedin_name or linkedin_name in resume_name:
        st.warning("⚠️ Names are similar but not identical")
    else:
        st.error("❌ Names don't match")
    
    # Skills comparison
    if resume_data.get('Skills') and linkedin_data.get('Skills'):
        st.markdown("### 🛠️ Skills Comparison")
        
        resume_skills = set(skill.lower() for skill in resume_data['Skills'])
        linkedin_skills = set(skill.lower() for skill in linkedin_data['Skills'])
        
        common_skills = resume_skills.intersection(linkedin_skills)
        resume_only = resume_skills - linkedin_skills
        linkedin_only = linkedin_skills - resume_skills
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.subheader("✅ Common Skills")
            st.write(f"**{len(common_skills)} skills** found in both profiles")
            for skill in list(common_skills)[:5]:
                st.markdown(f'<span class="skill-tag" style="background: #e8f5e8; color: #2e7d32;">{skill.title()}</span>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.subheader("📄 Resume Only")
            st.write(f"**{len(resume_only)} skills** only in resume")
            for skill in list(resume_only)[:5]:
                st.markdown(f'<span class="skill-tag" style="background: #fff3e0; color: #f57c00;">{skill.title()}</span>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.subheader("🔗 LinkedIn Only")
            st.write(f"**{len(linkedin_only)} skills** only in LinkedIn")
            for skill in list(linkedin_only)[:5]:
                st.markdown(f'<span class="skill-tag" style="background: #e3f2fd; color: #1976d2;">{skill.title()}</span>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Skills consistency score
        total_skills = len(resume_skills.union(linkedin_skills))
        consistency_score = len(common_skills) / total_skills * 100 if total_skills > 0 else 0
        
        st.metric("Skills Consistency Score", f"{consistency_score:.1f}%")
        
        # Recommendations
        st.markdown("### 💡 Recommendations")
        if len(resume_only) > 0:
            st.info(f"Consider adding these resume skills to LinkedIn: {', '.join(list(resume_only)[:3])}")
        if len(linkedin_only) > 0:
            st.info(f"Consider adding these LinkedIn skills to resume: {', '.join(list(linkedin_only)[:3])}")
        if consistency_score < 70:
            st.warning("Your profiles have low consistency. Consider aligning your skills across both platforms.")
        else:
            st.success("Great! Your profiles are well-aligned.")

if __name__ == "__main__":
    main()
