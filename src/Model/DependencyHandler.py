from src.Model.Application import ApplicationName


def get_handler(application_name):
    switcher = {
        ApplicationName.macroservice: PHPDependencyHandler,
        ApplicationName.admin: PHPDependencyHandler,
        ApplicationName.external_api: PHPDependencyHandler
    }

    result = switcher.get(application_name, "Error")

    if result == "Error":
        raise Exception("Unable to find application with name: " + application_name)

    return result


class DependencyHandlerFactory:
    def __init__(self):
        pass

    def get_dependencies(self):
        pass


class PHPDependencyHandler(DependencyHandlerFactory):
    def get_dependencies(self):
        return "PHP Dependencies"
