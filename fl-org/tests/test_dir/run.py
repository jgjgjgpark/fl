import time
import os

DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_DATABASE = os.environ.get('DB_DATABASE')
DB_SCHEMA = os.environ.get('DB_SCHEMA')


def doAnalysis():
    print('Analyzing...')


def main():
    time.sleep(10)
    print(f'{DB_USER}')
    doAnalysis()


if __name__ == '__main__':
    main()
