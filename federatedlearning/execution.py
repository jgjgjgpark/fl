import pykka
import aggregate_utils
from enum import Enum, auto


class ExecutionStatus(Enum):
    INITIALIZED = auto()
    EXECUTED = auto()
    PREPARING = auto()
    WAITING = auto()
    RUNNING = auto()
    SAVING = auto()
    COMPLETED = auto()
    DOWNLOADED = auto()
    SUCCEEDED = auto()
    FAILED = auto()


class Execution(pykka.ThreadingActor):
    def __init__(self, api, current_round, project_id, analysis_id, cdmId, research_file_location):
        super().__init__()
        self.api = api
        self.current_round = current_round
        self.project_id = project_id
        self.analysis_id = analysis_id
        self.cdmId = cdmId
        self.research_file_location = research_file_location
        self.status = ExecutionStatus.INITIALIZED

    def on_receive(self, message):
        if message == "execute":
            print(f'received execute message with cdm of id "{self.cdmId}"')
            self._execute()
        elif message == "status":
            return self._get_status()
        elif message == "download":
            self._download_result()

    def _execute(self):
        print(f"executing with cdm of id {self.cdmId}..\n")
        result = self.api.API_RUN(project_id=self.project_id, analysis_id=self.analysis_id, CDM_ID=self.cdmId)
        self.execution_id = result["data"]["execution"]["id"]
        self.status = ExecutionStatus.EXECUTED

    def _get_status(self):
        if not (self.status == ExecutionStatus.FAILED or self.status == ExecutionStatus.COMPLETED):
            response = self.api.API_RUN_STATUS(execution_id=self.execution_id, cdm_id=self.cdmId)
            self._set_status(response)
            if self.status == ExecutionStatus.COMPLETED:
                self._download_result()
        return self.status

    def _download_result(self):
        result_file_list = self.api.API_GET_RESULT_LIST(self.project_id, self.analysis_id, self.execution_id)
        for file in result_file_list["data"]["list"]:
            if file["resultFileType"] == 1:
                f = {"CDM_id": self.cdmId, "execution_id": file["executionId"], "file_id": file["id"]}
                self._download_file(f)

    def _download_file(self, file):
        zipFile = self.api.API_GET_RESULT_FILE(self.project_id, self.analysis_id,
                                               cdm_id=self.cdmId, execution_id=self.execution_id,
                                               file_id=file["file_id"], current_round=self.current_round, research_directory=self.research_file_location)
        aggregate_utils.move_unzip_file(zipFile[1], self.research_file_location)
        self.status = ExecutionStatus.SUCCEEDED

    def _set_status(self, response):
        status_code = response["data"]["execution"]["executionStatus"]
        if status_code == 9:
            self.status = ExecutionStatus.WAITING
        elif status_code == 11:
            self.status = ExecutionStatus.PREPARING
        elif status_code == 14:
            self.status = ExecutionStatus.RUNNING
        elif status_code == 15:
            self.status = ExecutionStatus.SAVING
        elif status_code == 20:
            self.status = ExecutionStatus.COMPLETED
        elif status_code == 21:
            self.status = ExecutionStatus.FAILED
