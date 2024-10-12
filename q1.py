import random


def primeNumSelector(d):
    loweBound = 2
    upperBound = 2000
    if loweBound < d < upperBound:
        chosenNum = (2 ** d) - 1
        return chosenNum
    else:
        print("Invalid Number Selected.")
        return None

def modExponent(n):


def millerRabinAlgo(n, k):
    if n % 2 == 0:
        return "Composite!"
    s = 0
    t = n - 1
    while t % 2 == 0:
        s = s + 1
        t = t // 2
    while k > 0:
        k -= 1
        a = random.choice(range(2, n - 1))
        if pow(a, n - 1, n) != 1:
            return "Composite"
        for i in range(1, s + 1):
            if pow(a, (2 ** i) * t, n) == 1 and \
                    (pow(a, (2 ** (i - 1) * t), n) != 1 and pow(a, (2 ** (i - 1) * t), n) != n - 1):
                return "Composite"
    return "probably_prime"


if __name__ == '__main__':
    d = 10
    n = primeNumSelector(d)
    i = 0
    curr = True
    while curr:
        k = random.choice(range(1, 1000))
        print(k)
        res = millerRabinAlgo(8191, k)
        if res == "probably_prime":
            i += 1
            print(i)
        else:
            print(i)
            curr = False
