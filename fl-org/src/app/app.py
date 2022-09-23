from flask import Flask, request
from flask_restx import Api, Resource

from .execution_manager import AnalysisManager

app = Flask(__name__)
api = Api(app)


def create_app():
    return app


@api.route('/fl/status')
class Organization(Resource):
    def get(self):
        return {
            "status": "ok"
        }


def run_execution():
    '''
    # run with thread
    1. get zip file
    2. unzip zip file
    3. check zip file whether all the files are there
    if not, -->
    if ok, -->
    4. create dir
    5. install requirements.txt
    6. run
    7. if completed, upload local weight to s3 and notify
    8. if error occurred, notify server
    :return:
    '''
    # api = server_api.API()
    # api.prepare()
    # analysis_id, requirement_file_path, run_script_path = api.get_python_execution_info()
    # execution = PythonExecution(analysis_id, requirement_file_path, run_script_path)
    # execution.execute()
    pass


def run_execution1():
    pass


manager = AnalysisManager()


@api.route('/fl/analyses')
class AnalysisList(Resource):
    def post(self):
        presigned_url = request.json['presignedUrl']
        cdmGlobalId = request.json['cdmGlobalId']
        round = request.json['round']
        analysisId = request.json['analysisId']
        manager.execute(analysisId, presigned_url, cdmGlobalId, round)
        # task = threading.Thread(target=run_execution1)
        # task.start()
        return {
            'execution': 'accepted',
            'url': presigned_url
        }

    def get(self):
        return {
            'execution': 'accepted'
        }


@api.route('/fl/analyses/<string:id>')
class Analysis(Resource):
    def delete(self, id):
        '''
        stop thread and delete directory
        '''
        return '', 204


@api.route('/fl/cdms')
class CdmList(Resource):
    def post(self):
        request.json
        return '', 201
