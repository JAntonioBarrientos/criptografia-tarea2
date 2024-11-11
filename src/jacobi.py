def jacobi(a, n):
    """
    Calcula el símbolo de Jacobi (a/n).
    
    Parámetros:
    a (int): Numerador del símbolo de Jacobi, debe cumplir 0 <= a < n.
    n (int): Denominador del símbolo de Jacobi, debe ser un entero impar y >= 3.
    
    Retorna:
    int: El símbolo de Jacobi, que puede ser -1, 0 o 1.
    """
    if n <= 0 or n % 2 == 0:
        raise ValueError("El denominador n debe ser un entero impar positivo mayor o igual a 3.")
    if a < 0 or a >= n:
        a = a % n  # Asegura que 0 <= a < n
    
    if a == 0:
        return 0
    if a == 1:
        return 1

    # Descomponer a = 2^e * a1, donde a1 es impar
    e = 0
    a1 = a
    while a1 % 2 == 0:
        a1 = a1 // 2
        e += 1

    # Determinar el factor s basado en el exponente de 2
    if e % 2 == 0:
        s = 1
    else:
        if n % 8 == 1 or n % 8 == 7:
            s = 1
        else:
            s = -1

    # Ajustar s si a1 ≡ n ≡ 3 mod 4
    if a1 % 4 == 3 and n % 4 == 3:
        s = -s

    # Calcular n1 = n mod a1
    n1 = n % a1

    if a1 == 1:
        return s
    else:
        return s * jacobi(n1, a1)

# Ejemplos de uso:
if __name__ == "__main__":
    ejemplos = [
        (83,593),
        (3677176, 4568731),
        (4568723, 4568731),
        (8, 21),
        (21, 29),
        (116, 2979),
        (2979, 3095),
        (24760, 27739),
        (27739, 107977),
        (431908, 459647),
        (3677176, 4568731)
    ]

    for a, n in ejemplos:
        try:
            simbolo = jacobi(a, n)
            print(f"Jacobi({a}/{n}) = {simbolo}")
        except ValueError as e:
            print(f"Error para Jacobi({a}/{n}): {e}")