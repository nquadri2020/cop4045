def find_Pythagorean(n):
    pythagoreantriple = []

    for a in range(1, n):
        pythagoreantriple.append((a, b, c))
    
    return pythagoreantriple

n = int(input("Enter a value for n > a, b, c > 0: "))
find_Pythagorean(n)