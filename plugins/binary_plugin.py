from plugins import Plugin
import re

class BinaryPlugin(Plugin):
    name = "Binary"

    def accepts(self, text: str) -> bool:
        # Allow 0/1 with spaces or newlines
        return re.fullmatch(r"[01\s]+", text) is not None

    def transform(self, text: str) -> list[str]:
        try:
            bits = text.replace(" ", "").replace("\n", "")
            # pad to nearest multiple of 8
            if len(bits) % 8 != 0:
                bits = bits[:-(len(bits) % 8)]
            chars = [chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8)]
            return ["".join(chars)]
        except Exception:
            return []

