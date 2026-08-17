# 📬 Redtape Decoder

> Decoding official German letters (*Amtsdeutsch*) the easy way. 

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)](https://streamlit.io/)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

---

## 🧐 What is Redtape Decoder?

Dealing with German bureaucracy (*Behördendeutsch*) can be stressful, confusing, and overwhelming. **Redtape Decoder** is an AI-powered web service designed to bridge the language and comprehension gap. 

The application translates official German letters or documents into clear, conversational language (**Russian, English, Ukrainian, or Simple German / Leichte Sprache**), determines the urgency/deadlines, and outlines exact action items so you never miss an important deadline.

---

## ✨ Key Features

- **🌐 Multilingual Support:** Translate and explain letters into Russian, English, Ukrainian, or Leichte Sprache.
- **📂 Flexible Input:** Paste the text directly or upload document files (`.txt`).
- **⏰ Deadline & Urgency Tracking:** Instantly highlights critical dates and tells you what happens if you ignore the letter.
- **📌 Executive Summary:** Breaks down complex administrative texts into simple bullet points.
- **🎨 Clean UI:** Built with Streamlit for a smooth and intuitive user experience.
- **👁️ Multimodal Support: Upload images (photos/scans) of letters directly alongside plain text.
- **🛡️ Structured Data & Validation: Powered by Pydantic to ensure strict data validation and type safety for all LLM responses.

---

## 🚀 Getting Started

### Prerequisites

Make sure you have **Python 3.13+** installed on your machine.

### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/imnaur/redtape_decoder.git](https://github.com/imnaur/redtape_decoder.git)
   cd redtape_decoder
2. Create and activate a virtual environment:
python -m venv .venv
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate
3. Install dependencies:
pip install -r requirements.txt
4. Run the Streamlit app:
streamlit run ui/app.py


##  🛠️ Tech Stack

Frontend / UI: Streamlit

AI / LLM Integration: Custom core client (core.llm_client) communicating with modern LLMs.

Data Validation: Pydantic (v2)

AI / LLM Integration: OpenAI API (gpt-4o with JSON mode support), custom core client.

Language Processing: Python, JSON parsing.


## 📝 Project Structure

redtape_decoder/
│
├── core/
│   └── llm_client.py       # Logic for communicating with the LLM API
│
├── ui/
│   └── app.py              # Main Streamlit web interface
│
├── .venv/                  # Virtual environment
└── README.md               # Project documentation EN
└── README_DE.md            # Project documentation GERMAN

## Core Response Schema

class LetterAnalysis(BaseModel):
    sender: str
    deadline: Optional[str]
    action_required: bool
    summary_simple_de: str
    translation: str
    consequences_if_ignored: Optional[str]
