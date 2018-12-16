import pickle
import base64


def dumps(data):
    # 1 将字典转字节
    data_to_bytes = pickle.dumps(data)
    # 2 加密字节
    bytes_to_encode = base64.b64encode(data_to_bytes)

    # 3 转字符串
    json_str = bytes_to_encode.decode()
    return json_str


def loads(str):
    # 1　转字节
    json_64 = str.encode()
    # 2.解密
    json_bytes = base64.b64decode(json_64)
    # 3.转字典
    json_dict = pickle.loads(json_bytes)
    return json_dict


if __name__ == '__main__':
    dict = {'1': {'count': 10, 'selected': True}, '2': {'count': 20, 'selected': False}}

    print(dumps(dict))
