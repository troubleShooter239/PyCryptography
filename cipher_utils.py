"""Module: Cipher Utils

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

from typing import Tuple
import re

digits = "0123456789"
rus36_str_upper = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ-_."
rus33_str_upper = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
eng26_str_upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
eng25_str_upper = "ABCDEFGHIKLMNOPQRSTUVWXYZ"


def generate_matrix(alphabet: str, cols: int) -> Tuple[Tuple[str]]:
    """Generate a matrix from the given alphabet with the specified number of columns.

    Args:
    - alphabet (str): String of alphabet characters.
    - cols (int): Number of columns in the matrix.

    Returns:
    - Tuple[Tuple[str]]: Matrix of characters.
    """
    return tuple(row for row in zip(*[iter(alphabet)] * cols))

rus36_matrix_upper = generate_matrix(rus36_str_upper, 6)
eng25_matrix_upper = generate_matrix(eng25_str_upper, 5)


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
