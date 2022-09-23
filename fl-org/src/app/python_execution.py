import subprocess
import shutil
import os
import venv
import requests
from .common import util
from pathlib import Path


class PythonExecution:

    def __init__(self, analysis_id, presigned_url, cdmGlobalID, round, workspace_path):
        self.analysis_id = analysis_id
        # self.working_dir = os.path.expanduser(f'{PythonExecution.base_path}/{self.analysis_id}')
        self.presigned_url = presigned_url
        self.cdmGlobalID = cdmGlobalID
        self.round = round
        self.workspace = Path(workspace_path)
        self.analysis_dir = self.workspace / self.analysis_id
        # self.requirement_file_path = requirement_file_path
        # self.run_script_path = run_script_path

    def execute(self):
        self._download()
        self._unzip()
        self._create_virtual_environment()
        self._pip_install()
        self._run()

    def _download(self):
        response = requests.get(self.presigned_url)
        file_name = self.workspace / f"{self.analysis_id}.zip"
        open(file_name, "wb").write(response.content)
        #util.unzip_fl_execution(file_name, self.analysis_dir)

    def _unzip(self):
        file_name = self.workspace / f"{self.analysis_id}.zip"
        shutil.unpack_archive(file_name, self.analysis_dir)

    def _create_virtual_environment(self):
        venv.create(self.analysis_dir, system_site_packages=True, with_pip=True)

    def _pip_install(self):
        install_command = [f'./workspace/{self.analysis_id}/bin/pip', 'install', '-r', f'./workspace/{self.analysis_id}/requirements.txt']
        process = subprocess.Popen(install_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        print(stdout)

    def _run(self):
        process = subprocess.Popen(['env', "DB_USER=jgjgpark", f"./workspace/{self.analysis_id}/bin/python", "run.py"], stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        print(stdout)

    def create_virtual_environment(self):
        '''
        1. create directory
        2. create virtual environment in the created directory
        3. install requirements.txt in virtual environment
        4. run "execution" with the created python interpreter
        :return:
        '''
        print(f'create dir {self.working_dir}')
        os.makedirs(self.working_dir)
        # venv.create(self.working_dir)

    def delete_virtual_environment(self):
        os.removedirs(self.working_dir)

    def destroy_virtual_environment(self):
        shutil.rmtree(self.working_dir)

    def activate_virtual_environment(self):
        pass

    def install_requirements(self):
        pass

    def run_program(self, interpreter, program):
        subprocess.run(['python', program])
