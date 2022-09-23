import lib
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
    time.sleep(10)
    lib.print_test(f'{DB_USER}')
    lib.print_test(f'{DB_PASSWORD}')
    lib.print_test(f'{DB_HOST}')
    lib.print_test(f'{DB_PORT}')
    lib.print_test(f'{DB_DATABASE}')
    lib.print_test(f'{DB_SCHEMA}')
    doAnalysis()


if __name__ == '__main__':
    main()
