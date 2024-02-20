from locust import HttpUser, TaskSet, task


class UserBehavior(TaskSet):
    @task
    def get_courses(self):
        self.client.get("http://127.0.0.1:8000/courses?symbol=BTCRUB")


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    min_wait = 1000
    max_wait = 1000

