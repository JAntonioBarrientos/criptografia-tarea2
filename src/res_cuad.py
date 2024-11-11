def es_residuo_cuadratico(a, n):
    """
    Determina si 'a' es un residuo cuadrático módulo 'n'.
    
    Parámetros:
    a (int): El número a verificar.
    n (int): El módulo.
    
    Retorna:
    bool: True si 'a' es residuo cuadrático módulo 'n', False en caso contrario.
    """
    
    if n <= 0:
        raise ValueError("El módulo 'n' debe ser un entero positivo.")
    
    a = a % n  # Reducir 'a' módulo 'n'
    
    if a == 0:
        return True  # 0 es siempre residuo cuadrático
    
    # Función para factorizar 'n' en factores primos
    def factorizar(n):
        factores = {}
        # Contar el número de 2s que dividen a n
        while n % 2 == 0:
            factores[2] = factores.get(2, 0) + 1
            n = n // 2
        # n debe ser impar ahora
        p = 3
        while p * p <= n:
            while n % p == 0:
                factores[p] = factores.get(p, 0) + 1
                n = n // p
            p += 2
        if n > 1:
            factores[n] = factores.get(n, 0) + 1
        return factores
    
    # Función para verificar si 'a' es residuo cuadrático módulo p^k
    def es_residuo_mod_pk(a, p, k):
        if p == 2:
            if k == 1:
                return a % 2 == 0 or a % 2 == 1
            elif k == 2:
                return a % 4 in [0,1]
            else:
                return a % 8 in [1]
        else:
            # Usar el símbolo de Legendre
            legendre = pow(a, (p - 1) // 2, p)
            if legendre != 1:
                return False
            # Si p ≡ 3 mod 4, verificar mayor potencia
            # Para simplificar, asumimos que si es residuo cuadrático en p, lo es en p^k
            return True
    
    factores = factorizar(n)
    
    for p, k in factores.items():
        if not es_residuo_mod_pk(a, p, k):
            return False
    return True

# Ejemplos de uso:
if __name__ == "__main__":
    a = 6007
    n = 1902
    
    if es_residuo_cuadratico(a, n):
        print(f"El número {a} es residuo cuadrático módulo {n}.")
    else:
        print(f"El número {a} NO es residuo cuadrático módulo {n}.")
