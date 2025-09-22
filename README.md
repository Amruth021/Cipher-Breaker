
Cipher-Breaker

**Cipher-Breaker** is a Python-based cryptographic text detector & decoder framework, designed for **CTF challenges** and general crypto fun.  
It draws inspiration from [Ciphey](https://github.com/bee-san/Ciphey), but is built from scratch with a plugin system, search engine, and optional hash cracking via **John the Ripper**.

---

## Installation

Clone the repo:

```bash
git clone https://github.com/Amruth021/Cipher-Breaker.git
cd Cipher-Breaker
````

Create a virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

(Dependencies: `argparse`, `scikit-learn`, `joblib`)

---

## (Optional) Install John the Ripper

To enable real hash cracking:

```bash
sudo apt install john   # May be old
# OR build jumbo (recommended):
git clone https://github.com/openwall/john.git
cd john/src
./configure && make -s
```

---

## Usage

### Detect / decode a file

```bash
python3 main.py --file samples/base64.txt
```

### Detect + crack hash with John

```bash
python3 main.py --file samples/hash.txt --john --wordlist wordlists/rockyou.txt --john-timeout 30
```

### Adjust depth & threshold

```bash
python3 main.py --file samples/complex.txt --max-depth 4 --threshold 0.75
```

---




