import math
import random

def gcd(a, b):
    """Calcula el máximo común divisor de a y b."""
    while b != 0:
        a, b = b, a % b
    return a

def pollards_rho(n):
    """Implementa el algoritmo Rho de Pollard para encontrar un factor no trivial de n."""
    if n % 2 == 0:
        return 2
    x = random.randrange(2, n)
    y = x
    c = random.randrange(1, n)
    d = 1

    while d == 1:
        x = (pow(x, 2, n) + c) % n
        y = (pow(y, 2, n) + c) % n
        y = (pow(y, 2, n) + c) % n  
        d = gcd(abs(x - y), n)
        if d == n:
            return None  # Fracaso, intentar de nuevo con otros valores
    return d

# Ejemplo de uso:
n = 8746
factor = pollards_rho(n)
if factor:
    print(f"Un factor no trivial de {n} es {factor}")
    print(f"El cofactor es {n // factor}")
else:
    print("No se encontró un factor. Intenta ejecutar el algoritmo nuevamente.")
