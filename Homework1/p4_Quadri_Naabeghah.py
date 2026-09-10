import math
import matplotlib.pyplot as plt

def plot_function(fun_str, domain, ns):
    xmin, xmax = domain
    xs = [
        xmin + i * (xmax - xmin) / (ns - 1)
        for i in range(ns)
    ]
    ys = []

    for x in xs:
        y = eval(fun_str)
        ys.append(y)
    print(" x          y")
    for i in range(ns):
        print("{:8.4f} {:8.4f}".format(xs[i], ys[i]))
    print("--------------------")
    plt.figure()
    plt.plot(xs, ys)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(fun_str)
    plt.grid()
    plt.show()

fun_str = input("Enter function of x fun_str: ")
ns = int(input("Enter number of samples ns: "))
xmin = float(input("Enter domain minimum xmin: "))
xmax = float(input("Enter domain maximum xmax: "))
plot_function(fun_str, (xmin, xmax), ns)