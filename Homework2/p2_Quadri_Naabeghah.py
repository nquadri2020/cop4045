pythagorean_tuples = [
    (a, b, c, d)
    for a in range(1, 11)
    for b in range(1, 11)
    for c in range(1, 11)
    for d in range(1, 11)
    if len({a, b, c, d}) == 4
    and a ** 2 + b ** 2 == c ** 2 + d ** 2
]
print("a)")
print(pythagorean_tuples)

strings = ["One", "SEVEN", "three", "two", "Ten"]
short_strings = [
    (word.lower(), len(word))
    for word in strings
    if len(word) < 5
]
print("b)")
print(short_strings)

names = [
    "Christopher Ashton Kutcher",
    "Elizabeth Stamatina Fey",
]
formatted_names = [
    "{} {}. {}".format(first, middle[0], last)
    for first, middle, last in (
        name.split() for name in names
    )
]
print("c)")
print(formatted_names)

lst1 = ["Spam", "Trams", "Elbows", "Tops", "Astral"]
lst2 = ["Bowels", "Sample", "Altars", "Stop", "Course", "Smart"]
anagram_pairs = [
    (word1, word2)
    for word1 in lst1
    for word2 in lst2
    if sorted(word1.lower()) == sorted(word2.lower())
]
print("d)")
print(anagram_pairs)

s = ["one", "two", "three"]
string_lengths = {
    word: len(word)
    for word in s
}
print("e)")
print(string_lengths)

text = "Hello world"
vowels = {
    index: character
    for index, character in enumerate(text)
    if character.lower() in "aeiou"
}
print("f)")
print(vowels)