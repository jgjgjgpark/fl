import os
import time

DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_DATABASE = os.environ.get('DB_DATABASE')
DB_SCHEMA = os.environ.get('DB_SCHEMA')


def doAnalysis():
    print('Analyzing...')


def main():
    print(f'{DB_USER}')
    print(f'{DB_PASSWORD}')
    print(f'{DB_HOST}')
    print(f'{DB_PORT}')
    print(f'{DB_DATABASE}')
    print(f'{DB_SCHEMA}')
    doAnalysis()


if __name__ == '__main__':
    main()