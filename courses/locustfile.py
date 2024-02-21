from locust import HttpUser, TaskSet, task


class UserBehavior(TaskSet):
    @task
    def get_courses(self):
        for symbol in ['BTC-RUB', 'ETH-BTC', 'BTC-USDT']:
            self.client.get(f'/courses?symbols={symbol}')

    @task
    def get_multi_courses(self):
        self.client.get('/courses?symbols=LTC-BTC&symbols=BNB-BTC&symbols=NEO-BTC&symbols=QTUM-ETH&symbols=EOS-ETH')


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    min_wait = 1000
    max_wait = 1000
