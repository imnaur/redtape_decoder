import pypdf


def extract_text_from_file(uploaded_file) -> str:
    """Extracts text from a PDF or TXT file."""
    if uploaded_file is None:
        return ""

    file_extension = uploaded_file.name.split(".")[-1].lower()

    if file_extension == "txt":
        return uploaded_file.getvalue().decode("utf-8")

    elif file_extension == "pdf":
        try:
            reader = pypdf.PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
            return text
        except Exception as e:
            raise RuntimeError(f"Failed to read PDF: {e}")

    return ""
