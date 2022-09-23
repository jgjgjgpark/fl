import time

class AggregationServer:
    def __init__(self, api=DefaultApi()):
        self.test = "me"
        self.round = 0
        self.api = api

    def execute(self):
        print(self.test)

    def start(self):
        self.login()
        # print(self.api.organizations_get(async_req=False, _preload_content=False).data)
        while not self.learning_stop_condition():
            self.processRound()
            self.updateCondition()

    def load_global_weight(self):
        '''

        :return:
        '''
        pass

    def processRound(self):
        '''
        1. increase round
        2.
        :return:
        '''
        self._increaseRound()
        print(f"round {self.round} starts...")
        self._upload_analysis_zip_file()


    def login(self):
        pass

    def learning_stop_condition(self):
        return False

    def updateCondition(self):
        pass

    def _increaseRound(self):
        '''
        private method
        increase the number of round
        :return:
        '''
        self.round = self.round + 1

    def _upload_analysis_zip_file(self):
        '''
        call api to upload zip files
        :return:
        '''
        time.sleep(1)

    def create_initial_global_weight(self):
        '''
        not...

        :return:
        '''
        pass



if __name__ == "__main__":
    server = AggregationServer()
    server.start()
