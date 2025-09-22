from plugins import Plugin
from utils.features import friedman_test
import re
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class VigenerePlugin(Plugin):
    name = "Vigenere"

    def accepts(self, text: str) -> bool:
    # Reject pure hex (hash-like) strings
        if re.fullmatch(r"[0-9a-fA-F]+", text):
            return False
        return any(c.isalpha() for c in text)






    def transform(self, text: str) -> list[str]:
        candidates = []
        key_len = friedman_test(text)
        
        # 🔑 Try small candidate keys
        trial_keys = ["KEY", "CTF", "FLAG"]
        trial_keys += ["A", "B", "C"]  # 1-char keys act like Caesar
        trial_keys += ["AB", "CD"]     # expand if you want

        for key in trial_keys:
            decoded = []
            ki = 0
            for c in text:
                if c.upper() in LETTERS:
                    shift = LETTERS.index(key[ki % len(key)].upper())
                    idx = (LETTERS.index(c.upper()) - shift) % 26
                    decoded.append(LETTERS[idx] if c.isupper() else LETTERS[idx].lower())
                    ki += 1
                else:
                    decoded.append(c)
            candidates.append("".join(decoded))

        return candidates

