# CS5158-Project-1-Index-of-Coincidence

A command-line tool for classical cryptanalysis of the Vigenère cipher. It computes letter-frequency statistics and the Index of Coincidence (IC) for a text, encrypts/decrypts short strings with a Vigenère key, and runs a Kasiski/IC-based attack to recover an unknown key length and key from ciphertext.

## Project Structure

```
ic_m14998238/
├── src/
│   └── main.py            # All program logic and the interactive menu
├── build/                  # Build output (empty; reserved per assignment spec)
├── data/
│   ├── GiftOfTheMagi.txt
│   ├── MasqueOfTheRedDeath.txt
│   └── TheGreatGatsby.txt
└── report.pdf              # Written report for the assignment
```

The sample texts in `data/` are used as plaintext source material for frequency analysis and for generating long ciphertexts to attack.

## Requirements

- Python 3
- [matplotlib](https://matplotlib.org/) (only required for the frequency bar graph option)

Install matplotlib if needed:

```bash
pip install matplotlib
```

## Usage

Run the program from the `ic_m14998238/src` directory:

```bash
cd ic_m14998238/src
python3 main.py
```

You'll be presented with a menu:

1. **Frequency** — print the frequency of each letter (a-z) in the loaded text.
2. **Index of Coincidence** — calculate the IC of the loaded text.
3. **Frequency Bar Graph** — display a bar chart of letter frequencies using matplotlib.
4. **Encrypt** — encrypt a 100-character lowercase string with a user-supplied key (2-20 characters) using a Vigenère cipher.
5. **Decrypt** — decrypt a 100-character uppercase ciphertext with a user-supplied key.
6. **Long Cipher Encryption** — build a 10,000-character plaintext from *The Masque of the Red Death* and encrypt it with a fixed key (`"google"`).
7. **Attack** — generate the long ciphertext from option 6 and attempt to recover the key length and key using average IC across candidate key lengths and chi-squared letter-frequency scoring.
8. **Quit** — exit the program.

## How the Attack Works

1. For each candidate key length (1-20), the ciphertext is split into columns (every Nth character) and the average Index of Coincidence across those columns is computed.
2. Key lengths whose average IC is close to the expected English IC (`0.0667`) are treated as likely candidates.
3. For the best candidate key length, each column is tested against all 26 possible Caesar shifts, scoring each shift with a chi-squared statistic against expected English letter frequencies.
4. The shift with the lowest chi-squared score for each column is used to recover that character of the key.
