def find_dup_str(s, n):
    for i in range(len(s) - n + 1):
        substring = s[i:i + n]

        for j in range(i + n, len(s) - n + 1):
            if s[j:j + n] == substring:
                return substring
    return ""

s = input("Enter a string: ")
n = int(input("Enter substring length: "))

print(find_dup_str(s, n))
