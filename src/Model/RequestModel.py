# Define models for scripts (1...1)
class S3Access:
    def __init__(self, jira_issue_key, db_name, user_id):
        self.jira_issue_key = jira_issue_key
        self.db_name = db_name
        self.user_id = user_id
