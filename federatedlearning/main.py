import pykka


class Executor(pykka.ThreadingActor):
    def __init__(self, cdmId):
        super().__init__()
        self.cdmId = cdmId

    def on_receive(self, message):
        print(f'c id:  {self.cdmId}')
        print(f'call organization')

    def execute(self):
        pass

def executeRound():
    pass


class FederatedLearning:
    def __init__(self):
        pass


if __name__ == '__main__':
    cdmIds = [1, 2, 3]
    actors = []
    for cdmId in cdmIds:
        actors.append(Executor.start(cdmId))

    print(actors)

    for actor in actors:
        actor.tell("")
        actor.stop()
