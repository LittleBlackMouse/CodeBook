import json
import os.path
import uuid

import rsa
import base64


# 加密
def encryption(path, file, text, uuid, typ):
    pubkey, prikey = rsa.newkeys(256)  # 将字符串转换成公钥和秘钥
    puk = pubkey.save_pkcs1().decode('utf-8')  # 公钥
    prk = prikey.save_pkcs1().decode('utf-8')  # 秘钥
    # 使用PKCS加密给定的消息,返回类型bytes
    crypto = rsa.encrypt(text.encode('utf-8'), pub_key=pubkey)
    # 对于保存，网络传输，打印不乱码，需要通base64编码进行转换
    # base64编解码能把一些无法直接用文件本信息编码的二进制数据，转换成常规的二进制数据。
    crypto_msg = base64.b64encode(crypto).decode('utf-8')  # 加密后的文本信息msg
    msg = 'save success!'
    if os.path.isfile(path + file):  # 判断文件是否存在
        with open(path + file, 'r') as f:  # 读取本地文件
            file_dict = json.load(f)
        new_dict = {'id': uuid, 'typ': typ, 'puk': puk, 'prk': prk, 'crypMsg': crypto_msg}
        file_dict['charStr'].append(new_dict)  # 字典更新
        with open(path + file, 'w') as f:
            f.write(json.dumps(file_dict))
        return msg
    else:
        file_dict = {'charStr': [{'id': uuid, 'typ': typ, 'puk': puk, 'prk': prk, 'crypMsg': crypto_msg}]}
        with open(path + file, 'w+') as f:
            f.write(json.dumps(file_dict))
        return msg


if __name__ == '__main__':
    path = './'
    text = '456'
    id = uuid.uuid1()
    encryption(path, str(id), 'parent')
