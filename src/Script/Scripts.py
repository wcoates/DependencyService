import enum

from src.Client.Clients import ClientWrapper
from src.Client.Config.ClientConfig import ConfigClient
from src.Model.Status import RequestState


class ScriptRunner:
    def __init__(self, jira_data):
        self.JiraData = jira_data
        self.ClientWrapper = self.build_client_wrapper()
        self.RequestState = RequestState("SUCCESS", [])
        self.JiraUpdate = JiraUpdate(self.JiraData, self.ClientWrapper, self.RequestState)

    @staticmethod
    def build_client_wrapper():
        config_client = ConfigClient()
        return ClientWrapper(config_client.retrieve_config())

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
        self.ClientWrapper = client_wrapper
        self.RequestState = request_state

    def run(self):
        print()
        self.ClientWrapper.mock_s3_client.add_user(self.JiraData.user_id)


class S3AccessFailure:
    def __init__(self, jira_data, client_wrapper, request_state):
        self.JiraData = jira_data
        self.ClientWrapper = client_wrapper
        self.RequestState = request_state

    def run(self):
        self.ClientWrapper.mock_s3_client.add_user(self.JiraData.user_id)

        # Pretend something went wrong
        self.RequestState.set_fail_status()
        self.RequestState.add_problem("Something went wrong")


class JiraUpdate:
    def __init__(self, jira_data, client_wrapper, request_state):
        self.JiraData = jira_data
        self.ClientWrapper = client_wrapper
        self.RequestState = request_state

    def update_status(self):
        self.ClientWrapper.mock_jira_client.update_status(self.JiraData.issue_key, self.RequestState.status)

    def post_problems(self):
        if self.RequestState.problems:
            self.ClientWrapper.mock_jira_client.comment_problems(self.JiraData.issue_key, self.RequestState.problems)

