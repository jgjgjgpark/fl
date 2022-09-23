from feedernet_api import API

api = API()


class Feedernet:
    def __init__(self):
        self.login_status = False

    def create_project(self):
        self._check_login()

    def create_analysis(self):
        self._check_login()

    def query_cdms(self, project_id, analysis_id):
        self._check_login()
        map = api.API_LIST_CDM(project_id, analysis_id)
        return map['data']['list']

    def query_images(self):
        self._check_login()
        map = api.API_LIST_CONTAINER_IMAGES()
        return map['data']['images']

    def login(self, user_id, password):
        login_status = api.API_LOGIN(user_id, password)
        if login_status == 200:
            self.login_status = True
            print("login success")
        else:
            self.login_status = False
            print("login fail !!!")

    def _check_login(self):
        if not self.login:
            raise Exception("login required")


if __name__ == "__main__":
    project_id = 145
    analysis_id = 158
    user_id = "fnet05@fnet.or.kr"
    password = "123456"
    aa = Feedernet()
    aa.login(user_id, password)

