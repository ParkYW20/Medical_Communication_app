
# Medical Communication App

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 📖 Overview

The **Medical Communication Analysis App** is designed to analyze doctor-patient conversations by utilizing advanced AI technologies. This app converts audio files into text, identifies speakers, and provides actionable feedback for improving communication. Its user-friendly interface ensures a seamless workflow for analyzing and reviewing results.

![App Screenshot](medical_communication_app/static/logo.png)

---

## 🚀 Features

- **Speech-to-Text (STT)**: Converts audio files to text using OpenAI's Whisper model.
- **Speaker Diarization**: Identifies and separates speakers using Pyannote's pipeline.
- **Text Analysis**: Processes conversations using Groq's LLMs to extract insights.
- **Database Integration**: Automatically stores analysis results with timestamps.
- **Web Interface**: Upload audio files, view results, and download analysis reports.

---

## 🛠️ Installation

### Prerequisites

- Python 3.10+
- Pip installed

### Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/medical_communication_app.git
   cd medical_communication_app
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Configuration**
   - Edit the `config/settings.yaml` file to include your:
     - **Groq API Key**
     - **Hugging Face Access Token**

4. **Initialize the Database**
   ```bash
   python -c "from app.database import init_db; init_db()"
   ```

---

## ▶️ Usage

### Run the App

Start the FastAPI server:
```bash
python main.py
```

The app will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## 📁 Directory Structure

```plaintext
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
```

---

## 🌟 Key Features Explained

### 1. **Speech-to-Text with Whisper**
Utilizes OpenAI's Whisper model for robust transcription.

### 2. **Speaker Diarization**
Separates speakers in multi-party conversations using Pyannote.

### 3. **LLM Integration**
Processes conversation data with Groq's LLM APIs for actionable insights.

### 4. **Database Storage**
Automatically saves analyzed conversations into a SQLite database with timestamps.

---

## 🧪 Example Output

### JSON Analysis Result
```json
{
    "문제점": "환자가 의사를 정확히 이해하지 못함",
    "개선방안": "더 명확한 설명과 환자의 반응 확인",
    "개선된대화예시": "의사: 이 약은 하루 세 번 드세요. 이해되셨나요?",
    "점수": 85,
    "평가근거": "환자의 이해도를 향상시키기 위한 노력이 부족함"
}
```

### Database Entry
```sql
+----+--------------------+---------------------+---------------------+
| id | conversation_text  | analysis_result    | timestamp           |
+----+--------------------+---------------------+---------------------+
|  1 | "환자와 의사의 대화..." | {...}           | 2024-11-19 14:25:00 |
+----+--------------------+---------------------+---------------------+
```

---

## 🎨 Frontend Design

- **Responsive Layout**: Optimized for all devices.
- **Clean UI**: Styled using a minimalist CSS design (`static/styles.css`).
- **Error Handling**: Clear feedback for missing data or processing issues.

---

## ⚙️ Configuration

### Example `settings.yaml`
```yaml
groq:
  api_key: "your-groq-api-key"

huggingface:
  access_token: "your-huggingface-access-token"

llm:
  model_name: "llama3-groq-70b-8192-tool-use-preview"
```

---

## ⚡ Troubleshooting

- **Database Issues**: Ensure the `data/database.db` file exists and is writable.
- **API Errors**: Verify your Groq and Hugging Face tokens in `settings.yaml`.
- **Python Dependencies**: Use a virtual environment to manage conflicts.

---

## 🤝 Contribution

Contributions are welcome! Feel free to submit issues, fork the repository, or create pull requests.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
