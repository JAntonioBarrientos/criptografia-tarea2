import math

def legendre_symbol(a, p):
    return pow(a, (p - 1) // 2, p)

def tonelli_shanks(a, p):
    if legendre_symbol(a, p) != 1:
        return []
    if p % 4 == 3:
        x = pow(a, (p + 1) // 4, p)
        return [x, p - x]
    # Find Q and S
    Q = p - 1
    S = 0
    while Q % 2 == 0:
        Q //= 2
        S += 1
    # Find a quadratic non-residue z
    for z in range(2, p):
        if legendre_symbol(z, p) == p - 1:
            break
    c = pow(z, Q, p)
    x = pow(a, (Q + 1) // 2, p)
    t = pow(a, Q, p)
    m = S
    while t != 1:
        temp = t
        i = 0
        while temp != 1:
            temp = pow(temp, 2, p)
            i += 1
            if i == m:
                return []
        b = pow(c, 2 ** (m - i - 1), p)
        x = (x * b) % p
        t = (t * b * b) % p
        c = pow(b, 2, p)
        m = i
    return [x, p - x]

def factorization(n):
    factors = {}
    # Trial division
    for i in range(2, int(math.sqrt(n)) + 1):
        while n % i == 0:
            factors[i] = factors.get(i, 0) + 1
            n = n // i
    if n > 1:
        factors[n] = 1
    return factors

def combine_roots(factors, a, n):
    from itertools import product
    roots = [[]]
    for p, exp in factors.items():
        res = tonelli_shanks(a, p)
        if not res:
            return []
        roots = [r + [root] for r in roots for root in res]
    combined = []
    for combination in roots:
        x = combination[0]
        for root in combination[1:]:
            x = chinese_remainder(x, n, root, n)
        combined.append(x % n)
    return list(set(combined))

def chinese_remainder(a, n1, b, n2):
    # Assuming n1 and n2 are coprime
    m1, m2 = extended_gcd(n1, n2)
    return (a * m2 * n2 + b * m1 * n1) % (n1 * n2)

def extended_gcd(a, b):
    if a == 0:
        return (0,1)
    else:
        x, y = extended_gcd(b % a, a)
        return (y - (b // a) * x, x)

def sqrt_Zn(a, n):
    factors = factorization(n)
    if len(factors) == 1 and list(factors.values())[0] == 1:
        return tonelli_shanks(a, n)
    else:
        return combine_roots(factors, a, n)

def is_prime(n):
    if n <=1:
        return False
    if n <=3:
        return True
    if n%2 ==0 or n%3 ==0:
        return False
    i =5
    while i * i <=n:
        if n%i ==0 or n%(i+2) ==0:
            return False
        i +=6
    return True

def main():
    a = int(input("Ingrese el valor de a: "))
    n = int(input("Ingrese el módulo n: "))
    if is_prime(n):
        roots = tonelli_shanks(a, n)
    else:
        roots = sqrt_Zn(a, n)
    if roots:
        print(f"Las raíces cuadradas de {a} en Z_{n} son: {roots}")
    else:
        print(f"No existen raíces cuadradas de {a} en Z_{n}.")

if __name__ == "__main__":
    main()