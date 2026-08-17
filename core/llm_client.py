import base64
import mimetypes
import os
import sys
from pathlib import Path
from typing import Any, Optional, cast

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

from .prompts import SYSTEM_PROMPT

root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

client = OpenAI()
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o")


class LetterAnalysis(BaseModel):
    sender: str = Field(..., description="The official name of the sender")
    deadline: Optional[str] = Field(None, description="Deadline in YYYY-MM-DD format")
    action_required: bool
    summary_simple_de: str
    translation: str
    consequences_if_ignored: Optional[str] = None


def send_to_llm(text: Optional[str] = None, image_file=None, target_language: str = "Russian") -> LetterAnalysis:
    """Send a bureaucratic letter  (text or image) to LLM and returns the analysis.

    Args:
        text: The text of the bureaucratic letter.
        image_file: Streamlit UploadedFile object (optional if text is provided).
        target_language: The language for the explanation.

    Returns:
        str: JSON-formatted string with the analysis.
    """

    has_text = text and text.strip() != ""
    has_image = image_file is not None
    if not has_text and not has_image:
        raise ValueError("Please provide the text or an image of the letter!")

    user_content: list[dict[str, Any]] = [
        {"type": "text", "text": f"Target language for explanation: {target_language}"}
    ]

    if has_text:
        user_content.append({"type": "text", "text": f"Letter text: \n{text}"})

    if has_image:
        image_bytes = image_file.getvalue()
        base64_image = base64.b64encode(image_bytes).decode("utf-8")

        mime_type, _ = mimetypes.guess_type(image_file.name)
        if not mime_type or not mime_type.startswith("image/"):
            mime_type = "image/jpeg"

        user_content.append({"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{base64_image}"}})

    try:
        response = cast(Any, client.chat).completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
            ],
            response_format={"type": "json_object"},
        )

        raw_content = response.choices[0].message.content
        if not raw_content:
            raise ValueError("Received empty response from LLM.")

        return LetterAnalysis.model_validate_json(raw_content)

    except Exception as e:
        raise RuntimeError(f"Failed to process letter with LLM: {e}")
