"""Module: CryptBase

This module defines an abstract class for ciphers.

Classes:
- CryptBase (ABC): Abstract base class for ciphers.

Public methods:
- encrypt(self, text: str) -> str: Abstract method for encrypting a message.
- decrypt(self, text: str) -> str: Abstract method for decrypting a message.
"""

from abc import ABC, abstractmethod

from utils import SupportedLanguages


class CryptBase(ABC):
    """Abstract class for ciphers."""
    def __init__(self, language: str) -> None:
        self.__is_valid_language(language)
        self.__language = language

    @staticmethod
    def __is_valid_language(language: str) -> None:
        if not isinstance(language, str) and not SupportedLanguages.is_supported(language):
            raise ValueError("Not supported language.")

    @property
    def language(self) -> str:
        """Get the current language value.

        Returns:
        - str: The current language value.
        """
        return self.__language
    
    @language.setter
    def language(self, language: str) -> None:
        """Set the language value.

        Args:
        - language (str): The new language value.

        Raises:
        - ValueError: If the language is not supported.
        """
        self.__is_valid_language(language)
        self.__language = language

    @abstractmethod
    def encrypt(self, text: str) -> str: 
        """Abstract method for encrypting a message.
        
        Args:
        - text (str): The message to be encrypted.
        
        Returns:
        - str: The encrypted message.
        """
        pass
    
    @abstractmethod
    def decrypt(self, text: str) -> str:
        """Abstract method for decrypting a message.
        
        Args:
        - text (str): The message to be decrypted.
        
        Returns:
        - str: The decrypted message.
        """
        pass

    @staticmethod
    def _validate_input_string(value: str) -> str:
        """Validate that the input value is a string.

        Args:
        - value (str): The value to validate.

        Raises:
        - ValueError: If the input value is not a string.
        
        Returns:
        - str: Input string in the uppercase.
        """
        if not isinstance(value, str):
            raise ValueError("Message must be a string.")
        
        return value.upper()
