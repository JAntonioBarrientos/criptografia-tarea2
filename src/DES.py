class DES:
    """
    Clase que implementa el algoritmo de cifrado DES (Data Encryption Standard).
    
    Este algoritmo utiliza permutaciones y sustituciones para cifrar y descifrar datos 
    de 64 bits utilizando una clave de 64 bits.
    """

    # Tablas de permutación y sustitución utilizadas por el algoritmo DES
    IP = [58, 50, 42, 34, 26, 18, 10, 2,
          60, 52, 44, 36, 28, 20, 12, 4,
          62, 54, 46, 38, 30, 22, 14, 6,
          64, 56, 48, 40, 32, 24, 16, 8,
          57, 49, 41, 33, 25, 17, 9, 1,
          59, 51, 43, 35, 27, 19, 11, 3,
          61, 53, 45, 37, 29, 21, 13, 5,
          63, 55, 47, 39, 31, 23, 15, 7]

    IP_INV = [40, 8, 48, 16, 56, 24, 64, 32,
              39, 7, 47, 15, 55, 23, 63, 31,
              38, 6, 46, 14, 54, 22, 62, 30,
              37, 5, 45, 13, 53, 21, 61, 29,
              36, 4, 44, 12, 52, 20, 60, 28,
              35, 3, 43, 11, 51, 19, 59, 27,
              34, 2, 42, 10, 50, 18, 58, 26,
              33, 1, 41, 9, 49, 17, 57, 25]

    E = [32, 1, 2, 3, 4, 5,
         4, 5, 6, 7, 8, 9,
         8, 9, 10, 11, 12, 13,
         12, 13, 14, 15, 16, 17,
         16, 17, 18, 19, 20, 21,
         20, 21, 22, 23, 24, 25,
         24, 25, 26, 27, 28, 29,
         28, 29, 30, 31, 32, 1]

    S_BOX =  [
        # S-box 1
        [[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
         [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
         [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
         [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]],
        # S-box 2
        [[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
         [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
         [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
         [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]],
        # S-box 3
        [[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
         [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
         [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
         [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]],
        # S-box 4
        [[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
         [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
         [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
         [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]],
        # S-box 5
        [[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
         [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
         [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
         [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]],
        # S-box 6
        [[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
         [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
         [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
         [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]],
        # S-box 7
        [[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
         [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
         [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
         [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]],
        # S-box 8
        [[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
         [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
         [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
         [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]],
    ]

    P = [16,7,20,21,
         29,12,28,17,
         1,15,23,26,
         5,18,31,10,
         2,8,24,14,
         32,27,3,9,
         19,13,30,6,
         22,11,4,25]

    # Permutación PC-1 para la generación de claves
    PC_1 = [57,49,41,33,25,17,9,
            1,58,50,42,34,26,18,
            10,2,59,51,43,35,27,
            19,11,3,60,52,44,36,
            63,55,47,39,31,23,15,
            7,62,54,46,38,30,22,
            14,6,61,53,45,37,29,
            21,13,5,28,20,12,4]

    # Permutación PC-2 para la generación de claves
    PC_2 = [14,17,11,24,1,5,
            3,28,15,6,21,10,
            23,19,12,4,26,8,
            16,7,27,20,13,2,
            41,52,31,37,47,55,
            30,40,51,45,33,48,
            44,49,39,56,34,53,
            46,42,50,36,29,32]

    # Número de desplazamientos para cada ronda
    SHIFT = [1, 1, 2, 2, 2, 2, 2, 2,
             1, 2, 2, 2, 2, 2, 2, 1]

    def __init__(self, key):
        """
        Inicializa la instancia de DES con una clave específica.

        :param key: Clave de 8 bytes para el cifrado.
        :raises ValueError: Si la clave no es de 8 caracteres.
        """
        if len(key) != 8:
            raise ValueError("La clave debe ser de 8 bytes.")
        self.key = key
        self.subkeys = self.generate_keys()

    def permute(self, block, table):
        """
        Aplica una permutación a un bloque de bits según una tabla dada.

        :param block: Lista de bits a permutar.
        :param table: Tabla de permutación.
        :return: Lista de bits permutados.
        """
        return [block[i -1] for i in table]

    def shift_left(self, k, n):
        """
        Realiza un desplazamiento circular a la izquierda en una lista de bits.

        :param k: Lista de bits.
        :param n: Número de posiciones a desplazar.
        :return: Lista de bits desplazada.
        """
        return k[n:] + k[:n]

    def xor(self, a, b):
        """
        Realiza una operación XOR entre dos listas de bits.

        :param a: Primera lista de bits.
        :param b: Segunda lista de bits.
        :return: Lista resultante de la operación XOR.
        """
        return [i ^ j for i, j in zip(a, b)]

    def sbox_substitution(self, bits):
        """
        Aplica las S-boxes al bloque de bits.

        :param bits: Lista de 48 bits.
        :return: Lista de 32 bits después de la sustitución.
        """
        result = []
        for i in range(8):
            block = bits[i*6:(i+1)*6]
            row = (block[0]<<1) + block[5]
            col = (block[1]<<3) + (block[2]<<2) + (block[3]<<1) + block[4]
            val = self.S_BOX[i][row][col]
            bin_val = [int(x) for x in f"{val:04b}"]
            result.extend(bin_val)
        return result

    def generate_keys(self):
        """
        Genera las subclaves para cada ronda del algoritmo DES.

        :return: Lista de 16 subclaves, cada una de 48 bits.
        """
        key_bits = [int(x) for x in f"{int.from_bytes(self.key.encode('ascii'), 'big'):064b}"]
        key_permuted = self.permute(key_bits, self.PC_1)
        C = key_permuted[:28]
        D = key_permuted[28:]
        subkeys = []
        for shift in self.SHIFT:
            C = self.shift_left(C, shift)
            D = self.shift_left(D, shift)
            CD = C + D
            subkey = self.permute(CD, self.PC_2)
            subkeys.append(subkey)
        return subkeys

    def f(self, R, K):
        """
        Función de mezcla del DES que expande, mezcla y permuta los bits.

        :param R: Lista de 32 bits de la mitad derecha del bloque.
        :param K: Subclave de 48 bits para la ronda actual.
        :return: Lista de 32 bits después de aplicar la función f.
        """
        R_expanded = self.permute(R, self.E)
        xor_result = self.xor(R_expanded, K)
        sbox_result = self.sbox_substitution(xor_result)
        f_result = self.permute(sbox_result, self.P)
        return f_result

    def encrypt_block(self, block):
        """
        Cifra un bloque de 8 bytes utilizando el algoritmo DES.

        :param block: Bloque de 8 bytes a cifrar.
        :return: Bloque cifrado de 8 bytes.
        """
        block_bits = [int(x) for x in f"{int.from_bytes(block, 'big'):064b}"]
        block_permuted = self.permute(block_bits, self.IP)
        L = block_permuted[:32]
        R = block_permuted[32:]
        for subkey in self.subkeys:
            L_prev = L
            L = R
            R = self.xor(L_prev, self.f(R, subkey))
        pre_output = R + L
        output_bits = self.permute(pre_output, self.IP_INV)
        output_int = int(''.join(str(x) for x in output_bits), 2)
        return output_int.to_bytes(8, 'big')

    def decrypt_block(self, block):
        """
        Descifra un bloque de 8 bytes utilizando el algoritmo DES.

        :param block: Bloque cifrado de 8 bytes a descifrar.
        :return: Bloque descifrado de 8 bytes.
        """
        block_bits = [int(x) for x in f"{int.from_bytes(block, 'big'):064b}"]
        block_permuted = self.permute(block_bits, self.IP)
        L = block_permuted[:32]
        R = block_permuted[32:]
        for subkey in reversed(self.subkeys):
            L_prev = L
            L = R
            R = self.xor(L_prev, self.f(R, subkey))
        pre_output = R + L
        output_bits = self.permute(pre_output, self.IP_INV)
        output_int = int(''.join(str(x) for x in output_bits), 2)
        return output_int.to_bytes(8, 'big')

    def pad(self, data):
        """
        Aplica relleno al texto plano para que su longitud sea múltiplo de 8 bytes.

        :param data: Datos en bytes a rellenar.
        :return: Datos rellenos en bytes.
        """
        pad_len = 8 - (len(data) % 8)
        return data + bytes([pad_len]*pad_len)

    def unpad(self, data):
        """
        Elimina el relleno de los datos descifrados.

        :param data: Datos en bytes con relleno.
        :return: Datos originales sin relleno en bytes.
        :raises ValueError: Si el relleno es inválido.
        """
        pad_len = data[-1]
        if pad_len < 1 or pad_len > 8:
            raise ValueError("Padding inválido.")
        return data[:-pad_len]

    def encrypt(self, plaintext):
        """
        Cifra un texto plano utilizando DES en modo ECB.

        :param plaintext: Texto plano en formato string.
        :return: Texto cifrado en bytes.
        """
        data = plaintext.encode('ascii')
        data = self.pad(data)
        ciphertext = b''
        for i in range(0, len(data), 8):
            block = data[i:i+8]
            ciphertext += self.encrypt_block(block)
        return ciphertext

    def decrypt(self, ciphertext):
        """
        Descifra un texto cifrado utilizando DES en modo ECB.

        :param ciphertext: Texto cifrado en bytes.
        :return: Texto descifrado en formato string.
        """
        data = b''
        for i in range(0, len(ciphertext), 8):
            block = ciphertext[i:i+8]
            data += self.decrypt_block(block)
        data = self.unpad(data)
        return data.decode('ascii')

if __name__ == "__main__":
    key = 'MiClave1'  # La clave debe ser de 8 caracteres
    des = DES(key)
    mensaje = 'Por fin salio el cifradooo :D'  # El mensaje a cifrar en ASCII
    cifrado = des.encrypt(mensaje)
    print('Cifrado (hex):', cifrado.hex())
    descifrado = des.decrypt(cifrado)
    print('Descifrado:', descifrado)