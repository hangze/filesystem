#

class FileInfo:
    file_name=""
    file_md5=""
    #文件大小，字节大小或KB,MB均可
    file_size=""
    #文件创建时间戳
    file_time_stamp=""

    def __init__(self,file_name:str,file_md5:str,file_size:int,file_time_stamp:int):
        self.file_name=file_name
        self.file_md5=file_md5
        self.file_size=file_size
        self.file_time_stamp=file_time_stamp
