
class Plugin:
    name = "BasePlugin"
    def accepts(self, text: str) -> bool: return False
    def transform(self, text: str) -> list[str]: return []
    def confidence(self, text: str) -> float:
        """Return cheap estimated confidence [0..1]. Default 0.5 for applicable."""
        return 0.5 if self.accepts(text) else 0.0


