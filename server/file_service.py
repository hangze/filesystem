import os

from basiclib.common_util import CommonUtil


def file_name_walk(user_disk_dir):
    file_dict=dict()
    for root, dirs, files in os.walk(user_disk_dir):
        print("root", root)  # 当前目录路径
        print("dirs", dirs)  # 当前路径下所有子目录
        print("files", files)  # 当前路径下所有非目录子文件
        if files:
            for file in files:
                file_dict[file]=root
    return file_dict


class FileService:

    # 创建用户的磁盘空间,并返回绝对路径
    @staticmethod
    def create_user_disk( user_name: str):
        base_dir = CommonUtil.get_base_disk_dir()
        user_disk_dir = base_dir + "\\" + user_name
        if not os.path.exists(user_disk_dir):
            os.mkdir(user_disk_dir)
        return user_disk_dir


    @staticmethod
    def ger_user_file_list(user_name):
        base_dir = CommonUtil.get_base_disk_dir()
        user_disk_dir = base_dir + "\\" + user_name
        return file_name_walk(user_disk_dir)




