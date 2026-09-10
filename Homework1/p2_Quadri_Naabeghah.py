def find_Pythagorean(n):
    pythagoreantriple = []

    for a in range(1, n):
        for b in range(a, n):
            c = (a ** 2 + b ** 2) ** 0.5
            if c.is_integer() and c <= n:
                pythagoreantriple.append((a, b, int(c)))
    return pythagoreantriple

n = int(input("Enter a value for n > a, b, c > 0: "))
result = find_Pythagorean(n)
print("Pythagorean triples:")
for triple in result:
    print(triple)