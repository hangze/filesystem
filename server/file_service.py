import os

from basiclib.common_util import get_base_disk_dir


class FileService:

    #创建用户的磁盘空间,并返回绝对路径
    def create_user_disk(self,user_disk_name:str):
        base_dir=get_base_disk_dir()
        user_disk_dir=base_dir+"\\"+user_disk_name
        if os.dir
        os.mkdir()
        pass
