import os
import shutil
import unittest
import sys
from pathlib import Path

from src.app.common import util
from pathlib import Path

class TestUtil(unittest.TestCase):
    def test(self):
        print(sys.path)
        assert "tests" == util.print_util()

    def test_zip(self):
        analysisId = 'zipfile'
        workspace = Path('./workspace')
        dir_to_zip = workspace / analysisId
        file_name = workspace / analysisId #Path('./workspace/zipfile')
        where = './workspace'
        # util.zip_fl_execution(file_name, file_name, 'test_dir', where)
        shutil.make_archive(file_name, 'zip', '.', './test_dir')

    def test_unzip(self):
        file_name = Path('./workspace/zipfile.zip')
        shutil.unpack_archive(file_name, './workspace')

    def test_clean(self):
        file_name = Path('./workspace/test_dir')
        shutil.rmtree(file_name)
        os.remove(Path('./workspace/zipfile.zip'))


    @staticmethod
    def clear_created_files(file_name):
        '''
        clear zip file and unzipped dir
        :param filename:
        :return:
        '''
        shutil.rmtree(file_name)
        os.remove(Path(file_name + '.zip'))
