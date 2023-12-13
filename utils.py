"""Module: Utils

This module provides utilities for working with ciphers, including functions 
for generating matrices from different alphabets.

Public module variables:
- digits (str): String containing numbers from 0 to 9
- rus36_str_lower (str): Russian lowercase alphabet with 36 characters
- rus33_str_lower (str): Russian lowercase alphabet with 33 characters
- rus36_str_upper (str): Russian uppercase alphabet with 36 characters
- rus33_str_upper (str): Russian uppercase alphabet with 33 characters
- eng26_str_lower (str): English lowercase alphabet with 26 characters
- eng25_str_lower (str): English lowercase alphabet with 25 characters
- eng26_str_upper (str): English uppercase alphabet with 26 characters
- eng25_str_upper (str): English uppercase alphabet with 25 characters
- rus36_matrix_lower (Tuple[Tuple[str]]): Matrix generated from Russian lowercase alphabet with 36 characters
- rus36_matrix_upper (Tuple[Tuple[str]]): Matrix generated from Russian uppercase alphabet with 36 characters
- eng25_matrix_lower (Tuple[Tuple[str]]): Matrix generated from English lowercase alphabet with 25 characters
- eng25_matrix_upper (Tuple[Tuple[str]]): Matrix generated from English uppercase alphabet with 25 characters

Usage:
- The 'generate_matrix' function generates a matrix from a given alphabet and 
number of columns.

Example:
    >>> generate_matrix("ABCDEF", 2)
    (('A', 'B'), ('C', 'D'), ('E', 'F'))
"""

from typing import Literal, List, Optional, Tuple
import re

digits = "0123456789"
rus36_str_upper = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ-_."
rus33_str_upper = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
eng26_str_upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
eng25_str_upper = "ABCDEFGHIKLMNOPQRSTUVWXYZ"


class SupportedLanguages:
    RUSSIAN = "ru"
    ENGLISH = "en"


def generate_matrix_by_cols(alphabet: str, cols: int) -> Tuple[Tuple[str]]:
    """Generate a matrix from the given alphabet with the specified number of columns.

    Args:
    - alphabet (str): String of alphabet characters.
    - cols (int): Number of columns in the matrix.

    Returns:
    - Tuple[Tuple[str]]: Matrix of characters.
    """
    return tuple(row for row in zip(*[iter(alphabet)] * cols))


def is_valid_rus(value: str) -> bool:
    """Check if the string contains only letters of the `Russian` alphabet.

    Args:
    - value (str): The input string.

    Returns:
    - bool: True if the string contains only letters of the Russian alphabet, False otherwise.
    """
    return bool(re.fullmatch("[А-ЯЁ]+", value))


def is_valid_eng(value: str) -> bool:
    """Check if the string contains only letters of the `English` alphabet.

    Args:
    - value (str): The input string.

    Returns:
    - bool: True if the string contains only letters of the English alphabet, False otherwise.
    """
    return bool(re.fullmatch("[A-Z]+", value))


def is_supported_language(language: str, key: str = "") -> Tuple[str, Literal[6]] | Tuple[str, Literal[5]]:
        """Determine the alphabet and matrix size based on the language.

        Args:
        - language (str): The language to use.

        Returns:
        - Tuple[str, Literal[6]] | Tuple[str, Literal[5]]: The alphabet and matrix size.
        """
        if (language == SupportedLanguages.ENGLISH) and (is_valid_eng(key) or ""):
            return eng25_str_upper, 5
        elif language == SupportedLanguages.RUSSIAN and is_valid_rus(key) or "":
            return rus36_str_upper, 6
        
        raise ValueError("Selected language is not supported!")


def generate_matrix_by_key(alphabet: str, size: int, key: str) -> List[List[str]]:
    """Generate the Playfair key matrix.

    Returns:
    - List[List[str]]: The generated key matrix.
    """
    key_text = key + alphabet
    unique = "".join(sorted(set(key_text), key=key_text.index))
    
    return [unique[i:i + size] for i in range(0, len(unique), size)]
    
