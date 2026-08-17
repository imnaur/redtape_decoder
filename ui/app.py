import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

import streamlit as st

from core.llm_client import send_to_llm
from core.processor import extract_text_from_file
from ui.languages import ui_texts

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
uploaded_images = []

if input_choice == t["mode_text"]:
    final_letter_text = st.text_area(
        "Paste the text of the German letter (Amtsdeutsch):",
        height=200,
        placeholder="For example: Sehr geehrte Damen und Herren...",
    )
else:
    uploaded_files = st.file_uploader(
        "Choose a PDF, TXT file or an image (photo of the letter)", type=["pdf", "txt", "png", "jpg", "jpeg"],
        accept_multiple_files=True
    )
    extracted_texts = []
    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_extension = uploaded_file.name.split(".")[-1].lower()

            if file_extension in ["png", "jpg", "jpeg"]:
                uploaded_images.append(uploaded_file)
                st.success(f"📷 Image '{uploaded_file.name}' uploaded successfully!")
            else:
                text = extract_text_from_file(uploaded_file)
                if text and text.strip():
                    extracted_texts.append(text)
                else:
                    st.warning(
                        f"⚠️ We were unable to extract text from '{uploaded_file.name}'. "
                        "It may be a scanned PDF. Try taking a photo of it and uploading it as an image."
                    )

        if extracted_texts:
            final_letter_text = "\n\n".join(extracted_texts)

if st.button("Decipher the letter 📩", type="primary"):
    has_text = bool(final_letter_text and final_letter_text.strip())
    has_images = len(uploaded_images) > 0

    if not has_text and not has_images:
        st.warning(t["error_empty"])
    else:
        with st.spinner(t["spinner"]):
            try:
                current_image = uploaded_images[0] if uploaded_images else None

                data = send_to_llm(
                    text=final_letter_text if has_text else None,
                    image_files=uploaded_images,
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
