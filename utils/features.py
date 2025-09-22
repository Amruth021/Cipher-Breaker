import math
from collections import Counter
import string


def friedman_test(text: str) -> int:
    """
    Estimate Vigenere key length using Friedman test.
    """
    ic = index_of_coincidence(text)
    if ic == 0:
        return 1
    k_est = (0.027 * len(text)) / ((len(text) - 1) * ic - 0.038 * len(text) + 0.065)
    return max(1, int(round(k_est)))

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def chi_squared_statistic(text: str) -> float:
    ENGLISH_FREQ = {
        'A': 8.167, 'B': 1.492, 'C': 2.782, 'D': 4.253, 'E': 12.702,
        'F': 2.228, 'G': 2.015, 'H': 6.094, 'I': 6.966, 'J': 0.153,
        'K': 0.772, 'L': 4.025, 'M': 2.406, 'N': 6.749, 'O': 7.507,
        'P': 1.929, 'Q': 0.095, 'R': 5.987, 'S': 6.327, 'T': 9.056,
        'U': 2.758, 'V': 0.978, 'W': 2.360, 'X': 0.150, 'Y': 1.974,
        'Z': 0.074
    }
    text = text.upper()
    letters = [c for c in text if c.isalpha()]
    N = len(letters)
    if N == 0:
        return float("inf")
    counts = Counter(letters)
    chi2 = 0
    for letter in ENGLISH_FREQ:
        expected = ENGLISH_FREQ[letter] * N / 100
        observed = counts.get(letter, 0)
        if expected > 0:
            chi2 += (observed - expected) ** 2 / expected
    return chi2

def index_of_coincidence(text: str) -> float:
    letters = [c for c in text.upper() if c.isalpha()]
    N = len(letters)
    if N <= 1:
        return 0.0
    counts = Counter(letters)
    numerator = sum(f * (f - 1) for f in counts.values())
    denominator = N * (N - 1)
    return numerator / denominator

def shannon_entropy(text: str) -> float:
    if not text:
        return 0.0
    freqs = Counter(text)
    return -sum((f/len(text)) * math.log2(f/len(text)) for f in freqs.values())

def printable_ratio(text: str) -> float:
    if not text:
        return 0.0
    return sum(c in string.printable for c in text) / len(text)

