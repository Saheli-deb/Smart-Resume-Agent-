# AI Resume Analyzer Pro 🚀

A modern, feature-rich Streamlit application for AI-powered resume analysis and insights.

## ✨ Features

### 📄 Resume Analysis
- **Multi-format Support**: Upload PDF, DOCX, and TXT files
- **AI-Powered Extraction**: Advanced text extraction and data parsing
- **Real-time Processing**: Progress tracking with visual feedback
- **Sample Data Demo**: Test the application with sample resume data
- **Comparison Tool**: Compare current analysis with previous ones

### 📊 Analytics Dashboard
- **Usage Statistics**: Track total analyses, unique candidates, and daily averages
- **Interactive Charts**: Visualize analysis trends and candidate data
- **Recent Activity**: Monitor latest resume analyses
- **Data Export**: Download analytics data in CSV format

### 📈 Skills Analysis
- **Skills Visualization**: Interactive pie charts and radar charts
- **Skills Gap Analysis**: Compare your skills with job requirements
- **Job Role Matching**: Pre-defined job roles (Software Engineer, Data Scientist, etc.)
- **Match Percentage**: Calculate skills compatibility with target roles
- **AI Recommendations**: Get personalized skills improvement suggestions

### 📋 Report Generator
- **Multiple Formats**: Generate reports in PDF, HTML, and JSON
- **Customizable Reports**: Choose from different report types
- **Chart Integration**: Include visualizations in reports
- **Professional Layout**: Clean, professional report formatting

### 🤖 AI Suggestions
- **Resume Improvement**: AI-powered recommendations for better resumes
- **Skills Enhancement**: Suggest trending skills in your field
- **Format Guidelines**: Best practices for resume structure
- **Content Quality**: Analyze and suggest improvements

### 🔗 LinkedIn Profile Analyzer
- **URL-based Import**: Automatically fetch LinkedIn profile data from URL
- **Profile Analysis**: Comprehensive analysis of LinkedIn profile data
- **Profile Comparison**: Compare LinkedIn profile with resume for consistency
- **Skills Consistency**: Check skills alignment between platforms
- **Recommendations**: Suggestions to improve profile consistency
- **Manual Input**: Alternative manual data entry option
- **URL Validation**: Smart URL format validation and error handling

### ⚙️ Settings
- **AI Model Configuration**: Choose between GPT-4 and GPT-3.5-turbo
- **File Processing**: Configure supported formats and file size limits
- **Report Preferences**: Set default report formats and options
- **Data Management**: Control analysis history and data retention
- **UI Customization**: Theme and language preferences

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd resume
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the root directory:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## 📦 Dependencies

- **Streamlit**: Web application framework
- **OpenAI**: AI model integration
- **LangChain**: AI prompt management
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualizations
- **ReportLab**: PDF generation
- **PyMuPDF**: PDF text extraction
- **docx2txt**: DOCX text extraction
- **streamlit-option-menu**: Enhanced navigation
- **BeautifulSoup4**: Web scraping for LinkedIn profiles
- **Requests**: HTTP requests for data fetching

## 🎯 Usage

1. **Upload Resume**: Use the file uploader to upload your resume
2. **Analyze**: Click "Analyze Sample Resume" for a demo or upload your own file
3. **LinkedIn Analysis**: Enter a LinkedIn profile URL to automatically fetch and analyze profile data
4. **Explore Results**: Navigate through different pages to explore insights
5. **Generate Reports**: Create professional reports in your preferred format
6. **Get Suggestions**: Use AI suggestions to improve your resume
7. **Compare Profiles**: Compare your resume with LinkedIn profile for consistency

## 🔧 Configuration

### AI Model Settings
- Choose between GPT-4 (recommended) and GPT-3.5-turbo
- Adjust creativity level (temperature) for different analysis styles

### File Processing
- Configure maximum file size (1-50 MB)
- Select supported file formats
- Set processing preferences

### Report Generation
- Choose default report format
- Enable/disable charts and visualizations
- Configure report styling options

## 📊 Analytics Features

### Dashboard Metrics
- **Total Analyses**: Number of resumes processed
- **Unique Candidates**: Number of different people analyzed
- **Daily Averages**: Average analyses per day
- **Recent Activity**: Latest analysis timestamps

### Visualizations
- **Timeline Charts**: Daily analysis trends
- **Candidate Rankings**: Most analyzed candidates
- **Skills Distribution**: Pie charts of skills
- **Radar Charts**: Skills coverage visualization

## 🎨 UI/UX Improvements

### Modern Design
- **Gradient Headers**: Beautiful gradient backgrounds
- **Card Layout**: Clean, organized information display
- **Skill Tags**: Colorful, interactive skill badges
- **Progress Indicators**: Visual feedback during processing

### Navigation
- **Sidebar Menu**: Easy navigation between features
- **Icons**: Intuitive icon-based navigation
- **Responsive Layout**: Works on different screen sizes

### Interactive Elements
- **Hover Effects**: Enhanced user interaction
- **Color Coding**: Visual distinction between different data types
- **Download Buttons**: Easy file downloads
- **Form Controls**: Intuitive input controls

## 🚀 Advanced Features

### Skills Gap Analysis
- Compare your skills with industry requirements
- Get match percentages for different job roles
- Receive personalized improvement suggestions

### AI-Powered Recommendations
- Resume structure suggestions
- Skills enhancement recommendations
- Format and content guidelines

### Data Export
- Export analytics data in CSV format
- Generate reports in multiple formats
- Download processed data for external use

## 🔮 Future Enhancements

- **Multi-language Support**: Support for different languages
- **Advanced Analytics**: More detailed insights and trends
- **Integration APIs**: Connect with job boards and ATS systems
- **Collaborative Features**: Team-based resume analysis
- **Mobile App**: Native mobile application

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the code comments

---

**Made with ❤️ using Streamlit and AI** 