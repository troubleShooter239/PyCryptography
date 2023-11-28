"""Module: CryptBase

This module defines an abstract class for ciphers.

Classes:
- CryptBase (ABC): Abstract base class for ciphers.

Public methods:
- encrypt(self, msg: str) -> str: Abstract method for encrypting a message.
- decrypt(self, msg: str) -> str: Abstract method for decrypting a message.
"""

from abc import ABC, abstractmethod


class CryptBase(ABC):
    """Abstract class for ciphers."""
    
    @abstractmethod
    def encrypt(self, msg: str) -> str: 
        """Abstract method for encrypting a message.
        
        Args:
        - msg (str): The message to be encrypted.
        
        Returns:
        - str: The encrypted message.
        """
        pass
    
    @abstractmethod
    def decrypt(self, msg: str) -> str:
        """Abstract method for decrypting a message.
        
        Args:
        - msg (str): The message to be decrypted.
        
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
