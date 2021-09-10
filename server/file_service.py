import os

from basiclib.common_util import CommonUtil


class FileService:


    # 创建用户的磁盘空间,并返回绝对路径
    @staticmethod
    def create_user_disk( user_name: str):
        base_dir = CommonUtil.get_base_disk_dir()
        user_disk_dir = base_dir + "\\" + user_name
        if not os.path.exists(user_disk_dir):
            os.mkdir(user_disk_dir)
        return user_disk_dir
