
# 의연담 : 의료 소통 분석 앱

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 📖 Overview

**의료 소통 분석 앱**은 의사와 환자 간의 대화를 분석하기 위해 고급 AI 기술을 활용하는 앱입니다. 이 앱은 오디오 파일을 텍스트로 변환하고, 화자를 식별하며, 소통 개선을 위한 실질적인 피드백을 제공합니다. 사용자 친화적인 인터페이스를 통해 분석 및 결과 검토를 손쉽게 진행할 수 있습니다.

![App Screenshot](medical_communication_app/static/logo.png)

---

## 🚀 Features

- **음성 인식 (STT)**: OpenAI의 Whisper 모델을 사용하여 오디오 파일을 텍스트로 변환합니다.
- **화자 분리**: Pyannote의 파이프라인을 활용해 화자를 식별하고 분리합니다.
- **텍스트 분석**: Groq의 LLM을 통해 대화를 분석하고 통찰을 추출합니다.
- **데이터베이스 연동**: 분석 결과를 타임스탬프와 함께 자동으로 저장합니다.
- **웹 인터페이스**: 오디오 파일 업로드, 결과 확인, 분석 보고서 다운로드 기능을 제공합니다.

---

## 🧪 Output

### JSON 분석 결과
```json
{
    "문제점": "환자가 의사를 정확히 이해하지 못함",
    "개선방안": "더 명확한 설명과 환자의 반응 확인",
    "개선된대화예시": "의사: 이 약은 하루 세 번 드세요. 이해되셨나요?",
    "점수": 85,
    "평가근거": "환자의 이해도를 향상시키기 위한 노력이 부족함"
}
```

### 데이터 베이스 저장
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

이 프로젝트는 MIT 라이선스로 제공됩니다.(LICENSE).
