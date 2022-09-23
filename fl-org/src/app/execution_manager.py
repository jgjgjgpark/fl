import threading
import requests
import venv
from .common import util
from .python_execution import PythonExecution
import os


class DbConnectionInfo:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            print(f"{key} : {value}")
            setattr(self, key, value)


class AnalysisManager:
    BASE_DIR = 'workspace'

    def __init__(self):
        self._create_workspace()
        self.executions = {}
        self.db = {
            "1": DbConnectionInfo(DB_USER='jgjgpark')
        }

    def create_execution(self):
        pass

    def delete(self, id):
        '''

        :param id:
        :return:
        '''

    def execute(self, analysisId, presigned_url, cdmGlobalId, round):
        task = threading.Thread(target=self.run, args=(analysisId, presigned_url, cdmGlobalId, round))
        task.start()
        self.executions[analysisId] = task

    def run(self, analysisId, presigned_url, cdmGlobalId, round):
        execution = PythonExecution(analysisId, presigned_url, cdmGlobalId, round, './workspace')
        execution.execute()

    def _create_virtual_environment(self, working_dir):
        venv.create(working_dir)

    def _create_workspace(self):
        os.makedirs(AnalysisManager.BASE_DIR, exist_ok=True)
