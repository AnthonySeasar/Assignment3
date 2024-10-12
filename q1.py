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


def modExponent(a, b, c):
    binB = bin(b)[2:]
    result = 1
    currPow = a % c
    first = True

    for i in binB[::-1]:
        if first:
            first = False
            currPow = a % c
        else:
            currPow = (currPow * currPow) % c
        if i == "1":
            result = (result * currPow) % c

    return result


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
        if modExponent(a, n - 1, n) != 1:
            return "Composite"
        for i in range(1, s + 1):
            if modExponent(a, (2 ** i) * t, n) == 1 and \
                    (modExponent(a, (2 ** (i - 1) * t), n) != 1 and modExponent(a, (2 ** (i - 1) * t), n) != n - 1):
                return "Composite"
    return n


#
def gcd(m, n):
    if n == 0:
        return m
    else:
        return gcd(n, m % n)


def lamDa(p, q):
    lamDaNum = ((p - 1) * (q - 1)) // gcd(p - 1, q - 1)
    e = random.choice(range(3, lamDaNum - 1))
    return e


def q1(d):
    primes = 0
    primeNum = []

    while primes < 2:
        k = random.choice(range(1, 10001))
        n = primeNumSelector(d)
        prime = millerRabinAlgo(n, k)
        if prime != "Composite":
            primes += 1
            primeNum.append(prime)
        d += 1
    n = primeNum[0] * primeNum[1]
    e = lamDa(primeNum[1],primeNum[0])


if __name__ == '__main__':


