
# 의연담 : 의료 소통 분석 앱

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 📖 Overview

The **의료 소통 분석 앱** is designed to analyze doctor-patient conversations by utilizing advanced AI technologies. This app converts audio files into text, identifies speakers, and provides actionable feedback for improving communication. Its user-friendly interface ensures a seamless workflow for analyzing and reviewing results.

![App Screenshot](medical_communication_app/static/logo.png)

---

## 🚀 Features

- **Speech-to-Text (STT)**: Converts audio files to text using OpenAI's Whisper model.
- **Speaker Diarization**: Identifies and separates speakers using Pyannote's pipeline.
- **Text Analysis**: Processes conversations using Groq's LLMs to extract insights.
- **Database Integration**: Automatically stores analysis results with timestamps.
- **Web Interface**: Upload audio files, view results, and download analysis reports.

---

## 🧪 Output

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


## 🤝 Contribution

Contributions are welcome! Feel free to submit issues, fork the repository, or create pull requests.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
