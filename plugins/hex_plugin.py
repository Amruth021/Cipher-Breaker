from plugins import Plugin
import re

class HexPlugin(Plugin):
    name = "Hex"

    def accepts(self, text: str) -> bool:
        return re.fullmatch(r"[0-9a-fA-F]+", text) is not None and len(text) % 2 == 0

    def transform(self, text: str) -> list[str]:
        try:
            return [bytes.fromhex(text).decode(errors="ignore")]
        except Exception:
            return []

