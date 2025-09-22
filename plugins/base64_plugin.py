import base64, re
from plugins import Plugin

class Base64Plugin(Plugin):
    name = "Base64"

    def accepts(self, text: str) -> bool:
        return re.fullmatch(r"[A-Za-z0-9+/=]+", text) is not None and len(text) % 4 == 0

    def transform(self, text: str) -> list[str]:
        try:
            return [base64.b64decode(text).decode(errors="ignore")]
        except Exception:
            return []
    def confidence(self, text):
    	if not self.accepts(text): return 0.0
    	# base64 valid and contains '=' padding or many lowercase/uppercase letters -> stronger
    	pad = text.endswith("=")
    	alpha_ratio = sum(c.isalpha() for c in text) / max(1, len(text))
    	return 0.6 + 0.3*pad + 0.1*alpha_ratio
