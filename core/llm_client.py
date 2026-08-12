import os
from dotenv import load_dotenv
from openai import OpenAI
from .prompts import SYSTEM_PROMPT
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

client = OpenAI()


def send_to_llm(text: str, target_language: str = "Russian") -> str | None:
    """Send a bureaucratic letter to LLM and returns the analysis.

        Args:
            text: The text of the bureaucratic letter.
            target_language: The language for the explanation.

        Returns:
            str: JSON-formatted string with the analysis.
        """
    if not text or not text.strip():
        raise ValueError("Please provide the text of the letter!")

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[  # type: ignore[list-item]
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",
                 "content": f"Target language for explanation: {target_language}\n\nLetter text: \n{text}"}
            ],
            response_format={"type": "json_object"}  # type: ignore[list-item]
        )
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"Failed to communicate with LLM: {e}")
