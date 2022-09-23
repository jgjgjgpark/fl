from federated_learning import FederatedLearning, RoundExecutionStatus
from execution import ExecutionStatus
import aggregate_utils


def test(a, func):
    return func(a)


def test_fl():
    project_id = 145
    analysis_id = 158
    user_id = "fnet05@fnet.or.kr"
    password = "123456"
    image = 'docker.evidnet.co.kr/base-images/evidnet/tensorflow:latest'
    research_file_location = 'research_no1'
    fl = FederatedLearning(project_id, analysis_id, [11], 2, image, research_file_location)
    fl.login(user_id, password)
    fl.execute()
    # print(fl.get_status())


def test_test():
    print(test(1, lambda a: a + 1))


def test_roundexecutionstatus():
    status = RoundExecutionStatus()
    assert not status.organization_learning_is_finished()
    status.set_status(12, "fail")
    status.set_status(10, "downloading")
    status.set_status(11, "success")
    assert not status.organization_learning_is_finished()


def test_enum():
    print(ExecutionStatus.FAILED)


def test_make_zip_file():
    aggregate_utils.make_zip_file(0)

def test_string():
    str1 = "research_no1/output/result_145_158_31_16212_0.zip"
    str2 = "researchno1/output/result_145_158_31_16212_0.zip"
    split_path = str1.split("_")
    length_of_array = len(split_path)
    cdm_id = split_path[length_of_array-3]
    execution_id = split_path[length_of_array-2]
    round_number = split_path[length_of_array-1].split(".")[0]
    print(cdm_id, execution_id, round_number)

    split_path = str2.split("_")
    length_of_array = len(split_path)
    cdm_id = split_path[length_of_array-3]
    execution_id = split_path[length_of_array-2]
    round_number = split_path[length_of_array-1].split(".")[0]
    print(cdm_id, execution_id, round_number)


def test_remove_temp():
    project_id = 145
    analysis_id = 158
    user_id = "fnet05@fnet.or.kr"
    password = "123456"
    image = 'docker.evidnet.co.kr/base-images/evidnet/tensorflow:latest'
    research_file_location = 'research_no1'
    fl = FederatedLearning(project_id, analysis_id, [11], 2, image, research_file_location)
    fl.finalize()


