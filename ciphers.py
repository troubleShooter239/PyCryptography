"""Module: Ciphers

This module...

Classes:

Public methods:
"""
from typing import Optional, Dict

from crypt_base import CryptBase
from cipher_utils import *
from crypt_bigrams_base import CryptBigramsBase


class Caesar(CryptBase):
    """Implementation of the `Caesar` cipher.

    Attributes:
    - _shift (int): The shift value used for encryption and decryption.

    Methods:
        `__init__(self, shift: int = 0)` -> None:
            Initializes an instance of the Caesar class.
            
            Raises:
                ValueError: If the input shift is not a int.

        `encrypt(self, msg: str)` -> str:
            Encrypts a message using the Caesar cipher.

            Args:
                msg (str): The message to be encrypted.

            Returns:
                str: The encrypted message.

            Raises:
                ValueError: If the input message is not a string.

        `decrypt(self, msg: str)` -> str:
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
        """Initializes an instance of the Caesar class.

        Args:
        - shift (int): The initial shift value.
        """
        if not isinstance(shift, int):
            raise ValueError("Shift must be of type int!")
        
        self._shift = shift
    
    @property
    def shift(self) -> int:
        """Get the current shift value.

        Returns:
        - int: The current shift value.
        """
        return self._shift
    
    @shift.setter
    def shift(self, value: int) -> None:
        """Set the shift value.

        Args:
        - value (int): The new shift value.

        Raises:
        - ValueError: If the value is not an integer.
        """
        if not isinstance(value, int):
            raise ValueError("Shift value must be of type int.")
        
        self._shift = value
    
    def encrypt(self, msg: str) -> str:
        """Encrypts a message using the Caesar cipher.

        Args:
        - msg (str): The message to be encrypted.

        Returns:
        - str: The encrypted message.

        Raises:
        - ValueError: If the input message is not a string.
        """
        msg = self._validate_input_string(msg)
        
        return "".join(
            chr((ord(char) + self._shift - ord('A')) % 26 + ord('A')) 
            if 'A' <= char <= 'Z' else char for char in msg
        )

    def decrypt(self, msg: str) -> str:
        """Decrypts a message encrypted with the Caesar cipher.

        Args:
        - msg (str): The message to be decrypted.

        Returns:
        - str: The decrypted message.

        Raises:
        - ValueError: If the input message is not a string.
        """
        msg = self._validate_input_string(msg)

        return "".join(
            chr((ord(char) - self._shift - ord('A')) % 26 + ord('A')) 
            if 'A' <= char <= 'Z' else char for char in msg
        )


class PolybiusSquare(CryptBase):
    """Implementation of the `Polybius Square` cipher.

    Attributes:
    - _table (List[List[str]]): The Polybius Square table.
    - _coords (Dict[str, Tuple[int, int]]): Dictionary mapping characters to their coordinates.

    Methods:
        `__init__(self, table: Optional[List[List[str]]] = eng25_matrix_upper)` -> None:
            Initializes an instance of the PolybiusSquare class.

            Args:
                table (Optional[List[List[str]]]): The Polybius Square table.

        `_get_coords(self)` -> Dict[str, Tuple[int, int]]:
            Get the coordinates of characters in the Polybius Square table.

            Returns:
                Dict[str, Tuple[int, int]]: Dictionary mapping characters to their coordinates.

        `@property
        table(self)` -> List[List[str]]:
            Get the current table value.

            Returns:
                List[List[str]]: The current table value.

        `@table.setter
        table(self, table: List[List[str]])` -> None:
            Set the table value.

            Args:
                table (List[List[str]]): The new table value.

            Raises:
                ValueError: If the table is not a list of lists of strings.

        `encrypt(self, msg: str)` -> str:
            Encrypts a message using the Polybius Square.

            Args:
                msg (str): The message to be encrypted.

            Returns:
                str: The encrypted message.

            Raises:
                ValueError: If the input message contains invalid characters.

        `decrypt(self, msg: str)` -> str:
            Decrypts a message encrypted with the Polybius Square.

            Args:
                msg (str): The message to be decrypted.

            Returns:
                str: The decrypted message.

            Raises:
                ValueError: If the input message contains invalid characters or has an odd length.
    """
    def __init__(self, 
                 table: Optional[List[List[str]]] = eng25_matrix_upper) -> None:
        """Initializes an instance of the PolybiusSquare class.

        Args:
        - table (Optional[List[List[str]]]): The Polybius Square table.
        """
        self._table = table
        self._coords = self._get_coords()
        
    def _get_coords(self) -> Dict[str, Tuple[int, int]]:
        """Get the coordinates of characters in the Polybius Square table.

        Returns:
        - Dict[str, Tuple[int, int]]: Dictionary mapping characters to their coordinates.
        """
        return {char: (i, row.index(char)) for i, row in enumerate(self._table) for char in row}
    
    @property
    def table(self) -> List[List[str]]:
        """Get the current table value.

        Returns:
        - List[List[str]]: The current table value.
        """
        return self._table
    
    @table.setter
    def table(self, table: List[List[str]]) -> None:
        """Set the table value.

        Args:
        - table (List[List[str]]): The new table value.

        Raises:
        - ValueError: If the table is not a list of lists of strings.
        """
        if not all(isinstance(row, list) and 
                   all(isinstance(c, str) for c in row) for row in table):
            raise ValueError("Table value must be a list of lists of strings.")
        
        self._table = table
        self._coords = self._get_coords()

    def encrypt(self, msg: str) -> str:
        """Encrypts a message using the Polybius Square.

        Args:
        - msg (str): The message to be encrypted.

        Returns:
        - str: The encrypted message.

        Raises:
        - ValueError: If the input message contains invalid characters.
        """
        msg = self._validate_input_string(msg)
        
        return "".join([
            f"{self._coords[c][0]}{self._coords[c][1]}" for c in msg if c in self._coords
        ])

    def decrypt(self, msg: str) -> str:
        """Decrypts a message encrypted with the Polybius Square.

        Args:
        - msg (str): The message to be decrypted.

        Returns:
        - str: The decrypted message.

        Raises:
        - ValueError: If the input message contains invalid characters or has an odd length.
        """
        msg = self._validate_input_string(msg)
        
        if len(msg) % 2 != 0:
            raise ValueError("Input message must have an even length.")
        
        return "".join(
            self._table[int(msg[i])][int(msg[i+1])] for i in range(0, len(msg), 2)
        )


class Vigenere(CryptBase):
    """Implementation of the `Vigenere` cipher.

    Attributes:
    - _key (str): The key for Vigenere encryption.
    - _shift (int): The shift value used for encryption and decryption.
    - _alphabet (str): The shifted alphabet for encryption.
    - _matrix (List[List[str]]): The Vigenere encryption matrix.

    Methods:
        `__init__(self, key: Optional[str] = "A", shift: Optional[int] = 0)` -> None:
            Initializes an instance of the Vigenere class.

            Args:
                key (Optional[str]): The key for Vigenere encryption.

            If `key` is not provided, a default key "A" is used.

                shift (Optional[int]): The shift value.

            If `shift` is not provided, a default shift value of 0 is used.

        `@property
        key(self)` -> str:
            Get the current key value.

            Returns:
                str: The current key value.

        `@key.setter
        key(self, key: str)` -> None:
            Set the key value.

            Args:
                key (str): The new key value.

            Raises:
                ValueError: If the key is not a string.

        `@property
        shift(self)` -> int:
            Get the current shift value.

            Returns:
                int: The current shift value.

        `@shift.setter
        shift(self, shift: int)` -> None:
            Set the shift value.

            Args:
                shift (int): The new shift value.

            Raises:
                ValueError: If the shift is not an integer.
                
        `_shift_alphabet(self)` -> None:
            Shifts the alphabet by the specified number of positions.

        `_generate_matrix(self)` -> List[List[str]]:
            Generates the Vigenere encryption matrix.

            Returns:
                List[List[str]]: The Vigenere encryption matrix.

        `encrypt(self, msg: str)` -> str:
            Encrypts a message using the Vigenere cipher.

            Args:
                msg (str): The message to be encrypted.

            Returns:
                str: The encrypted message.

            Raises:
                ValueError: If the input message is not a string.

        `decrypt(self, msg: str)` -> str:
            Decrypts a message encrypted with the Vigenere cipher.

            Args:
                msg (str): The message to be decrypted.

            Returns:
                str: The decrypted message.

            Raises:
                ValueError: If the input message is not a string.
    """
    def __init__(self, 
                 key: Optional[str] = "A",
                 shift: Optional[int] = 0) -> None:
        """Initializes an instance of the Vigenere class.

        Args:
        - key (Optional[str]): The key for Vigenere encryption.

        If `key` is not provided, a default key "A" is used.
        
        If `shift` is not provided, a default shift value of 0 is used.
        """
        self._key = key
        self._shift = shift
        self._alphabet = self._shift_alphabet()
        self._matrix = self._generate_matrix()

    @property
    def key(self) -> str:
        """Get the current key value.

        Returns:
        - str: The current key value.
        """
        return self._key
    
    @key.setter
    def key(self, key: str) -> None:
        """Set the key value.

        Args:
        - key (str): The new key value.

        Raises:
        - ValueError: If the key is not a list of lists of strings.
        """
        if not isinstance(key, str):
            raise ValueError("Key value must be a list of lists of strings.")
        
        self._key = key
        
    @property
    def shift(self) -> int:
        """Get the current shift value.

        Returns:
        - int: The current shift value.
        """
        return self._shift
    
    @shift.setter
    def shift(self, shift: int) -> None:
        """Set the shift value.

        Args:
        - shift (int): The new shift value.

        Raises:
        - ValueError: If the shift is not an integer.
        """
        if not isinstance(shift, int):
            raise ValueError("Shift value must be an integer.")
        
        self._shift = shift
        self._alphabet = self._shift_alphabet()
        
    def _shift_alphabet(self) -> str:
        """Shifts the alphabet by the specified number of positions."""
        return eng26_str_upper[self._shift:] + eng26_str_upper[:self._shift]

    def _generate_matrix(self):
        """Generates the Vigenere encryption matrix.

        Returns:
        - List[List[str]]: The Vigenere encryption matrix.
        """
        unique_chars = sorted(
            set(self._key + self._alphabet), 
            key=lambda x: self._key.index(x) if x in self._key else self._alphabet.index(x)
        )   
        
        return [
            list(unique_chars[-i:] + unique_chars[:-i]) for i in range(len(unique_chars), 0, -1)
        ]

    def encrypt(self, msg: str) -> str:
        """Encrypts a message using the Vigenere cipher.

        Args:
        - msg (str): The message to be encrypted.

        Returns:
        - str: The encrypted message.

        Raises:
        - ValueError: If the input message is not a string.
        """
        msg = self._validate_input_string(msg)
        
        msg_ind = [self._matrix[0].index(c) for c in msg]
        key_ind = [self._matrix[0].index(c) for c in self.key]
        adj_ind = [key_ind[i % len(key_ind)] for i in range(len(msg_ind))]
        
        return "".join(self._matrix[msg_ind[i]][adj_ind[i]] for i in range(len(msg_ind)))

    def decrypt(self, msg: str) -> str:
        """Decrypts a message encrypted with the Vigenere cipher.

        Args:
        - msg (str): The message to be decrypted.

        Returns:
        - str: The decrypted message.

        Raises:
        - ValueError: If the input message is not a string.
        """
        msg = self._validate_input_string(msg)

        key_ind = [self._matrix[0].index(c) for c in self.key]
        adj_ind = [key_ind[i % len(key_ind)] for i in range(len(msg))]
        
        return "".join(
            self._matrix[0][self._matrix[adj_ind[i]].index(c)] for i, c in enumerate(msg)
        )


class Playfer(CryptBigramsBase):
    """Implementation of the `Playfer` cipher.
    
    Attributes:
    - _alphabet (str): The alphabet used for encryption.
    - _size (int): The size of the matrix (5 for English, 6 for Russian).
    - _key (str): The key for the Playfair cipher.
    - _matrix (List[List[str]]): The Playfair encryption matrix.

    Methods:
        `__init__(self, key: Optional[str] = "", language: Optional[str] = "eng")` -> None:
            Initialize the Playfair cipher.

            Args:
                key (Optional[str]): The key for the cipher.
                language (Optional[str]): The language to use (default is "eng" for English).

        `_generate_matrix(self, key: Optional[str] = None)` -> List[List[str]]:
            Generate the Playfair key matrix.

            Args:
                key (Optional[str]): The key for the cipher.

            Returns:
                List[List[str]]: The generated key matrix.

        `_find_position(self, char: str)` -> Tuple[int, int]:
            Find the position of a character in the key matrix.

            Args:
                char (str): The character to find.

            Returns:
                Tuple[int, int]: The row and column indices of the character.

        `_process_pair(self, char1: str, char2: str, direction: int)` -> str:
            Process a pair of characters based on the specified direction.

            Args:
                char1 (str): The first character.
                char2 (str): The second character.
                direction (int): The direction of processing (-1 for encryption, 1 for decryption).

            Returns:
                str: The processed pair of characters.

        `encrypt(self, msg: str)` -> str:
            Encrypt a message using the Playfair cipher.

            Args:
                msg (str): The message to encrypt.

            Returns:
                str: The encrypted message.

            Raises:
                ValueError: If the input message is not a string.

        `decrypt(self, msg: str)` -> str:
            Decrypt a message using the Playfair cipher.

            Args:
                msg (str): The message to decrypt.

            Returns:
                str: The decrypted message.

            Raises:
                ValueError: If the input message is not a string.
    """
    def __init__(self,
                 key: Optional[str] = "",
                 language: Optional[str] = "eng") -> None:
        """Initialize the Playfair cipher.

        Args:
        - key: Optional[str]: The key for the cipher.
        - language: Optional[str]: The language to use (default is "eng" for English).
        """
        self._alphabet, self._size = is_english(language)
        key = key.upper()
        
        if language == "eng" and not is_valid_eng(key) or\
            language == "rus" and not is_valid_rus(key):
            raise ValueError("Language in key is not the selected language!")
        
        self._language = language
        self._key = key
        self._matrix = generate_matrix_by_key(self._alphabet, self._key, self._key)
    
    @property
    def key(self) -> str:
        """Get the current shift value.

        Returns:
        - str: The current key value.
        """
        return self._key
    
    @key.setter
    def key(self, key: str) -> None:
        """Set the key value.

        Args:
        - key (str): The new key value.

        Raises:
        - ValueError: If the key is not a string.
        """
        if not isinstance(key, str):
            raise ValueError("Key must be a string.")

        if self._language == "eng" and not is_valid_eng(key) or\
            self._language == "rus" and not is_valid_rus(key):
            raise ValueError("Selected language is not supported!")

        self._key = key
        self._matrix = generate_matrix_by_key(self._alphabet, self._key, self._key)
        
    def _process_pair(self, char1: str, char2: str, direction: int) -> str:
        """Process a pair of characters based on the specified direction.

        Args:
        - char1 (str): The first character.
        - char2 (str): The second character.
        - direction (int): The direction of processing (-1 for encryption, 1 for decryption).

        Returns:
        - str: The processed pair of characters.
        """
        row1, col1 = self._find_position(char1)
        row2, col2 = self._find_position(char2)
        
        self._update_coords(row1, row2, col1, col2, direction, self._size)
                
        if row1 == row2:
            col1, col2 = (col1 + direction) % self._size, (col2 + direction) % self._size
        elif col1 == col2:
            row1, row2 = (row1 + direction) % self._size, (row2 + direction) % self._size
        else:
            col1, col2 = col2, col1
            
        return self._matrix[row1][col1] + self._matrix[row2][col2]
    
    def _find_position(self, char: str, matrix: List[List[str]]) -> Tuple[int, int]:
        """Find the position of a character in the key matrix.

        Args:
        - char (str): The character to find.
        - matrix (List[List[str]]): The matrix for searching the position.

        Returns:
        - Tuple[int, int]: The row and column indices of the character.
        """
        for i, row in enumerate(matrix):
            try: 
                return i, row.index(char)
            except ValueError: 
                pass
        return -1, -1
        
    def encrypt(self, msg: str) -> str:
        """Encrypt a message using the Playfair cipher.

        Args:
        - msg (str): The message to encrypt.

        Returns:
        - str: The encrypted message.
        """
        msg = self._validate_input_string(msg)
        msg = "".join([char for char in msg if char in self._alphabet])
        
        if len(msg) % 2 != 0:
            msg += 'X'
        
        return "".join(
            self._process_pair(msg[i], msg[i + 1], -1) for i in range(0, len(msg), 2)
        )

    def decrypt(self, msg: str) -> str:
        """Decrypt a message using the Playfair cipher.

        Args:
        - msg (str): The message to decrypt.

        Returns:
        - str: The decrypted message.
        """
        msg = self._validate_input_string(msg)
        
        return "".join(
            self._process_pair(msg[i], msg[i + 1], 1) for i in range(0, len(msg), 2)
        )
        

class TwoSquare(CryptBigramsBase):
    def __init__(self,
                 key1: Optional[str] = "",
                 key2: Optional[str] = "",
                 language: Optional[str] = "eng") -> None:
        self._alphabet, self._size = is_english(language)
        self._key1, self._key2 = key1, key2
        self._matrix1 = generate_matrix_by_key(self._alphabet, self._size, self._key1)
        self._matrix2 = generate_matrix_by_key(self._alphabet, self._size, self._key2)
    
    def encrypt(self, msg: str) -> str:        
        msg = self._validate_input_string(msg)
        
        if len(msg) % 2 != 0:
            msg += 'X'
        
        return "".join(
            self._proccess_pair(msg[i], msg[i + 1], self._matrix1, self._matrix2, -1, self._size) for i in range(0, len(msg), 2)
        )

    def decrypt(self, msg: str) -> str:
        msg = self._validate_input_string(msg)
        
        return "".join(
            self._proccess_pair(msg[i], msg[i + 1], self._matrix1, self._matrix2, 1, self._size) for i in range(0, len(msg), 2)
        )
