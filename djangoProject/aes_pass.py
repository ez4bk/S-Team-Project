import base64
import random

from Cryptodome.Cipher import AES


class AESCipher:

    def __init__(self, key="USERPASSWORD_KEY"):
        self.key = key[0:16].encode("utf-8")
        self.iv = b"0" * 13 + "{}{}{}".format(random.randint(0, 9), random.randint(0, 9),
                                              random.randint(0, 9)).encode()

    @staticmethod
    def __pad(text):
        text_length = len(text)
        amount_to_pad = AES.block_size - (text_length % AES.block_size)
        if amount_to_pad == 0:
            amount_to_pad = AES.block_size
        pad = chr(amount_to_pad)
        return text + pad * amount_to_pad

    @staticmethod
    def __unpad(text):
        pad = ord(text[-1])
        return text[:-pad]

    def encrypt(self, raw):
        """加密"""
        raw = self.__pad(raw)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return base64.b64encode(self.iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc, iv=None):
        """解密"""
        if iv is None:
            iv = self.iv
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self.__unpad(cipher.decrypt(enc).decode())

    def encrypt_main(self, number):
        return self.encrypt(number).decode()

    def decrypt_main(self, secret_number):
        temp_data = []
        if isinstance(secret_number, str):
            temp_data = base64.decodebytes(bytes(secret_number, encoding="utf-8"))
        elif isinstance(secret_number, bytes):
            temp_data = secret_number
        decode_str = self.decrypt(temp_data[16::], temp_data[0:16])
        return decode_str


if __name__ == '__main__':
    e = AESCipher(key="ADMINPASSWORDKEY")
    aes_str = e.encrypt_main("123456")
    print(aes_str)
    aes_decode = e.decrypt_main(aes_str)

    print(aes_decode)
