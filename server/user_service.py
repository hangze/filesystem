class UserService:
    #保持已登录的token，现实中一般还会做刷新和过期操作
    token_set=set()

    #登录后添加token
    def add_token(self,token:str):
        if token not in self.token_set:
            self.token_set.add(token)

    #判断token是否仍处于有效状态
    def is_login(self,token:str):
        if token in self.token_set:
            return True
        return False

