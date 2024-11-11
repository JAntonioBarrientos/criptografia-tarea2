def es_primo(n):
    """
    Determina si un número 'n' es primo por medio de fuerza bruta.

    Parámetros:
    n (int): El número a verificar.

    Retorna:
    bool: True si 'n' es primo, False en caso contrario.
    """
    if n <= 1:
        return False  # Los números menores o iguales a 1 no son primos
    if n == 2:
        return True   # 2 es el único número par que es primo
    if n % 2 == 0:
        return False  # Los números pares mayores que 2 no son primos

    # Solo se necesitan verificar los divisores impares hasta la raíz cuadrada de 'n'
    raiz = int(n**0.5) + 1
    for divisor in range(3, raiz, 2):
        if n % divisor == 0:
            return False
    return True

# Ejemplos de uso:
if __name__ == "__main__":
    try:
        numero = int(input("Ingrese un número para verificar si es primo: "))
        if es_primo(numero):
            print(f"El número {numero} es primo.")
        else:
            print(f"El número {numero} NO es primo.")
    except ValueError:
        print("Por favor, ingrese un número entero válido.")
