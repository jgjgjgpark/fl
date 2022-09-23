import zipfile
import shutil
import os
from pathlib import Path


def zip_fl_execution(dir_to_zip, zip_file_name, base_dir, where):
    '''

    :param zip_dir_name: Path type
    :param zip_file_name: str type
    :return:
    '''
    if not os.path.isdir(dir_to_zip):
        raise Exception("not a directory")
    shutil.make_archive(zip_file_name, 'zip', base_dir, 'test')
    #shutil.move(zip_file_name + '.zip', where)


def unzip_fl_execution(zip_file_name, to):
    '''
    unzip zipfile in the directory named zipfile
    :param zip_file_name: name of zip file
    :return:
    '''
    shutil.unpack_archive(zip_file_name, to, 'zip')


def print_util():
    return "tests"
