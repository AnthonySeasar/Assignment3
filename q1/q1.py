# Author : Zijie Zhang
# StudentID: 32397216
# Date: 13/10/2024

import random
import sys


# Read d and check if it is below or beyond the lower and upper bound
# if it is valid, return it as chosenNum
def primeNumSelector(d):
    loweBound = 2
    # Upper bound set to 2000 as the specification said
    upperBound = 2000
    # Check if 'd' is within the valid range
    if loweBound < d < upperBound:
        chosenNum = (2 ** d) - 1
        return chosenNum
    else:
        print("Invalid Number Selected.")
        # Return None to indicate an invalid input
        return None


# Computes modular exponentiation (a^b) % c, optimizing the calculation.
def modExponent(a, b, c):
    # Convert 'b' to a binary string
    binB = bin(b)[2:]
    result = 1
    # Initial a^1 % c
    currPow = a % c
    first = True
    # Iterate over the binary representation of 'b' in reverse
    for i in binB[::-1]:
        # if it is the first iterate, stay remain
        if first:
            # Mark the first iteration as done
            first = False
            currPow = a % c
        else:
            # Square the current power and take mod
            # We can construct the required terms through repeated squaring
            currPow = (currPow * currPow) % c
        # Whenever the binary representation of the exponent has a 1 in position i
        if i == "1":
            # Update the result
            result = (result * currPow) % c

    return result


# millerRabinAlgo function: Implements the Miller-Rabin primality test to check if 'n' is prime
def millerRabinAlgo(n, k):
    # If 'n' is even, return "Composite" directly
    if n % 2 == 0:
        return "Composite!"
    # Initialize 's', which represents the power of 2 in n-1
    s = 0
    # Set t to n-1
    t = n - 1
    # at this stage , n-1 will be 2ˆs.t, where t is odd
    while t % 2 == 0:
        # update s and t
        s = s + 1
        t = t // 2
    # k random tests
    while k > 0:
        # Decrease the number of tests
        k -= 1
        # Randomly choose 'a' between 2 and n-1
        a = random.randint(2, n - 1)
        # If a^(n-1) % n != 1, return "Composite"
        if modExponent(a, n - 1, n) != 1:
            return "Composite"
        for i in range(1, s + 1):
            # If a^((2^i)*t) % n == 1 and a^((2^(i-1))*t) != 1 and != n-1, return "Composite"
            if modExponent(a, (2 ** i) * t, n) == 1 and \
                    (modExponent(a, (2 ** (i - 1) * t), n) != 1 and modExponent(a, (2 ** (i - 1) * t), n) != n - 1):
                return "Composite"
    # probably prime  // accuracy depends on k
    return n


# A helper function:
# Calculates the greatest common divisor (GCD) of 'm' and 'n' using the Euclidean algorithm
def gcd(m, n):
    if n == 0:
        return m
    else:
        # call gcd Recursively until a GCD is found
        return gcd(n, m % n)


# A helper function that Calculates λ(p, q), which is the least common divide by (p-1) and (q-1).
# Then, it randomly selects a valid 'e'.
def lamDa(p, q):
    lamDaNum = ((p - 1) * (q - 1)) // gcd(p - 1, q - 1)
    e = random.randint(3, lamDaNum - 1)
    return e


def write_public_file(nAnde, filename):
    with open(filename, 'w') as file:
        file.write(f"# modulus (n)\n{nAnde[0]}\n")
        file.write(f"# exponent (e)\n{nAnde[1]}\n")


def write_private_file(primes, filename):
    with open(filename, 'w') as file:
        file.write(f"# p\n{primes[0]}\n")
        file.write(f"# q\n{primes[1]}\n")


def q1(d):
    primes = 0
    primeNum = []
    while primes < 2:
        k = random.choice(range(1, 10001))
        n = primeNumSelector(d)
        # if n return from function primeNumSelector is None, return the error message directly.
        if n is None:
            return "Invalid n Selected."
        # obtain the prime using function millerRabinAlgo
        prime = millerRabinAlgo(n, k)
        # if prime
        if prime != "Composite":
            primes += 1
            primeNum.append(prime)
        d += 1
    n = primeNum[0] * primeNum[1]
    e = lamDa(primeNum[1], primeNum[0])
    nAnde = [n, e]
    write_private_file(primeNum, "output_q1_private.txt")
    write_public_file(nAnde, "output_q1_public.txt")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        d = int(sys.argv[1])
        q1(d)
    else:
        print("Please provide a value for d.")
