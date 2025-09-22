# Cipher Detector 🔍

An experimental hybrid cipher/encoding detector & decoder for CTF challenges.  
Inspired by [Ciphey](https://github.com/bee-san/Ciphey) but built from scratch in Python with
frequency analysis, chi-squared statistics, Index of Coincidence, and heuristic search.

## Features
- Detects and decodes common ciphers:
  - Caesar, Atbash, Vigenère
  - Base32/Base64
  - Hex, Binary, Morse
  - Hash detection (MD5, SHA1, SHA256, SHA512)
- Optional integration with [John the Ripper](https://www.openwall.com/john/) for hash cracking
- Search engine (AuSearchV2) that combines multiple transformations
- Language scoring to pick the most English-like plaintext
- Extensible plugin system

## Installation
```bash
git clone https://github.com/<your-username>/CIpher-Detector.git
cd CIpher-Detector
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

