#!/usr/bin/env python3
"""
main.py — entrypoint for the cipher detector with optional John-the-Ripper integration.

Usage examples:
  python3 main.py --file hash.txt
  python3 main.py --file hash.txt --john --wordlist wordlists/small.txt --john-timeout 10
"""

import argparse
from pathlib import Path

# detector & plugins (your modules)
from detector.language import LanguageChecker
from search.ausearch import AuSearchV2

from plugins.base64_plugin import Base64Plugin
from plugins.hex_plugin import HexPlugin
from plugins.caesar_plugin import CaesarPlugin
from plugins.atbash_plugin import AtbashPlugin
from plugins.vigenere_plugin import VigenerePlugin
from plugins.hash_plugin import HashPlugin
from plugins.base32_plugin import Base32Plugin
from plugins.binary_plugin import BinaryPlugin
from plugins.morse_plugin import MorsePlugin

# john wrapper (utils/john_wrapper.py)
try:
    from utils.john_wrapper import try_crack_with_john, john_installed
except Exception:
    # If utils.john_wrapper is missing, provide a no-op fallback.
    def try_crack_with_john(hash_text, detected_alg, john_path=None, wordlist=None, timeout=20):
        return False, None, "john-not-available"
    def john_installed(john_path=None):
        return None


def build_argparser():
    p = argparse.ArgumentParser(description="Cipher Detector Framework (with optional John the Ripper integration)")
    p.add_argument("--file", "-f", required=True, dest="file", help="Path to ciphertext file")
    # John-the-Ripper options
    p.add_argument("--john", action="store_true", help="Attempt to crack detected hashes using John the Ripper")
    p.add_argument("--john-path", default=None, help="Path to john binary (if not in PATH)")
    p.add_argument("--wordlist", default=None, help="Wordlist for John (or fallback quick cracker). If omitted, John uses its default rules.")
    p.add_argument("--john-timeout", type=int, default=20, help="Timeout (seconds) for John to run")
    # AuSearch options
    p.add_argument("--threshold", type=float, default=0.80, help="LanguageChecker score threshold (0..1)")
    p.add_argument("--max-depth", type=int, default=3, help="Max recursion depth for pipeline search")
    return p


def main():
    args = build_argparser().parse_args()
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"[!] File not found: {file_path}")
        return

    text = file_path.read_text(encoding="utf-8", errors="ignore").strip()
    print(f"[*] Loaded text: {repr(text)}")

    # instantiate language checker + plugins
    checker = LanguageChecker()
    plugins = [
        Base64Plugin(), HexPlugin(), CaesarPlugin(),
        AtbashPlugin(), VigenerePlugin(),
        HashPlugin(), Base32Plugin(), BinaryPlugin(), MorsePlugin()
    ]

    # Step 0: Immediate hash detection (before AuSearch)
    hash_plugin = HashPlugin()
    if hash_plugin.accepts(text):
        # get detected algorithm name from transform() output (expects "HASH DETECTED: MD5", etc.)
        detected_out = hash_plugin.transform(text)
        detected_label = detected_out[0] if detected_out else "HASH DETECTED: UNKNOWN"
        # normalize algorithm extraction (MD5 / SHA1 / ...)
        alg = None
        for tok in ("MD5", "SHA1", "SHA256", "SHA512"):
            if tok in detected_label.upper():
                alg = tok
                break

        # If user asked to crack with John, attempt it
        if args.john:
            john_path = args.john_path
            # quick presence check
            if not john_installed(john_path):
                print(f"[✓] Hash detected: {alg or 'UNKNOWN'}")
                print(f"[→] John status: john not found at PATH (set --john-path or install john).")
                return

            print(f"[✓] Hash detected: {alg or 'UNKNOWN'}")
            print(f"[→] Attempting to crack with John (timeout={args.john_timeout}s, wordlist={args.wordlist})...")
            cracked, plaintext, msg = try_crack_with_john(text, alg or "UNKNOWN", john_path=john_path, wordlist=args.wordlist, timeout=args.john_timeout)
            if cracked:
                print(f"[+] Hash cracked! Algorithm: {alg or 'UNKNOWN'}")
                print(f"[→] Plaintext: {plaintext}")
            else:
                print(f"[×] John status: {msg}")
                print(f"[→] Detected label: {detected_label}")
            return
        else:
            # no cracking requested: print detection only
            print(f"[✓] Hash detected: {alg or 'UNKNOWN'}")
            print(f"[→] Detected label: {detected_label}")
            print("[→] Tip: re-run with --john --wordlist <path> to attempt cracking.")
            return

    # Step 1: Not a hash — run AuSearch
    ausearch = AuSearchV2(plugins, checker, threshold=args.threshold, max_depth=args.max_depth, max_expansions=500)
    results = ausearch.search(text, top_k=3)
    
    if results:
        
        for rank,(pt,pipeline,score) in enumerate(results, start=1):
            
        	print(f"{rank}) Score={score:.3f} Pipeline={' -> '.join(pipeline)}")
        	print(f"    {pt}\n")
    else:
        print("[-] Could not decode.")


    if plaintext:
        # If the plugin returned a "HASH DETECTED" style string unexpectedly, present nicely.
        if isinstance(plaintext, str) and plaintext.upper().startswith("HASH DETECTED"):
            print(f"[✓] {plaintext}")
            print(f"[→] Pipeline: {' -> '.join(pipeline)}")
            return

        print(f"[✓] Found plaintext! Score={score:.2f}")
        print(f"[→] Pipeline: {' -> '.join(pipeline)}")
        print(f"[→] Plaintext: {plaintext}")
    else:
        print("[-] Could not decode.")


if __name__ == "__main__":
    main()
