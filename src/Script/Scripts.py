import enum
from Model.JiraData import JiraData
from Model.Status import RequestState
from Client.Config.ClientConfig import ConfigClient
from Client.Clients import ClientWrapper, MockS3Client, MockJiraClient


class ScriptRunner:
    def __init__(self, jira_data):
        self.JiraData = jira_data
        self.ClientWrapper = self.build_client_wrapper()
        self.RequestState = RequestState("SUCCESS", [])
        self.JiraUpdate = JiraUpdate(JiraData, ClientWrapper, self.RequestState)

    def build_client_wrapper(self):
        config_client = ConfigClient()

        return ClientWrapper(config_client.retrieve_config())

    def run(self, script_name):
        if script_name == ScriptDefinitions.S3AccessSuccessExample.value:
            S3AccessSuccessful(self.JiraData, self.ClientWrapper, self.RequestState)
            S3AccessSuccessful.run(self)
        if script_name == ScriptDefinitions.S3AccessFailureExample.value:
            S3AccessFailure(self.JiraData, self.ClientWrapper, self.RequestState)
            S3AccessFailure.run(self)
        # Add more scripts here

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
        self.ClientWrapper.MockS3Client.add_user(self.JiraData.user_id)


class S3AccessFailure:
    def __init__(self, jira_data, client_wrapper, request_state):
        self.JiraData = jira_data
        self.ClientWrapper = client_wrapper
        self.RequestState = request_state

    def run(self):
        self.ClientWrapper.MockS3Client.add_user(self.JiraData.user_id)

        # Pretend something went wrong
        self.RequestState.set_fail_status()
        self.RequestState.add_problem("Something went wrong")


class JiraUpdate:
    def __init__(self, jira_data, client_wrapper, request_state):
        self.JiraData = jira_data
        self.ClientWrapper = client_wrapper
        self.RequestState = request_state

    def update_status(self):
        self.ClientWrapper.MockJiraClient.update_status(self.jira_data.issue_key, self.RequestState.status)

    def post_problems(self):
        self.ClientWrapper.MockJiraClient.comment_problems(self.jira_data.issue_key, self.RequestState.problems)
