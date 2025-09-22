import re
from plugins import Plugin

class HashPlugin(Plugin):
    name = "Hash"

    patterns = {
        "MD5": re.compile(r"^[a-f0-9]{32}$", re.IGNORECASE),
        "SHA1": re.compile(r"^[a-f0-9]{40}$", re.IGNORECASE),
        "SHA256": re.compile(r"^[a-f0-9]{64}$", re.IGNORECASE),
        "SHA512": re.compile(r"^[a-f0-9]{128}$", re.IGNORECASE),
    }

    def accepts(self, text: str) -> bool:
        return any(p.match(text) for p in self.patterns.values())

    def transform(self, text: str) -> list[str]:
        detected = [name for name, p in self.patterns.items() if p.match(text)]
        if detected:
            return [f"HASH DETECTED: {detected[0]}"]
        return ["HASH DETECTED: UNKNOWN"]
    def confidence(self, text):
    	return 1.0 if self.accepts(text) else 0.0
