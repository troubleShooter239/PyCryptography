from abc import ABC, abstractmethod


class CryptBase(ABC):
    @abstractmethod
    def encrypt(self, msg: str) -> str: ...

    @abstractmethod
    def decrypt(self, msg: str) -> str: ...
