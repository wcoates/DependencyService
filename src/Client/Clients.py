class ClientWrapper:
    def __init__(self, client_config):
        self.client_config = client_config
        self.mock_s3_client = MockS3Client(client_config.user, client_config.key)
        self.mock_jira_client = MockJiraClient(client_config.user, client_config.key)


class MockS3Client:
    def __init__(self, user, key):
        self.user = user
        self.key = key

    def add_user(self, user):
        print("Using MockS3Client to add permissions for user: ", user)


class MockJiraClient:
    def __init__(self, user, key):
        self.user = user
        self.key = key

    def update_status(self, issue_key, status):
        print("Using MockJiraClient to update status for ", issue_key, " to status ", status)

    def comment_problems(self, issue_key, problems):
        #TODO concatenate problems
        print("Using MockJiraClient to comment problems for ", issue_key, " w/problems: ", problems)

