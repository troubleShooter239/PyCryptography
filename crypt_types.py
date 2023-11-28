from crypt_base import CryptBase


class BigramCipher(CryptBase):
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
        
        if row1 == row2:
            col1, col2 = (col1 + direction) % self._size, (col2 + direction) % self._size
        elif col1 == col2:
            row1, row2 = (row1 + direction) % self._size, (row2 + direction) % self._size
        else:
            col1, col2 = col2, col1
            
        return self._matrix[row1][col1] + self._matrix[row2][col2]