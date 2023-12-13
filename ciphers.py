"""Module: Ciphers

This module...

Classes:

Public methods:
"""
from typing import Optional

from crypt_base import CryptBase
from crypt_bigrams_base import CryptBigramsBase
from utils import SupportedLanguages, is_supported_language, generate_matrix_by_cols, generate_matrix_by_key, \
    eng25_str_upper


class Caesar(CryptBase):
    """Implementation of the `Caesar` cipher.

    Attributes:
    - _shift (int): The shift value used for encryption and decryption.

    Methods:
        `__init__(self, shift: int = 0)` -> None:
            Initializes an instance of the Caesar class.
            
            Raises:
                ValueError: If the input shift is not a int.

        `encrypt(self, text: str)` -> str:
            Encrypts a message using the Caesar cipher.

            Args:
                text (str): The message to be encrypted.

            Returns:
                str: The encrypted message.

            Raises:
                ValueError: If the input message is not a string.

        `decrypt(self, text: str)` -> str:
            Decrypts a message encrypted with the Caesar cipher.

            Args:
                text (str): The message to be decrypted.

            Returns:
                str: The decrypted message.

            Raises:
                ValueError: If the input message is not a string.
    """
    def __init__(self,
                 shift: int = 0,
                 language: str = SupportedLanguages.ENGLISH) -> None:
        """Initializes an instance of the Caesar class.

        Args:
        - shift (int): The initial shift value.
        - language (str): The supported language.
        """
        super().__init__(language)

        if self._language == SupportedLanguages.ENGLISH:
            self.__size = 26
            self.__start = ord('A')
        else:
            self.__size = 33
            self.__start = ord('А')
        self.__end = self.__start + self.__size

        if not isinstance(shift, int):
            raise ValueError("Shift must be of type int.")
        
        self.__shift = shift

    @property
    def shift(self) -> int:
        """Get the current shift value.

        Returns:
        - int: The current shift value.
        """
        return self.__shift
    
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
        
        self.__shift = value

    def __apply_cipher(self, text: str, is_encryption: bool) -> str:
        """Applies the Caesar cipher to the given text.

        Args:
        - text (str): The message to be encrypted or decrypted.
        - direction (bool): The direction of the operation (True for encryption, False for decryption).

        Returns:
        - str: The result of the encryption or decryption.
        """
        s = self.__shift if is_encryption else -self.__shift
        return "".join(chr((ord(c) + s - self.__start) % self.__size + self.__start) if self.__start <= ord(c) <= self.__end else c for c in text)

    def encrypt(self, text: str) -> str:
        """Encrypts a message using the Caesar cipher.

        Args:
        - text (str): The message to be encrypted.

        Returns:
        - str: The encrypted message.

        Raises:
        - ValueError: If the input message is not a string.
        """
        text = self._validate_input_string(text)
        return self.__apply_cipher(text, True)

    def decrypt(self, text: str) -> str:
        """Decrypts a message encrypted with the Caesar cipher.

        Args:
        - text (str): The message to be decrypted.

        Returns:
        - str: The decrypted message.

        Raises:
        - ValueError: If the input message is not a string.
        """
        text = self._validate_input_string(text)
        return self.__apply_cipher(text, False)
    
# TODO: Refactor that code >>>
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

        `encrypt(self, text: str)` -> str:
            Encrypts a message using the Polybius Square.

            Args:
                text (str): The message to be encrypted.

            Returns:
                str: The encrypted message.

            Raises:
                ValueError: If the input message contains invalid characters.

        `decrypt(self, text: str)` -> str:
            Decrypts a message encrypted with the Polybius Square.

            Args:
                text (str): The message to be decrypted.

            Returns:
                str: The decrypted message.

            Raises:
                ValueError: If the input message contains invalid characters or has an odd length.
    """
    def __init__(self, 
                 language: str = SupportedLanguages.ENGLISH) -> None:
        """Initializes an instance of the PolybiusSquare class.

        Args:
        - table (Optional[List[List[str]]]): The Polybius Square table.
        """
        super().__init__(language)
        self.__alphabet, self.__size = is_supported_language(language)
        self.__table = generate_matrix_by_cols(self.__alphabet, self.__size)
        self.__coords = {c: (i, row.index(c)) for i, row in enumerate(self.__table) for c in row}

    def encrypt(self, text: str) -> str:
        """Encrypts a message using the Polybius Square.

        Args:
        - text (str): The message to be encrypted.

        Returns:
        - str: The encrypted message.

        Raises:
        - ValueError: If the input message contains invalid characters.
        """
        text = self._validate_input_string(text)
        return "".join([f"{self.__coords[c][0]}{self.__coords[c][1]}" for c in text if c in self.__coords])

    def decrypt(self, text: str) -> str:
        """Decrypts a message encrypted with the Polybius Square.

        Args:
        - text (str): The message to be decrypted.

        Returns:
        - str: The decrypted message.

        Raises:
        - ValueError: If the input message contains invalid characters or has an odd length.
        """
        text = self._validate_input_string(text)
        
        if len(text) % 2 != 0:
            raise ValueError("Input message must have an even length.")
        
        return "".join(self.__table[int(text[i])][int(text[i+1])] for i in range(0, len(text), 2))


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

        `encrypt(self, text: str)` -> str:
            Encrypts a message using the Vigenere cipher.

            Args:
                text (str): The message to be encrypted.

            Returns:
                str: The encrypted message.

            Raises:
                ValueError: If the input message is not a string.

        `decrypt(self, text: str)` -> str:
            Decrypts a message encrypted with the Vigenere cipher.

            Args:
                text (str): The message to be decrypted.

            Returns:
                str: The decrypted message.

            Raises:
                ValueError: If the input message is not a string.
    """
    def __init__(self, 
                 key: Optional[str] = "A",
                 shift: Optional[int] = 0,
                 language: Optional[str] = SupportedLanguages.ENGLISH) -> None:
        """Initializes an instance of the Vigenere class.

        Args:
        - key (Optional[str]): The key for Vigenere encryption.

        If `key` is not provided, a default key "A" is used.
        
        If `shift` is not provided, a default shift value of 0 is used.
        """
        self.__key = key.upper()
        self.__alphabet = is_supported_language(language, self.__key)[0]
        self.__shift = shift
        self.__alphabet = self.__shift_alphabet()
        self.__matrix = self.__generate_matrix()

    @property
    def key(self) -> str:
        """Get the current key value.

        Returns:
        - str: The current key value.
        """
        return self.__key
    
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
        
        self.__key = key
        
    @property
    def shift(self) -> int:
        """Get the current shift value.

        Returns:
        - int: The current shift value.
        """
        return self.__shift
    
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
        
        self.__shift = shift
        self.__alphabet = self.__shift_alphabet()
        
    def __shift_alphabet(self) -> str:
        """Shifts the alphabet by the specified number of positions."""
        return self.__alphabet[self.__shift:] + self.__alphabet[:self.__shift]

    def __generate_matrix(self):
        """Generates the Vigenere encryption matrix.

        Returns:
        - List[List[str]]: The Vigenere encryption matrix.
        """
        unique_chars = sorted(
            set(self.__key + self.__alphabet), 
            key=lambda x: self.__key.index(x) if x in self.__key else self.__alphabet.index(x)
        )   
        
        return [
            list(unique_chars[-i:] + unique_chars[:-i]) for i in range(len(unique_chars), 0, -1)
        ]

    def encrypt(self, text: str) -> str:
        """Encrypts a message using the Vigenere cipher.

        Args:
        - text (str): The message to be encrypted.

        Returns:
        - str: The encrypted message.

        Raises:
        - ValueError: If the input message is not a string.
        """
        text = self._validate_input_string(text)
        
        text_ind = [self.__matrix[0].index(c) for c in text]
        key_ind = [self.__matrix[0].index(c) for c in self.__key]
        adj_ind = [key_ind[i % len(key_ind)] for i in range(len(text_ind))]
        
        return "".join(self.__matrix[text_ind[i]][adj_ind[i]] for i in range(len(text_ind)))

    def decrypt(self, text: str) -> str:
        """Decrypts a message encrypted with the Vigenere cipher.

        Args:
        - text (str): The message to be decrypted.

        Returns:
        - str: The decrypted message.

        Raises:
        - ValueError: If the input message is not a string.
        """
        text = self._validate_input_string(text)

        key_ind = [self.__matrix[0].index(c) for c in self.__key]
        adj_ind = [key_ind[i % len(key_ind)] for i in range(len(text))]
        
        return "".join(
            self.__matrix[0][self.__matrix[adj_ind[i]].index(c)] for i, c in enumerate(text)
        )


class Playfer(CryptBigramsBase):
    """Implementation of the `Playfer` cipher.
    
    Attributes:
    - _alphabet (str): The alphabet used for encryption.
    - _size (int): The size of the matrix (5 for English, 6 for Russian).
    - _key (str): The key for the Playfair cipher.
    - _matrix (List[List[str]]): The Playfair encryption matrix.

    Methods:
        `__init__(self, key: Optional[str] = "", language: Optional[str] = SupportedLanguages.ENGLISH)` -> None:
            Initialize the Playfair cipher.

            Args:
                key (Optional[str]): The key for the cipher.
                language (Optional[str]): The language to use (default is SupportedLanguages.ENGLISH for English).

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

        `encrypt(self, text: str)` -> str:
            Encrypt a message using the Playfair cipher.

            Args:
                text (str): The message to encrypt.

            Returns:
                str: The encrypted message.

            Raises:
                ValueError: If the input message is not a string.

        `decrypt(self, text: str)` -> str:
            Decrypt a message using the Playfair cipher.

            Args:
                text (str): The message to decrypt.

            Returns:
                str: The decrypted message.

            Raises:
                ValueError: If the input message is not a string.
    """
    def __init__(self,
                 key: Optional[str] = "",
                 language: Optional[str] = SupportedLanguages.ENGLISH) -> None:
        """Initialize the Playfair cipher.

        Args:
        - key: Optional[str]: The key for the cipher.
        - language: Optional[str]: The language to use (default is SupportedLanguages.ENGLISH for English).
        """
        self.__key = key.upper()
        self.__alphabet, self.__size = is_supported_language(language, self.__key)        
        self.__matrix = generate_matrix_by_key(self.__alphabet, self.__size, self.__key)
    
    @property
    def key(self) -> str:
        """Get the current shift value.

        Returns:
        - str: The current key value.
        """
        return self.__key
    
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
        
        self.__key = key.upper()
        self.__matrix = generate_matrix_by_key(self.__alphabet, self.__size, self.__key)
        
    def encrypt(self, text: str) -> str:
        """Encrypt a message using the Playfair cipher.

        Args:
        - text (str): The message to encrypt.

        Returns:
        - str: The encrypted message.
        """
        text = self._validate_input_string(text)
        text = "".join([char for char in text if char in self._alphabet])
        
        if len(text) % 2 != 0:
            text += 'X'
        
        return "".join(
            self._process_pair(text[i], text[i + 1], self._matrix, None, -1, self._size) 
            for i in range(0, len(text), 2)
        )

    def decrypt(self, text: str) -> str:
        """Decrypt a message using the Playfair cipher.

        Args:
        - text (str): The message to decrypt.

        Returns:
        - str: The decrypted message.
        """
        text = self._validate_input_string(text)
        
        return "".join(
            self._process_pair(text[i], text[i + 1], self._matrix, None, 1, self._size) 
            for i in range(0, len(text), 2)
        )
        

class TwoSquare(CryptBigramsBase):
    def __init__(self,
                 key1: Optional[str] = "",
                 key2: Optional[str] = "",
                 language: Optional[str] = SupportedLanguages.ENGLISH) -> None:
        self._alphabet, self._size = eng25_str_upper, 5
        self._key1, self._key2 = key1.upper(), key2.upper()
        self._matrix1 = generate_matrix_by_key(self._alphabet, self._size, self._key1)
        self._matrix2 = generate_matrix_by_key(self._alphabet, self._size, self._key2)
    
    def encrypt(self, text: str) -> str:        
        text = self._validate_input_string(text)
        
        if len(text) % 2 != 0:
            text += 'X'
        
        text = ""
        for i in range(0, len(text), 2):
            pos1 = self._find_position(text[i], self._matrix1)
            pos2 = self._find_position(text[i + 1], self._matrix2)
            
            if pos1[0] != pos2[0]:
                cipher1 = self._matrix1[pos2[0]][pos1[1]]
                cipher2 = self._matrix2[pos1[0]][pos2[1]]
                text += cipher1 + cipher2
            else:
                cipher1 = self._matrix1[pos1[0]][pos2[1]]
                cipher2 = self._matrix2[pos2[0]][pos1[1]]
                text += cipher1 + cipher2
                
        return text

    def decrypt(self, text: str) -> str:
        text = self._validate_input_string(text)

        text = ""
        for i in range(0, len(text), 2):
            pos1 = self._find_position(text[i], self._matrix1)
            pos2 = self._find_position(text[i + 1], self._matrix2)

            if pos1[0] != pos2[0]:
                decipher1 = self._matrix1[pos2[0]][pos1[1]]
                decipher2 = self._matrix2[pos1[0]][pos2[1]]
                text += decipher1 + decipher2
            else:
                decipher1 = self._matrix1[pos1[0]][pos2[1]]
                decipher2 = self._matrix2[pos2[0]][pos1[1]]
                text += decipher1 + decipher2

        return text


cipher = TwoSquare("example", "keyword")
crypt = cipher.encrypt("helloworld")
print(crypt)
print(cipher.decrypt(crypt))