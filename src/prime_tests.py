import random

def test_de_fermat(n, k=5):
    """
    Determina si un número n es primo usando el Test de Fermat.

    Args:
        n (int): El número a verificar.
        k (int): Número de iteraciones (bases aleatorias a probar).

    Returns:
        bool: True si n es probablemente primo, False si es compuesto.
    """
    if n <= 1:
        print(f"{n} no es primo porque es menor o igual a 1.")
        return False
    print(f"Realizando {k} iteraciones del Test de Fermat para {n}...")
    for i in range(1, k + 1):
        a = random.randint(2, n - 2)
        resultado = pow(a, n - 1, n)
        print(f"Iteración {i}: a = {a}, a^(n-1) mod n = {resultado}")
        if resultado != 1:
            print(f"Resultado: {n} es compuesto según el Test de Fermat.\n")
            return False
    print(f"Resultado: {n} es probablemente primo según el Test de Fermat.\n")
    return True

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
        if n % 8 in [1, 7]:
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

def test_de_solovay_strassen(n, k=5):
    """
    Determina si un número n es primo usando el Test de Solovay-Strassen.

    Args:
        n (int): El número a verificar.
        k (int): Número de iteraciones (bases aleatorias a probar).

    Returns:
        bool: True si n es probablemente primo, False si es compuesto.
    """
    if n < 2:
        print(f"{n} no es primo porque es menor que 2.")
        return False
    if n == 2:
        print(f"{n} es primo.")
        return True
    if n % 2 == 0:
        print(f"{n} no es primo porque es par.")
        return False

    print(f"Realizando {k} iteraciones del Test de Solovay-Strassen para {n}...")
    for i in range(1, k + 1):
        a = random.randint(2, n - 2)
        jac = jacobi(a, n)
        print(f"Iteración {i}: a = {a}, (a/n) = {jac}")
        if jac == 0:
            print(f"Resultado: {n} es compuesto porque (a/n) = 0.\n")
            return False
        mod = pow(a, (n - 1) // 2, n)
        print(f"Iteración {i}: a^((n-1)/2) mod n = {mod}")
        if mod != 1 and mod != n - 1:
            print(f"Resultado: {n} es compuesto porque {mod} != 1 y {mod} != n-1.\n")
            return False
        if mod != jac % n:
            print(f"Resultado: {n} es compuesto porque {mod} != (a/n) mod n.\n")
            return False
    print(f"Resultado: {n} es probablemente primo según el Test de Solovay-Strassen.\n")
    return True

def miller_rabin(n, k=5):
    """
    Determina si un número n es primo usando el Test de Miller-Rabin.

    Args:
        n (int): El número a verificar.
        k (int): Número de iteraciones (bases aleatorias a probar).

    Returns:
        bool: True si n es probablemente primo, False si es compuesto.
    """
    if n <= 1:
        print(f"{n} no es primo porque es menor o igual a 1.")
        return False
    if n <= 3:
        print(f"{n} es primo.")
        return True
    if n % 2 == 0:
        print(f"{n} no es primo porque es par.")
        return False

    # Escribir n-1 como 2^s * d
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    print(f"Realizando {k} iteraciones del Test de Miller-Rabin para {n}...")
    for i in range(1, k + 1):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)  # a^d mod n
        print(f"Iteración {i}: a = {a}, x = a^d mod n = {x}")

        if x == 1 or x == n - 1:
            print(f"Iteración {i}: {a} pasa la prueba.")
            continue

        for r in range(1, s):
            x = pow(x, 2, n)
            print(f"Iteración {i}: x = x^2 mod n = {x}")
            if x == n - 1:
                print(f"Iteración {i}: {a} pasa la prueba en la ronda r={r}.")
                break
        else:
            print(f"Resultado: {n} es compuesto según el Test de Miller-Rabin.\n")
            return False
    print(f"Resultado: {n} es probablemente primo según el Test de Miller-Rabin.\n")
    return True

def main():
    # Definir los números y los tests a aplicar
    pruebas = [
        {"numero": 131317, "test": "Fermat"},
        {"numero": 193394587, "test": "Solovay-Strassen"},
        {"numero": 1346459137, "test": "Miller-Rabin"}
    ]

    for prueba in pruebas:
        numero = prueba["numero"]
        test = prueba["test"]

        print(f"---\nAplicando el Test de {test} para el número {numero}:")

        if test == "Fermat":
            es_primo = test_de_fermat(numero)
        elif test == "Solovay-Strassen":
            es_primo = test_de_solovay_strassen(numero)
        elif test == "Miller-Rabin":
            es_primo = miller_rabin(numero)
        else:
            print(f"Test desconocido: {test}")
            continue

        resultado = "primo" if es_primo else "compuesto"
        print(f"Resultado Final: {numero} es {resultado} según el Test de {test}.")

if __name__ == "__main__":
    main()
