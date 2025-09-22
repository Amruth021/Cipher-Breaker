import base64, re
from plugins import Plugin

class Base32Plugin(Plugin):
    name = "Base32"

    def accepts(self, text: str) -> bool:
        return re.fullmatch(r"[A-Z2-7=]+", text) is not None

    def transform(self, text: str) -> list[str]:
        try:
            return [base64.b32decode(text).decode(errors="ignore")]
        except Exception:
            return []

