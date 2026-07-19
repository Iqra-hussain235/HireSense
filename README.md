# HireSense AI 🤖

**AI Resume Analyzer & Smart Recruitment Platform**

A production-ready SaaS application that leverages Google Gemini AI to provide comprehensive resume analysis for candidates and bulk screening capabilities for HR recruiters.

![HireSense AI](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-green.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.31.0-red.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)

---

## 🌟 Features

### For Candidates 👨‍💼

- **📊 Comprehensive Resume Analysis**
  - Overall score calculation (0-100)
  - ATS (Applicant Tracking System) compatibility score
  - Grammar and communication assessment
  - Resume design evaluation

- **🎯 Detailed Insights**
  - Strengths and weaknesses analysis
  - Missing skills identification
  - Improvement suggestions
  - Recommended projects to add

- **🗺️ Career Roadmap**
  - Personalized career path planning
  - Skill gap analysis
  - Learning milestones
  - Recommended certifications

- **💰 Salary Prediction**
  - Market-based salary estimation
  - Industry comparison
  - Negotiation tips

- **❓ Interview Preparation**
  - Technical questions generation
  - Behavioral questions
  - HR interview questions
  - Project-specific questions

- **🏆 Certificate Analysis**
  - Industry value assessment
  - Relevance scoring
  - Complementary certification suggestions

- **🌐 Multi-language Support**
  - English and Hinglish translations
  - Localized AI explanations

### For HR Recruiters 🏢

- **📋 Bulk Resume Screening**
  - Upload multiple resumes at once
  - Automated analysis for each candidate
  - Job description matching

- **🏆 Candidate Ranking**
  - AI-powered scoring system
  - Automated candidate sorting
  - Match status classification

- **📊 Hiring Dashboard**
  - Total candidates overview
  - Strong match identification
  - Average score tracking
  - Rejection rate monitoring

- **🎯 Skill Matrix**
  - Skill comparison across candidates
  - Experience distribution analysis
  - ATS score distribution

- **📈 Data Visualization**
  - Interactive charts and graphs
  - Candidate comparison radar charts
  - Hiring funnel visualization

- **📤 Export Options**
  - PDF report generation
  - Excel export
  - CSV export

### Technical Features ⚙️

- **🔍 OCR Processing**
  - Automatic text extraction from images
  - Scanned PDF processing
  - Multi-format support (PDF, DOCX, PNG, JPG)

- **🎨 Premium UI/UX**
  - Glassmorphism design
  - Aurora animated background
  - Smooth animations
  - Dark premium theme
  - Responsive layout

- **🐳 Docker Support**
  - Containerized deployment
  - Easy scaling
  - Production-ready configuration

---

## 🚀 Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Google Gemini API Key

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/HireSense-AI.git
cd HireSense-AI
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

```bash
cp .env.example .env
```

Edit the `.env` file and add your Google Gemini API Key:

```env
GEMINI_API_KEY=your_actual_api_key_here
```

### Step 5: Run the Application

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

---

## 🏗️ Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     HireSense AI                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │   Landing    │    │  Candidate   │    │   Recruiter  │ │
│  │    Page      │    │   Module     │    │   Module     │ │
│  └──────────────┘    └──────────────┘    └──────────────┘ │
│         │                    │                    │          │
│         └────────────────────┼────────────────────┘          │
│                              │                               │
│                    ┌───────────▼───────────┐                  │
│                    │   Core AI Module     │                  │
│                    │  (Gemini Client)    │                  │
│                    └───────────┬───────────┘                  │
│                              │                               │
│         ┌────────────────────┼────────────────────┐          │
│         │                    │                    │          │
│  ┌──────▼──────┐    ┌───────▼──────┐    ┌──────▼──────┐  │
│  │ OCR Module  │    │  Document    │    │ Translation │  │
│  │ (EasyOCR)   │    │  Extractor  │    │   Service   │  │
│  └─────────────┘    └─────────────┘    └─────────────┘  │
│                                                              │
│         ┌────────────────────┼────────────────────┐          │
│         │                    │                    │          │
│  ┌──────▼──────┐    ┌───────▼──────┐    ┌──────▼──────┐  │
│  │ Certificate │    │  PDF Report  │    │   Charts    │  │
│  │  Analyzer   │    │  Generator  │    │ Component  │  │
│  └─────────────┘    └─────────────┘    └─────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

#### Frontend
- **Streamlit**: Web framework
- **Plotly**: Interactive charts
- **Custom CSS**: Glassmorphism styling
- **JavaScript**: Animations and interactions

#### Backend
- **Python 3.10+**: Core language
- **Google Gemini AI**: AI analysis
- **EasyOCR**: Text extraction from images
- **PyMuPDF**: PDF processing
- **python-docx**: DOCX processing
- **Pillow**: Image processing
- **Pandas/NumPy**: Data manipulation
- **ReportLab**: PDF generation

#### Deployment
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Render**: Cloud deployment (optional)

---

## 📁 Folder Structure

```
HireSense-AI/
│
├── app.py                          # Main application entry point
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
├── Dockerfile                      # Docker configuration
├── docker-compose.yml              # Docker Compose configuration
│
├── assets/                         # Static assets
│   └── animations.js              # Custom JavaScript animations
│
├── css/                            # Stylesheets
│   └── styles.css                  # Global CSS with glassmorphism
│
├── components/                     # Reusable components
│   └── charts.py                   # Data visualization components
│
├── pages/                          # Page modules
│   ├── candidate/                  # Candidate-specific pages
│   └── recruiter/                  # Recruiter-specific pages
│
├── core/                           # Core business logic
│   └── ai/                         # AI integration
│       └── gemini_client.py       # Gemini API client
│
└── utils/                          # Utility modules
    ├── ocr_processor.py           # OCR text extraction
    ├── document_extractor.py      # Document text extraction
    ├── certificate_analyzer.py    # Certificate analysis
    ├── translator.py              # Translation service
    └── pdf_report_generator.py    # PDF report generation
```

---

## 🎯 Usage

### For Candidates

1. **Navigate to Candidate Module**
   - Click "Start Analysis" on the landing page

2. **Upload Resume**
   - Supported formats: PDF, DOCX, PNG, JPG
   - Maximum file size: 10MB

3. **Provide Job Context** (Optional)
   - Enter job role or paste job description
   - Upload certificates for additional analysis

4. **Select Language**
   - Choose English or Hinglish for output

5. **View Analysis**
   - Overall score and metrics
   - Detailed section analysis
   - Strengths and weaknesses
   - Improvement suggestions

6. **Additional Features**
   - Generate career roadmap
   - Get salary prediction
   - Prepare for interviews
   - Download PDF report

### For HR Recruiters

1. **Navigate to Recruiter Module**
   - Click "Start Recruiting" on the landing page

2. **Provide Job Description**
   - Paste the complete job description
   - Include required skills and qualifications

3. **Upload Resumes**
   - Upload multiple resumes at once
   - Supported formats: PDF, DOCX, PNG, JPG

4. **Analyze Candidates**
   - Click "Analyze Candidates"
   - Wait for AI processing

5. **Review Results**
   - View candidate rankings
   - Check match scores
   - Analyze skill matrix
   - Compare candidates

6. **Export Data**
   - Download PDF reports
   - Export to Excel
   - Export to CSV

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Google Gemini API Key (Required)
GEMINI_API_KEY=your_gemini_api_key_here

# Application Configuration
APP_NAME=HireSense AI
APP_VERSION=1.0.0
DEBUG=False

# OCR Configuration
OCR_LANGUAGE=en
OCR_GPU=False

# File Upload Configuration
MAX_FILE_SIZE=10485760
ALLOWED_EXTENSIONS=pdf,docx,png,jpg,jpeg

# AI Model Configuration
GEMINI_MODEL=gemini-pro
GEMINI_TEMPERATURE=0.7
GEMINI_MAX_TOKENS=2048
```

### Getting Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the API key
5. Add it to your `.env` file

---

## 🐳 Docker Deployment

### Build Docker Image

```bash
docker build -t hiresense-ai .
```

### Run with Docker

```bash
docker run -p 8501:8501 \
  -e GEMINI_API_KEY=your_api_key \
  -v $(pwd)/uploads:/app/uploads \
  hiresense-ai
```

### Run with Docker Compose

```bash
# Copy .env.example to .env and add your API key
cp .env.example .env

# Start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

---

## 🌐 Deployment

### Deploy to Render

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Create Render Account**
   - Visit [render.com](https://render.com)
   - Sign up and create a new web service

3. **Configure Deployment**
   - Connect your GitHub repository
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
   - Add environment variables (especially `GEMINI_API_KEY`)

4. **Deploy**
   - Click "Deploy Web Service"
   - Wait for deployment to complete

### Deploy to Other Platforms

The application can be deployed to any platform that supports:
- Python 3.10+
- Streamlit
- Environment variables

Popular options:
- **Heroku**: Using the Procfile approach
- **AWS**: Using EC2 or Elastic Beanstalk
- **Google Cloud**: Using Cloud Run
- **Azure**: Using App Service

---

## 📊 Screenshots

### Landing Page
*[Placeholder: Screenshot of the premium landing page with glassmorphism cards]*

### Candidate Analysis
*[Placeholder: Screenshot of candidate analysis dashboard with scores]*

### HR Dashboard
*[Placeholder: Screenshot of HR recruiter dashboard with candidate rankings]*

### Report Generation
*[Placeholder: Screenshot of PDF report generation]*

---

## 🔮 Future Improvements

### Planned Features

- **🤖 Enhanced AI Models**
  - Integration with additional AI providers
  - Custom model fine-tuning
  - Multi-language support expansion

- **📱 Mobile Application**
  - React Native mobile app
  - Push notifications
  - Offline mode

- **🔐 Authentication & User Management**
  - User registration and login
  - Role-based access control
  - OAuth integration
  - Profile management

- **💾 Database Integration**
  - PostgreSQL for data persistence
  - MongoDB for document storage
  - Redis for caching
  - Analysis history

- **📈 Advanced Analytics**
  - Real-time analytics dashboard
  - Trend analysis
  - Predictive hiring insights
  - Market salary trends

- **🔔 Notification System**
  - Email notifications
  - SMS alerts
  - In-app notifications
  - Integration with Slack/Teams

- **🌍 Global Expansion**
  - Multi-language support (10+ languages)
  - Region-specific salary data
  - Local job market insights
  - Currency conversion

- **🔗 API Development**
  - RESTful API endpoints
  - API documentation
  - Rate limiting
  - Webhook support

- **🎨 UI/UX Enhancements**
  - Dark/Light theme toggle
  - Customizable dashboards
  - Drag-and-drop file uploads
  - Real-time progress indicators

### Technical Improvements

- **⚡ Performance Optimization**
  - Caching layer implementation
  - Async processing for large files
  - Database query optimization
  - CDN integration for static assets

- **🧪 Testing**
  - Unit tests with pytest
  - Integration tests
  - E2E testing with Playwright
  - CI/CD pipeline

- **📝 Documentation**
  - API documentation
  - Contributing guidelines
  - Code of conduct
  - Architecture documentation

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

1. **Code Style**
   - Follow PEP 8 guidelines
   - Use type hints
   - Add docstrings to functions
   - Write clean, modular code

2. **Testing**
   - Write tests for new features
   - Ensure all tests pass
   - Maintain test coverage above 80%

3. **Documentation**
   - Update README for new features
   - Add inline comments for complex logic
   - Keep documentation up-to-date

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **Google Gemini AI** for providing the powerful AI API
- **Streamlit** for the amazing web framework
- **EasyOCR** for the OCR text extraction
- **Plotly** for the interactive charts
- **Open-source community** for the incredible tools and libraries

---

## 📞 Support

For support, please:

1. Open an issue on GitHub
2. Email: support@hiresense.ai
3. Join our Discord community

---

## 🌟 Star History

If you find this project useful, please consider giving it a ⭐ on GitHub!

---

## 📞 Contact

- **Author**: HireSense AI Team
- **Email**: contact@hiresense.ai
- **Website**: [hiresense.ai](https://hiresense.ai)
- **GitHub**: [github.com/yourusername/HireSense-AI](https://github.com/yourusername/HireSense-AI)

---

**Built with ❤️ using AI-Powered Resume Analysis**

*© 2024 HireSense AI. All rights reserved.*
