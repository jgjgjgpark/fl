import json
import os

import numpy as np
from zipfile import ZipFile

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
    #print("read_weight_from_json: len: ", len(body_to_list), type(body_to_list))

    '''
        layer의 weight -> bias -> weight -> bias -> ... 순서
    '''
    for i in range(len(body_to_list)):
        temp = np.array(body_to_list[i], dtype=np.float32)
        global_weight.append(temp)

    return global_weight

class FileWriter:
    '''
        파일 처리 경로 설정 ...
    '''
    def __enter__(self):
        os.chdir("/data/results/")
        #print("current pwd: ", os.getcwd())
        return self

    def writer_body(self, file_name, body):
        with open(file_name, 'w') as f:
            f.write(body)
            #print("file write success!!!")

    def write_json(self, file_name, json_body):
        with open(file_name, 'w') as f:
            weight_to_json = json.dumps(json_body, cls = NumpyEncoder)
            json.dump(weight_to_json, f)

    def save_csv(self, file_name, data):
        data.to_csv(file_name, index=False, header=False, float_format="%.3f")

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir("/script")
        #print("current pwd: ", os.getcwd())

class NumpyEncoder(json.JSONEncoder):
    '''
         통신에 필요한 serialize 과정 진행 (ndarray -> list)
     '''
    def default(self, o):
        if isinstance(o, np.ndarray):
            return o.tolist()
        return json.JSONEncoder.default(self, o)

