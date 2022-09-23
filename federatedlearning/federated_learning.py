from execution import Execution
import aggregate_utils
from feedernet_api import API
import time
from execution import ExecutionStatus
import numpy as np
import glob
import shutil
import os


class FederatedLearning:
    def __init__(self, project_id, analysis_id, cdms, max_round, image, research_file_location):
        self.max_round = max_round
        self.project_id = project_id
        self.analysis_id = analysis_id
        self.cdms = cdms
        self.round_executions = []
        self.api = API()
        self.login_status = False
        self.image = image
        self.research_file_location = research_file_location
        # self.func = func  # define stop state
        self.state = {
            "round": 0,
            "metric": {
                "accuracy": 0
            }
        }

    def get_round(self):
        return self.current_round

    def login(self, user_id, password):
        response_status = self.api.API_LOGIN(user_id, password)
        if response_status == 200:
            self.login_status = True
            print("login successful")
        else:
            print("login fail")

    def execute(self):
        self.execute_round_from(0)

    def resume(self, round_to_resume):
        self.execute_round_from(round_to_resume)

    def execute_round_from(self, round_to_resume):
        '''
        start fl from round x
        :return:
        '''
        for current_round in range(round_to_resume, self.max_round):
            if current_round == 0:
                self.prepare()
            print(f"starts round {current_round} \n")
            execution = RoundExecution(self, self.image, current_round, self.research_file_location)
            self.round_executions.append(execution)
            if not execution.execute():
                print(f"Failed in {current_round}")
                break
        self.finalize()

    def prepare(self):
        self._check_if_dir_exists_and_delete_and_create(f"temp")
        self._check_if_dir_exists_and_delete_and_create(f"{self.research_file_location}/output")

    def _check_if_dir_exists_and_delete_and_create(self, path):
        if os.path.exists(path):
            shutil.rmtree(path)
        os.mkdir(path)

    def finalize(self):
        shutil.rmtree('temp')


    def stop_condition_is_met(self):
        '''

        :return: Boolean
        '''
        return self.func(self.state)

    def get_cdms(self):
        return self.cdms

    def get_status(self):
        self._check_login()
        status = []
        for exec in self.round_executions:
            status.append(exec.get_status())
        return status

    def _check_login(self):
        if not self.login_status:
            raise Exception("login required")


class RoundExecutionStatus:
    def __init__(self, cdms):
        self._initialize_status(cdms)
        self.success = False
        self.finished = False

    def _initialize_status(self, cdms):
        self.status = {}
        for cdm in cdms:
            self.status[cdm] = {
                "status": ExecutionStatus.INITIALIZED,
                "finished": False,
                "succeeded": False
            }

    def is_success(self):
        for key in self.status:
            if self.status[key]["status"] != ExecutionStatus.SUCCEEDED:
                return False
        return True

    def organization_learning_is_finished(self):
        for key in self.status:
            if not (self.status[key]["status"] == ExecutionStatus.SUCCEEDED
                    or self.status[key]["status"] == ExecutionStatus.FAILED):
                return False
        return True

    def set_status(self, cdmId, status):
        self.status[cdmId] = {
            "status": status,
            "finished": status == ExecutionStatus.FAILED or status == ExecutionStatus.SUCCEEDED,
            "succeeded": status == ExecutionStatus.SUCCEEDED
        }

    def is_finished(self, cdmId):
        return self.status[cdmId]["finished"]


class RoundExecution:
    def __init__(self, fl, image, current_round, research_file_location):
        self.fl = fl
        self.image = image
        self.project_id = fl.project_id
        self.analysis_id = fl.analysis_id
        self.current_round = current_round
        self.research_file_location = research_file_location
        self.cdm_execution_map = {}
        self.status = RoundExecutionStatus(fl.get_cdms())

    def _load_global_weight(self):
        file_name = f"{self.research_file_location}/global_weight_{self.current_round}.json"
        print(f"####################{file_name}")
        global global_weight
        global_weight = aggregate_utils.read_weight_from_json(file_name)

    def _print_message_of_round(self, message):
        print(f"""
        ###################  Round {self.current_round} {message}   ###########################
        """)

    def execute(self):
        success = True
        self._print_message_of_round("Starts ...")
        self._load_global_weight()
        self._upload_analysis_file()
        for cdmId in self.fl.get_cdms():
            execution = Execution.start(self.fl.api, self.current_round, self.project_id, self.analysis_id, cdmId, self.research_file_location)
            self.cdm_execution_map[cdmId] = execution
            execution.tell("execute")
        self._update_status()
        if self.status.is_success():
            self._update_global_weight()
        else:
            print("Failed..")
            success = False
        for cdmId in self.fl.get_cdms():
            self.cdm_execution_map[cdmId].stop()
        self._print_message_of_round("Ends ...")
        return success

    def _update_status(self):
        while not self.status.organization_learning_is_finished():
            for cdmId in self.cdm_execution_map:
                if not (self.status.is_finished(cdmId)):
                    status = self.cdm_execution_map[cdmId].ask("status")
                    self.status.set_status(cdmId, status)
                    print(f"status: {status}")
            time.sleep(10)

    def _download_result(self):
        for key in self.cdm_execution_map:
            self.cdm_execution_map[key].tell("download")
        while not (self.status == ExecutionStatus.SUCCEEDED or self.status == ExecutionStatus.FAILED):
            for key in self.cdm_execution_map:
                status = self.cdm_execution_map[key].ask("status")
                self.status.set_status(key, status)
                print(f"status: {status}")

    def get_status(self):
        return self.status

    def _upload_analysis_file(self):
        zip_file_path = aggregate_utils.make_zip_file(self.current_round, self.research_file_location)
        path = "{}".format(zip_file_path)

        print("upload_analysis_file : ", zip_file_path, " ::: ", path)
        upload_result = self.fl.api.API_UPLOAD(project_id=self.project_id, analysis_id=self.analysis_id, file_path=path, image=self.image)

    def _update_global_weight(self):
        weight_folder_path = f"{self.research_file_location}/output/{self.current_round}/*.json"
        print(f"weight_folder_path=={weight_folder_path}")
        weight_file_list = glob.glob(weight_folder_path)
        print("weight_file_list : ", weight_file_list)
        updated_global_weight = self._fed_avg(weight_file_list)
        aggregate_utils.save_global_weight_to_json(self.research_file_location, self.current_round + 1, updated_global_weight)

    def _fed_avg(self, weight_file_list):
        print("==========> fed_avg")
        """
            평균화 계산
            global weight 업데이트
        :return:
        """
        # file open
        local_weight_list = []

        print("weight file list : ", weight_file_list)

        for f in weight_file_list:
            local_weight = aggregate_utils.read_weight_from_json(f)
            # print("local weight : ", len(local_weight), type(local_weight), type(local_weight[0]))
            local_weight_list.append(local_weight)

        updated_global_weight = np.average(local_weight_list, axis=0)
        # print("weight average : ", len(updated_global_weight), type(updated_global_weight))
        print("> weight average !!!")

        return updated_global_weight


if __name__ == "__main__":
    project_id = 145
    analysis_id = 158
    user_id = "fnet05@fnet.or.kr"
    password = "123456"
    image = 'docker.evidnet.co.kr/base-images/evidnet/tensorflow:latest'
    fl = FederatedLearning(project_id, analysis_id, [13, 22], 3, image, 'research_no1')
    fl.login(user_id, password)
    fl.execute()