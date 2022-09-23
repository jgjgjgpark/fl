import swagger_client
import json

client = swagger_client.DefaultApi()


def getUrl():
    result = client.analyses_analysis_id_executions_post(_preload_content=False)


if __name__ == '__main__':
    a = client.analyses_post(_preload_content=False)
    data = json.loads(a.data.decode('utf-8'))
    print(data['data']['analysisId'])
    a = client.analyses_analysis_id_predefined_url_get(1, "a", _preload_content=False)
    data = json.loads(a.data.decode('utf-8'))
    print(data['data'])
    client.analyses_analysis_id_rounds_round_put("analysisId", 1)
