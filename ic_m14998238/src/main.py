import os
import matplotlib.pyplot as plt

# Global variable for the alphabet
alphabet = 'abcdefghijklmnopqrstuvwxyz'

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

def read_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None

    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

def print_frequencies(text):
    freq = frequency(text)
    for letter in alphabet:
        print(f"{letter}: {freq[letter]:.6f}")

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

def encryption(text, shift):
    while True:
        print("\n Enter a text to encrypt between 100 characters long: ")
        text = input().strip()
        print("\n Enter a key to encrypt the text between 2-20 characters long: ")
        key = input().strip()
        if len(text) < 100 or 2 <= len(key) <= 20:
            break
        print("Invalid input. Please enter a text 100 characters long and a key between 2-20 characters long.")
        
    pass


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
        print(" 4. Quit")
        choice = input("Enter choice (1, 2, 3, or 4): ").strip()

        if choice == "1":
            print_frequencies(text)
        elif choice == "2":
            ic = index_of_coincidence(text)
            print(f"Index of Coincidence: {ic}")
        elif choice == "3":
            print_bar_graph(text)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print(f"Invalid choice: {choice}")


if __name__ == "__main__":
    main()
