class API:
    def __init__(self):
        pass

    def prepare(self):
        '''

        :return:
        '''
        self.get_file('presigned_url')
        self.create_dir()
        self.unzip()

    def get_python_execution_info(self):
        '''

        :return: python path
        '''
        return ('requirements.txt path', 'script file')

    def get_file(self, presigned_url):
        '''
        get zip from presigned url
        :param presigned_url:
        :return:
        '''

    def create_dir(self):
        pass

    def unzip(self):
        pass











