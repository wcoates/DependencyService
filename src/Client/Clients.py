class MockS3Client:
    def __init__(self):
        self.base_url = ""
        self.key_id = ""
        self.key = ""

    def add_user(self, user):
        print("Using MockS3Client to add permissions for user: ", user)


class MockJiraClient:
    def __init__(self):
        self.base_url = ""
        self.key_id = ""
        self.key = ""

    def update_status(self, issue_key, status):
        print("Using MockJiraClient to update status for ", issue_key, " to status ", status)

    def comment_problems(self, issue_key, problems):
        # TODO concatenate problems
        print("Using MockJiraClient to comment problems for ", issue_key, " w/problems: ", problems)
