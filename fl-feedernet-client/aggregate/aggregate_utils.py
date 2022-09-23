import json
import os
import shutil

import numpy as np
from zipfile import ZipFile

from json import JSONDecodeError

import zipfile

def save_global_weight_to_json(next_round = 0, global_weight=[]):
    print("save_global_weight_to_json")
    global_weight_file_path = "../script/global_weight_{}.json".format(next_round)
    with open(global_weight_file_path, "w") as json_file:
        to_json = json.dumps(global_weight, cls=NumpyEncoder)
        json.dump(to_json, json_file)

    print("global weight file update success")


def read_weight_from_json(path=None):
    global_weight = []
    '''
        실행 시 type 체크 필요
    '''
    try:
        with open(path, "r") as weight_json:
            body = json.load(weight_json)  # type(body): str
    except FileNotFoundError:
        return global_weight

    body_to_list = json.loads(body)  # type(body_to_list): list
    print("read_weight_from_json: len: ", len(body_to_list), type(body_to_list))

    '''
        layer의 weight -> bias -> weight -> bias -> ... 순서
    '''
    for i in range(len(body_to_list)):
        temp = np.array(body_to_list[i], dtype=np.float32)
        print(temp.shape, type(temp))
        global_weight.append(temp)

    #global_weight = np.array(global_weight)

    return global_weight

def make_zip_file(current_round = 0):
    print("make_zip_file : ", os.getcwd())
    file_name = "run_{}.zip".format(current_round)

    try:
        shutil.copy("global_weight_{}.json".format(current_round), "global_weight.json")
    except FileNotFoundError as err:
        '''
            global_weight_[round].json 파일이 없는 경우
        '''
        print("make_zip_file : global_weight.json : ", err)
    except JSONDecodeError as err:
        '''
            global_weight_[round].json 파일 내용을 읽을 수 없는 경우
        '''
        print("make_zip_file : JSONDecodeError : ", err)

    '''
        global_weight 파일 여부 확인하여 zip 파일 목록에 추가 
    '''
    file_list = ["run.py", "utils.py"]
    if os.path.isfile("global_weight.json"):
        file_list.append("global_weight.json")

    '''
        :parameter: compression check  
        https://kibua20.tistory.com/163
    '''
    with ZipFile(file_name, "w", compression=zipfile.ZIP_DEFLATED) as zipObj:
        for f in file_list:
            zipObj.write(f)

    return file_name

def move_unzip_file(src):
    """
        추가 확인 및 최적화 필요

    :param src:
    :return:
    """

    split_path = src.split("_")
    cdm_id = split_path[3]
    execution_id = split_path[4]
    round_number = split_path[5].split(".")[0]

    dst = src.replace("result", f"{round_number}/result")
    print("child path : ", dst)

    directory = os.path.dirname(dst)
    if not os.path.exists(directory):
        os.makedirs(directory)

    shutil.move(src, dst)


    weight_file_name = directory+"/local_weight_{}.json".format(execution_id)
    weight_file_name = weight_file_name.replace("../", "")
    print("directory : ", directory, " : ", weight_file_name)

    weight_folder_dir = "../download/{}".format(str(round_number))

    zipdata = zipfile.ZipFile(dst)
    zipinfos = zipdata.infolist()

    for zi in zipinfos:
        if zi.filename.endswith(".json"):
            zi.filename = "local_weight_{}.json".format(execution_id)
            print(">>> : ", zi.filename)
            zipdata.extract(zi, weight_folder_dir)







def get_status(status_code):
    """
        status code를 텍스트로 변환
        Waiting : 9
        Preparing : 11
        Running : 14
        Saving : 15
        Finished : 20
        Failed : 21

    :param status_code:
    :return:
    """

    return {9: "Waiting", 11: "Preparing", 14: "Running", 15: "Saving", 20: "Finished", 21: "Failed"}\
        .get(status_code, "")


class FileWriter:
    '''
        파일 처리 경로 설정 ...
    '''
    def __enter__(self):
        os.chdir("/data/results/")
        print("current pwd: ", os.getcwd())
        return self

    def writer_body(self, file_name, body):
        with open(file_name, 'w') as f:
            f.write(body)
            print("file write success!!!")

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir("/script")
        print("current pwd: ", os.getcwd())

class NumpyEncoder(json.JSONEncoder):
    '''
         통신에 필요한 serialize 과정 진행 (ndarray -> list)
     '''
    def default(self, o):
        if isinstance(o, np.ndarray):
            return o.tolist()
        return json.JSONEncoder.default(self, o)

