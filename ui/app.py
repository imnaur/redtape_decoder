import json
import sys
from pathlib import Path
from ui.languages import ui_texts

root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

from core.llm_client import send_to_llm
import streamlit as st

st.set_page_config(page_title="Redtape Decoder", page_icon="📬", layout="centered")

st.title("📬 Redtape Decoder")
st.subheader("Decoding official German letters the easy way")

target_language = st.selectbox(
    "Into which language should this be translated and explained??",
    ["Russian", "English", "Ukrainian", "Simple German (Leichte Sprache)"],
    key="target_language_selector",
)

t = ui_texts.get(target_language, ui_texts["English"])


def extract_text_from_file(uploaded_file):
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split(".")[-1].lower()
        if file_extension == "txt":
            return uploaded_file.getvalue().decode("utf-8")
        elif file_extension == "pdf":
            try:
                import pypdf

                reader = pypdf.PdfReader(uploaded_file)
                text = ""
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
                return text
            except Exception as e:
                st.error(f"Ошибка при чтении PDF: {e}")
                return ""
    return ""


input_choice = st.radio(
    t["input_mode"], [t["mode_text"], t["mode_file"]], horizontal=True
)

final_letter_text = ""

if input_choice == t["mode_text"]:
    letter_text = st.text_area(
        "Paste the text of the German letter (Amtsdeutsch):",
        height=200,
        placeholder="For example: Sehr geehrte Damen und Herren...",
    )
    final_letter_text = letter_text
else:
    uploaded_file = st.file_uploader(
        "Choose a PDF or TXT file", type=["pdf", "txt"]
    )
    if uploaded_file is not None:
        final_letter_text = extract_text_from_file(uploaded_file)

        if not final_letter_text.strip():
            st.warning(
                "⚠️ Не удалось извлечь текст из файла. Возможно, это сканированный PDF (картинка). Попробуйте скопировать текст вручную."
            )

# -----------------------------------------------------------------------------------------------------------------------

if st.button("Decipher the letter 📩", type="primary"):
    if not final_letter_text.strip():
        st.warning(t["error_empty"])
    else:
        with st.spinner(t["spinner"]):
            try:
                response_json = send_to_llm(final_letter_text, target_language)
                data = json.loads(response_json)
                st.divider()
                st.success(t["success"])

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(
                        f"**{t['sender']}:** {data.get('sender', 'Not specified')}"
                    )
                with col2:
                    deadline = data.get("deadline")
                    if deadline:
                        st.markdown(f"**{t['deadline']}:** {deadline}")
                    else:
                        st.markdown(f"**{t['no_deadline']}**")

                st.markdown(f"### {t['nutshell']}")
                st.info(data.get("summary_simple_de"))

                st.markdown(f"### {t['translation']}")
                st.write(data.get("translation"))

                if data.get("consequences_if_ignored"):
                    st.markdown(f"### {t['consequences']}")
                    st.warning(data.get("consequences_if_ignored"))

            except Exception as e:
                st.error(f"An error occurred during processing: {e}")
