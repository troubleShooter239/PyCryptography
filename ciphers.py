import string
from typing import Optional

from crypt_base import CryptBase


class Caesar(CryptBase):
    """
    Implementation of the Caesar cipher.

    Attributes:
        _shift (int): The shift value used for encryption and decryption.

    Methods:
        __init__(self, shift: int = 0) -> None:
            Initializes an instance of the Caesar class.
            
            Raises:
                ValueError: If the input shift is not a int.

        encrypt(self, msg: str) -> str:
            Encrypts a message using the Caesar cipher.

            Args:
                msg (str): The message to be encrypted.

            Returns:
                str: The encrypted message.

            Raises:
                ValueError: If the input message is not a string.

        decrypt(self, msg: str) -> str:
            Decrypts a message encrypted with the Caesar cipher.

            Args:
                msg (str): The message to be decrypted.

            Returns:
                str: The decrypted message.

            Raises:
                ValueError: If the input message is not a string.
    """
    def __init__(self, 
                 shift: int = 0) -> None:
        """
        Initializes an instance of the Caesar class.

        Args:
            shift (int): The initial shift value.
        """
        if not isinstance(shift, int):
            raise ValueError("Shift must be of type int!")
        self._shift = shift
    
    @property
    def shift(self) -> int:
        """
        Get the current shift value.

        Returns:
            int: The current shift value.
        """
        return self._shift
    
    @shift.setter
    def shift(self, value: int) -> None:
        """
        Set the shift value.

        Args:
            value (int): The new shift value.

        Raises:
            ValueError: If the value is not an integer.
        """
        if not isinstance(value, int):
            raise ValueError("Shift value must be of type int.")
        self._shift = value
    
    def encrypt(self, msg: str) -> str:
        """
        Encrypts a message using the Caesar cipher.

        Args:
            msg (str): The message to be encrypted.

        Returns:
            str: The encrypted message.

        Raises:
            ValueError: If the input message is not a string.
        """
        if not isinstance(msg, str):
            raise ValueError("Input message must be a string.")
        msg = msg.upper()
        return ''.join(
            chr((ord(char) + self._shift - ord('A')) % 26 + ord('A')) 
            if 'A' <= char <= 'Z' else char for char in msg
        )

    def decrypt(self, msg: str) -> str:
        """
        Decrypts a message encrypted with the Caesar cipher.

        Args:
            msg (str): The message to be decrypted.

        Returns:
            str: The decrypted message.

        Raises:
            ValueError: If the input message is not a string.
        """
        if not isinstance(msg, str):
            raise ValueError("Input message must be a string.")
        msg = msg.upper()
        return ''.join(
            chr((ord(char) - self._shift - ord('A')) % 26 + ord('A')) 
            if 'A' <= char <= 'Z' else char for char in msg
        )


class PolybiusSquare(CryptBase):
    def __init__(self, 
                 table: Optional[list[list[str]]] = None) -> None:
        """
        Initializes an instance of the PolybiusSquare class.

        Args:
            table (Optional[list[list[str]]]): The Polybius Square table.

        If `table` is not provided, the default table is used.
        """
        if table is None:
            table = [
                ['A', 'B', 'C', 'D', 'E'],
                ['F', 'G', 'H', 'I', 'K'],
                ['L', 'M', 'N', 'O', 'P'],
                ['Q', 'R', 'S', 'T', 'U'],
                ['V', 'W', 'X', 'Y', 'Z']
            ] 
        self._table = table
        self._char_coords = {
            char: (i, row.index(char)) for i, row in enumerate(self._table) for char in row
        }

    def encrypt(self, msg: str) -> str:
        """
        Encrypts a message using the Polybius Square.

        Args:
            msg (str): The message to be encrypted.

        Returns:
            str: The encrypted message.

        Raises:
            ValueError: If the input message contains invalid characters.
        """
        if not isinstance(msg, str):
            raise ValueError("Input message must be a string.")         
        msg = msg.upper()
        return "".join([
            f"{self._char_coords[c][0]}{self._char_coords[c][1]}" for c in msg if c in self._char_coords
        ])
############################################## Optimize decrypt!
    def decrypt(self, msg: str) -> str:
        """
        Decrypts a message encrypted with the Polybius Square.

        Args:
            msg (str): The message to be decrypted.

        Returns:
            str: The decrypted message.

        Raises:
            ValueError: If the input message contains invalid characters or has an odd length.
        """
        if not isinstance(msg, str):
            raise ValueError("Input message must be a string.")
        text = ""
        for i in range(0, len(msg), 2):
            row, col = msg[i:i+2]
            text += self._table[int(row)][int(col)]
        
        return text


class Vigenere(CryptBase):
    def __init__(self, 
                 key: Optional[str] = None) -> None:
        if key is None:
            key = "A"
        self.key = key
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
        if not isinstance(msg, str):
            raise ValueError("Input message must be a string.")
        msg = msg.upper()
        ind_msg = [self.matrix[0].index(c) for c in msg]
        ind_key = [self.matrix[0].index(c) for c in self.key]
        adjusted_ind = [ind_key[i % len(ind_key)] for i in range(len(ind_msg))]
        
        return ''.join(
            self.matrix[ind_msg[i]][adjusted_ind[i]] 
            for i in range(len(ind_msg))
        )

    def decrypt(self, msg: str) -> str:
        if not isinstance(msg, str):
            raise ValueError("Input message must be a string.")
        msg = msg.upper()
        ind_key = [self.matrix[0].index(c) for c in self.key]
        adjusted_ind = [ind_key[i % len(ind_key)] for i in range(len(msg))]
        
        return ''.join(
            self.matrix[0][self.matrix[adjusted_ind[i]].index(c)] 
            for i, c in enumerate(msg)
        )
####################################################################
#FIX BIGRAMS! ДОБАВИТЬ СМЕНУ ЯЗЫКОВ, УКАЗАНИЕ РАЗМЕРОВ И ТД!!Ё"!№
####################################################################
class Playfer(CryptBase):
    def __init__(self,
                 key: Optional[str] = None) -> None:         
        self.alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        self.size = (5, 5)
        self.key = key or ""
        self.matrix = self.generate_matrix(self.key)

    def generate_matrix(self, key: str) -> list[list[str]]:
        cols = self.size[1]
        text = ""
        for c in key + self.alphabet:
            if c not in text:
                text += c  
        return [text[i:i + cols] for i in range(0, len(text), cols)]
    
    def find_position(self, char: str) -> tuple[int, int]:
        for i, row in enumerate(self.matrix):
            try:
                j = row.index(char)
                return i, j
            except ValueError: ...
        return -1, -1
        
    def process_pair(self, char1: str, char2: str, direction: int) -> str:
        row1, col1 = self.find_position(char1)
        row2, col2 = self.find_position(char2)

        if row1 == row2:
            col1, col2 = (col1 + direction) % self.size[1], (col2 + direction) % self.size[1]
        elif col1 == col2:
            row1, row2 = (row1 + direction) % self.size[0], (row2 + direction) % self.size[0]
        else:
            col1, col2 = col2, col1

        return self.matrix[row1][col1] + self.matrix[row2][col2]
        
    def encrypt(self, msg: str) -> str:
        if not isinstance(msg, str):
            raise ValueError("Input message must be a string.")
        msg = msg.upper().replace(' ', '_')
        text = ""
        for i in range(0, len(msg), 2):
            char1 = msg[i]
            char2 = msg[i + 1] if i + 1 < len(msg) else 'Х'
            text += self.process_pair(char1, char2, 1)
        return text

    def decrypt(self, msg: str) -> str:
        if not isinstance(msg, str):
            raise ValueError("Input message must be a string.")
        msg = msg.upper()
        text = ""
        for i in range(0, len(msg), 2):
            char1, char2 = msg[i], msg[i + 1]
            text += self.process_pair(char1, char2, 1)
        return text.replace('_', ' ')
