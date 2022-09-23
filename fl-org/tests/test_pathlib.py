from pathlib import Path


def test_path():
    data_folder = Path("./Downloads/oreilly-annotations.csv")
    print(data_folder.absolute())
