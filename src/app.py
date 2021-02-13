from flask import Flask, request
import json

from Model.RequestModel import S3Access
from Scripts.Script import S3AccessSuccessful, S3AccessFailure
from Model.Status import RequestState

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return "Hello World"


@app.route('/s3access_success', methods=['POST'])
def successful_s3access_request():
    print("Received request: ", request.get_json())

    # Serialize Json
    x = ' {"jira_issue_key": "ITOOLS-1", "db_name": "STAGE", "user_id": "WC045050"} '
    y = json.loads(x)
    # print("Jira issue key: ", y['jira_issue_key'])
    # print("DB Name", y['db_name'])
    # print("UserId: ", y['user_id'])

    # TODO parse from response body
    # json_data = json.loads(request.get_json())
    # ^ this is converting response body from " -> ' and which blows up things
    # ^ replace y with json_data once formatting is resolved

    # Run script
    request_state = RequestState("SUCCESS", [])
    s3_access = S3Access(y['jira_issue_key'], y['db_name'], y['user_id'])
    s3access_request = S3AccessSuccessful(
        s3_access, request_state)
    s3access_request.run()
    update_jira_request_state(s3access_request.S3Access.jira_issue_key, request_state)

    return ""


@app.route('/s3access_failure', methods=['POST'])
def failed_s3access_request():
    print("Received request: ", request.get_json())

    # Serialize Json
    x = ' {"jira_issue_key": "ITOOLS-1", "db_name": "STAGE", "user_id": "WC045050"} '
    y = json.loads(x)
    request_state = RequestState("SUCCESS", [])
    s3_access = S3Access(y['jira_issue_key'], y['db_name'], y['user_id'])

    # Run script
    s3access_request = S3AccessFailure(
        s3_access, request_state)
    s3access_request.run()
    update_jira_request_state(s3access_request.S3Access.jira_issue_key, request_state)

    return ""


# POST updates to Jira ticket
def update_jira_request_state(jira_issue_key, RequestState):
    post_jira_status(jira_issue_key, RequestState)
    post_jira_comment(jira_issue_key, RequestState)


def post_jira_status(jira_issue_key, RequestState):
    print("Updating Jira ticket status to ", RequestState.status)


def post_jira_comment(jira_issue_key, RequestState):
    if RequestState.problems:
        print("Commenting problems on ", jira_issue_key, ": ", RequestState.problems)


if __name__ == "__main__":  # for Docker
    app.run(host='0.0.0.0')