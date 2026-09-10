import matplotlib.pyplot as plt

while True:
    a_input = input("Enter a: ")
    if a_input == "":
        break
    a = float(a_input)
    b = float(input("Enter b: "))
    c = float(input("Enter c: "))
    sqrt = b ** 2 - 4 * a * c

    if sqrt < 0:
        print("no real solutions")
        xopt = -b / (2 * a)
        x_min = xopt - 5
        x_max = xopt + 5

    elif sqrt == 0:
        x1 = -b / (2 * a)
        print("one solution: {:.5f}".format(x1))
        x_min = x1 - 5
        x_max = x1 + 5

    else:
        x1 = (-b - sqrt ** 0.5) / (2 * a)
        x2 = (-b + sqrt ** 0.5) / (2 * a)
        print("two solutions: x1={:.5f} x2={:.5f}".format(x1, x2))
        margin = 2
        x_min = min(x1, x2) - margin
        x_max = max(x1, x2) + margin

    xs = [
        x_min + i * (x_max - x_min) / 149
        for i in range(150)
    ]
    ys = [
        a * x ** 2 + b * x + c
        for x in xs
    ]