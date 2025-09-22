# utils/john_wrapper.py
import subprocess
import shutil
import tempfile
from pathlib import Path
from typing import Optional, Tuple

# map detected -> john format
JOHN_FORMAT_MAP = {
    "MD5": "raw-md5",
    "SHA1": "raw-sha1",
    "SHA256": "raw-sha256",
    "SHA512": "raw-sha512",
}

def john_installed(john_path: Optional[str] = None) -> Optional[str]:
    """Return path to john binary or None."""
    if john_path:
        p = Path(john_path)
        return str(p) if p.exists() else None
    # try system lookup
    p = shutil.which("john")
    return p

def try_crack_with_john(hash_text: str,
                        detected_alg: str,
                        john_path: Optional[str] = None,
                        wordlist: Optional[str] = None,
                        timeout: int = 30) -> Tuple[bool, Optional[str], str]:
    """
    Try to crack hash_text with John.
    Returns: (cracked_bool, plaintext_or_None, message)
    - Timeout is seconds to allow for john to run.
    """
    john_bin = john_installed(john_path)
    if not john_bin:
        return False, None, "john-not-found"

    fmt = JOHN_FORMAT_MAP.get(detected_alg.upper())
    if not fmt:
        return False, None, f"unsupported-format-{detected_alg}"

    # create temp dir + hash file
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        hash_file = td_path / "hashes.txt"
        # write exact hash line (john expects one-per-line)
        hash_file.write_text(hash_text.strip() + "\n")

        cmd = [john_bin, f"--format={fmt}"]
        if wordlist:
            cmd += [f"--wordlist={wordlist}"]
        cmd += [str(hash_file)]

        try:
            # run john with timeout
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=timeout, check=False)
        except subprocess.TimeoutExpired:
            # give john a last chance: run --show even if timed out (it may have cracked)
            show = subprocess.run([john_bin, "--show", str(hash_file)], capture_output=True, text=True)
            out = show.stdout.strip()
            # Parse --show output for cracked values
            cracked = _parse_john_show_output(out)
            if cracked:
                return True, cracked, "cracked-after-timeout"
            return False, None, "timeout"

        # after john finishes (or returned quickly) check results
        show = subprocess.run([john_bin, "--show", str(hash_file)], capture_output=True, text=True)
        out = show.stdout.strip()
        cracked = _parse_john_show_output(out)
        if cracked:
            return True, cracked, "cracked"
        return False, None, "not-cracked"

def _parse_john_show_output(show_output: str) -> Optional[str]:
    """
    parse john --show output.
    Format example (when cracked):
      hash:password
    or lines like:
      5d41402abc4b2a76b9719d911017c592:hello
    john --show also prints summary; we search for ':' lines.
    """
    if not show_output:
        return None
    for line in show_output.splitlines():
        line = line.strip()
        if ":" in line and not line.lower().startswith("guesses"):
            parts = line.split(":", 1)
            if len(parts) >= 2 and parts[1]:
                return parts[1]
    return None

