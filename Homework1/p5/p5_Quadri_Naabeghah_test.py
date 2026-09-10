import unittest

from p5_Quadri_Naabeghah import caesar_cipher, caesar_decipher, letter_frequency


class TestCaesarCipher(unittest.TestCase):
    def test_caesar_cipher_basic(self):
        self.assertEqual(caesar_cipher("Hello World", 3), "Khoor Zruog")

    def test_caesar_cipher_preserves_spaces_and_case(self):
        self.assertEqual(caesar_cipher("AbC xyz", 2), "CdE zab")

    def test_caesar_cipher_wraps_around_alphabet(self):
        self.assertEqual(caesar_cipher("xyz", 3), "abc")

    def test_caesar_decipher_basic(self):
        self.assertEqual(caesar_decipher("Khoor Zruog", 3), "Hello World")

    def test_letter_frequency_ignores_case_and_non_letters(self):
        text = "Hello, World! 123"
        expected = {
            'a': 0,
            'b': 0,
            'c': 0,
            'd': 1,
            'e': 1,
            'f': 0,
            'g': 0,
            'h': 1,
            'i': 0,
            'j': 0,
            'k': 0,
            'l': 3,
            'm': 0,
            'n': 0,
            'o': 2,
            'p': 0,
            'q': 0,
            'r': 1,
            's': 0,
            't': 0,
            'u': 0,
            'v': 0,
            'w': 1,
            'x': 0,
            'y': 0,
            'z': 0,
        }
        self.assertEqual(letter_frequency(text), expected)


if __name__ == "__main__":
    unittest.main()
