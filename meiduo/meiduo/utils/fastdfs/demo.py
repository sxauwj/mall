from fdfs_client.client import Fdfs_client

if __name__ == '__main__':
    # 根据配置文件，创建对象
    client = Fdfs_client('client.conf')
    # 调用方法，上传
    result = client.upload_by_filename('/home/python/Desktop/jp2.jpeg')

    print(result)
    # {'Remote file_id': 'group1/M00/00/02/wKgrKlwSHh-AU-igAABS0ZSky7I31.jpeg', 'Storage IP': '192.168.43.42',
    #  'Uploaded size': '20.00KB', 'Status': 'Upload successed.', 'Group name': 'group1',
    #  'Local file name': '/home/python/Desktop/jp2.jpeg'}