from locust import HttpUser, between, task

class MyUser(HttpUser):

    wait_time = between(1, 10)

    @task
    def get_world_summary(self):
        self.client.get("/reports/world?filter_date=2021-07-01")

    @task
    def get_country_report_large(self):
        self.client.get("/reports/?country_region=US&date_from=2021-05-05&date_to=2021-05-08&province_state=Missouri")

    @task
    def get_country_report_medium(self):
        self.client.get("/reports/?country_region=Singapore&date_from=2021-05-05&date_to=2021-05-08")

    @task
    def get_country_report_small(self):
        self.client.get("/reports/5189")

    @task
    def get_daily_world_summary(self):
        self.client.get("/daily/world?filter_date=2021-07-01")

    @task
    def get_daily_country_report_large(self):
        self.client.get("/daily/?country_region=US&_date=2021-05-05&province_state=Missouri")

    @task
    def get_daily_country_report_small(self):
        self.client.get("/daily/?country_region=Singapore&_date=2021-05-05")
        