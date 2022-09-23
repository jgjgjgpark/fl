import unittest
from src.app.python_execution import PythonExecution


class TestPythonExecution(unittest.TestCase):
    def setUp(self):
        analysis_id = 'analysis_id_1'
        requirement_file_path = ''
        run_script_path = ''
        self.execution = PythonExecution(analysis_id, requirement_file_path, run_script_path)

    def test_create(self):
        self.execution.create_virtual_environment()

    def test_delete(self):
        self.execution.delete_virtual_environment()

    def test_zip_file(self):
        zip_dir_name = 'sample_execution'
        file_name = 'zipfile'
        self.execution.zip_fl_execution(zip_dir_name, file_name)

    def test_run(self):
        interpreter = ''
        program = 'sample_execution/run.py'
        self.execution.run_program(interpreter, program)
