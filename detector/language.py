from utils.features import chi_squared_statistic, index_of_coincidence, shannon_entropy, printable_ratio

class LanguageChecker:
    def __init__(self):
        # expected values for English
        self.ic_expected = 0.065
        self.entropy_expected = 4.0  # bits/char
    
    def score(self, text: str) -> float:
        chi2 = chi_squared_statistic(text)
        ic = index_of_coincidence(text)
        entropy = shannon_entropy(text)
        printable = printable_ratio(text)

        # Normalize features into [0..1] scores
        chi2_score = 1 / (1 + chi2 / 100)  # lower chi2 = better
        ic_score = 1 - abs(ic - self.ic_expected) / 0.065
        entropy_score = 1 - abs(entropy - self.entropy_expected) / 3
        score = 0.4 * printable + 0.3 * chi2_score + 0.2 * ic_score + 0.1 * entropy_score
        if text.startswith("[HASH DETECTED"):
    	    return 1.0

        if "CTF" in text.upper() or "FLAG{" in text.upper():
            
            score += 0.3  # 🚩 boost if it looks like a flag


        return max(0, min(score, 1))  # clamp 0..1

