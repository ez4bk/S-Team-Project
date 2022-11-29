from lib.base_lib.utils.aes_pass import AESCipher

aes_cipher = AESCipher()


class TestAesPass(object):
    def test_t04_pwd_decrypt_01(self):
        # encrypted value of string 'test'
        result = 'test'
        test_e = ['MDAwMDAwMDAwMDAwMDI5OCdo9hwvFr57rrdNvkn4v60=',
                  'MDAwMDAwMDAwMDAwMDk1NB7loOgv4sIpJHC8utZ9Wrc=',
                  'MDAwMDAwMDAwMDAwMDIzMn9DwsIUj53O16S7buFmZGE=',
                  'MDAwMDAwMDAwMDAwMDg3Nmj9ysF/oeHjTiaR6a1v9Tk=',
                  'MDAwMDAwMDAwMDAwMDQ4MkqaGa14xKLj3e72J+rDEd0=']
        for e in test_e:
            assert aes_cipher.decrypt_main(e) == result

    def test_t04_pwd_encrypt_01(self):
        input_pass = 'test'
        aes_pass = 'MDAwMDAwMDAwMDAwMDI5OCdo9hwvFr57rrdNvkn4v60='
        e_input = aes_cipher.encrypt_main(input_pass)
        assert aes_cipher.decrypt_main(e_input) == aes_cipher.decrypt_main(aes_pass)

    def test_t04_pwd_encrypt_02(self):
        input_pass = 'errorPWD'
        expect = aes_cipher.encrypt_main('test')
        e_input = aes_cipher.encrypt_main(input_pass)

        assert aes_cipher.decrypt_main(e_input) != aes_cipher.decrypt_main(expect)

    def test_t04_pwd_key_01(self):
        aes_different_key = AESCipher(key='DIFFERENT_KEY_16')
        encrypted_text = 'MDAwMDAwMDAwMDAwMDQ4MkqaGa14xKLj3e72J+rDEd0='  # 'test' in aes_cipher
        diff_decrypted_text = ''
        try:
            diff_decrypted_text = aes_different_key.decrypt_main(encrypted_text)
        except UnicodeDecodeError:
            pass

        assert diff_decrypted_text != aes_cipher.decrypt_main(encrypted_text)

    # def test_t04_pwd_key_02(self):
