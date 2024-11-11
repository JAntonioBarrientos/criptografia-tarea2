import sys
import random

class CribaCuadratica:
    def __init__(self, N):
        self.N = N
        self.a = 1
        self.b = self.isqrt(N) + 1
        self.bound = 50
        self.base = self.create_base(self.N, self.bound)
        self.needed = self.phi(self.base[-1]) + 1
        self.sieve_start = 0
        self.sieve_stop = 0
        self.sieve_interval = 100000
        self.M = []
        self.smooth_vals = []
        self.start_vals = self.solve(self.a, self.b, self.N)
        self.seen = set()
    
    '''
    Esta sección implementa la eliminación gaussiana para resolver sistemas de ecuaciones lineales en GF(2).
    '''
    def gauss(self, M):
        marks = [False] * len(M)
        for j in range(len(M[0])):
            for i in range(len(M)):
                if M[i][j] == 1:
                    marks[i] = True
                    # Eliminar los 1 en las columnas anteriores
                    for k in range(j):
                        if M[i][k] == 1:
                            for row in range(len(M)):
                                M[row][k] = (M[row][k] + M[row][j]) % 2
                    # Eliminar los 1 en las columnas posteriores
                    for k in range(j+1, len(M[0])):
                        if M[i][k] == 1:
                            for row in range(len(M)):
                                M[row][k] = (M[row][k] + M[row][j]) % 2
                    break
        return (marks, M)
    
    '''
    Obtiene las columnas que tienen un valor "1" en una fila específica.
    '''
    def get_dep_cols(self, row):
        ret = []
        for i in range(len(row)):
            if row[i] == 1:
                ret.append(i)
        return ret
    
    '''
    Suma dos filas en GF(2), es decir, realiza una operación XOR.
    '''
    def row_add(self, new_row, current, M):
        ret = current[:]
        for i in range(len(M[new_row])):
            ret[i] ^= M[new_row][i]
        return ret
    
    '''
    Verifica si una fila es dependiente de un conjunto de columnas.
    '''
    def is_dependent(self, cols, row):
        for i in cols:
            if row[i] == 1:
                return True
        return False
    
    '''
    Encuentra un conjunto de filas que, al combinarse, resultan en una suma cero, indicando una dependencia lineal.
    '''
    def find_linear_deps(self, row):
        ret = []
        dep_cols = self.get_dep_cols(self.M[row])
        current_rows = [row]
        current_sum = self.M[row][:]
        for i in range(len(self.M)):
            if i == row:
                continue
            if self.is_dependent(dep_cols, self.M[i]):
                current_rows.append(i)
                current_sum = self.row_add(i, current_sum, self.M)
                if sum(current_sum) == 0:
                    ret.append(current_rows[:])
        return ret
    
    '''
    Prueba las dependencias lineales encontradas para intentar factorizar N.
    '''
    def testdep(self, dep):
        x = y = 1
        for row in dep:
            x *= self.smooth_vals[row][0]
            y *= self.smooth_vals[row][1]
        return self.xgcd(x - self.isqrt(y), self.N)[0]
    
    '''
    Calcula la función totiente de Euler para un primo p.
    '''
    def phi(self, p):
        return p - 1
    
    '''
    Calcula el símbolo de Legendre, determinando si a es residuo cuadrático módulo p.
    '''
    def legendre(self, a, p):
        if a % p == 0:
            return 0
        return pow(a, (p - 1) // 2, p)
    
    '''
    Realiza la prueba de primalidad de Miller-Rabin de manera probabilística.
    '''
    def miller_rabin(self, n, trials=5):
        if n == 2:
            return True
        if n % 2 == 0 or n <= 1:
            return False
        # Escribir n-1 como 2^s * d
        s = 0
        d = n - 1
        while d % 2 == 0:
            d //= 2
            s += 1
        for _ in range(trials):
            a = random.randrange(2, n - 1)
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(s - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True
    
    '''
    Calcula la raíz cuadrada entera de n usando el método de Newton.
    '''
    def isqrt(self, n):
        if n == 0:
            return 0
        x = n
        y = (x + 1) // 2
        while y < x:
            x = y
            y = (x + n // x) // 2
        return x
    
    '''
    Implementa el algoritmo extendido de Euclides para encontrar el MCD y los coeficientes de Bézout.
    '''
    def xgcd(self, a, b):
        prevx, x = 1, 0
        prevy, y = 0, 1
        while b:
            q, r = divmod(a, b)
            x, prevx = prevx - q * x, x
            y, prevy = prevy - q * y, y
            a, b = b, r
        return a, prevx, prevy
    
    '''
    Resuelve la ecuación cuadrática x² ≡ n mod p usando el algoritmo de Tonelli-Shanks.
    '''
    def tonelli_shanks(self, n, p):
        if self.legendre(n, p) != 1:
            return None
        if p == 2:
            return n
        if p % 4 == 3:
            return pow(n, (p + 1) // 4, p)
        # Encuentra Q y S tal que p-1 = Q * 2^S con Q impar
        Q = p - 1
        S = 0
        while Q % 2 == 0:
            Q //= 2
            S += 1
        # Encuentra un z que no sea residuo cuadrático
        z = 2
        while self.legendre(z, p) != p - 1:
            z += 1
        c = pow(z, Q, p)
        x = pow(n, (Q + 1) // 2, p)
        t = pow(n, Q, p)
        m = S
        while t != 1:
            # Encuentra el menor i (0 < i < m) tal que t^(2^i) ≡ 1 mod p
            i = 1
            temp = pow(t, 2, p)
            while i < m and temp != 1:
                temp = pow(temp, 2, p)
                i += 1
            if i == m:
                return None
            b = pow(c, 1 << (m - i - 1), p)
            x = (x * b) % p
            t = (t * b * b) % p
            c = (b * b) % p
            m = i
        return x
    
    '''
    Crea una base de factores que consiste en primos para los cuales N es un residuo cuadrático.
    '''
    def create_base(self, n, B):
        base = []
        i = 2
        while len(base) < B:
            if self.legendre(n, i) == 1:
                if self.miller_rabin(i):
                    base.append(i)
            i += 1
        return base
    
    '''
    Define el polinomio de cribado de la forma (Ax + B)^2 - N.
    '''
    def poly(self, x, a, b, n):
        return ((a * x + b) ** 2) - n
    
    '''
    Encuentra las soluciones x para el polinomio en cada primo de la base de factores.
    '''
    def solve(self, a, b, n):
        start_vals = []
        for p in self.base:
            ainv = 1
            if a != 1:
                g, ainv, _ = self.xgcd(a, p)
                if g != 1:
                    raise ValueError(f"No existe inverso modular para a={a} y p={p}")
            r1 = self.tonelli_shanks(n, p)
            if r1 is None:
                continue
            r2 = (-r1) % p
            start1 = (ainv * (r1 - b)) % p
            start2 = (ainv * (r2 - b)) % p
            start_vals.append([start1, start2])
        return start_vals
    
    '''
    Usa la división por prueba para producir un vector de exponentes para y con respecto a la base de factores.
    Los exponentes son considerados en GF(2).
    '''
    def trial(self, y, base):
        ret = [0] * len(base)
        if y > 0:
            for i in range(len(base)):
                while y % base[i] == 0:
                    y //= base[i]
                    ret[i] = (ret[i] + 1) % 2
        return ret
    
    '''
    Ejecuta el algoritmo de la Criba Cuadrática.
    '''
    def run(self):
        print('==')
        print(f'Buscando {self.needed} enteros que sean suaves respecto a la base de factores')
        print('==\n')
        
        # Realiza la cribada hasta encontrar suficientes números suaves
        while len(self.smooth_vals) < self.needed:
            self.sieve_start = self.sieve_stop
            self.sieve_stop += self.sieve_interval
            interval = [self.poly(x, self.a, self.b, self.N) for x in range(self.sieve_start, self.sieve_stop)]
            
            for p_index, p in enumerate(self.base):
                t = self.start_vals[p_index][0]
                
                while self.start_vals[p_index][0] < self.sieve_start + self.sieve_interval:
                    while interval[self.start_vals[p_index][0] - self.sieve_start] % p == 0:
                        interval[self.start_vals[p_index][0] - self.sieve_start] //= p
                    self.start_vals[p_index][0] += p
                
                # Aplica la cribada usando ambas soluciones si no son iguales
                if self.start_vals[p_index][1] != t:
                    while self.start_vals[p_index][1] < self.sieve_start + self.sieve_interval:
                        while interval[self.start_vals[p_index][1] - self.sieve_start] % p == 0:
                            interval[self.start_vals[p_index][1] - self.sieve_start] //= p
                        self.start_vals[p_index][1] += p
            
            # Almacena los valores suaves encontrados
            for i in range(self.sieve_interval):
                if interval[i] == 1:
                    x = self.sieve_start + i
                    y = self.poly(x, self.a, self.b, self.N)
                    exp = self.trial(y, self.base)
                    exp_tuple = tuple(exp)
                    if exp_tuple not in self.seen:
                        self.smooth_vals.append(((self.a * x) + self.b, y))
                        self.M.append(exp)
                        self.seen.add(exp_tuple)
            
            print(f'Después de la cribada en el siguiente intervalo tenemos {len(self.smooth_vals)} números suaves')
        
        print('\n==')
        print('Ejecutando Eliminación Gaussiana')
        print('==\n')
        
        marks, M_reducida = self.gauss(self.M)
        self.M = M_reducida
        print('Reducción hecha')
        
        print('\n==')
        print('Probando Dependencias Lineales')
        print('==\n')
        
        for i in range(len(marks)):
            if not marks[i]:
                deps = self.find_linear_deps(i)
                for dep in deps:
                    print(f'Dependencias encontradas: {dep}')
                    gcd = self.testdep(dep)
                    if gcd != 1 and gcd != self.N:
                        print(f'\nFactor no trivial encontrado: {gcd}')
                        print(f'Los factores de {self.N} son {gcd} y {self.N // gcd}')
                        sys.exit(0)
        
        print('No se encontraron factores no triviales.')

# Punto de entrada del programa
if __name__ == "__main__":
    try:
        numero = int(input("Ingrese el número que desea factorizar: "))
        if numero <= 1:
            print("Por favor, ingrese un número entero mayor que 1.")
            sys.exit(1)
    except ValueError:
        print("Entrada inválida. Por favor, ingrese un número entero.")
        sys.exit(1)
    
    criba = CribaCuadratica(numero)
    criba.run()
