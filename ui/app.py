import json
import sys
from pathlib import Path

import streamlit as st

from core.llm_client import send_to_llm
from core.processor import extract_text_from_file
from ui.languages import ui_texts

root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

st.set_page_config(page_title="Redtape Decoder", page_icon="📬", layout="centered")

target_language = st.selectbox(
    "Into which language should this be translated and explained??",
    ["Russian", "English", "Ukrainian", "Simple German (Leichte Sprache)"],
    key="target_language_selector",
)

t = ui_texts.get(target_language, ui_texts["English"])

st.title("📬 Redtape Decoder")
st.subheader("Decoding official German letters the easy way")

input_choice = st.radio(t["input_mode"], [t["mode_text"], t["mode_file"]], horizontal=True)

final_letter_text = ""
uploaded_image = None
uploaded_file = None

if input_choice == t["mode_text"]:
    final_letter_text = st.text_area(
        "Paste the text of the German letter (Amtsdeutsch):",
        height=200,
        placeholder="For example: Sehr geehrte Damen und Herren...",
    )
else:
    uploaded_file = st.file_uploader(
        "Choose a PDF, TXT file or an image (photo of the letter)", type=["pdf", "txt", "png", "jpg", "jpeg"]
    )

    if uploaded_file is not None:
        file_extension = uploaded_file.name.split(".")[-1].lower()

        if file_extension in ["png", "jpg", "jpeg"]:
            uploaded_image = uploaded_file
            st.success("📷 Image uploaded successfully!")
        else:
            final_letter_text = extract_text_from_file(uploaded_file)
            if not final_letter_text.strip():
                st.warning(
                    "⚠️ We were unable to extract text from the file. It may be a scanned PDF. Try taking a photo of it and uploading it as an image."
                )

# Кнопка отправки
if st.button("Decipher the letter 📩", type="primary"):
    has_text = bool(final_letter_text and final_letter_text.strip())
    has_image = uploaded_image is not None

    if not has_text and not has_image:
        st.warning(t["error_empty"])
    else:
        with st.spinner(t["spinner"]):
            try:
                response_json = send_to_llm(
                    text=final_letter_text if has_text else None,
                    image_file=uploaded_image,
                    target_language=target_language,
                )
                data = send_to_llm(
                    text=final_letter_text if has_text else None,
                    image_file=uploaded_image,
                    target_language=target_language,
                )

                st.divider()
                st.success(t["success"])

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**{t['sender']}:** {data.sender}")
                with col2:
                    deadline = data.deadline
                    if deadline:
                        st.markdown(f"**{t['deadline']}:** {deadline}")
                    else:
                        st.markdown(f"**{t['no_deadline']}**")

                st.markdown(f"### {t['nutshell']}")
                st.info(data.summary_simple_de)

                st.markdown(f"### {t['translation']}")
                st.write(data.translation)

                if data.consequences_if_ignored:
                    st.markdown(f"### {t['consequences']}")
                    st.warning(data.consequences_if_ignored)

            except Exception as e:
                st.error(f"An error occurred during processing: {e}")
