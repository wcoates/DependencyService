from flask import Flask, request
import json

from Model.JiraData import JiraData
from Script.Scripts import ScriptDefinitions, ScriptRunner

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return "Hello World"


@app.route("/" + ScriptDefinitions.S3AccessSuccessExample.value, methods=['POST'])
def s3access_request_success():
    jira_data = parse_jira_data(request.get_json())
    script = ScriptRunner(jira_data)
    script.run(request.path[1:])

    return ""


@app.route("/" + ScriptDefinitions.S3AccessFailureExample.value, methods=['POST'])
def s3access_request_failure():
    jira_data = parse_jira_data(request.get_json())
    script = ScriptRunner(jira_data)
    script.run(request.path[1:])

    return ""


def parse_jira_data(jira_issue_json):
    #TODO parse response body / delete mock

    return JiraData("ITOOLS-1", "STAGE", "WC045050")


if __name__ == "__main__":  # for Docker
    app.run(host='0.0.0.0')
