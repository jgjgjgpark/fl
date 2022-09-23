from aggregation_server import AggregationServer


class MyServer(AggregationServer):
    def test(self):
        print(self.test)

    def learning_stop_condition(self):
        return self.round == 5
