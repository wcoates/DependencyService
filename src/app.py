from flask import Flask

from src.Model.Application import ApplicationFactory

app = Flask(__name__)


@app.route("/dependencies/<application_name>/<commit_hash>", methods=['GET'])
def commit_dependencies(application_name, commit_hash):
    # commit hash should be comma separated
    application = app_factory.get_application(application_name)

    return application.name + " " + commit_hash


@app.route("/dependencies/<application>/composer.json", methods=['GET'])
def commit_dependencies_file(application_name):

    return application_name


@app.route("/dependencies/<application_name>/compare", methods=['GET'])
def compare_application_commits(application_name):
    # if all

    return application_name


@app.route("/dependencies/<application>/compare/latest", methods=['GET'])
def compare_application_latest(application_name):

    return application_name


if __name__ == "__main__":  # for Docker
    app_factory = ApplicationFactory()
    app_factory.initialize_applications()
    app.run(host='0.0.0.0')
