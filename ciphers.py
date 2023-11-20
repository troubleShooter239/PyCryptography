from typing import Optional, List, Dict, Tuple
import string
from crypt_base import CryptBase

eng26_str_upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"  # With j
eng25_str_upper = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # Without j
eng_matrix_upper = [
    ['A', 'B', 'C', 'D', 'E'],
    ['F', 'G', 'H', 'I', 'K'],
    ['L', 'M', 'N', 'O', 'P'],
    ['Q', 'R', 'S', 'T', 'U'],
    ['V', 'W', 'X', 'Y', 'Z']
]


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
                 shift: Optional[int] = 0) -> None:
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
                 table: Optional[List[List[str]]] = eng_matrix_upper) -> None:
        """
        Initializes an instance of the PolybiusSquare class.

        Args:
            table (Optional[List[List[str]]]): The Polybius Square table.

        If `table` is not provided, the default table is used.
        """
        self._table = table
        self._coords = self._get_coords()
        
    def _get_coords(self) -> Dict[str, Tuple[int, int]]:
        """
        Get the coordinates of characters in the Polybius Square table.

        Returns:
            Dict[str, Tuple[int, int]]: Dictionary mapping characters to their coordinates.
        """
        return {char: (i, row.index(char)) for i, row in enumerate(self._table) for char in row}
    
    @property
    def table(self) -> List[List[str]]:
        """
        Get the current table value.

        Returns:
            List[List[str]]: The current table value.
        """
        return self._table
    
    @table.setter
    def table(self, table: List[List[str]]) -> None:
        """
        Set the table value.

        Args:
            table (List[List[str]]): The new table value.

        Raises:
            ValueError: If the table is not a list of lists of strings.
        """
        if not all(isinstance(row, list) and all(isinstance(c, str) for c in row) for row in table):
            raise ValueError("Table value must be a list of lists of strings.")
        self._table = table
        self._coords = self._get_coords()

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
            f"{self._coords[c][0]}{self._coords[c][1]}" for c in msg if c in self._coords
        ])

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
        if len(msg) % 2 != 0:
            raise ValueError("Input message must have an even length.")
        return "".join(self._table[int(msg[i])][int(msg[i+1])] for i in range(0, len(msg), 2))


######################################## ADD SHIFT!@!!@
class Vigenere(CryptBase):
    def __init__(self, 
                 key: Optional[str] = "A",
                 shift: Optional[int] = 0) -> None:
        """
        Initializes an instance of the Vigenere class.

        Args:
            key (Optional[str]): The key for Vigenere encryption.

        If `key` is not provided, a default key "A" is used.
        """
        self._key = key
        self._shift = shift
        self._matrix = self.generate_matrix()
        
    @property
    def key(self) -> str:
        """
        Get the current key value.

        Returns:
            str: The current key value.
        """
        return self._key
    
    @key.setter
    def key(self, key: str) -> None:
        """
        Set the key value.

        Args:
            key (str): The new key value.

        Raises:
            ValueError: If the key is not a list of lists of strings.
        """
        if not isinstance(key, str):
            raise ValueError("Key value must be a list of lists of strings.")
        self._key = key
        
    @property
    def shift(self) -> int:
        """
        Get the current shift value.

        Returns:
            int: The current shift value.
        """
        return self._shift
    
    @shift.setter
    def shift(self, shift: int) -> None:
        """
        Set the shift value.

        Args:
            shift (int): The new shift value.

        Raises:
            ValueError: If the shift is not a list of lists of strings.
        """
        if not all(isinstance(row, list) and all(isinstance(c, str) for c in row) for row in shift):
            raise ValueError("Shift value must be a list of lists of strings.")
        self._shift = shift

    def generate_matrix(self) -> List[List[str]]:
        """
        Generates the Vigenere encryption matrix.

        Returns:
            List[List[str]]: The Vigenere encryption matrix.
        """
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        unique_chars = sorted(
            set(self._key + alphabet), 
            key=lambda x: self._key.index(x) if x in self._key else alphabet.index(x)
        )
        return [
            list(unique_chars[-i:] + unique_chars[:-i]) for i in range(len(unique_chars), 0, -1)
        ]

    def encrypt(self, msg: str) -> str:
        """
        Encrypts a message using the Vigenere cipher.

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
        msg_ind = [self._matrix[0].index(c) for c in msg]
        key_ind = [self._matrix[0].index(c) for c in self.key]
        adj_ind = [key_ind[i % len(key_ind)] for i in range(len(msg_ind))]
        return "".join(self._matrix[msg_ind[i]][adj_ind[i]] for i in range(len(msg_ind)))

    def decrypt(self, msg: str) -> str:
        """
        Decrypts a message encrypted with the Vigenere cipher.

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
        key_ind = [self._matrix[0].index(c) for c in self.key]
        adj_ind = [key_ind[i % len(key_ind)] for i in range(len(msg))]
        return "".join(
            self._matrix[0][self._matrix[adj_ind[i]].index(c)] for i, c in enumerate(msg)
        )
        
        
####################################################################
#FIX BIGRAMS! ДОБАВИТЬ СМЕНУ ЯЗЫКОВ, УКАЗАНИЕ РАЗМЕРОВ И ТД!!Ё"!№
####################################################################
class Playfer(CryptBase):
    def __init__(self,
                 key: Optional[str] = "") -> None:         
        self.alphabet = eng26_str_upper
        self.size = (5, 5)
        self.key = key
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
