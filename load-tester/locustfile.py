from locust import HttpLocust, TaskSet, task
import requests

# send in one thousand tweet packets
tweets = ["this is an example. it is rather neutral in sentiment and will be analyzed many times."] * 1000

class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        pass

    @task(1)
    def get_sentiment(self):
        self.client.post("", json = {"data":tweets})

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait=5000
    max_wait=9000
