import string
from typing import Optional

from crypt_base import CryptBase


class Caesar(CryptBase):
    def __init__(self, 
                 shift: int = 0):
        self.shift = shift

    def encrypt(self, msg: str) -> str:
        return ''.join(
            chr((ord(char) + self.shift - ord('A')) % 26 + ord('A')) 
            if 'A' <= char <= 'Z' else char for char in msg
        )

    def decrypt(self, msg: str) -> str:
        return ''.join(
            chr((ord(char) - self.shift - ord('A')) % 26 + ord('A')) 
            if 'A' <= char <= 'Z' else char for char in msg
        )


class PolybiusSquare(CryptBase):
    def __init__(self, 
                 table: Optional[list] = None):
        if table is None:
            table = [
                ['D', 'N', 'K', 'R', 'Y', '4'],
                ['E', 'A', 'L', 'S', 'Z', '5'],
                ['B', 'C', 'M', 'T', '0', '6'],
                ['U', 'F', 'O', 'V', '1', '7'],
                ['G', 'H', 'P', 'W', '2', '8'],
                ['I', 'J', 'Q', 'X', '3', '9']
            ]  # Example table
        
        self.table = table

    def encrypt(self, msg: str) -> str:
        text = ""
        for c in msg:
            for i in range(len(self.table)):
                for j in range(len(self.table[0])):
                    if c == self.table[i][j]:
                        text += str(i) + str(j)
        
        return text

    def decrypt(self, msg: str) -> str:
        text = ""
        for i in [msg[i:i+2] for i in range(0, len(msg), 2)]:
            row, col = i
            text += self.table[int(row)][int(col)]
        
        return text


class Vigenere(CryptBase):
    def __init__(self, 
                 key: Optional[str] = None):
        if key is None:
            self.key = "A"  # Key for default Vigenere's table
        self.matrix = self.generate_vigenere_matrix()

    def generate_vigenere_matrix(self) -> list[list[str]]:
        alphabet = string.ascii_uppercase
        unique_chars = sorted(
            set(self.key + alphabet), 
            key=lambda x: self.key.index(x) 
            if x in self.key else alphabet.index(x)
        )
        
        return [
            list(unique_chars[-i:] + unique_chars[:-i]) 
            for i in range(len(unique_chars), 0, -1)
        ]

    def encrypt(self, msg: str) -> str:
        ind_msg = [self.matrix[0].index(c) for c in msg]
        ind_key = [self.matrix[0].index(c) for c in self.key]
        adjusted_ind = [ind_key[i % len(ind_key)] for i in range(len(ind_msg))]
        
        return ''.join(
            self.matrix[ind_msg[i]][adjusted_ind[i]] 
            for i in range(len(ind_msg))
        )

    def decrypt(self, msg: str) -> str:
        ind_key = [self.matrix[0].index(c) for c in self.key]
        adjusted_ind = [ind_key[i % len(ind_key)] for i in range(len(msg))]
        
        return ''.join(
            self.matrix[0][self.matrix[adjusted_ind[i]].index(c)] 
            for i, c in enumerate(msg)
        )
