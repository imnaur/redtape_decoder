import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

import streamlit as st
import json
from core.llm_client import send_to_llm

st.set_page_config(page_title='Redtape Decoder', page_icon='📬', layout='centered')

st.title('📬 Redtape Decoder')
st.subheader('Расшифровка немецких официальных писем без боли')

letter_text = st.text_area(
    "Вставьте текст немецкого письма (Amtsdeutsch):",
    height=200,
    placeholder="Например: Sehr geehrte Damen und Herren, hiermit fordern wir Sie auf..."
)
target_language = st.selectbox(
    "На какой язык перевести и объяснить?",
    ["Russian", "English", "Simple German (Leichte Sprache)", "Ukrainian"]
)
if st.button('Расшифровать письмо ✍️', type='primary'):
    if not letter_text.strip():
        st.warning('Пожалуйста, вставьте текст письма!')
    else:
        with st.spinner('Нейросеть разбирает письмо...'):
            try:
                response_json = send_to_llm(letter_text, target_language)
                data = json.loads(response_json)
                st.divider()
                st.success('Готово! Вот что от Вас хотят:')
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Отправитель** {data.get('sender', 'Не указан')}")
                with col2:
                    deadline = data.get('deadline')
                    if deadline:
                        st.markdown(f"**Дедлайн** {data.get('deadline')}")
                    else:
                        st.markdown("**Дедлайна нет!**")
                st.markdown("### 📌 Краткая суть:")
                st.info(data.get('summary_simple_de'))

                st.markdown("### 🌍 Перевод и объяснение:")
                st.write(data.get('translation'))

                if data.get('consequences_if_ignored'):
                    st.markdown("### ⚠️ Что будет, если проигнорировать:")
                    st.warning(data.get('consequences_if_ignored'))

            except Exception as e:
                st.error(f"Произошла ошибка при обработке: {e}")
