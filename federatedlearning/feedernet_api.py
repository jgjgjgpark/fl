import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


# import shutilpip

class API:
    # ID = "fltester@fnet.or.kr"
    # PW = "123456"
    URL_BASE = "https://qa-api.feedernet.kr/api"
    URL_LOGIN = URL_BASE + "/login"
    URL_CDM_LIST = URL_BASE + "/project/{}/analysis/{}/cdm"
    URL_IMG_LIST = URL_BASE + "/container-images"
    URL_UPLOAD = URL_BASE + "/project/{}/analysis/{}/researchFileForML?containerImage={}"
    URL_RUN = URL_BASE + "/project/{}/analysis/{}/execution?cdmId={}"
    URL_RUN_STATUS = URL_BASE + "/execution/{}"
    URL_GET_RESULT_LIST = URL_BASE + "/project/{}/analysis/{}/execution/{}/resultFile"
    URL_GET_RESULT_FILE = URL_BASE + "/project/{}/analysis/{}/execution/{}/resultFile/{}/export"

    RESEARCH_NAME = "M/L Tensorflow Analysis Test"
    DOWNLOAD_FILE_PATH = "{}/output/result_{}_{}_{}_{}_{}.zip"
    OUTPUT_FILE_PATH = "../data/results/result_{}_{}_{}_{}_{}.zip"

    LOGIN_COOKIES = None

    test_task_id = 1500
    test_cdm_id = [4, 6]
    test_execution_status = [9, 9, 11, 11, 14, 15, 20]

    def __int__(self):
        pass

    """       
    로그인
    :return: status_code
    """

    def API_LOGIN(self, ID, PW):
        data = {'email': ID, 'password': PW}
        res = requests.post(url=self.URL_LOGIN, data=data)
        self.LOGIN_COOKIES = res.cookies
        # print("API_LOGIN : ", self.LOGIN_COOKIES)
        return res.status_code

    """
    CDM 조회
    :parameter: project_id, analysis_id
    :return: status_code
    """

    def API_LIST_CDM(self, project_id, analysis_id):
        url = self.URL_CDM_LIST.format(project_id, analysis_id)
        res = requests.get(url, cookies=self.LOGIN_COOKIES)
        return res.json()

        """
        return 200
        """

    """
    이미지 조회
    :parameter: project_id, analysis_id
    :return: status_code
    """

    def API_LIST_CONTAINER_IMAGES(self):
        url = self.URL_IMG_LIST
        res = requests.get(url, cookies=self.LOGIN_COOKIES)
        return res.json()

    """
    업데이트
    :parameter: project_id, analysis_id
    :return: status_code
    """

    def API_UPLOAD(self, project_id, analysis_id, file_path, image):
        print("==============================")
        url = self.URL_UPLOAD.format(project_id, analysis_id, image)
        print("API_UPDATE URL : ", url)
        file = open(file_path, 'rb')
        mp_encoder = MultipartEncoder(
            fields={'researchFile': (file_path, file, 'application/zip')}
        )
        headers = {'Content-Type': mp_encoder.content_type}
        res = requests.post(url, data=mp_encoder, headers=headers, cookies=self.LOGIN_COOKIES)
        print("API_UPDATE : RESULT : ", res.json())
        return res.status_code

        """
        return 200
        """

    """
    연구 실행
    :parameter: project_id, analysis_id
    :     
    """

    def API_RUN(self, project_id, analysis_id, CDM_ID):
        print("==============================")
        url = self.URL_RUN.format(project_id, analysis_id, CDM_ID)
        body = {"name": self.RESEARCH_NAME,
                "rVersion": "custom",
                "researchType": 4}
        res = requests.post(url, data=body, cookies=self.LOGIN_COOKIES)
        print("API_RUN : RESULT : ", res.json())
        return res.json()

        """
        self.test_task_id += 1
        test_status_index = random.randrange(0, len(self.test_execution_status))
        test = {'data': {'execution':{'id': self.test_task_id,'analysisId': 86,'createdAt': '2021-07-28T07:40:11.000Z','executionStatus': self.test_execution_status[test_status_index],'executionStatusLast': None,'uidCreator': 23,'cdmId': CDM_ID,'token': 'b42bf99c45e240788fe0b12f70a5495119c8f2a778b145f39eec1a56c895','researchType': 4,'updatedAt': '2021-07-28T07:40:10.000Z','rVersion': 'custom','clientId': None,'containerId': None,'startedAt': None,'endedAt': None,'errorMessage': None,'resourceUsage': None,'numOutputFiles': 0,'name': 'M/L Tensorflow Analysis Test','engineVer': '0.2.1','atlasVersion': None}},'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjIzLCJscG0iOjE1OTg0ODU0MzQwNDMsInRzIjoxNjI3NDU4MDEwNDY2LCJpYXQiOjE2Mjc0NTgwMDl9.DnUjvCfqTzMoMBEOeUUKiiUn5NY5GRhT2V6Tlw1B_Ig'}
        return test
        """

    """
    !!! polling 기능 들어가야 함 
        
    연구 상태 확인
    :parameter: execution_id
    :result: executionStatus 
        # STATUS LIST
        # - Waiting : 9
        # - Preparing : 11
        # - Running : 14
        # - Saving : 15
        # - Finished : 20
        # - Failed : 21
    ex) execution_id : 1192
    """

    def API_RUN_STATUS(self, execution_id, cdm_id):
        print("==============================")
        url = self.URL_RUN_STATUS.format(execution_id)
        res = requests.get(url, cookies=self.LOGIN_COOKIES)
        print("API_RUN_STATUS : RESULT : ", res.json())
        return res.json()

        """
        test_status_index = random.randrange(0, len(self.test_execution_status))
        test = {'data': {
    'execution': {
      'id': execution_id,
      'analysisId': 86,
      'createdAt': '2021-07-28T07:40:11.000Z',
      'executionStatus': self.test_execution_status[test_status_index],
      'executionStatusLast': None,
      'uidCreator': 23,
      'cdmId': cdm_id,
      'token': 'b42bf99c45e240788fe0b12f70a5495119c8f2a778b145f39eec1a56c895',
      'researchType': 4,
      'updatedAt': '2021-07-28T07:40:10.000Z',
      'rVersion': 'custom',
      'clientId': None,
      'containerId': None,
      'startedAt': None,
      'endedAt': None,
      'errorMessage': None,
      'resourceUsage': None,
      'numOutputFiles': 0,
      'name': 'M/L Tensorflow Analysis Test',
      'engineVer': '0.2.1',
      'atlasVersion': None
    }
  },
  'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjIzLCJscG0iOjE1OTg0ODU0MzQwNDMsInRzIjoxNjI3NDU4MDEwNDY2LCJpYXQiOjE2Mjc0NTgwMDl9.DnUjvCfqTzMoMBEOeUUKiiUn5NY5GRhT2V6Tlw1B_Ig'
}
        return test
        """

    """
    연구 결과 파일 목록 및 ID
    :parameter: project_id, analysis_id, execution_id
    """

    def API_GET_RESULT_LIST(self, project_id, analysis_id, execution_id):
        print("==============================")
        url = self.URL_GET_RESULT_LIST.format(project_id, analysis_id, execution_id)
        print(url)
        res = requests.get(url, cookies=self.LOGIN_COOKIES)
        print("API_GET_RESULT_LIST : RESULT : ", res.json())
        return res.json()

        """
        return {
  'data': {
    'list': [
      {
        'id': 'f2354380-9741-46d9-8ac1-9dae9f50dc4c',
        'fileName': 'result.zip/data/results/log.txt',
        'mimeType': 'text/plain',
        'createdAt': '2021-07-28T05:50:34.000Z',
        'deletedAt': None,
        'sha1': 'a893555d6c4857f2bf15a2b0e38146f5e5c8b19f',
        'executionId': execution_id,
        'resultFileType': 2
      },
      {
        'id': '372bffb1-71c7-4e31-b567-175a2ff50ce8',
        'fileName': 'result.zip',
        'mimeType': 'application/zip',
        'createdAt': '2021-07-28T05:50:33.000Z',
        'deletedAt': None,
        'sha1': 'c4f7f9cc1fbe495970abca6747ada76620e61c90',
        'executionId': execution_id,
        'resultFileType': 1
      },
      {
        'id': '3de60195-9771-436d-b234-ee1276a68287',
        'fileName': 'result.zip/data/results/record.txt',
        'mimeType': 'text/plain',
        'createdAt': '2021-07-28T05:50:33.000Z',
        'deletedAt': None,
        'sha1': 'bce862043e401fafc42cae2843ab7bad6997585b',
        'executionId': execution_id,
        'resultFileType': 2
      }
    ],
    'page': 1,
    'pageSize': 30,
    'totalCount': 3
  },
  'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjIzLCJscG0iOjE1OTg0ODU0MzQwNDMsInRzIjoxNjI3NDU4MzcxNDQxLCJpYXQiOjE2Mjc0NTgzNzB9.zi0uqmThijhIo9GNZRNOBpb5lX-WKJngLAuPKUkPFJo'
}
        """

    """
    연구 결과 다운로드 
    :parameter: project_id, analysis_id, execution_id, file_id
    """

    def API_GET_RESULT_FILE(self, project_id, analysis_id, cdm_id, execution_id, file_id,
                            current_round, research_directory):
        print("==============================")
        result_file_path = self.DOWNLOAD_FILE_PATH.format(research_directory, project_id, analysis_id, cdm_id,
                                                          execution_id, current_round)
        print(f"result_file_path: {result_file_path}")

        url = self.URL_GET_RESULT_FILE.format(project_id, analysis_id, execution_id, file_id)
        res = requests.get(url, cookies=self.LOGIN_COOKIES)

        open(result_file_path, 'wb').write(res.content)

        return res.status_code, result_file_path