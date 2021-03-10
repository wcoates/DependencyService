import enum

from src.Client.ClientWrapper import ClientWrapper
from src.Client.Config.ClientConfig import ConfigClient, ClientName
from src.Model.Status import RequestState


class ScriptRunner:
    def __init__(self, jira_data):
        self.JiraData = jira_data
        self.ClientWrapper = self.build_client_wrapper()
        self.RequestState = RequestState("SUCCESS", [])
        self.JiraUpdate = JiraUpdater(self.JiraData, self.ClientWrapper, self.RequestState)

    @staticmethod
    def build_client_wrapper():
        config_client = ConfigClient()
        return ClientWrapper(config_client)

    def run(self, script_name):
        if script_name == ScriptDefinitions.S3AccessSuccessExample.value:
            S3AccessSuccessful(self.JiraData, self.ClientWrapper, self.RequestState).run()
        if script_name == ScriptDefinitions.S3AccessFailureExample.value:
            S3AccessFailure(self.JiraData, self.ClientWrapper, self.RequestState).run()

        self.JiraUpdate.update_status()
        self.JiraUpdate.post_problems()


class ScriptDefinitions(enum.Enum):
    S3AccessSuccessExample = "s3access_success"
    S3AccessFailureExample = "s3access_failure"
    # Add more script names here


class S3AccessSuccessful:
    def __init__(self, jira_data, client_wrapper, request_state):
        self.JiraData = jira_data
        self.S3Client = client_wrapper.client_list[ClientName.s3.value]
        self.RequestState = request_state

    def run(self):
        self.S3Client.add_user(self, self.JiraData.user_id)


class S3AccessFailure:
    def __init__(self, jira_data, client_wrapper, request_state):
        self.JiraData = jira_data
        self.S3Client = client_wrapper.client_list[ClientName.s3.value]
        self.RequestState = request_state

    def run(self):
        self.S3Client.add_user(self, self.JiraData.user_id)

        print(self.S3Client.base_url)
        # Pretend something went wrong
        self.RequestState.set_fail_status()
        self.RequestState.add_problem("Something went wrong")


class JiraUpdater:
    def __init__(self, jira_data, client_wrapper, request_state):
        self.JiraData = jira_data
        self.JiraClient = client_wrapper.client_list[ClientName.jira.value]
        self.RequestState = request_state

    def update_status(self):
        self.JiraClient.update_status(self, self.JiraData.issue_key, self.RequestState.status)

    def post_problems(self):
        if self.RequestState.problems:
            self.JiraClient.comment_problems(self, self.JiraData.issue_key, self.RequestState.problems)
