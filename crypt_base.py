from abc import ABC, abstractmethod


class CryptBase(ABC):
    """
    Abtract class for ciphers.
    """
    @abstractmethod
    def encrypt(self, msg: str) -> str: 
        """
        Abstract method for encrypting a message.
        """
        pass
    
    @abstractmethod
    def decrypt(self, msg: str) -> str:
        """
        Abstract method for decrypting a message.
        """
        pass
