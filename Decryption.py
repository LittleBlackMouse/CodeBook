import json

import rsa
import base64


# 解密

def decrypt(path, file, id, typ):
    # 读取本地加密文件
    with open(path + file, 'r') as f:
        f = json.load(f)
        for msg in f['charStr']:
            if msg['id'] == id and msg['typ'] == typ:
                prikey = rsa.PrivateKey.load_pkcs1(msg['prk'])  # pem格式加载私钥
                crypto_msg = base64.b64decode(msg['crypMsg'])  # base64解码
                decrypto_msg = rsa.decrypt(crypto_msg, prikey)  # 私钥解密
                decrypto_msg = decrypto_msg.decode('utf-8')  # utf8解码
    return decrypto_msg


if __name__ == '__main__':
    path = './'
    id = 'f7f80d00-f1ff-11ed-9aea-d8bbc1a44ec9'
    typ = 'parent'
    decrypto_msg = decrypt(path, id, typ)
    print(decrypto_msg)