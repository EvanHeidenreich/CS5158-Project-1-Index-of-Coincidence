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
    # Calculate the frequency of each letter in the text
    freq = frequency(text)
    # Count the total number of letters in the text
    n = sum(1 for char in text.lower() if char in alphabet)
    # Return 0 if n <= 1 to avoid division by zero
    if n <= 1:
        return 0
    # convert each decimal frequency back to its letter count
    ic = sum(round(f * n) * (round(f * n) - 1) for f in freq.values()) / (n * (n - 1))
    return ic

# Read the contents of a file and return it as a string
def read_file(file_path):
    # Check if the file exists before attempting to read it
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None
    # Read the file and return its contents
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

# Print the frequency of each letter in the text
def print_frequencies(text):
    # Calculate the frequency of each letter in the text
    freq = frequency(text)
    # Print the frequency of each letter in the text
    for letter in alphabet:
        print(f"{letter}: {freq[letter]:.6f}")

# Print a bar graph of the frequency of each letter in the text
def print_bar_graph(text, width=50):
    # Calculate the frequency of each letter in the text
    freq = frequency(text)
    # Create a bar graph of the frequency of each letter in the text
    letters = list(alphabet)
    # Create a list of values corresponding to the frequency of each letter
    values = [freq[letter] for letter in letters]

# Create a bar graph using matplotlib
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
    # Initialize an empty string to hold the encrypted text
    encrypted = ""
    # Prompt the user for input until valid text and key are provided
    while True:
        print("\n Enter a text to encrypt 100 lowercase characters long: ")
        text = input().strip()
        print("\n Enter a key to encrypt the text between 2-20 characters long: ")
        key = input().strip()
        if len(text) == 100 and 2 <= len(key) <= 20:
            break
        print("Invalid input. Please enter a text 100 characters long and a key between 2-20 characters long.")
    # Loop through each character in the text and encrypt it using the Vigenère cipher
    for i in range(len(text)):
        # Calculate the numerical value of the text character (0-25)
        text_value = ord(text[i]) - ord('a')
        # Calculate the numerical value of the key character (0-25), wrapping around if the key is shorter than the text
        key_value = ord(key[i % len(key)]) - ord('a')
        # Calculate the encrypted value using modular arithmetic
        encrypted_value = (text_value + key_value) % 26
        # Convert the encrypted value back to a character and append it to the encrypted string
        encrypted += chr(encrypted_value + ord('a'))    

    return encrypted.upper()

# Function to decrypt a text Vigenere cipher style using a key
def decryption():
    # Initialize an empty string to hold the decrypted text
    decrypted = ""
    # Prompt the user for input until valid text and key are provided
    while True:
        print("\n Enter a text to decrypt 100 Upper case characters long: ")
        text = input().strip()
        print("\n Enter a key to decrypt the text between 2-20 characters long: ")
        key = input().strip()
        if len(text) == 100 and 2 <= len(key) <= 20:
            break
        print("Invalid input. Please enter a text 100 characters long and a key between 2-20 characters long.")
    # Loop through each character in the text and decrypt it using the Vigenère cipher
    for i in range(len(text)):
        # Calculate the numerical value of the text character (0-25)
        text_value = ord(text[i]) - ord('A')
        # Calculate the numerical value of the key character (0-25), wrapping around if the key is shorter than the text
        key_value = ord(key[i % len(key)]) - ord('a')
        # Calculate the decrypted value using modular arithmetic
        decrypted_value = (text_value - key_value) % 26
        # Convert the decrypted value back to a character and append it to the decrypted string
        decrypted += chr(decrypted_value + ord('a'))

    return decrypted
# Function to encrypt a long text Vigenere cipher style using a key
def long_cipher_encryption():
    # Read the contents of the file "MasqueOfTheRedDeath.txt" and store it in the variable "text"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    text = read_file(os.path.join(script_dir, "build/data/MasqueOfTheRedDeath.txt"))
    if text is None:
        return
    # Filter the text to include only lowercase alphabetic characters
    text = ''.join(char.lower() for char in text if char.lower() in alphabet)
    # Repeat the text until it reaches at least 10,000 characters
    while len(text) < 10000:
        text +=text 
    # Truncate the text to exactly 10,000 characters
    text = text[:10000]  # Truncate to exactly 10,000 characters
    # Set the key for encryption
    key = "google"
    # Initialize an empty string to hold the ciphertext
    ciphertext = ""
    # Loop through each character in the text and encrypt it using the Vigenère cipher
    for i in range(len(text)):
        # Calculate the numerical value of the text character (0-25)
        text_value = ord(text[i]) - ord('a')
        # Calculate the numerical value of the key character (0-25), wrapping around if the key is shorter than the text
        key_value = ord(key[i % len(key)]) - ord('a')
        # Calculate the encrypted value using modular arithmetic
        encrypted_value = (text_value + key_value) % 26
        # Convert the encrypted value back to a character and append it to the ciphertext string
        ciphertext += chr(encrypted_value + ord('A'))

    print("\n Key String: ", key)
    print("\n Plaintext: ", text)
    print("\n Ciphertext: ", ciphertext)

    return ciphertext

# Function to perform an attack on a ciphertext to find the best key length
def attack(ic_english, ciphertext):
    # Initialize variables to keep track of the best key length and its corresponding index of coincidence
    best_key_length = 0
    best_ic = 0
    possible_lengths = []

    print("\n Testing key lengths: ")
    # Loop through key lengths from 1 to 20 and calculate the average index of coincidence for each key length
    for key_length in range(1, 21):
        # Calculate the average index of coincidence for the current key length
        total_ic = 0
        # Loop through each column of the ciphertext corresponding to the current key length
        for i in range(key_length):
            # Extract the column of characters corresponding to the current key length
            column = ciphertext[i::key_length]
            # Calculate the index of coincidence for the current column and add it to the total index of coincidence
            ic = index_of_coincidence(column)
            # Add the index of coincidence for the current column to the total index of coincidence
            total_ic += ic
        # Calculate the average index of coincidence for the current key length
        average_ic = total_ic / key_length

        print(f"Key Length: {key_length}, Average IC: {average_ic:.6f}")
        # Check if the average index of coincidence is close to the expected English index of coincidence
        if abs(average_ic - ic_english) <= 0.005:  
            possible_lengths.append((key_length, average_ic))
    # Sort the possible key lengths by their average index of coincidence in descending order
    if possible_lengths:
        best_key_length = possible_lengths[0][0]
        best_ic = possible_lengths[0][1]

    print(f"\nBest Key Length: {best_key_length}, Best Average IC: {best_ic:.6f}")

    # Find the key characters for the best key length
    key = ""
    # Loop through each column of the ciphertext corresponding to the best key length and find the best shift for each column
    for i in range(best_key_length):
        # Extract the column of characters corresponding to the best key length
        column = ciphertext[i::best_key_length]
        # Calculate the index of coincidence for the current column
        column_ic = index_of_coincidence(column)
        # Find the best shift for the current column using the best_shift_key function
        shift, score = best_shift_key(column)
        # Convert the best shift to a character and append it to the key
        key_character = chr(shift + ord('a'))
        # Append the key character to the key string
        key += key_character

        print(f"Column {i + 1}: IC: {column_ic:.6f}, Best Shift: {shift}, Score: {score:.6f}, Key Character: {key_character}")

    print(f"\nRecovered Key: {key}")

    return best_key_length, key
# Function to find the best shift key for a given column of ciphertext
def best_shift_key(column):
    # Initialize variables to keep track of the best shift and its corresponding score
    best_shift = 0
    best_score = float('inf')
    # Loop through all possible shifts (0-25) and calculate the score for each shift
    for shift in range(26):
        # Decrypt the column using the current shift
        decrypted = ""
        # Loop through each character in the column and decrypt it using the current shift
        for char in column:
            # Calculate the numerical value of the character (0-25)
            cipher_value = ord(char) - ord('A')
            # Calculate the decrypted value using modular arithmetic
            plain_value = (cipher_value - shift) % 26
            # Convert the decrypted value back to a character and append it to the decrypted string
            decrypted += chr(plain_value + ord('a'))
        # Calculate the frequency of each letter in the decrypted text
        freq = frequency(decrypted)
        
        score = 0
        # Loop through each letter in the alphabet and calculate the chi-squared score for the decrypted text
        for letter in alphabet:
            # Calculate the expected frequency of the letter based on English letter frequency
            expected = ENGLISH_FREQUENCY[letter]
            # Get the actual frequency of the letter in the decrypted text
            actual = freq[letter]
            # Calculate the chi-squared score for the letter and add it to the total score
            score += ((actual - expected) ** 2) / expected
        # Check if the current score is better than the best score found so far
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
