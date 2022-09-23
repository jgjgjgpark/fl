from src.app.execution_manager import *


def test_create_analysis():
    connectionInfo = DbConnectionInfo(DB_USER='jgjgpark')
    assert connectionInfo.DB_USER is 'jgjgpark'
