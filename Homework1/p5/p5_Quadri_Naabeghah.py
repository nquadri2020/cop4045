def caesar_cipher(text, shift):
    """Shift letters in a string by a given integer, preserving spaces and casing."""
    result = ""

    for char in text:
        if char.isalpha():
            if char.isupper():
                start = ord('A')
            else:
                start = ord('a')

            offset = (ord(char) - start + shift) % 26
            result += chr(start + offset)
        else:
            result += char

    return result


def caesar_decipher(ciphertext, shift):
    """Decrypt a Caesar-encrypted string by shifting letters backward."""
    return caesar_cipher(ciphertext, -shift)


def letter_frequency(text):
    """Count how many times each letter appears in the text, ignoring case and non-letters."""
    counts = {chr(ord('a') + i): 0 for i in range(26)}

    for char in text:
        if char.isalpha():
            lower = char.lower()
            counts[lower] += 1

    return counts


def main():
    """Prompt the user for a message and shift value, then display encrypted, frequency, and decrypted output."""
    print("Caesar Cipher and Letter Frequency Analyzer")
    print("-" * 40)

    message = input("Enter a message: ")

    while True:
        try:
            shift = int(input("Enter a shift value (integer): "))
            break
        except ValueError:
            print("Please enter a valid integer for the shift.")

    encrypted = caesar_cipher(message, shift)
    frequencies = letter_frequency(message)
    decrypted = caesar_decipher(encrypted, shift)

    print("\nEncrypted text:", encrypted)
    print("\nLetter frequency:")
    for letter in "abcdefghijklmnopqrstuvwxyz":
        print(f"{letter}: {frequencies[letter]}")

    print("\nDecrypted text:", decrypted)


if __name__ == "__main__":
    main()
