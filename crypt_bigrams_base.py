from typing import List, Tuple, Optional
from crypt_base import CryptBase


class CryptBigramsBase(CryptBase):
    
    @staticmethod
    def _find_position(char: str, matrix: List[List[str]]) -> Tuple[int, int]:
        """Find the position of a character in the key matrix.

        Args:
        - char (str): The character to find.
        - matrix (List[List[str]]): The matrix for searching position.

        Returns:
        - Tuple[int, int]: The row and column indices of the character.
        """
        for i, row in enumerate(matrix):
            try: 
                return i, row.index(char)
            except ValueError: 
                pass
            
        return -1, -1
            
    @staticmethod
    def _process_pair(char1: str, char2: str, 
                       matrix1: List[List[str]], matrix2: Optional[List[List[str]]],
                       direction: int, size: int) -> str:
        """Process a pair of characters based on the specified direction.

        Args:
        - char1 (str): The first character.
        - char2 (str): The second character.
        - matrix1 (List[List[str]]): The first matrix.
        - matrix2 (Optional[List[List[str]]]): The second matrix.
        - direction (int): Direction (-1 for encrypt, -1 for decrypt)
        - size (int): Size of the matrix.

        Returns:
        - str: The processed pair of characters.
        """
        matrix2 = matrix2 or matrix1
            
        row1, col1 = CryptBigramsBase.__find_position(char1, matrix1)
        row2, col2 = CryptBigramsBase.__find_position(char2, matrix2)
                
        if row1 == row2:
            col1, col2 = (col1 + direction) % size, (col2 + direction) % size
        elif col1 == col2:
            row1, row2 = (row1 + direction) % size, (row2 + direction) % size
        else:
            col1, col2 = col2, col1
            
        return matrix1[row1][col1] + matrix2[row2][col2]
