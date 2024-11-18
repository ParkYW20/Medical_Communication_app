# Medical Communication Analysis App

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 📖 Overview

The **Medical Communication Analysis App** analyzes doctor-patient conversations to identify issues, suggest improvements, and provide examples of better communication. It uses cutting-edge **speech-to-text (STT)**, **language models (RAG)**, and **text analysis techniques** to deliver actionable insights.

![App Screenshot](static/logo.png)

---

## 🚀 Features

- **Speech-to-Text (STT)**: Converts audio conversations into text.
- **Speaker Diarization**: Identifies who said what.
- **Text Analysis with LLMs**: Extracts key insights and recommendations from conversations.
- **Database Integration**: Stores analyzed conversations with timestamps.
- **Web Interface**: Intuitive design for easy upload, processing, and results viewing.

---

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/medical_communication_app.git
cd medical_communication_app
2. Install Dependencies

pip install -r requirements.txt
3. Set Up Configuration
Edit the config/settings.yaml file with your credentials:
Groq API Key
Hugging Face Access Token
4. Initialize the Database

python -c "from app.database import init_db; init_db()"
▶️ Usage
Run the App

python main.py
The app will be available at http://127.0.0.1:8000.
Workflow
Upload Audio: Provide a conversation audio file.
Processing: Wait while the app transcribes and analyzes the conversation.
Results: View the analysis and download the report.
📁 Directory Structure

medical_communication_app/
├── app/
│   ├── __init__.py         # Application initialization
│   ├── stt_processor.py    # Handles STT and speaker diarization
│   ├── rag_agent.py        # Analyzes conversations using LLMs
│   ├── database.py         # Manages SQLite database
│   └── templates/          # HTML templates for the web interface
│       ├── index.html      # Home page
│       ├── processing.html # Processing page
│       ├── result.html     # Results page
│       └── error.html      # Error page
├── config/
│   └── settings.yaml       # Configuration file for API keys and settings
├── data/
│   └── database.db         # SQLite database for storing results
├── output/                 # Stores transcription and analysis JSON files
├── static/
│   ├── styles.css          # CSS for styling the web interface
│   ├── logo.png            # Logo for branding
├── main.py                 # Entry point for the application
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies
└── .gitignore              # Ignore unnecessary files in version control
⚙️ Configuration
Update the config/settings.yaml file:

groq:
  api_key: "your-groq-api-key"

huggingface:
  access_token: "your-huggingface-token"

llm:
  model_name: "llama3-groq-70b-8192-tool-use-preview"
🌟 Key Features Explained
1. Speech-to-Text with Whisper
Powered by OpenAI's whisper model for large-scale transcription accuracy.
2. Speaker Diarization
Leverages pyannote.audio to separate speakers in multi-party conversations.
3. LLM Integration
Processes and analyzes text using Groq's LLM APIs, providing insights into communication.
4. Database Storage
Conversation data and analysis results are stored in a SQLite database

📋 Example Output
JSON Analysis Result

{
    "문제점": "환자가 의사를 정확히 이해하지 못함",
    "개선방안": "더 명확한 설명과 환자의 반응 확인",
    "개선된대화예시": "의사: 이 약은 하루 세 번 드세요. 이해되셨나요?",
    "점수": 85,
    "평가근거": "환자의 이해도를 향상시키기 위한 노력이 부족함"
}

🧪 Testing
Unit Tests

Add tests in the tests/ directory (if applicable).
Run tests using:

pytest
Manual Testing

Upload various conversation audio files to verify functionality.
🎨 Frontend Design
Responsive Layout: Adjusts to different screen sizes.
Clean UI: Uses a professional CSS design (static/styles.css).
Error Handling: Clear messages for missing data or processing issues.
🔧 Troubleshooting
Database Issues: Ensure database.db is created and writable.
API Key Errors: Verify your Groq and Hugging Face tokens in settings.yaml.
Python Dependency Conflicts: Use a virtual environment.
🤝 Contribution
Feel free to submit issues, create pull requests, or suggest new features!

📝 License
This project is licensed under the MIT License.

---

### 주요 포인트
1. **디렉토리 구조**:
   - 디렉토리와 파일의 역할을 명확히 설명.

2. **설치 및 실행 방법**:
   - `pip install`, 설정 파일 편집, 데이터베이스 초기화 과정 포함.

3. **사용법**:
   - 단계별 사용 절차 안내.

4. **결과 예시**:
   - JSON 분석 결과와 화면 스크린샷 설명.

5. **에러 처리**:
   - 발생 가능한 문제와 해결책.

이 `README.md`와 디렉토리 구조를 사용하면 프로젝트의 가독성과 완성도가 높아집니다!
