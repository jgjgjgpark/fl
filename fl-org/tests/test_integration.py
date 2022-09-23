from app.model import PrintActor


# def test_post(client):
#     response = client.post("/fl/executions", json={
#         "presigned_url": "http://123.124.214.123"
#     })
#     print("test")
#     assert response != None


def test_create_analysis(client):
    url = "/fl/analyses"
    response = client.post(url, json={
        "presignedUrl": "https://federated-learning-bucket.s3.ap-northeast-2.amazonaws.com/8f013dce-320d-48dc-9954-35609d8b827d/round_1/input/input.zip?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIATMS34QJ5GGZKCLOF%2F20220721%2Fap-northeast-2%2Fs3%2Faws4_request&X-Amz-Date=20220721T051257Z&X-Amz-Expires=36000&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPX%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDmFwLW5vcnRoZWFzdC0yIkYwRAIgFKyAe28CkWntUJlT7%2FCgTtrG0q5h2skpaD3hUNsdAosCIDRQixanPWgb5FWmb6KG4DdRx82Utp3k5BCRMDm9Na3jKsYDCD4QAxoMMjMzMTk0Njg1MDUwIgxpTvPIuXPy%2BZFaKBgqowN28ERDmLyr%2FaewKIP9aH4fRA814xOGQLqGzNY1kUuTYyg%2BMOrh5MUQn%2FooktZHpxaroOrFOf1SRwT1%2B3l56lA08bJaZKU7eYCSbHtt90%2Bg3LF2rd4GPn9r2vY0lVKReBkaJNik9F2effUUtnsvj%2FtKS2OhCHT2m6qfKTxPCwWORci4f%2BpSmm%2FUbILazwRGMUQHkn3WC2dsA%2BL3PQs56Jh4EKGB1t1gepYqIqq8%2Bd%2BBrdbGkJLAMlR2znbOfs4m6UTE7ZNoF4%2FxCVK50X%2FP5PRVVmL%2Fg%2BEHj97z7qlJGuohbpYazeWuz2kuTv7jrK73GygoHqw1M1rhKsL7Es9l6SpSR5ZwRbXD35OJaSP%2FaflpfssyCEvvy7GzelllLuSSGkq%2B5Gh65V8Q1FfCtErL4V4p5o%2B7OflohK4hVXVn%2FtNgF8SCMHlR3MtpIrORaSdq2k%2F2a4zqm%2BX3yfPfErRBhGntEwYOU80wOEUPKAcdZY23gUBY2yetKZj7KnxDqmcRsMsfek%2FCJO7vxJ%2Fk4GvsLvJmczKds%2F86Pm8CrkLqNfAG2ETtCzDYwOOWBjqfAW0Eynhfd%2FUIY93%2FJQa9bHc0L3jdTV1Gj0%2By61FAZ0G9AFdqEE7h7kyF8Imp%2FkLoMPYzEDeFUUwRGu60F4Iw1l2SvnWOOepupnintrw%2FsvOzNIppc%2BSwINylv9LfYFHE%2Fm50a4Vf5EVbbUK5gKxPyG0%2BNDFTRiKDGRkh0BPkxrWxzDgd2AV%2BZEWMtvUEBE6tlp99bX%2FWfU2fiIQ1LFUajQ%3D%3D&X-Amz-Signature=129a8d82139926ec7aabdd29983172fa99d5011e4e6c0d9989b8aa261a35ca78&X-Amz-SignedHeaders=host&x-id=GetObject",
        "cdmGlobalId": "fasfwerdsfsafs",
        "analysisId": "1fb906bc-f6f5-431c-8add-4458447716e0",
        "round": 1
    })
    print(response.json)
    assert response.status_code == 200


def test_create_cdm(client):
    url = "/fl/analyses"
    response = client.post(url, json={
        "presignedUrl": "",
        "analysisId": "231h321312lnjl",
        "round": 1
    })
    print(response.json)
    assert response.status_code == 200


def test_actor():
    actor = PrintActor()
    actor.start()
    actor.send("Hello")
    actor.send("World")
    actor.close()
    actor.join()

