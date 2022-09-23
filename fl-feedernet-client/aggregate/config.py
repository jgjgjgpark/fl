import json
import os

"""
:Config
{
  "current_round": 0,
  "max_round": 10,
  "CDM_execution_list": {
    "4": {
      "1501": 20
    },
    "6": {
      "1502": 20
    }
  },
  "project_name": "M/L Tensorflow Analysis Test",
  "user_id": "fltester@fnet.or.kr",
  "user_pw": "123456",
  "project_id": 65,
  "analysis_id": 86,
  "database": {
    "DB_USER": "readonlyuser",
    "DB_PASSWORD": "x741TuPDpO1y",
    "DB_URL": "203.245.2.199:5432",
    "DB_DATABASE": "omop",
    "DB_SCHEMA": "cdm_synpuf",
    "DB_HOST": "203.245.2.199",
    "DB_PORT": "5432"
  }
}
"""
class Config:

    def __init__(self):
        self.config_file_path = "{}/config.json".format(os.path.dirname(os.path.realpath(__file__)))
        with open(self.config_file_path, "r") as c:
            self.value = json.load(c)
        print("config : ", json.dumps(self.value, indent="\t"))

    def update(self, key, v):
        self.value[key] = v
        #print(self.value)
        self.save_config()

    def save_config(self):
        with open(self.config_file_path, "w") as c:
            #c.write(self.value)
            json.dump(self.value, c)
            print("config update !!!")
