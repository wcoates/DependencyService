import enum

from src.Model import DependencyHandler


class Application:
    def __init__(self, application_name, dependency_handler):
        self.application_name = application_name
        self.dependency_handler = dependency_handler

    def get_dependencies(self):
        return self.dependency_handler.get_dependencies()


class ApplicationName(enum.Enum):
    macroservice = 'macroservice'
    admin = 'admin'
    external_api = 'external_api'


class ApplicationFactory:
    def __init__(self):
        self.applications = self.initialize_applications()

    def initialize_applications(self):
        application_list = list()

        for x in ApplicationName:
            application_list.append(Application(x, DependencyHandler.get_handler(x)))

        return application_list

    def get_application(self, name):
        for x in self.applications:
            if x.application_name == name:
                return x

        raise Exception("Unable to find application with name: " + name)
