import base64
import random

from Cryptodome.Cipher import AES


class AESCipher:

    def __init__(self, key="USERPASSWORD_KEY"):
        self.key = key[0:16].encode("utf-8")  # 只截取16位
        self.iv = b"0" * 13 + "{}{}{}".format(random.randint(0, 9), random.randint(0, 9),
                                              random.randint(0, 9)).encode()  # 16位字符，用来填充缺失内容，可固定值也可随机字符串，具体选择看需求。

    @staticmethod
    def __pad(text):
        """填充方式，加密内容必须为16字节的倍数，若不足则使用self.iv进行填充"""
        text_length = len(text)
        amount_to_pad = AES.block_size - (text_length % AES.block_size)
        # amount_to_pad = AES.key_size[0] - (text_length % AES.block_size)
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
        return self.encrypt(number).decode()  # 字节类型转换为 str

    def decrypt_main(self, secret_number):
        temp_data = []
        if isinstance(secret_number, str):
            temp_data = base64.decodebytes(bytes(secret_number, encoding="utf-8"))
        elif isinstance(secret_number, bytes):
            temp_data = secret_number
        decode_str = self.decrypt(temp_data[16::], temp_data[0:16])
        return decode_str


if __name__ == '__main__':

    list = []
    for i in range(100):
        e = AESCipher()
        aes_str = e.encrypt_main("test")
        if list == [] or aes_str not in list:
            list.append(aes_str)

    print(len(list))
    # print(aes_str)
    # print(e.decrypt_main("MDAwMDAwMDAwMDAwMDAwMD0ua7+uvFbUtY2nmhcpfZ0="))
    # print(e.decrypt_main("JQmzjE1xpe0KqxEATCHBdDGZefY4POsRff6Zq1q8sIQ="))
    # aes_decode = e.decrypt_main("aes_str")
    # aes_decode = e.decrypt_main("X2uM+Ehq9PIU4aopVZSVkBmmvdPezrqrd1TA8jf5Rtw=")
    # aes_decode = e.decrypt_main("22coWECApt5xPUhVP/SZ2GiMEelsmPYHgXjsmtar+ik=")
    # aes_decode = e.decrypt_main("ohfj6bHebB+qdUcH1dcFgXim0FAeWh/nqAEFHI0CjIs=")
    # aes_decode = e.decrypt_main("P4vHehC1PMtxLn736Ds/6aRCSuzI3TFxMTP+QGV5j98=")
    # aes_decode = e.decrypt_main("n6yTadggnwVLgo0G/W9Z5Ttcegy7liAtQaRdAgU0vZk=")

    # print(aes_decode)
