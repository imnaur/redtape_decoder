# 📬 Redtape Decoder

> Behördenschreiben (*Amtsdeutsch*) ganz einfach entschlüsseln.

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)](https://streamlit.io/)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

---

## 🧐 Was ist Redtape Decoder?

Der Umgang mit deutscher Bürokratie (*Behördendeutsch*) kann stressig, verwirrend und überwältigend sein. **Redtape Decoder** ist ein KI-gestützter Webdienst, der entwickelt wurde, um die Sprach- und Verständnisschranke zu überbrücken.

Die Anwendung übersetzt offizielle deutsche Schreiben oder Dokumente in klare, umgangssprachliche Sprache (**Russisch, Englisch, Ukrainisch oder Leichte Sprache**), ermittelt die Dringlichkeit und Fristen und zeigt konkrete Handlungsschritte auf, damit Sie keine wichtige Frist verpassen.

---

## ✨ Wichtigste Funktionen

- **🌐 Mehrsprachige Unterstützung:** Übersetzen und erklären Sie Schreiben ins Russische, Englische, Ukrainische oder in Leichte Sprache.
- **📂 Flexible Eingabe:** Füge den Text direkt ein oder lade Dokumentdateien (`.txt`) hoch.
- **⏰ Fristen- und Dringlichkeitsüberwachung:** Hebt wichtige Termine sofort hervor und informiert dich darüber, was passiert, wenn du das Schreiben ignorierst.
- **📌 Zusammenfassung:** Schlüsselt komplexe Verwaltungstexte in einfache Stichpunkte auf.
- **🎨 Übersichtliche Benutzeroberfläche:** Mit Streamlit erstellt für eine reibungslose und intuitive Benutzererfahrung.

---

## 🚀 Erste Schritte

### Voraussetzungen

Stellen Sie sicher, dass **Python 3.13+** auf Ihrem Rechner installiert ist.

### Installation

1. **Das Repository klonen:**
   ```bash
   git clone [https://github.com/imnaur/redtape_decoder.git](https://github.com/imnaur/redtape_decoder.git)
   cd redtape_decoder
2. Eine virtuelle Umgebung erstellen und aktivieren:
python -m venv .venv
# Unter macOS/Linux:
source .venv/bin/activate
# Unter Windows:
# .venv\Scripts\activate
3. Installieren Sie die Abhängigkeiten:
pip install -r requirements.txt
4. Starten Sie die Streamlit-App:
streamlit run ui/app.py


##  🛠️ Tech-Stack

Frontend / UI: Streamlit

KI / LLM-Integration: Benutzerdefinierter Core-Client (core.llm_client) zur Kommunikation mit modernen LLMs.

Sprachverarbeitung: Python, JSON-Parsing.


## 📝 Projektstruktur

redtape_decoder/
│
├── core/
│   └── llm_client.py       # Logik für die Kommunikation mit der LLM-API
│
├── ui/
│   └── app.py              # Haupt-Weboberfläche von Streamlit
│
├── .venv/                  # Virtuelle Umgebung
└── README.md               # Projektdokumentation EN
└── README_DE.md            # Projektdokumentation DEUTSCH
