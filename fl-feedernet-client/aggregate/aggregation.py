import argparse
from collections import deque

import json
import numpy as np

import aggregate_utils
from config import Config
from feedernet_api import API
import threading
import queue
import glob


script_step = 0

api = API()
config = Config()

global_weight = None
delay_time = 20

# CDM 대상 연구 실행 결과 dict list
#run_result_dict = []

# 연구 상태 확인 dict list
#result_info_dict = []

# 작업 큐
task_queue = queue.Queue()

def login():
    print("==========> login")
    """
        login using by id & pw

    :return:
        True or False
    """
    login_status = api.API_LOGIN(config.value["user_id"], config.value["user_pw"])
    if login_status == 200:
        print("> login success")
        return True
    else:
        print("> login fail !!!")
        return False

def get_images():
    images = api.API_LIST_CONTAINER_IMAGES()
    
    return images


def get_cdms():
    cdms = api.API_LIST_CDM(project_id=config.value["project_id"], analysis_id=config.value["analysis_id"])
    return cdms


def load_global_weight():
    print("==========> load_global_weight")
    """
        global weight json file load from local storage

    :return:
    """
    file_name = "global_weight_{}.json".format(config.value["current_round"])
    global global_weight
    global_weight = aggregate_utils.read_weight_from_json(file_name)

    if len(global_weight) == 0:
        print("> global weight None")
        pass

    print("global weight len : ", len(global_weight))


def upload_analysis_file():
    print("==========> upload_analysis_file")
    '''
        script 파일 업로드
        zip 파일 생성
       
        !!! current_round : 0 일때만 script 업로드 ???

    :return: None
    '''
    zip_file_path = aggregate_utils.make_zip_file(config.value["current_round"])
    # path = "../script/{}".format(zip_file_path)
    path = "{}".format(zip_file_path)

    print("upload_analysis_file : ", zip_file_path, " ::: ", path)
    upload_result = api.API_UPLOAD(project_id=config.value["project_id"], analysis_id=config.value["analysis_id"],
                                   file_path=path)
    print("upload_analysis_file : ", upload_result)


def run_script():
    print("==========> run_script")
    '''
        분석 실행

    :parameter: project_id, analysis_id, CDM_ID
    :return: True or False
    '''
    cdm_execution_list = config.value["CDM_execution_list"]
    execution_list = cdm_execution_list

    for key in execution_list:
        run_result = api.API_RUN(project_id=config.value["project_id"], analysis_id=config.value["analysis_id"],
                                 CDM_ID=key)
        print("API RUN RESULT : " , run_result)
        task_id = run_result["data"]["execution"]["id"]
        execution_status = run_result["data"]["execution"]["executionStatus"]

        '''
            config 파일에 task 목록 업데이트 
        '''
        cdm_execution_list[key][task_id] = execution_status
        item = {"CDM_id" : key, "task_id": task_id, "executionStatus": execution_status}
        #cdm_execution_list[key].append(item)
        config.update("CDM_execution_list", cdm_execution_list)

        task_queue.put(item)


def check_run_status():
    print("==========> check run status")
    '''
        상태를 주기적으로 체크         

    :return:
    '''

    queue_size = task_queue.qsize()

    for _ in range(queue_size):
        '''
            item :
                
       '''
        item = task_queue.get()


        run_status = api.API_RUN_STATUS(execution_id=item["task_id"], cdm_id=item["CDM_id"])
        result = run_status["data"]
        result_status = result["execution"]["executionStatus"]
        item.update({"executionStatus": result_status})
        print("check_run_status : current > ", item)

        cdm_execution_list = config.value["CDM_execution_list"]
        cdm_execution_list[item["CDM_id"]][item["task_id"]] = result_status
        config.update("CDM_execution_list", cdm_execution_list)

        if not (result_status == 21 or result_status == 20):
            '''
                Waiting / Preparing / Running / Saving
            '''
            print("result status : ", aggregate_utils.get_status(result_status))
            task_queue.put(item)

        else:
            '''
                Finished : 20 / Failed : 21
            '''
            print("check_run_status : ", item["task_id"], " > ", aggregate_utils.get_status(result_status))
            get_result_file_list(item)

    if task_queue.qsize() > 0:
        threading.Timer(delay_time, check_run_status).start()
    else:
        process_finish_check()


def get_result_file_list(item):
    print("==========> get result file list")
    '''
        결과 파일 목록 확인
        
    :return:
    '''

    #item = {"CDM_id": key, "task_id": task_id, "executionStatus": execution_status}

    result_file_list = api.API_GET_RESULT_LIST(config.value["project_id"], config.value["analysis_id"], item["task_id"])

    for file in result_file_list["data"]["list"]:
        if file["resultFileType"] == 1:
            f = {"CDM_id": item["CDM_id"], "execution_id": file["executionId"], "file_id": file["id"]}
            result_file_download(f)


def result_file_download(file):
    print("==========> result file download")
    '''

    :return:
    '''
    get_result_file = api.API_GET_RESULT_FILE(config.value["project_id"], config.value["analysis_id"],
                                              cdm_id=file["CDM_id"], execution_id=file["execution_id"],
                                              file_id=file["file_id"], current_round=config.value["current_round"])

    print("result_file_download : ", get_result_file, " ::: ", file["CDM_id"], " > ", file["execution_id"], " : ", file["file_id"])

    unzip(get_result_file[1])


def process_finish_check():
    print("==========> process_finish_check")
    """
        FL process end status check
        global weight 업데이트 여기서 하도록 함

    :return:
    """

    if config.value["current_round"] == config.value["max_round"]:
        print("End FL process")
    else:
        print("Next FL round : ", config.value["current_round"], " >>> ", config.value["current_round"] + 1)
        update_global_weight()
        config.update("current_round", config.value["current_round"] + 1)
        threading.Timer(delay_time, process).start()

    print("process_finish_check : END")

    return 0

def update_global_weight():
    print("==========> update_global_weight")
    """
        1번의 round 수행 후 global weight 를 업데이트 함

    """
    current_round = config.value["current_round"]
    weight_folder_path = "../download/{}/*.json".format(current_round)
    weight_file_list = glob.glob(weight_folder_path)
    print("weight_file_list : ", weight_file_list)
    updated_global_weight = fed_avg(weight_file_list)

    '''
        !!! global_weight to file
        라운드 별 global weight 저장 및, 서버에 전송하기 위해 json 파일 업데이트 
        filename : global_weight_{}.json 참고 
    '''

    aggregate_utils.save_global_weight_to_json(current_round+1, updated_global_weight)


def unzip(zip_path):
    """
        압축 품

        파일 다운로드 완료
        해당 파일을 round 별 폴더로 이동
        폴더에서 압축 해제

    :return:
    """
    aggregate_utils.move_unzip_file(zip_path)


def fed_avg(weight_file_list):
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
        #print("local weight : ", len(local_weight), type(local_weight), type(local_weight[0]))

        local_weight_list.append(local_weight)

    updated_global_weight = np.average(local_weight_list, axis=0)
    #print("weight average : ", len(updated_global_weight), type(updated_global_weight))
    print("> weight average !!!")

    return updated_global_weight


def process():
    print("==========> process")
    '''
        FL PROCESS

    :return:
    '''
    # aggregation에 저장되어 있는 global weight를 로드함
    load_global_weight()

    # global weight & script 파일 업로드
    upload_analysis_file()

    # 업로드한 script 실행
    run_script()

    # script 실행 상태 체크
    check_run_status()


def temp():
    """
    run_status = api.API_RUN_STATUS(execution_id=1356)
    print(run_status)
    result_file_list = api.API_GET_RESULT_LIST(config.value["project_id"], config.value["analysis_id"], 1356)
    print(result_file_list)
    file = api.API_GET_RESULT_FILE(config.value["project_id"], config.value["analysis_id"],
                            cdm_id=6, execution_id=1356,
                            file_id="372bffb1-71c7-4e31-b567-175a2ff50ce8")
    print(file)
    """
    update_global_weight()


    '''
    temp_list = []

    a1 = np.array([1, 3, 5, 7])
    a2 = np.array([9, 11, 0, 15, 17, 19])
    a3 = np.array([21, 23, 25])

    a = np.array((a1, a2, a3))


    b1 = np.array([2, 4, 6, 8])
    b2 = np.array([10, 12, 14, 16, 18, 20])
    b3 = np.array([22, 0, 26])
    b = np.array((b1, b2, b3))


    temp_list.append(a)
    temp_list.append(b)

    print("a: ", len(a), type(a), a.shape, a[0].shape)
    print("b: ", len(b), type(b), b.shape)
    print("temp_list: " , len(temp_list), type(temp_list), type(temp_list[0]))

    result = np.average(temp_list, axis=0)
    print("result : " , result)
    '''


if __name__ == "__main__":
    np.random.seed(19)

    parameter = argparse.ArgumentParser()
    parameter.add_argument("--step",
                           default= 0,
                           help='FL process step, 0 : default | 1 : upload_analysis_file')

    args = parameter.parse_args()
    script_step = args.step
    print("script_step: ", script_step)

    # load config file
    # config.update("current_round", 0)

    # 피더넷 로그인
    login()

    """
    if script_step == 1:
        # 분석하기 위한 스크립트 파일을 업로드
        upload_analysis_file()

        # 스크립트 파일 실행 호출
        run_script()

    # 실행한 스크립트 파일의 현재 상태 확인
    check_run_status()
    """

    process()
    #temp()

