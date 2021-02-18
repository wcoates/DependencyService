import logging


class RequestState:
    def __init__(self, status, problems):
        self.status = status  # status SUCCESS/FAIL
        self.problems = problems

    def set_fail_status(self):
        self.status = "FAIL"
        logging.info("RequestState failure flag has been set")

    def add_problem(self, problem):
        self.problems.append(problem)
        logging.info("RequestState problem has been added: ", problem)
