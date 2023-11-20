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
    """Abtract class for ciphers."""
    
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
