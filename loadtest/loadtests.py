from locust import HttpLocust, TaskSet, task


class UserBehavior(TaskSet):
    @task(2)
    def index(self):
        self.client.get("/")

    @task(2)
    def search(self):
        self.client.get("/api-book/?search=hello_boy")

    @task(3)
    def book(self):
        self.client.get("/book/8943309066")

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait=5000
    max_wait=9000
