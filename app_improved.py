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
            options=["📄 Resume Analysis", "📊 Analytics Dashboard", "📈 Skills Analysis", "📋 Report Generator", "⚙️ Settings"],
            icons=["file-earmark-text", "graph-up", "bar-chart", "file-earmark-pdf", "gear"],
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
                return
    
    # Display results if data exists
    if st.session_state.resume_data:
        display_resume_results(st.session_state.resume_data)

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
            # Skills frequency chart
            st.subheader("🛠️ Skills Distribution")
            
            # Create a simple skills frequency (for demo purposes)
            skills_freq = {skill: 1 for skill in skills}
            
            fig = px.pie(
                values=list(skills_freq.values()),
                names=list(skills_freq.keys()),
                title="Skills Overview"
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            # Skills by category (demo categorization)
            st.subheader("📊 Skills by Category")
            
            # Demo categorization
            categories = {
                "Programming Languages": ["Python", "Java", "JavaScript", "C++", "C#", "Ruby", "PHP", "Go", "Rust", "Swift"],
                "Web Technologies": ["HTML", "CSS", "React", "Angular", "Vue.js", "Node.js", "Django", "Flask", "Express"],
                "Databases": ["SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis", "Oracle", "SQLite"],
                "Cloud & DevOps": ["AWS", "Azure", "GCP", "Docker", "Kubernetes", "Jenkins", "Git", "CI/CD"],
                "Data Science": ["Machine Learning", "Deep Learning", "Data Analysis", "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "PyTorch"],
                "Other": []
            }
            
            categorized_skills = {}
            for skill in skills:
                categorized = False
                for category, category_skills in categories.items():
                    if skill.lower() in [s.lower() for s in category_skills]:
                        if category not in categorized_skills:
                            categorized_skills[category] = []
                        categorized_skills[category].append(skill)
                        categorized = True
                        break
                if not categorized:
                    if "Other" not in categorized_skills:
                        categorized_skills["Other"] = []
                    categorized_skills["Other"].append(skill)
            
            # Display categorized skills
            for category, category_skills in categorized_skills.items():
                if category_skills:
                    st.write(f"**{category}:**")
                    for skill in category_skills:
                        st.markdown(f'<span class="skill-tag">{skill}</span>', unsafe_allow_html=True)
                    st.write("")
    
    # Skills gap analysis (demo)
    st.subheader("🎯 Skills Gap Analysis")
    
    # Demo job requirements
    job_requirements = {
        "Software Engineer": ["Python", "JavaScript", "SQL", "Git", "Docker"],
        "Data Scientist": ["Python", "Machine Learning", "SQL", "Pandas", "NumPy"],
        "Frontend Developer": ["JavaScript", "React", "HTML", "CSS", "Git"],
        "DevOps Engineer": ["Docker", "Kubernetes", "AWS", "Jenkins", "Linux"]
    }
    
    selected_job = st.selectbox("Select job role for comparison:", list(job_requirements.keys()))
    
    if selected_job and data.get('Skills'):
        candidate_skills = set(skill.lower() for skill in data['Skills']) if isinstance(data['Skills'], list) else set()
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
    
    # Preview section
    st.subheader("👀 Report Preview")
    
    if report_type == "Comprehensive Analysis":
        display_comprehensive_preview(data)
    elif report_type == "Skills Summary":
        display_skills_preview(data)
    elif report_type == "Career Overview":
        display_career_preview(data)

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

def display_comprehensive_preview(data):
    st.markdown("### 📊 Comprehensive Analysis Preview")
    st.json(data)

def display_skills_preview(data):
    st.markdown("### 🛠️ Skills Summary Preview")
    if data.get('Skills'):
        skills = data['Skills']
        if isinstance(skills, list):
            for skill in skills:
                st.markdown(f'<span class="skill-tag">{skill}</span>', unsafe_allow_html=True)

def display_career_preview(data):
    st.markdown("### 💼 Career Overview Preview")
    col1, col2 = st.columns(2)
    
    with col1:
        if data.get('Education'):
            st.write("**Education:**")
            st.write(data['Education'])
    
    with col2:
        if data.get('Internships / Work experience'):
            st.write("**Experience:**")
            st.write(data['Internships / Work experience'])

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

if __name__ == "__main__":
    main() 