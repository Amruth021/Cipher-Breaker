from plugins import Plugin

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class AtbashPlugin(Plugin):
    name = "Atbash"

    def accepts(self, text: str) -> bool:
        return all(c.upper() in LETTERS or not c.isalpha() for c in text)

    def transform(self, text: str) -> list[str]:
        result = []
        decoded = []
        for c in text:
            if c.upper() in LETTERS:
                idx = 25 - LETTERS.index(c.upper())
                decoded.append(LETTERS[idx] if c.isupper() else LETTERS[idx].lower())
            else:
                decoded.append(c)
        result.append("".join(decoded))
        return result

