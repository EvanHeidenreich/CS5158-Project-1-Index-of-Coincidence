import os
import matplotlib.pyplot as plt

# Global variable for the alphabet
alphabet = 'abcdefghijklmnopqrstuvwxyz'
# Global variable for IC English Frequency
IC_ENGLISH = 0.0667
# Global variable for English letter frequency
ENGLISH_FREQUENCY = {
    'a': 0.0812,
    'b': 0.0149,
    'c': 0.0271,
    'd': 0.0432,
    'e': 0.1202,
    'f': 0.0230,
    'g': 0.0203,
    'h': 0.0592,
    'i': 0.0731,
    'j': 0.0010,
    'k': 0.0069,
    'l': 0.0398,
    'm': 0.0261,
    'n': 0.0695,
    'o': 0.0768,
    'p': 0.0182,
    'q': 0.0011,
    'r': 0.0602,
    's': 0.0628,
    't': 0.0910,
    'u': 0.0288,
    'v': 0.0111,
    'w': 0.0209,
    'x': 0.0017,
    'y': 0.0211,
    'z': 0.0007
}

# Frequency Function to compute the decimal frequency of each letter:
# count of letter over the total number of letters in the text.
# Non-alphabet characters are ignored.
def frequency(text):
    frequencies = {}

    for letter in alphabet:
        frequencies[letter] = 0

    for char in text.lower():
        if char in frequencies:
            frequencies[char] += 1

    total = sum(frequencies.values())
    for letter in alphabet:
        frequencies[letter] = frequencies[letter] / total if total > 0 else 0.0

    return frequencies

# Calculate the index of coincidence for a given text
def index_of_coincidence(text):
    freq = frequency(text)

    n = sum(1 for char in text.lower() if char in alphabet)

    if n <= 1:
        return 0
    # convert each decimal frequency back to its letter count
    ic = sum(round(f * n) * (round(f * n) - 1) for f in freq.values()) / (n * (n - 1))
    return ic

# Read the contents of a file and return it as a string
def read_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None

    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

# Print the frequency of each letter in the text
def print_frequencies(text):
    freq = frequency(text)
    for letter in alphabet:
        print(f"{letter}: {freq[letter]:.6f}")

# Print a bar graph of the frequency of each letter in the text
def print_bar_graph(text, width=50):
    freq = frequency(text)
    letters = list(alphabet)
    values = [freq[letter] for letter in letters]

    plt.bar(letters, values)
    for i, value in enumerate(values):
        plt.text(i, value, f"{value:.4f}", ha='center', va='bottom',
                 fontsize=6, rotation=90)
    plt.xlabel("Letters")
    plt.ylabel("Frequency")
    plt.title("Frequency of Letters in Text")
    plt.show()

# Function to encrypt a text Vigenère cipher style using a key
def encryption():
    encrypted = ""
    while True:
        print("\n Enter a text to encrypt 100 lowercase characters long: ")
        text = input().strip()
        print("\n Enter a key to encrypt the text between 2-20 characters long: ")
        key = input().strip()
        if len(text) == 100 and 2 <= len(key) <= 20:
            break
        print("Invalid input. Please enter a text 100 characters long and a key between 2-20 characters long.")

    for i in range(len(text)):
        text_value = ord(text[i]) - ord('a')

        key_value = ord(key[i % len(key)]) - ord('a')

        encrypted_value = (text_value + key_value) % 26

        encrypted += chr(encrypted_value + ord('a'))    

    return encrypted.upper()

# Function to decrypt a text Vigenère cipher style using a key
def decryption():
    decrypted = ""

    while True:
        print("\n Enter a text to decrypt 100 Upper case characters long: ")
        text = input().strip()
        print("\n Enter a key to decrypt the text between 2-20 characters long: ")
        key = input().strip()
        if len(text) == 100 and 2 <= len(key) <= 20:
            break
        print("Invalid input. Please enter a text 100 characters long and a key between 2-20 characters long.")

    for i in range(len(text)):
        text_value = ord(text[i]) - ord('A')

        key_value = ord(key[i % len(key)]) - ord('a')

        decrypted_value = (text_value - key_value) % 26

        decrypted += chr(decrypted_value + ord('a'))

    return decrypted

def long_cipher_encryption():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    text = read_file(os.path.join(script_dir, "build/data/MasqueOfTheRedDeath.txt"))
    if text is None:
        return

    text = ''.join(char.lower() for char in text if char.lower() in alphabet)

    while len(text) < 10000:
        text +=text  # Repeat the text until it reaches at least 10,000 characters

    text = text[:10000]  # Truncate to exactly 10,000 characters

    key = "google"

    ciphertext = ""

    for i in range(len(text)):
        text_value = ord(text[i]) - ord('a')
        key_value = ord(key[i % len(key)]) - ord('a')
        encrypted_value = (text_value + key_value) % 26
        ciphertext += chr(encrypted_value + ord('A'))

    print("\n Key String: ", key)
    print("\n Plaintext: ", text)
    print("\n Ciphertext: ", ciphertext)

    return ciphertext


def attack(ic_english, ciphertext):
    best_key_length = 0
    best_ic = 0
    possible_lengths = []

    print("\n Testing key lengths: ")

    for key_length in range(1, 21):
        total_ic = 0
        for i in range(key_length):
            column = ciphertext[i::key_length]
            ic = index_of_coincidence(column)
            total_ic += ic

        average_ic = total_ic / key_length

        print(f"Key Length: {key_length}, Average IC: {average_ic:.6f}")

        if abs(average_ic - ic_english) <= 0.005:  # Allowing a small tolerance
            possible_lengths.append((key_length, average_ic))

    if possible_lengths:
        best_key_length = possible_lengths[0][0]
        best_ic = possible_lengths[0][1]

    print(f"\nBest Key Length: {best_key_length}, Best Average IC: {best_ic:.6f}")

    # Find the key characters for the best key length
    key = ""
    for i in range(best_key_length):
        column = ciphertext[i::best_key_length]
        column_ic = index_of_coincidence(column)
        shift, score = best_shift_key(column)
        key_character = chr(shift + ord('a'))

        key += key_character

        print(f"Column {i + 1}: IC: {column_ic:.6f}, Best Shift: {shift}, Score: {score:.6f}, Key Character: {key_character}")

    print(f"\nRecovered Key: {key}")

    return best_key_length, key

def best_shift_key(column):
    best_shift = 0
    best_score = float('inf')

    for shift in range(26):
        decrypted = ""
        for char in column:
            cipher_value = ord(char) - ord('A')
            plain_value = (cipher_value - shift) % 26
            decrypted += chr(plain_value + ord('a'))

        freq = frequency(decrypted)

        score = 0

        for letter in alphabet:
            expected = ENGLISH_FREQUENCY[letter]
            actual = freq[letter]

            score += ((actual - expected) ** 2) / expected

        if score < best_score:
            best_score = score
            best_shift = shift

    return best_shift, best_score
    

# Main function to run the program
def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    text = read_file(os.path.join(script_dir, "build/data/MasqueOfTheRedDeath.txt"))
    if text is None:
        return

    while True:
        print("\nSelect what to run:")
        print(" 1. Frequency  - print the frequency of each character in the text")
        print(" 2. Index of Coincidence - calculate the index of coincidence")
        print(" 3. Frequency Bar Graph - print a bar graph of the frequency of each character in the text")
        print(" 4. To Encrypt a text - encrypt a text using a key")
        print(" 5. To Decrypt a text - decrypt a text using a key")
        print(" 6. Long Cipher Encryption - encrypt a long text using a key")
        print(" 7. Attack - perform an attack on a ciphertext to find the best key length")
        print(" 8. Quit")
        choice = input("Enter choice (1, 2, 3, 4, 5, 6, 7, or 8): ").strip()

        if choice == "1":
            print_frequencies(text)
        elif choice == "2":
            ic = index_of_coincidence(text)
            print(f"Index of Coincidence: {ic}")
        elif choice == "3":
            print_bar_graph(text)
        elif choice == "4":
            encrypted_text = encryption()
            print(f"Encrypted Text: {encrypted_text}")
        elif choice == "5":
            decrypted_text = decryption()
            print(f"Decrypted Text: {decrypted_text}")
        elif choice == "6":
            long_cipher_encryption()
        elif choice == "7":
            ciphertext = long_cipher_encryption()
            if ciphertext:
                attack(IC_ENGLISH, ciphertext)
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print(f"Invalid choice: {choice}")


if __name__ == "__main__":
    main()
