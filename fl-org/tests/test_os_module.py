import os
import subprocess
import venv


def test_os_command():
    result = os.system('ls')
    print(result)


def test_venv():
    version_command = ['python', '-V']
    process = subprocess.Popen(version_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    print(stdout)


def test_venv1():
    version_command = ['python', '-m', 'venv', 'input']
    process = subprocess.Popen(version_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    print(stdout)


def test_venv_programmatically():
    venv.create("workspace/1fb906bc-f6f5-431c-8add-4458447716e0", system_site_packages=True, with_pip=True)


def test_venv_programmatically1():
    pass
    # venv.main("input")


def test_pip():
    install_command = ['./input/bin/pip', 'install', '-r', './input/requirements.txt']
    process = subprocess.Popen(install_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    print(stdout)


def test_run():
    process = subprocess.Popen(['env', "DB_USER=jgjgpark", "./input/bin/python", "run.py"], stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    print(stdout)


def test_mkdir():
    os.makedirs('test/hello/workd', exist_ok=True)
