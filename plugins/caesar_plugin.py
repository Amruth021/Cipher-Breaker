from plugins import Plugin
import re
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class CaesarPlugin(Plugin):
    name = "Caesar"

    def accepts(self, text: str) -> bool:
    # Reject pure hex (hash-like) strings
        if re.fullmatch(r"[0-9a-fA-F]+", text):
            return False
        return any(c.isalpha() for c in text)



    def transform(self, text: str) -> list[str]:
        results = []
        for shift in range(1, 26):  # ROT1..ROT25
            decoded = []
            for c in text:
                if c.upper() in LETTERS:
                    idx = (LETTERS.index(c.upper()) - shift) % 26
                    decoded.append(LETTERS[idx] if c.isupper() else LETTERS[idx].lower())
                else:
                    decoded.append(c)
            results.append("".join(decoded))
        return results

