from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client
from django.conf import settings


class FdfsStorage(Storage):
    def open(self, name, mode='rb'):
        # 打开文件，文件读取在fastdfs中不需要本地读取，通过url读取
        pass

    def save(self, name, content, max_length=None):
        # content表示客户端上传的文件对象

        # 创建对象
        client = Fdfs_client(settings.FDFS_CLIENT)
        # 上传，读取请求报文中的文件数据
        result = client.upload_by_buffer(content.read())
        # 返回文件名
        return result['Remote file_id']

    def exists(self, name):
        # 文件不存再本地，直接返回false
        return False

    def url(self, name):
        # 通过nginx访问，返回访问的域名及地址
        return settings.FDFS_URL + name
